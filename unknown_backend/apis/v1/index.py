import logging
import uuid

from fastapi import APIRouter
from starlette.responses import PlainTextResponse

from unknown_backend import schemas
from unknown_backend.models import Account
from unknown_backend.schemas import Paginated
from unknown_backend.services import account_service

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/", response_class=PlainTextResponse)
async def index():
    """Index Page of the API."""
    return "Hello, World!"


@router.get("/example", response_class=PlainTextResponse)
async def example():
    """CRUD Example is here!"""
    uid = str(uuid.uuid4())
    await account_service.create_account(uid)
    account = await account_service.get_account(uid=uid)
    return f"Created Account UID: {account['uid']}"


@router.get("/example2", response_class=PlainTextResponse)
async def example2():
    """CRUD Example is here!"""
    uid = str(uuid.uuid4())
    await account_service.create_account(uid)
    await account_service.create_account(uid)  # will be raised here
    return f"Here not be reached!"


@router.get("/example3", response_class=PlainTextResponse)
async def example3():
    """CRUD Example is here!"""
    uid = str(uuid.uuid4())
    await account_service.force_exception(uid)
    return "Here not be reached!"


@router.get(
    "/accounts",
    response_model=Paginated[schemas.Account],
)
async def list_users(offset: int = 0, count: int = 10) -> Paginated[schemas.Account]:
    """List all users."""
    accounts = await Account.list_accounts(offset=offset, count=count)
    total_count = 10
    return Paginated(
        current=offset,
        limit=count,
        results=accounts,
        total_count=total_count,
    )
