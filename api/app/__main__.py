import os
import sys
from typing import NoReturn

from litestar.cli.main import litestar_group


def run_litestar() -> NoReturn:
    """Entry point for the app, creates the app."""
    os.environ.setdefault("LITESTAR_APP", "app.asgi:create_app")

    sys.exit(litestar_group())  # type: ignore[reportUnknownArgumentType]


if __name__ == "__main__":
    run_litestar()
