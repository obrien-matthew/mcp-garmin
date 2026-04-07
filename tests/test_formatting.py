"""Tests for response formatters."""

from garmin_mcp.formatting import format_response


class TestFormatResponse:
    def test_formats_dict(self):
        result = format_response({"steps": 10000})
        assert '"steps": 10000' in result

    def test_formats_list(self):
        result = format_response([1, 2, 3])
        assert "[" in result

    def test_none_returns_message(self):
        result = format_response(None)
        assert result == "No data available."

    def test_empty_dict_returns_message(self):
        result = format_response({})
        assert result == "No data available."

    def test_empty_list_returns_message(self):
        result = format_response([])
        assert result == "No data available."

    def test_custom_empty_message(self):
        result = format_response(None, empty_message="Nothing here.")
        assert result == "Nothing here."
