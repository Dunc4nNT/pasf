from typing import TYPE_CHECKING

import pytest
from litestar import Litestar, Response
from litestar.status_codes import HTTP_200_OK
from litestar.testing import AsyncTestClient

from app import __version__
from app.domain.system import urls as system_urls

if TYPE_CHECKING:
    from httpx import Response


pytestmark: pytest.MarkDecorator = pytest.mark.anyio


async def test_system_health(client: AsyncTestClient[Litestar]) -> None:
    response: Response = await client.get(system_urls.SYSTEM_HEALTH)
    assert response.status_code == HTTP_200_OK

    expected_response = {
        "database_status": "online",
        "version": __version__,
    }
    assert response.json() == expected_response
