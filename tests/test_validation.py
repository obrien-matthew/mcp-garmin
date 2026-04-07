"""Tests for input validation helpers."""

import pytest

from garmin_mcp.validation import validate_date, validate_limit


class TestValidateLimit:
    def test_within_range(self):
        assert validate_limit(10) == 10

    def test_clamps_to_min(self):
        assert validate_limit(0) == 1

    def test_clamps_to_max(self):
        assert validate_limit(200) == 100

    def test_custom_max(self):
        assert validate_limit(75, max_val=50) == 50


class TestValidateDate:
    def test_valid_date(self):
        assert validate_date("2024-12-25") == "2024-12-25"

    def test_invalid_format(self):
        with pytest.raises(ValueError, match="YYYY-MM-DD"):
            validate_date("12/25/2024")

    def test_invalid_date(self):
        with pytest.raises(ValueError):
            validate_date("2024-02-30")

    def test_empty_string(self):
        with pytest.raises(ValueError, match="YYYY-MM-DD"):
            validate_date("")
