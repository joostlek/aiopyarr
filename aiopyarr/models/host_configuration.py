"""PyArrHostConfiguration."""
from __future__ import annotations

from dataclasses import dataclass
from re import search

from aiopyarr.const import HEADERS

from .. import ArrException


@dataclass
class PyArrHostConfiguration:  # pylint: disable=too-many-instance-attributes
    """PyArrHostConfiguration."""

    api_token: str | None = None
    hostname: str | None = None
    ipaddress: str | None = None
    port: int | None = None
    ssl: bool = False
    verify_ssl: bool = True
    base_api_path: str | None = None
    url: str | None = None
    api_ver: str | None = None

    def __post_init__(self) -> None:
        """Post init."""
        if self.api_token is None:
            raise ArrException(message="No api token to the server was provided")
        if self.hostname is None and self.ipaddress is None and self.url is None:
            raise ArrException(
                message="No url, hostname or ipaddress to the server was provided"
            )
        HEADERS["X-Api-Key"] = self.api_token

    def api_url(self, command: str, initialize: bool = False) -> str:
        """Return the generated base URL based on host configuration."""
        if initialize:
            return f"{self.base_url}/initialize.js"
        return f"{self.base_url}/api/{self.api_ver}/{command}"

    @property
    def base_url(self) -> str:
        """Return the base URL for the configured service."""
        if self.url is not None:
            self.url = self.url[:-1] if self.url[-1] == "/" else self.url
            if res := search(r"(https?:\/\/[a-z|\d|\.]*[^:])([\/^:\d]*)(.*)", self.url):
                if not res.group(2):
                    self.url = f"{res.group(1)[:-1]}:{self.port}/{res.group(3)}"
            return self.url
        protocol = f"http{'s' if self.ssl else ''}"
        host = f"{self.hostname or self.ipaddress}:{self.port}"
        return f"{protocol}://{host}{self.base_api_path or ''}"
