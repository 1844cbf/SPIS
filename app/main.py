from typing import Annotated

from fastapi import BackgroundTasks, Depends, FastAPI, Header, HTTPException

from app.config import Settings, get_settings
from app.orchestrator import Orchestrator
from app.schemas import AgentRole, HermesTaskPayload, TaskRecord, TaskRequest
from app.storage import TaskStore

app = FastAPI(title="SPIS Agent Platform", version="0.1.0")


SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_store(settings: SettingsDep) -> TaskStore:
    return TaskStore(settings.task_db_path)


StoreDep = Annotated[TaskStore, Depends(get_store)]


def get_orchestrator(
    settings: SettingsDep,
    store: StoreDep,
) -> Orchestrator:
    return Orchestrator(settings=settings, store=store)


OrchestratorDep = Annotated[Orchestrator, Depends(get_orchestrator)]
SecretHeader = Annotated[str | None, Header()]


def verify_shared_secret(
    settings: SettingsDep,
    x_spis_secret: SecretHeader = None,
) -> None:
    if settings.app_env == "dev":
        return
    if not x_spis_secret or x_spis_secret != settings.orchestrator_shared_secret:
        raise HTTPException(status_code=401, detail="invalid shared secret")


SecretCheck = Annotated[None, Depends(verify_shared_secret)]


@app.get("/health")
async def health(settings: SettingsDep) -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name, "env": settings.app_env}


@app.post("/tasks", response_model=TaskRecord)
async def create_task(
    request: TaskRequest,
    _: SecretCheck,
    orchestrator: OrchestratorDep,
) -> TaskRecord:
    return await orchestrator.create_and_run(request)


@app.post("/tasks/async", response_model=TaskRecord)
async def create_task_async(
    request: TaskRequest,
    background_tasks: BackgroundTasks,
    _: SecretCheck,
    orchestrator: OrchestratorDep,
) -> TaskRecord:
    task = orchestrator.create(request)
    background_tasks.add_task(orchestrator.run, task)
    return task


@app.get("/tasks", response_model=list[TaskRecord])
async def list_tasks(store: StoreDep) -> list[TaskRecord]:
    return store.list_recent()


@app.get("/tasks/{task_id}", response_model=TaskRecord)
async def get_task(task_id: str, store: StoreDep) -> TaskRecord:
    task = store.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    return task


@app.post("/webhooks/hermes/tasks", response_model=TaskRecord)
async def hermes_task_webhook(
    payload: HermesTaskPayload,
    _: SecretCheck,
    orchestrator: OrchestratorDep,
) -> TaskRecord:
    request = TaskRequest(
        title=payload.text[:80],
        instruction=payload.text,
        requester=payload.user_id,
        source="hermes-feishu",
        roles=[AgentRole.BUSINESS, AgentRole.CODER, AgentRole.REVIEWER],
        metadata={
            "chat_id": payload.chat_id,
            "message_id": payload.message_id,
            **payload.metadata,
        },
    )
    return await orchestrator.create_and_run(request)


@app.post("/webhooks/hermes/tasks/async", response_model=TaskRecord)
async def hermes_task_webhook_async(
    payload: HermesTaskPayload,
    background_tasks: BackgroundTasks,
    _: SecretCheck,
    orchestrator: OrchestratorDep,
) -> TaskRecord:
    request = TaskRequest(
        title=payload.text[:80],
        instruction=payload.text,
        requester=payload.user_id,
        source="hermes-feishu",
        roles=[AgentRole.BUSINESS, AgentRole.CODER, AgentRole.REVIEWER],
        metadata={
            "chat_id": payload.chat_id,
            "message_id": payload.message_id,
            **payload.metadata,
        },
    )
    task = orchestrator.create(request)
    background_tasks.add_task(orchestrator.run, task)
    return task
