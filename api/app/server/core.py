from typing import override

from click import Group
from litestar.config.app import AppConfig
from litestar.plugins import CLIPluginProtocol, InitPluginProtocol

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
        app_config.route_handlers.extend([
            SystemController,
        ])

        return super().on_app_init(app_config)
