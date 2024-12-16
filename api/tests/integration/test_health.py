from typing import TYPE_CHECKING

import pytest
from litestar import Litestar
from litestar.status_codes import HTTP_200_OK
from litestar.testing import AsyncTestClient

if TYPE_CHECKING:
    from httpx import Response


pytestmark: pytest.MarkDecorator = pytest.mark.anyio


async def test_health(client: AsyncTestClient[Litestar]) -> None:
    response: Response = await client.get("/health-check")

    assert response.status_code == HTTP_200_OK
    assert response.text == "definitely healthy"
