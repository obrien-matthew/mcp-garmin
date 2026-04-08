"""Response transformers for Garmin MCP tools.

Each function accepts raw API data and returns a trimmed version that preserves
summary information while stripping large time-series arrays. Transformers are
applied in _garmin_call before format_response so the empty-message path is
still reached when a transform reduces a payload to nothing.
"""

from __future__ import annotations

from typing import Any


def trim_heart_rates(data: Any) -> Any:
    """Strip per-reading heartRateValues array; add computed average.

    The raw array contains ~300 [timestamp, bpm] pairs for the day.
    All scalar summary fields (restingHeartRate, maxHeartRate, etc.) are kept.
    """
    if not isinstance(data, dict):
        return data
    readings = data.get("heartRateValues") or []
    valid = [v for _, v in readings if isinstance(v, (int, float)) and v > 0]
    result = {
        k: v
        for k, v in data.items()
        if k not in ("heartRateValues", "heartRateValueDescriptors")
    }
    if valid:
        result["averageHeartRate"] = round(sum(valid) / len(valid))
    return result


def trim_stress(data: Any) -> Any:
    """Strip per-3-min stress and body battery arrays; add computed stats.

    stressValuesArray entries: [timestamp, value] where -1 = unmeasured,
    -2 = during activity, 0-100 = actual stress. bodyBatteryValuesArray
    entries: [timestamp, value, status_string].
    Sentinel values (< 0) are excluded from averages.
    """
    if not isinstance(data, dict):
        return data

    stress_arr = data.get("stressValuesArray") or []
    bb_arr = data.get("bodyBatteryValuesArray") or []

    stress_vals = [
        v
        for entry in stress_arr
        if len(entry) >= 2
        for v in (entry[1],)
        if isinstance(v, (int, float)) and v >= 0
    ]
    bb_vals = [
        entry[1]
        for entry in bb_arr
        if len(entry) >= 2 and isinstance(entry[1], (int, float)) and entry[1] >= 0
    ]

    _strip = {
        "stressValuesArray",
        "bodyBatteryValuesArray",
        "stressValueDescriptorsDTOList",
    }
    result = {k: v for k, v in data.items() if k not in _strip}

    if stress_vals:
        result["computedAvgStress"] = round(sum(stress_vals) / len(stress_vals))
    if bb_vals:
        result["computedAvgBodyBattery"] = round(sum(bb_vals) / len(bb_vals))
        result["computedMinBodyBattery"] = int(min(bb_vals))
        result["computedMaxBodyBattery"] = int(max(bb_vals))

    return result


def trim_sleep(data: Any) -> Any:
    """Strip per-epoch time-series arrays; keep the dailySleepDTO summary.

    All top-level keys whose values are lists are per-epoch arrays
    (sleepLevels, remSleepData, sleepMovement, hrvData, etc.). Keeping only
    dicts, scalars, and None preserves the summary without the raw series.
    """
    if not isinstance(data, dict):
        return data
    return {k: v for k, v in data.items() if not isinstance(v, list)}


def trim_respiration(data: Any) -> Any:
    """Strip raw 2-min respirationValuesArray; keep hourly averages array."""
    if not isinstance(data, dict):
        return data
    return {k: v for k, v in data.items() if k != "respirationValuesArray"}


def trim_hrv(data: Any) -> Any:
    """Strip per-5-min hrvReadings array; keep lastNight and baseline summaries."""
    if not isinstance(data, dict):
        return data
    return {k: v for k, v in data.items() if k != "hrvReadings"}


def trim_activity_list(data: Any) -> Any:
    """Strip userRoles array from activity objects.

    Handles both list[dict] (get_activities, get_activities_by_date) and
    a single dict (get_activity). get_last_activity returns a list even
    though it contains only one entry.
    """
    if isinstance(data, list):
        return [_drop_user_roles(a) for a in data]
    if isinstance(data, dict):
        return _drop_user_roles(data)
    return data


def _drop_user_roles(activity: Any) -> Any:
    if isinstance(activity, dict) and "userRoles" in activity:
        return {k: v for k, v in activity.items() if k != "userRoles"}
    return activity
