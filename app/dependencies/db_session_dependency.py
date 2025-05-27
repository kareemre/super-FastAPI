from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection.connection import sessionmanager

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Database session dependency with auto-commit on success.
    
    Automatically commits the transaction if no exceptions occur.
    Use this when you want automatic transaction management.
    """
    async with sessionmanager.session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise