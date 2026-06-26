# API Keys to Prepare

Do not paste keys into chat. Put them into `.env` on the server.

## Required

- `OPENAI_API_KEY`: final review and architecture review
- `DEEPSEEK_API_KEY`: coding and repair
- `GITHUB_TOKEN`: GitHub branch/PR automation later
- `ORCHESTRATOR_SHARED_SECRET`: Hermes-to-orchestrator authentication

## Recommended

- `ARK_API_KEY`: Doubao business/rule/document agent
- `FEISHU_APP_ID` and `FEISHU_APP_SECRET`: direct Feishu reply later

## Not Needed for v1

- Local LLM runtime
- Postgres on the Hermes CVM
- MinIO
- Gitea
