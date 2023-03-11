from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import engine
from elasticsearch import Elasticsearch
from app.core.config import settings


async def get_session() -> AsyncGenerator:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


async def get_es():
    try:
        es = Elasticsearch(
            hosts=[
                f"http://{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}/"
            ]
        )
        yield es
    finally:
        es.close()
