from typing import override

from click import Group
from litestar.config.app import AppConfig
from litestar.openapi.config import OpenAPIConfig
from litestar.plugins import CLIPluginProtocol, InitPluginProtocol
from litestar_asyncpg import AsyncpgConfig, AsyncpgPlugin, PoolConfig

from app import __version__
from app.domain.cards.controllers import CardController, DeckController, TagController
from app.domain.system.controllers import SystemController


class PasfCore(CLIPluginProtocol, InitPluginProtocol):
    """Main pasf core plugin.

    This configures routes, guards, plugins, etc.
    """

    @override
    def on_cli_init(self, cli: Group) -> None:
        return super().on_cli_init(cli)

    @override
    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        app_config.openapi_config = OpenAPIConfig(
            title="pasf", version=__version__, use_handler_docstrings=True
        )

        app_config.route_handlers.extend([
            CardController,
            DeckController,
            TagController,
            SystemController,
        ])

        asyncpg_plugin = AsyncpgPlugin(
            config=AsyncpgConfig(
                pool_config=PoolConfig(
                    dsn="postgresql://pasf:test@localhost:5432/pasf",
                )
            )
        )

        app_config.plugins.extend([
            asyncpg_plugin,
        ])

        return super().on_app_init(app_config)
