import os

from dotenv import load_dotenv
from fastapi import FastAPI

from server.routers import generate_prompt as generate_prompt_router
from server.routers import rag as rag_router
from server.routers import search as search_router
from server.routers import summarize as summarize_router

DEBUG = str(os.getenv("DEBUG")).lower() == "true"

if DEBUG:
    print("DEBUG MODE")
    load_dotenv("./langsmith.env")

app = FastAPI()

summarize_router.add_router(
    app=app,
    path="/summarize",
)

search_router.add_router(
    app=app,
    path="/search",
)

rag_router.add_router(
    app=app,
    path="/rag",
)

generate_prompt_router.add_router(
    app=app,
    path="/generate_prompt",
)
