"""Tests for the Garmin Connect client wrapper."""

import pytest

from garmin_mcp.client import GarminClientError


class TestGarminClientError:
    def test_is_exception(self):
        exc = GarminClientError("test")
        assert isinstance(exc, Exception)

    def test_message(self):
        exc = GarminClientError("something went wrong")
        assert str(exc) == "something went wrong"


class TestCallWithoutCredentials:
    def test_call_raises_without_env(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.delenv("GARMIN_EMAIL", raising=False)
        monkeypatch.delenv("GARMIN_PASSWORD", raising=False)
        # Reset the singleton so it attempts to create a new client
        import garmin_mcp.client as mod

        mod._client = None
        with pytest.raises(RuntimeError, match="GARMIN_EMAIL"):
            from garmin_mcp.client import call

            call("get_full_name")
        # Clean up
        mod._client = None
