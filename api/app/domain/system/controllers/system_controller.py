from collections.abc import Sequence

from litestar import Controller, MediaType, Response, get

from app.domain.system import urls
from app.domain.system.schemas import SystemHealth


class SystemController(Controller):
    """Controller for the system health endpoint."""

    tags: Sequence["str"] | None = ["System"]

    @get(
        operation_id="SystemHealth",
        name="system:health",
        path=urls.SYSTEM_HEALTH,
        summary="Health Check",
        description="Checks whether backend services (database) are online.",
    )
    async def system_health(self) -> Response[SystemHealth]:
        """Check whether backend services (database) are online.

        Returns
        -------
        Response[SystemHealth]
            Schema containing information about system health.
        """
        return Response(
            SystemHealth(database_status="online"), status_code=200, media_type=MediaType.JSON
        )
