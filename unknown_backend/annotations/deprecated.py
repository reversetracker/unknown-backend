import asyncio
import functools
import logging
from collections import defaultdict

from unknown_backend.database import contexts
from unknown_backend.database import session

logger = logging.getLogger(__name__)


def transactional(f):
    """
    데코레이터는 함수를 감싸고 데이터베이스 트랜잭션 관리를 합니다. 트랜잭션 범위가 중첩될 수 있도록 설계 되었습니다.

    주요 로직은 다음과 같습니다:
    - 각 함수 호출 시작 시 트랜잭션 중첩 카운트를 증가시킵니다.
    - 함수 실행이 성공하면 가장 바깥 트랜잭션에서만 커밋합니다.
    - 함수 실행 중 예외가 발생하면 가장 바깥 트랜잭션에서만 롤백합니다.
    - 함수 실행이 완료되면 트랜잭션 중첩 카운트를 감소시킵니다.

    Example::
    @transactional
    def func1():
        # do something

    @transactional
    def func2():
        func1()  # 이 경우 func1은 이미 트랜잭션 내부에 있습니다.
        # do something else

    func2 호출 시 func1과 func2 모두 트랜잭션 내부에 있지만 커밋과 롤백은 func2에서만 발생합니다.
    func1 이 실패 시 func1 과 func2 는 모두 롤백됩니다.
    """

    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        nested_count = contexts.get_current_context_nested_count()
        is_outermost_transaction = nested_count == 0
        try:
            contexts.increase_current_context_nested_count()
            result = await f(*args, **kwargs)
            if is_outermost_transaction:
                logger.info(f"COMMITTING {f.__name__} session..")
                await session.commit()
        except Exception as e:
            if is_outermost_transaction:
                logger.info(f"ROLLING BACK {f.__name__} session..")
                await session.rollback()
            raise e
        finally:
            contexts.decrease_current_context_nested_count()
        return result

    return wrapper


class Serializable:
    locks = defaultdict(asyncio.Lock)

    def __init__(self, context: str):
        self.context = context

    def __call__(self, f):
        @functools.wraps(f)
        async def wrapper(*args, **kwargs):
            nested_count = contexts.get_current_context_nested_count()
            is_outermost_transaction = nested_count == 0
            if not is_outermost_transaction:
                return await f(*args, **kwargs)
            async with self.locks[self.context]:
                return await f(*args, **kwargs)

        return wrapper


serializable = Serializable("transaction")
