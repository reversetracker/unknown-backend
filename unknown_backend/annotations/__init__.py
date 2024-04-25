import asyncio
import contextlib
import functools
import logging
import time
from collections import defaultdict
from contextvars import ContextVar

from sqlalchemy.exc import OperationalError

from unknown_backend.database import session

logger = logging.getLogger(__name__)

nested_count_context: ContextVar[int] = ContextVar("transaction_count", default=0)


@contextlib.asynccontextmanager
async def transaction_scope():
    """Provide a transactional scope around a series of operations."""

    # 중첩된 트랜잭션 카운트 설정
    nested_count = nested_count_context.get()
    nested_count_context.set(nested_count + 1)
    is_outermost_transaction = nested_count == 0

    try:
        yield None
        if is_outermost_transaction:  # 가장 바깥의 트랜잭션인 경우에만 커밋
            await session.commit()
    except Exception as e:
        if is_outermost_transaction:  # 가장 바깥의 트랜잭션인 경우에만 롤백
            await session.rollback()
        raise e
    finally:
        nested_count = nested_count_context.get()
        nested_count_context.set(nested_count - 1)
        if is_outermost_transaction:
            await session.close()  # 가장 바깥의 트랜잭션인 경우 세션 종료


def transactional(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        async with transaction_scope():
            result = await func(*args, **kwargs)
        return result

    return wrapper


def retry_on_deadlock(retries=3):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return await func(*args, **kwargs)
                except OperationalError as e:
                    # Assuming "OperationalError" is the deadlock exception from SQLAlchemy
                    # Adjust this if your deadlock exception is different
                    if "deadlock" not in str(e).lower():
                        raise
                    if i == retries - 1:  # last retry
                        raise

        return wrapper

    return decorator


def elapsed(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        _elapsed = round(end - start, 2)

        if asyncio.iscoroutine(result):
            result = asyncio.ensure_future(result)
        elif isinstance(result, list) and not isinstance(result, str):
            logger.debug(
                f"{f.__name__}: took {_elapsed} sec with {len(result)} results."
            )
        else:
            logger.debug(f"{f.__name__}: took {_elapsed} sec.")

        return result

    return wrapper


class Serializable:
    locks = defaultdict(asyncio.Lock)

    def __init__(self, context: str):
        self.context = context

    def __call__(self, f):
        @functools.wraps(f)
        async def wrapper(*args, **kwargs):
            nested_count = nested_count_context.get()
            is_outermost_transaction = nested_count == 0
            if not is_outermost_transaction:
                return await f(*args, **kwargs)
            async with self.locks[self.context]:
                return await f(*args, **kwargs)

        return wrapper


serializable = Serializable("transaction")
