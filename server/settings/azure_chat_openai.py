from pydantic import (
    Field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class AzureChatOpenAiSettings(BaseSettings):
    # See API versions here: https://github.com/Azure/azure-rest-api-specs/tree/main/specification/cognitiveservices/data-plane/AzureOpenAI/inference
    api_version: str = Field("2023-12-01-preview", alias="api_version")
    azure_endpoint: str = Field(
        "https://YOUR_AOAI_NAME.openai.azure.com/", alias="azure_endpoint"
    )
    azure_deployment: str = Field("gpt-35-turbo", alias="azure_deployment")
    api_key: str = Field("YOUR_API_KEY", alias="api_key")

    model_config = SettingsConfigDict(
        env_file="azure_chat_openai.env", env_file_encoding="utf-8"
    )
