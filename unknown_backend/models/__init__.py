from __future__ import annotations as __annotations__

from typing import Sequence

from pydantic import BaseModel
from sqlalchemy import Column, select
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base

from unknown_backend import annotations
from unknown_backend.database import session

Base = declarative_base()


class Account(Base):
    __tablename__ = "account"

    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uid: str = Column(String(40), nullable=False, index=True, unique=True)

    def dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    @staticmethod
    def from_schema(schema: BaseModel) -> Account:
        fields = set(inspect(Account).attrs.keys())
        dictionary = {f: v for f, v in schema.dict().items() if f in fields}
        orm = Account(**dictionary)
        return orm

    def __repr__(self):
        return f"Account(id={self.id}, uid='{self.uid})'"

    @classmethod
    @annotations.transactional
    async def get_by_uid(cls, uid: str) -> Account:
        query = select(Account).where(Account.uid == uid)
        query_result = await session.execute(query)
        transaction = query_result.scalar()
        return transaction

    @classmethod
    @annotations.transactional
    async def list_accounts(cls, offset: int, count: int) -> Sequence[Account]:
        query = select(Account).offset(offset).limit(count)
        query_result = await session.execute(query)
        return query_result.scalars().all()

    @classmethod
    @annotations.transactional
    async def create(cls, uid: str) -> Account:
        account = Account(uid=uid)
        session.add(account)
        return account

    @classmethod
    @annotations.transactional
    async def count(cls) -> int:
        query = select(Account).count()
        query_result = await session.execute(query)
        return query_result.scalar()
