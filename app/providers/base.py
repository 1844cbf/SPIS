from abc import ABC, abstractmethod


class ModelProvider(ABC):
    provider_name: str
    model: str

    @abstractmethod
    async def complete(self, system_prompt: str, user_prompt: str) -> str:
        """Return a single model response."""
