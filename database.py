from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

DATABASE_URL = "sqlite+aiosqlite:///books.db"

engine = create_async_engine(DATABASE_URL)

new_session = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_db():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]