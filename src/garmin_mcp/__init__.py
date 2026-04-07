"""MCP server for Garmin Connect health and fitness data."""

from .auth import interactive_login
from .server import mcp


def main() -> None:
    """Run the MCP server over stdio."""
    mcp.run(transport="stdio")


def login() -> None:
    """CLI entry point for interactive Garmin login."""
    interactive_login()


__all__ = ["login", "main", "mcp"]
