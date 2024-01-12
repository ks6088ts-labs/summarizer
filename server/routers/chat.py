from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models import AzureChatOpenAI
from langserve import add_routes

from server.settings import azure_chat_openai as azure_chat_openai_settings


def add_router(app: FastAPI, path: str):
    chat_settings = azure_chat_openai_settings.AzureChatOpenAiSettings()

    azure_chat_openai_model = AzureChatOpenAI(
        api_version=chat_settings.api_version,
        azure_endpoint=chat_settings.azure_endpoint,
        azure_deployment=chat_settings.azure_deployment,
        api_key=chat_settings.api_key,
    )

    prompt = ChatPromptTemplate.from_template(
        "Please summarize the following sentences in three lines,\
        using the same language as the original text.\n```\n{topic}\n```"
    )

    add_routes(
        app,
        prompt | azure_chat_openai_model,
        path=path,
    )
