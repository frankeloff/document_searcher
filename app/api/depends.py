from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import engine
from elasticsearch import Elasticsearch
import os

ELASTICSEARCH_HOST = os.environ.get("ELASTICSEARCH_HOST")
ELASTICSEARCH_PORT = os.environ.get("ELASTICSEARCH_PORT")


async def get_session() -> AsyncGenerator:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


async def get_es():
    try:
        es = Elasticsearch(hosts=[f"http://{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}/"])
        yield es
    finally:
        es.close()
