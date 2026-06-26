#!/usr/bin/env python3
"""Small Hermes bridge for SPIS-Orchestrator.

Usage:
  python scripts/hermes_spis.py submit "开发供应商价格管理模块"
  python scripts/hermes_spis.py status spis-xxxx
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"


def load_env() -> dict[str, str]:
    values: dict[str, str] = {}
    if ENV_PATH.exists():
        for raw_line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    values.update({key: value for key, value in os.environ.items() if key.startswith("SPIS_")})
    return values


def request(method: str, url: str, payload: dict[str, Any] | None, secret: str) -> dict[str, Any]:
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "X-SPIS-Secret": secret,
            "User-Agent": "hermes-spis-bridge/0.1",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"SPIS request failed: HTTP {exc.code} {body[:600]}") from exc


def submit(args: argparse.Namespace, env: dict[str, str]) -> None:
    base_url = env.get("SPIS_ORCHESTRATOR_URL", "http://127.0.0.1:18080").rstrip("/")
    secret = env.get("ORCHESTRATOR_SHARED_SECRET", "")
    payload = {
        "text": args.instruction,
        "user_id": args.user,
        "chat_id": args.chat_id,
        "metadata": {"source_command": "hermes_spis.py"},
    }
    task = request("POST", f"{base_url}/webhooks/hermes/tasks/async", payload, secret)
    print(f"SPIS task submitted: {task['task_id']}")
    print(f"Status: {task['status']}")
    print(f"Check later: python scripts/hermes_spis.py status {task['task_id']}")


def status(args: argparse.Namespace, env: dict[str, str]) -> None:
    base_url = env.get("SPIS_ORCHESTRATOR_URL", "http://127.0.0.1:18080").rstrip("/")
    secret = env.get("ORCHESTRATOR_SHARED_SECRET", "")
    task = request("GET", f"{base_url}/tasks/{args.task_id}", None, secret)
    print(f"Task: {task['task_id']}")
    print(f"Status: {task['status']}")
    if task.get("result"):
        results = task["result"].get("agent_results", [])
        if results:
            last = results[-1]
            print(f"Last agent: {last.get('role')} via {last.get('provider')}/{last.get('model')}")
            print((last.get("content") or "")[:1800])
        if "error" in task["result"]:
            print("Error:")
            print(task["result"]["error"])


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Submit/check SPIS Orchestrator tasks.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    submit_parser = subparsers.add_parser("submit")
    submit_parser.add_argument("instruction")
    submit_parser.add_argument("--user", default="hermes-feishu")
    submit_parser.add_argument("--chat-id", default=None)
    submit_parser.set_defaults(func=submit)

    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("task_id")
    status_parser.set_defaults(func=status)

    args = parser.parse_args(argv)
    args.func(args, load_env())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
