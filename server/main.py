import os

from dotenv import load_dotenv
from fastapi import FastAPI

from server.routers import chat as chat_router
from server.routers import rag as rag_router
from server.routers import search as search_router

DEBUG = str(os.getenv("DEBUG")).lower() == "true"

if DEBUG:
    print("DEBUG MODE")
    load_dotenv("./langsmith.env")

app = FastAPI()

chat_router.add_router(
    app=app,
    path="/chat",
)

search_router.add_router(
    app=app,
    path="/search",
)

rag_router.add_router(
    app=app,
    path="/rag",
)
