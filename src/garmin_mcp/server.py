"""MCP server for Garmin Connect."""

from mcp.server.fastmcp import FastMCP

from .client import GarminClientError, call
from .formatting import format_response
from .validation import validate_date, validate_limit

mcp = FastMCP("mcp-garmin")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _garmin_call(
    method: str,
    *args: object,
    empty_message: str = "No data available.",
    **kwargs: object,
) -> str:
    """Call a Garmin client method, format the result, handle errors."""
    try:
        data = call(method, *args, **kwargs)
    except GarminClientError as exc:
        return str(exc)
    return format_response(data, empty_message=empty_message)


# ---------------------------------------------------------------------------
# Daily Health
# ---------------------------------------------------------------------------


@mcp.tool()
def get_daily_summary(date: str) -> str:
    """Get daily activity summary (steps, calories, distance, active minutes).

    Args:
        date: Date in YYYY-MM-DD format.
    """
    d = validate_date(date)
    return _garmin_call(
        "get_user_summary", d, empty_message=f"No summary data for {d}."
    )


@mcp.tool()
def get_heart_rates(date: str) -> str:
    """Get heart rate data for a given date.

    Args:
        date: Date in YYYY-MM-DD format.
    """
    d = validate_date(date)
    return _garmin_call(
        "get_heart_rates", d, empty_message=f"No heart rate data for {d}."
    )


@mcp.tool()
def get_sleep_data(date: str) -> str:
    """Get sleep stages and metrics for a given date.

    Args:
        date: Date in YYYY-MM-DD format.
    """
    d = validate_date(date)
    return _garmin_call("get_sleep_data", d, empty_message=f"No sleep data for {d}.")


@mcp.tool()
def get_stress_data(date: str) -> str:
    """Get stress levels throughout the day.

    Args:
        date: Date in YYYY-MM-DD format.
    """
    d = validate_date(date)
    return _garmin_call("get_stress_data", d, empty_message=f"No stress data for {d}.")


@mcp.tool()
def get_all_day_stress(date: str) -> str:
    """Get all-day stress summary for a given date.

    Args:
        date: Date in YYYY-MM-DD format.
    """
    d = validate_date(date)
    return _garmin_call(
        "get_all_day_stress", d, empty_message=f"No stress data for {d}."
    )


@mcp.tool()
def get_body_battery(date: str) -> str:
    """Get Body Battery (energy) levels for a given date.

    Args:
        date: Date in YYYY-MM-DD format.
    """
    d = validate_date(date)
    return _garmin_call(
        "get_body_battery", d, empty_message=f"No Body Battery data for {d}."
    )


@mcp.tool()
def get_steps_data(date: str) -> str:
    """Get detailed step data for a given date.

    Args:
        date: Date in YYYY-MM-DD format.
    """
    d = validate_date(date)
    return _garmin_call("get_steps_data", d, empty_message=f"No step data for {d}.")


@mcp.tool()
def get_hrv_data(date: str) -> str:
    """Get Heart Rate Variability (HRV) data for a given date.

    Args:
        date: Date in YYYY-MM-DD format.
    """
    d = validate_date(date)
    return _garmin_call("get_hrv_data", d, empty_message=f"No HRV data for {d}.")


@mcp.tool()
def get_spo2_data(date: str) -> str:
    """Get blood oxygen saturation (SpO2) data for a given date.

    Args:
        date: Date in YYYY-MM-DD format.
    """
    d = validate_date(date)
    return _garmin_call("get_spo2_data", d, empty_message=f"No SpO2 data for {d}.")


@mcp.tool()
def get_respiration_data(date: str) -> str:
    """Get respiratory rate data for a given date.

    Args:
        date: Date in YYYY-MM-DD format.
    """
    d = validate_date(date)
    return _garmin_call(
        "get_respiration_data", d, empty_message=f"No respiration data for {d}."
    )


@mcp.tool()
def get_training_readiness(date: str) -> str:
    """Get training readiness score for a given date.

    Args:
        date: Date in YYYY-MM-DD format.
    """
    d = validate_date(date)
    return _garmin_call(
        "get_training_readiness",
        d,
        empty_message=f"No training readiness data for {d}.",
    )


@mcp.tool()
def get_intensity_minutes(date: str) -> str:
    """Get intensity minutes data for a given date.

    Args:
        date: Date in YYYY-MM-DD format.
    """
    d = validate_date(date)
    return _garmin_call(
        "get_intensity_minutes_data",
        d,
        empty_message=f"No intensity minutes data for {d}.",
    )


@mcp.tool()
def get_resting_heart_rate(date: str) -> str:
    """Get resting heart rate for a given date.

    Args:
        date: Date in YYYY-MM-DD format.
    """
    d = validate_date(date)
    return _garmin_call(
        "get_resting_heart_rate",
        d,
        empty_message=f"No resting heart rate data for {d}.",
    )


# ---------------------------------------------------------------------------
# Activities
# ---------------------------------------------------------------------------


@mcp.tool()
def get_activities(start: int = 0, limit: int = 20) -> str:
    """List recent activities, newest first.

    Args:
        start: Zero-based index to start from.
        limit: Maximum number of activities to return (1-100).
    """
    return _garmin_call(
        "get_activities",
        start,
        validate_limit(limit),
        empty_message="No activities found.",
    )


@mcp.tool()
def get_activities_by_date(
    start_date: str, end_date: str, activity_type: str | None = None
) -> str:
    """Get activities within a date range, optionally filtered by type.

    Args:
        start_date: Start date in YYYY-MM-DD format.
        end_date: End date in YYYY-MM-DD format.
        activity_type: Optional activity type filter (e.g. "running", "cycling").
    """
    sd = validate_date(start_date)
    ed = validate_date(end_date)
    return _garmin_call(
        "get_activities_by_date",
        sd,
        ed,
        activity_type,
        empty_message=f"No activities found between {sd} and {ed}.",
    )


@mcp.tool()
def get_activities_for_date(date: str) -> str:
    """Get all activities for a specific date.

    Args:
        date: Date in YYYY-MM-DD format.
    """
    d = validate_date(date)
    return _garmin_call(
        "get_activities_fordate", d, empty_message=f"No activities on {d}."
    )


@mcp.tool()
def get_last_activity() -> str:
    """Get the most recent activity."""
    return _garmin_call("get_last_activity", empty_message="No activities found.")


@mcp.tool()
def get_activity(activity_id: int) -> str:
    """Get a single activity by its ID.

    Args:
        activity_id: Garmin activity ID.
    """
    return _garmin_call(
        "get_activity", activity_id, empty_message=f"Activity {activity_id} not found."
    )


@mcp.tool()
def get_activity_details(activity_id: int) -> str:
    """Get detailed metrics for an activity (laps, charts, etc.).

    Args:
        activity_id: Garmin activity ID.
    """
    return _garmin_call(
        "get_activity_details",
        activity_id,
        empty_message=f"No details for activity {activity_id}.",
    )


@mcp.tool()
def get_activity_splits(activity_id: int) -> str:
    """Get split/lap data for an activity.

    Args:
        activity_id: Garmin activity ID.
    """
    return _garmin_call(
        "get_activity_splits",
        activity_id,
        empty_message=f"No splits for activity {activity_id}.",
    )


@mcp.tool()
def get_activity_weather(activity_id: int) -> str:
    """Get weather conditions during an activity.

    Args:
        activity_id: Garmin activity ID.
    """
    return _garmin_call(
        "get_activity_weather",
        activity_id,
        empty_message=f"No weather data for activity {activity_id}.",
    )


@mcp.tool()
def get_activity_hr_zones(activity_id: int) -> str:
    """Get heart rate zone distribution for an activity.

    Args:
        activity_id: Garmin activity ID.
    """
    return _garmin_call(
        "get_activity_hr_in_timezones",
        activity_id,
        empty_message=f"No HR zone data for activity {activity_id}.",
    )


@mcp.tool()
def get_activity_gear(activity_id: int) -> str:
    """Get equipment/gear used in an activity.

    Args:
        activity_id: Garmin activity ID.
    """
    return _garmin_call(
        "get_activity_gear",
        activity_id,
        empty_message=f"No gear data for activity {activity_id}.",
    )


@mcp.tool()
def get_activity_exercise_sets(activity_id: int) -> str:
    """Get strength training exercise sets for an activity.

    Args:
        activity_id: Garmin activity ID.
    """
    return _garmin_call(
        "get_activity_exercise_sets",
        activity_id,
        empty_message=f"No exercise set data for activity {activity_id}.",
    )


# ---------------------------------------------------------------------------
# Workouts
# ---------------------------------------------------------------------------


@mcp.tool()
def get_workouts() -> str:
    """List saved workout templates."""
    return _garmin_call("get_workouts", empty_message="No workouts found.")


@mcp.tool()
def get_workout(workout_id: int) -> str:
    """Get a saved workout template by ID.

    Args:
        workout_id: Garmin workout ID.
    """
    return _garmin_call(
        "get_workout_by_id",
        workout_id,
        empty_message=f"Workout {workout_id} not found.",
    )


# ---------------------------------------------------------------------------
# Body Composition
# ---------------------------------------------------------------------------


@mcp.tool()
def get_body_composition(start_date: str, end_date: str) -> str:
    """Get body composition data for a date range.

    Args:
        start_date: Start date in YYYY-MM-DD format.
        end_date: End date in YYYY-MM-DD format.
    """
    sd = validate_date(start_date)
    ed = validate_date(end_date)
    return _garmin_call(
        "get_body_composition",
        sd,
        ed,
        empty_message=f"No body composition data between {sd} and {ed}.",
    )


@mcp.tool()
def get_weigh_ins(start_date: str, end_date: str) -> str:
    """Get weight measurements for a date range.

    Args:
        start_date: Start date in YYYY-MM-DD format.
        end_date: End date in YYYY-MM-DD format.
    """
    sd = validate_date(start_date)
    ed = validate_date(end_date)
    return _garmin_call(
        "get_weigh_ins",
        sd,
        ed,
        empty_message=f"No weigh-in data between {sd} and {ed}.",
    )



# ---------------------------------------------------------------------------
# Profile & Fitness
# ---------------------------------------------------------------------------


@mcp.tool()
def get_user_profile() -> str:
    """Get the user's Garmin Connect profile information."""
    return _garmin_call("get_user_profile", empty_message="Unable to retrieve profile.")


@mcp.tool()
def get_max_metrics(date: str) -> str:
    """Get VO2 max and related fitness metrics for a given date.

    Args:
        date: Date in YYYY-MM-DD format.
    """
    d = validate_date(date)
    return _garmin_call("get_max_metrics", d, empty_message=f"No max metrics for {d}.")


@mcp.tool()
def get_fitness_age(date: str) -> str:
    """Get calculated fitness age for a given date.

    Args:
        date: Date in YYYY-MM-DD format.
    """
    d = validate_date(date)
    return _garmin_call(
        "get_fitnessage_data", d, empty_message=f"No fitness age data for {d}."
    )


@mcp.tool()
def get_training_status(date: str) -> str:
    """Get current training status for a given date.

    Args:
        date: Date in YYYY-MM-DD format.
    """
    d = validate_date(date)
    return _garmin_call(
        "get_training_status", d, empty_message=f"No training status for {d}."
    )


@mcp.tool()
def get_personal_records() -> str:
    """Get personal best records across all activities."""
    return _garmin_call(
        "get_personal_records", empty_message="No personal records found."
    )
