"""Singleton client wrapper for the Garmin Connect API."""

from typing import Any

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

from .auth import create_client


class GarminClientError(Exception):
    """Raised when a Garmin API call fails."""


_client: Garmin | None = None


def get_client() -> Garmin:
    """Return the shared Garmin client, creating it on first call."""
    global _client
    if _client is None:
        _client = create_client()
    return _client


def call(method: str, *args: Any, **kwargs: Any) -> Any:
    """Call a method on the Garmin client with standardised error handling.

    Returns the raw result from the library, or raises
    ``GarminClientError`` with a user-friendly message.
    """
    client = get_client()
    fn = getattr(client, method, None)
    if fn is None:
        msg = f"Unknown Garmin API method: {method}"
        raise GarminClientError(msg)
    try:
        return fn(*args, **kwargs)
    except GarminConnectAuthenticationError as exc:
        msg = (
            f"Authentication failed: {exc}. Run `mcp-garmin-login` to re-authenticate."
        )
        raise GarminClientError(msg) from exc
    except GarminConnectTooManyRequestsError as exc:
        msg = f"Rate limited by Garmin. Try again later. ({exc})"
        raise GarminClientError(msg) from exc
    except GarminConnectConnectionError as exc:
        msg = f"Connection error: {exc}"
        raise GarminClientError(msg) from exc
