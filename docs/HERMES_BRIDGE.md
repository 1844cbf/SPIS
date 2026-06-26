# Hermes Bridge

This bridge lets Hermes submit SPIS work to the orchestrator without changing Hermes source code.

## Submit

```bash
cd /opt/spis/spis-agent-platform
python scripts/hermes_spis.py submit "开发供应商价格管理模块，支持当前价格和历史价格"
```

The command returns immediately with a task ID.

## Check Status

```bash
python scripts/hermes_spis.py status spis-xxxxxxxxxxxx
```

## Hermes Quick Commands

Hermes exec quick commands do not append user arguments to the configured command,
so they are not a good fit for `/spis <instruction>`.

You can still add fixed utility commands:

```yaml
quick_commands:
  spis-health:
    type: exec
    command: curl -s http://127.0.0.1:18080/health
  spis-latest:
    type: exec
    command: cd /opt/spis/spis-agent-platform && python -c "from app.config import get_settings; print(get_settings().app_name)"
```

For parameterized SPIS work, use the skill route below.

## Hermes Skill Route

Install `hermes-skills/spis-orchestrator` into `~/.hermes/skills/spis-orchestrator`.

Then in Feishu:

```text
/spis-orchestrator 开发供应商价格管理模块，支持阶梯价、MOQ、币种、有效期
```

The skill instructs Hermes to run:

```text
python /opt/spis/spis-agent-platform/scripts/hermes_spis.py submit "<user request>"
```

For local Windows testing, the path is:

```text
python C:/CC/spis-agent-platform/scripts/hermes_spis.py submit "<user request>"
```
