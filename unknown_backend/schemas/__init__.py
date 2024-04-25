from __future__ import annotations

from typing import Generic
from typing import Optional
from typing import Sequence
from typing import TypeVar

import pydantic
from pydantic import BaseModel

DataT = TypeVar("DataT")


class Paginated(BaseModel, Generic[DataT]):
    """
    `Paginated` 클래스는 FastAPI 응답에서 페이징 처리된 데이터를 나타냅니다.

    이 클래스는 총 항목 수(`total_count`), 현재 페이지 항목 수(`current_count`), 페이지당 항목 수(`limit`),
    현재 페이지 번호(`current`), 다음 페이지 번호(`next`), 이전 페이지 번호(`previous`),
    그리고 현재 페이지의 실제 결과(`results`)를 속성으로 갖습니다.

    클래스는 Pydantic의 root_validator를 사용하여 `next`, `previous`, `current_count`를 자동으로 계산합니다.

    이 클래스는 아래와 같은 FastAPI 경로 작업에서 사용될 수 있습니다.

    ```python
    @router.get(
        "/transactions/users/{uid}",
        response_model=Paginated[schemas.TransactionGet],
    )
    async def your_fastapi_end_point():
        # Implement the route logic here
        # ...
        # ...
        return schemas.Paginated(
            current=page,
            limit=limit,
            results=transactions,  # <- List[schemas.TransactionGet]
            total_count=total_count,
        )
    ```
    이런 식으로 FastAPI 라우트에서 이 클래스를 사용하면 클라이언트는 총 항목 수, 현재 페이지 번호, 다음/이전 페이지 번호 등의 정보와 함께
    `Generic` 에 명시 된 클래스를 이용하여 validation 을 진행하고 그에 맞는 결과를 받아 볼 수 있습니다.
    """

    # count information
    total_count: int
    current_count: Optional[int] = None

    # page information
    limit: int
    next: Optional[int] = None
    current: int
    previous: Optional[int] = None

    # actual results
    results: Sequence[DataT]

    @pydantic.model_validator(mode="before")
    @classmethod
    def calculate_next(cls, values):
        if not isinstance(values, dict):
            return values
        current = values.get("current")
        total_count = values.get("total_count")
        limit = values["limit"]
        if current is not None and total_count is not None:
            if (current * limit) < total_count:
                values["next"] = current + 1
        return values

    @pydantic.model_validator(mode="before")
    @classmethod
    def calculate_previous(cls, values):
        if not isinstance(values, dict):
            return values
        current = values.get("current")
        if current is not None and current > 1:
            values["previous"] = current - 1
        return values

    @pydantic.model_validator(mode="before")
    @classmethod
    def calculate_current_count(cls, values):
        if not isinstance(values, dict):
            return values
        results = values.get("results", [])
        values["current_count"] = len(results)
        return values


class Account(BaseModel):
    id: int
    uid: str

    class Config:
        from_attributes = True
