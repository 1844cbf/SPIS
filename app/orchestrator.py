from app.agents.prompts import SYSTEM_PROMPTS
from app.config import Settings
from app.providers.factory import provider_for_role
from app.schemas import AgentResult, TaskRecord, TaskRequest, TaskStatus
from app.storage import TaskStore


class Orchestrator:
    def __init__(self, settings: Settings, store: TaskStore) -> None:
        self.settings = settings
        self.store = store

    async def create_and_run(self, request: TaskRequest) -> TaskRecord:
        task = self.create(request)
        return await self.run(task)

    def create(self, request: TaskRequest) -> TaskRecord:
        task = TaskRecord(
            title=request.title,
            instruction=request.instruction,
            requester=request.requester,
            source=request.source,
            roles=request.roles,
            metadata=request.metadata,
        )
        return self.store.create(task)

    async def run(self, task: TaskRecord) -> TaskRecord:
        self.store.update(task, TaskStatus.RUNNING)
        results: list[AgentResult] = []

        try:
            for role in task.roles:
                provider = provider_for_role(role, self.settings)
                result = await provider.complete(
                    system_prompt=SYSTEM_PROMPTS[role],
                    user_prompt=self._build_role_prompt(task, results),
                )
                results.append(
                    AgentResult(
                        role=role,
                        provider=provider.provider_name,
                        model=provider.model,
                        content=result,
                    )
                )

            task.result = {"agent_results": [item.model_dump(mode="json") for item in results]}
            return self.store.update(task, TaskStatus.COMPLETED)
        except Exception as exc:
            task.result = {
                "error": str(exc),
                "agent_results": [item.model_dump(mode="json") for item in results],
            }
            return self.store.update(task, TaskStatus.FAILED)

    def _build_role_prompt(self, task: TaskRecord, previous_results: list[AgentResult]) -> str:
        previous = "\n\n".join(
            f"## Previous {item.role.value} result\n{item.content}" for item in previous_results
        )
        return (
            f"# Task\n{task.title}\n\n"
            f"# Instruction\n{task.instruction}\n\n"
            f"# Metadata\n{task.metadata}\n\n"
            f"# Previous Results\n{previous or 'None'}"
        )
