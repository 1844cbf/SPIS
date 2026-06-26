import asyncio
import json
import urllib.error
import urllib.request

from app.providers.base import ModelProvider


class OpenAICompatibleProvider(ModelProvider):
    def __init__(self, provider_name: str, api_key: str, base_url: str, model: str) -> None:
        self.provider_name = provider_name
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model

    async def complete(self, system_prompt: str, user_prompt: str) -> str:
        if not self.api_key:
            return (
                f"[{self.provider_name}] API key is not configured. "
                "Set the matching key in .env before running live tasks."
            )

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
            "max_tokens": 1024,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "spis-agent-platform-test",
        }

        return await asyncio.to_thread(self._complete_sync, headers, payload)

    def _complete_sync(self, headers: dict[str, str], payload: dict[str, object]) -> str:
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"{self.provider_name} returned HTTP {exc.code}: {body[:1000]}"
            ) from exc

        message = data["choices"][0]["message"]
        return message.get("content") or "[empty model response]"
