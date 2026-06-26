---
name: spis-orchestrator
description: Send SPIS development, review, pricing, supplier, BOM, and rules tasks to the SPIS-Orchestrator multi-agent workflow.
---

# SPIS Orchestrator

Use this skill when the user asks Hermes from Feishu/Lark to develop, review, plan,
inspect, or improve SPIS, the Supplier Price Intelligence System for fasteners.

## What To Do

1. Preserve the user's request exactly.
2. Submit it to SPIS-Orchestrator with the bridge script.
3. Return the task ID to the user.
4. Tell the user they can ask for status using the task ID.

## Local Windows Command

```bash
python C:/CC/spis-agent-platform/scripts/hermes_spis.py submit "<USER_REQUEST>"
```

## Tencent CVM Command

```bash
cd /opt/spis/spis-agent-platform && .venv/bin/python scripts/hermes_spis.py submit "<USER_REQUEST>"
```

## Status Command

```bash
python C:/CC/spis-agent-platform/scripts/hermes_spis.py status <TASK_ID>
```

On Tencent CVM:

```bash
cd /opt/spis/spis-agent-platform && .venv/bin/python scripts/hermes_spis.py status <TASK_ID>
```

## Response Shape

Reply in Chinese, using this structure:

```text
SPIS task submitted.
Task ID: spis-xxxxxxxxxxxx
Status: pending
Check later with: spis-xxxxxxxxxxxx
```

Do not paste API keys or secrets into chat.
