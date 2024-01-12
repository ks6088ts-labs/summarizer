from fastapi import FastAPI

from server.routers import chat as chat_router
from server.routers import search as search_router

app = FastAPI()

chat_router.add_router(
    app=app,
    path="/chat",
)

search_router.add_router(
    app=app,
    path="/search",
)
