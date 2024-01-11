from pydantic import (
    Field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class AzureAiSearchSettings(BaseSettings):
    azure_search_endpoint: str = Field(
        "https://YOUR_AI_SEARCH.search.windows.net/", alias="azure_search_endpoint"
    )
    azure_search_key: str = Field("YOUR_API_KEY", alias="azure_search_key")
    index_name: str = Field("YOUR_INDEX_NAME", alias="index_name")

    model_config = SettingsConfigDict(
        env_file="azure_ai_search.env", env_file_encoding="utf-8"
    )
