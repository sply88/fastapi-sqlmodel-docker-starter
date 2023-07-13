from fastapi import FastAPI

from .data_management import Database
from .routers import health, messages
from .settings import Settings

app = FastAPI(
    title="Message API",
    description="A simple API to `GET` `POST` `PATCH` and `DELETE` messages."
)

app.include_router(messages.router)
app.include_router(health.router, prefix="/health")


@app.on_event("startup")
def setup_db():
    Database.setup(db_uri=Settings().db_uri)
