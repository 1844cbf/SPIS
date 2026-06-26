# Deploy on Tencent CVM

Target server:

- Tencent Cloud CVM
- Ubuntu 24.04 LTS
- x86-64
- 4 cores / 4G RAM
- about 15GB free disk

## 1. Install Docker

```bash
sudo apt update
sudo apt install -y ca-certificates curl git
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker "$USER"
```

Log out and back in after adding the Docker group.

## 2. Upload Project

```bash
cd /opt
sudo mkdir -p spis
sudo chown "$USER:$USER" spis
cd spis
git clone <your-github-repo-url> spis-agent-platform
cd spis-agent-platform
cp .env.example .env
```

Fill in `.env` with API keys.

## 3. Start

```bash
docker compose up -d --build
curl http://127.0.0.1:18080/health
```

## 4. Resource Guardrails

This compose file limits the orchestrator to:

- 1 CPU
- 768MB memory
- Docker logs capped at 3 x 10MB

Keep Postgres and heavy build workers off this CVM until disk space is expanded.

## 5. Hermes Call Example

```bash
curl -X POST http://127.0.0.1:18080/webhooks/hermes/tasks \
  -H "Content-Type: application/json" \
  -H "X-SPIS-Secret: change-me-long-random-string" \
  -d '{"text":"开发供应商价格管理模块，支持阶梯价、MOQ、币种、有效期","user_id":"feishu-user"}'
```

In production set:

```env
APP_ENV=prod
ORCHESTRATOR_SHARED_SECRET=<long-random-secret>
```
