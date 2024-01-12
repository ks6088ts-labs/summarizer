from fastapi import FastAPI
from langserve import add_routes

from server.routers import util


def add_router(app: FastAPI, path: str):
    azure_openai_embeddings = util.get_azure_openai_embeddings()
    azure_search_fields = util.get_azure_search_fields(
        embeddings=azure_openai_embeddings,
    )
    azure_search = util.get_azure_search(
        fields=azure_search_fields,
        embeddings=azure_openai_embeddings,
    )

    add_routes(
        app,
        azure_search.as_retriever(),
        path=path,
    )
