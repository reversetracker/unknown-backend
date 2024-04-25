# from typing import Union
#
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.ext.asyncio import create_async_engine
# from sqlalchemy.ext.asyncio import async_scoped_session
# from sqlalchemy.orm import sessionmaker, Session
# from sqlalchemy.sql import Update, Delete, Insert
#
# from backends.http.database import contexts
# from configs import settings
#
# MYSQL_SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL  # mysql
# SQLITE3_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sqlite3.db"  # sqlite3
#
# # Please don't change it unless you know what you are doing.
# WRITER_ISOLATION_LEVEL = "SERIALIZABLE"
#
# writer_engine = create_async_engine(
#     MYSQL_SQLALCHEMY_DATABASE_URL, echo=False, future=True, isolation_level=WRITER_ISOLATION_LEVEL
# )
#
# reader_engine = create_async_engine(
#     SQLITE3_SQLALCHEMY_DATABASE_URL, echo=False, future=True
# )
#
# engines = {
#     "writer": writer_engine,
#     "reader": reader_engine,
# }
#
#
# class SqlSession(Session):
#     def get_bind(self, mapper=None, clause=None, **kw):
#         if self._flushing or isinstance(clause, (Update, Delete, Insert)):
#             return engines["writer"].sync_engine
#         else:
#             return engines["reader"].sync_engine
#
#
# async_session_factory = sessionmaker(
#     class_=AsyncSession, sync_session_class=SqlSession, expire_on_commit=False,
# )
#
# session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
#     session_factory=async_session_factory,
#     scopefunc=contexts.get_current_context_session_id,
# )
