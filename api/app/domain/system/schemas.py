from typing import Literal

from pydantic import BaseModel

from app import __version__

__all__ = (
    "HealthStatus",
    "SystemHealth",
)

type HealthStatus = Literal["online", "offline"]


class SystemHealth(BaseModel):
    """Contains information about the system.

    Attributes
    ----------
    database_status : :type:`HealthStatus`
        Whether the database is online or offline.
    version : :class:`str`
        Version of the application.
    """

    database_status: HealthStatus
    version: str = __version__
