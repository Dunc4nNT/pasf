import pytest

pytestmark: pytest.MarkDecorator = pytest.mark.anyio
pytest_plugins: list[str] = ["tests.data_fixtures"]


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"
