import pytest
from litestar import Litestar

from app.asgi import create_app

pytestmark: pytest.MarkDecorator = pytest.mark.anyio


@pytest.fixture(name="app")
def fx_app() -> Litestar:
    return create_app()
