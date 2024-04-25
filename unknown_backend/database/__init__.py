import asyncio

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from unknown_backend.configs import settings

# Please don't change it unless you know what you are doing.
ISOLATION_LEVEL = "SERIALIZABLE"

engine: AsyncEngine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,
    isolation_level=ISOLATION_LEVEL,
    # pool_size=5,
    # max_overflow=20,
)

async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

session: AsyncSession | async_scoped_session = async_scoped_session(
    session_factory=async_session_factory,
    # Note: asyncio.gather 사용 금지.
    scopefunc=asyncio.current_task,
    # scopefunc=contexts.get_current_context_session_id,
)
