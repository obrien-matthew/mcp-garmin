"""Garmin Connect authentication and credential management."""

import os
import sys

from garminconnect import Garmin


def get_credentials() -> tuple[str, str]:
    """Load Garmin credentials from environment variables.

    Returns:
        Tuple of (email, password).

    Raises:
        RuntimeError: If required environment variables are missing.
    """
    email = os.environ.get("GARMIN_EMAIL", "")
    password = os.environ.get("GARMIN_PASSWORD", "")
    if not email or not password:
        msg = "GARMIN_EMAIL and GARMIN_PASSWORD environment variables are required"
        raise RuntimeError(msg)
    return email, password


def create_client() -> Garmin:
    """Create a Garmin client and log in using saved tokens or credentials.

    The garminconnect library persists tokens to
    ``~/.garminconnect/garmin_tokens.json`` automatically. On subsequent
    calls the saved tokens are loaded and refreshed transparently.
    """
    email, password = get_credentials()
    client = Garmin(email, password)
    client.login()
    return client


def interactive_login() -> None:
    """Run an interactive login flow, prompting for MFA if needed.

    This is intended to be called from the ``mcp-garmin-login`` CLI
    entry point so the user can establish tokens before starting the
    MCP server.
    """
    email = os.environ.get("GARMIN_EMAIL", "")
    password = os.environ.get("GARMIN_PASSWORD", "")

    if not email:
        email = input("Garmin email: ")
    if not password:
        password = input("Garmin password: ")

    def prompt_mfa() -> str:
        return input("Enter MFA code: ")

    client = Garmin(email, password, prompt_mfa=prompt_mfa)

    try:
        client.login()
    except Exception as exc:
        print(f"Login failed: {exc}", file=sys.stderr)
        sys.exit(1)

    name = client.get_full_name()
    print(f"Logged in as {name}")
    print("Tokens saved to ~/.garminconnect/garmin_tokens.json")
