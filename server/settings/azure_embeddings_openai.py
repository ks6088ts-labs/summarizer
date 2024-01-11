from pydantic import (
    Field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class AzureEmbeddingsOpenAiSettings(BaseSettings):
    api_version: str = Field("2023-07-01-preview", alias="api_version")
    azure_endpoint: str = Field(
        "https://YOUR_AOAI_NAME.openai.azure.com/", alias="azure_endpoint"
    )
    azure_deployment: str = Field("text-embedding-ada-002", alias="azure_deployment")
    api_key: str = Field("YOUR_API_KEY", alias="api_key")

    model_config = SettingsConfigDict(
        env_file="azure_embeddings_openai.env", env_file_encoding="utf-8"
    )
