from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "spis-agent-platform"
    app_env: str = "dev"
    log_level: str = "INFO"
    task_db_path: str = "/data/spis_tasks.sqlite3"
    worker_concurrency: int = 1
    orchestrator_shared_secret: str = Field(default="change-me-long-random-string")

    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-5.5"
    review_provider: str = "openai"

    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-chat"

    ark_api_key: str = ""
    ark_base_url: str = "https://ark.cn-beijing.volces.com/api/v3"
    doubao_model: str = ""

    github_token: str = ""
    github_owner: str = ""
    github_repo: str = ""
    git_default_branch: str = "main"

    feishu_app_id: str = ""
    feishu_app_secret: str = ""
    feishu_default_chat_id: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
