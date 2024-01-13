from fastapi import FastAPI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import SystemMessage
from langserve import add_routes

from server.routers import util


def add_router(app: FastAPI, path: str):
    azure_chat_openai = util.get_azure_chat_openai()

    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content="あなたは与えられた文章を簡潔な要約を出力するアシスタントです。"),
            HumanMessagePromptTemplate.from_template("以下の文章を要約してください。\n{article}"),
        ]
    )

    add_routes(
        app,
        prompt | azure_chat_openai,
        path=path,
    )
