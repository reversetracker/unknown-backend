from uuid import UUID

import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture

from unknown_backend.models import Account


@pytest.mark.asyncio
async def test_example(client: AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == 200
    assert response.text == "Hello, World!"


@pytest.mark.asyncio
async def test_example2(mocker: MockerFixture, client: AsyncClient) -> None:
    mocker.patch(
        "uuid.uuid4", return_value=UUID("17fd37b9-50bc-4ae3-b9ae-aebdb927c2c3")
    )
    response = await client.get("/example")
    assert response.status_code == 200
    assert response.text == "Created Account UID: 17fd37b9-50bc-4ae3-b9ae-aebdb927c2c3"


@pytest.mark.asyncio
async def test_example3(mocker: MockerFixture, client: AsyncClient) -> None:
    mocker.patch(
        "uuid.uuid4", return_value=UUID("17fd37b9-50bc-b9ae-4ae3-aebdb927c2c3")
    )
    response = await client.get("/example")
    assert response.status_code == 200
    account = await Account.get_by_uid(uid="17fd37b9-50bc-b9ae-4ae3-aebdb927c2c3")
    assert account.uid == "17fd37b9-50bc-b9ae-4ae3-aebdb927c2c3"
