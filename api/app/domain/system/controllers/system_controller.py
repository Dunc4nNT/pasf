from collections.abc import Sequence

from asyncpg import Connection
from litestar import Controller, MediaType, Request, Response, get

from app.domain.system import urls
from app.domain.system.schemas import HealthStatus, SystemHealth


class SystemController(Controller):
    """Controller for the system health endpoint."""

    tags: Sequence[str] | None = ["System"]

    @get(
        operation_id="SystemHealth",
        name="system:health",
        path=urls.SYSTEM_HEALTH,
        summary="Health check.",
        description="Checks whether backend services (database) are online.",
    )
    async def system_health(
        self, request: Request, db_connection: Connection
    ) -> Response[SystemHealth]:
        """Check whether backend services (database) are online.

        Returns
        -------
        Response[SystemHealth]
            Schema containing information about system health.
        """
        db_ping_success = False
        try:
            await db_connection.fetch("SELECT 1;")
            db_ping_success = True
        except ConnectionRefusedError:
            pass

        db_status: HealthStatus = "online" if db_ping_success else "offline"

        return Response(
            SystemHealth(database_status=db_status), status_code=200, media_type=MediaType.JSON
        )
