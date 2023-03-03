from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import engine


async def get_session() -> AsyncGenerator:
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
