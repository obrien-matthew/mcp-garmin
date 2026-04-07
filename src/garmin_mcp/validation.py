"""Input validation helpers for Garmin MCP tools."""

import re
from datetime import date

_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate_date(value: str) -> str:
    """Validate and return an ISO-format date string (YYYY-MM-DD).

    Raises:
        ValueError: If the format is invalid or the date is not real.
    """
    if not _ISO_DATE.match(value):
        msg = f"Date must be in YYYY-MM-DD format, got: {value!r}"
        raise ValueError(msg)
    # Confirm the date is real (e.g. reject 2024-02-30)
    date.fromisoformat(value)
    return value


def validate_limit(value: int, max_val: int = 100) -> int:
    """Clamp a limit/count parameter to [1, max_val]."""
    return max(1, min(value, max_val))
