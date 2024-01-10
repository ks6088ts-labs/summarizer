from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_openai.chat_models import AzureChatOpenAI
from langserve import add_routes

from server.settings import azure_openai as azure_openai_settings

app = FastAPI()

prompt = ChatPromptTemplate.from_template(
    "Please summarize the following sentences in three lines,\
    using the same language as the original text.\n```\n{topic}\n```"
)

settings = azure_openai_settings.AzureOpenAiSettings()

azure_chat_openai_model = AzureChatOpenAI(
    api_version=settings.api_version,
    azure_endpoint=settings.azure_endpoint,
    azure_deployment=settings.azure_deployment,
    api_key=settings.api_key,
)

add_routes(
    app,
    prompt | azure_chat_openai_model,
    path="/azure_openai",
)
