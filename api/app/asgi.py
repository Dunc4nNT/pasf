from litestar import Litestar

from app.server import PasfCore


def create_app() -> Litestar:
    """Create the main litestar app.

    Returns
    -------
    Litestar
        The litestar application.
    """
    return Litestar(plugins=[PasfCore()])
