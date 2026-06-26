from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class AgentRole(StrEnum):
    ARCHITECT = "architect"
    CODER = "coder"
    REPAIR = "repair"
    BUSINESS = "business"
    REVIEWER = "reviewer"


class TaskStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    NEEDS_APPROVAL = "needs_approval"
    COMPLETED = "completed"
    FAILED = "failed"


class TaskRequest(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    instruction: str = Field(min_length=1)
    requester: str = "feishu"
    source: str = "manual"
    roles: list[AgentRole] = Field(default_factory=lambda: [AgentRole.CODER, AgentRole.REVIEWER])
    metadata: dict[str, Any] = Field(default_factory=dict)


class TaskRecord(BaseModel):
    task_id: str = Field(default_factory=lambda: f"spis-{uuid4().hex[:12]}")
    title: str
    instruction: str
    requester: str
    source: str
    roles: list[AgentRole]
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = Field(default_factory=dict)
    result: dict[str, Any] = Field(default_factory=dict)


class HermesTaskPayload(BaseModel):
    text: str = Field(min_length=1)
    user_id: str = "unknown"
    chat_id: str | None = None
    message_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentResult(BaseModel):
    role: AgentRole
    provider: str
    model: str
    content: str
