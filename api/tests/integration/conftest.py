from collections.abc import AsyncIterator

import pytest
from litestar import Litestar
from litestar.testing import AsyncTestClient

pytestmark: pytest.MarkDecorator = pytest.mark.anyio


@pytest.fixture(name="client")
async def fx_client(app: Litestar) -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app) as client:
        yield client
