from unknown_backend import annotations
from unknown_backend import models


@annotations.transactional
async def get_account(uid: str) -> dict:
    """
    계정을 가져옵니다.
    """
    account = await models.Account.get_by_uid(uid)
    return account.dict()


@annotations.transactional
async def list_accounts(offset: int, count: int) -> list[dict]:
    """
    계정 목록을 가져옵니다.
    """
    accounts = await models.Account.list_accounts(offset, count)
    return [account.dict() for account in accounts]


@annotations.transactional
async def create_account(uid: str) -> dict:
    """
    새로운 계정을 생성합니다.
    """
    if await models.Account.get_by_uid(uid):
        raise ValueError(f"Account with uid '{uid}' already exists")

    account = await models.Account.create(uid)
    return account.dict()


@annotations.transactional
async def force_exception(uid: str) -> dict:
    """
    새로운 계정을 생성합니다.
    """
    account = await models.Account.create(uid)
    raise ValueError("Forced exception")
    return account.dict()
