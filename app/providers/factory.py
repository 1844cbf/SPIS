from app.config import Settings
from app.providers.openai_compatible import OpenAICompatibleProvider
from app.schemas import AgentRole


def provider_for_role(role: AgentRole, settings: Settings) -> OpenAICompatibleProvider:
    if role in {AgentRole.ARCHITECT, AgentRole.REVIEWER} and settings.review_provider == "deepseek":
        return OpenAICompatibleProvider(
            provider_name="deepseek",
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
            model=settings.deepseek_model,
        )

    if role in {AgentRole.ARCHITECT, AgentRole.REVIEWER} and settings.review_provider == "doubao":
        return OpenAICompatibleProvider(
            provider_name="doubao",
            api_key=settings.ark_api_key,
            base_url=settings.ark_base_url,
            model=settings.doubao_model,
        )

    if role in {AgentRole.ARCHITECT, AgentRole.REVIEWER}:
        return OpenAICompatibleProvider(
            provider_name="openai",
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
            model=settings.openai_model,
        )

    if role in {AgentRole.CODER, AgentRole.REPAIR}:
        return OpenAICompatibleProvider(
            provider_name="deepseek",
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
            model=settings.deepseek_model,
        )

    return OpenAICompatibleProvider(
        provider_name="doubao",
        api_key=settings.ark_api_key,
        base_url=settings.ark_base_url,
        model=settings.doubao_model,
    )
