# Feishu and Hermes Integration

The first version should keep your existing Hermes Feishu connection.

## Recommended Flow

```text
Feishu message
  -> Hermes
  -> local HTTP call to SPIS-Orchestrator
  -> agent result
  -> Hermes replies to Feishu
```

## Orchestrator Endpoint

```text
POST http://127.0.0.1:18080/webhooks/hermes/tasks
Header: X-SPIS-Secret: <ORCHESTRATOR_SHARED_SECRET>
```

Body:

```json
{
  "text": "开发供应商价格管理模块，支持阶梯价、MOQ、币种、有效期",
  "user_id": "feishu-user-id",
  "chat_id": "optional-chat-id",
  "message_id": "optional-message-id",
  "metadata": {
    "priority": "normal"
  }
}
```

## Hermes Responsibility

- Accept Feishu command
- Call the orchestrator endpoint
- Return task ID and result summary

## Orchestrator Responsibility

- Select roles
- Call model providers
- Store task result
- Never directly bypass SPIS business API rules
