# SPIS Agent Platform

Lightweight orchestration layer for SPIS agent collaboration.

Current target:

- Tencent Cloud CVM, Ubuntu 24.04, x86-64, 4c/4G
- Hermes remains the Feishu entrypoint
- FastAPI orchestrator receives tasks and routes agents
- DeepSeek writes and repairs code
- OpenAI performs architecture and final review
- Doubao handles Chinese business/rule analysis

This project is intentionally small. It is the control plane, not the SPIS business database.

## Quick Start

```bash
cp .env.example .env
docker compose up -d --build
curl http://127.0.0.1:18080/health
```

## First Workflow

```text
Feishu -> Hermes -> POST /webhooks/hermes/tasks -> Orchestrator
       -> DeepSeek coding agent
       -> OpenAI review agent
       -> optional Feishu callback
```

## Safety Rules

- Hermes and OpenClaw do not write the SPIS database directly.
- Agent workers produce proposals, patches, reports, or pull requests.
- SPIS business writes go through the FastAPI business service.
- Production merge/deploy requires explicit approval from Feishu.
