"""Response formatting for Garmin MCP tools."""

import json
from typing import Any


def format_response(data: Any, *, empty_message: str = "No data available.") -> str:
    """Serialize a Garmin API response to a JSON string.

    Returns *empty_message* when the data is None or empty.
    """
    if data is None:
        return empty_message
    if isinstance(data, (list, dict)) and not data:
        return empty_message
    return json.dumps(data, default=str, indent=2)
