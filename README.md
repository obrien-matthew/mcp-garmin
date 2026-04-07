# mcp-garmin

MCP server for Garmin Connect health and fitness data. Read-only access to daily health metrics, activities, workouts, and body composition via the [python-garminconnect](https://github.com/cyberjunky/python-garminconnect) library.

## Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- A Garmin Connect account

## Authentication

Garmin Connect uses email/password authentication with optional MFA. The library persists session tokens to `~/.garminconnect/garmin_tokens.json` after initial login.

### First-time setup

Run the interactive login command to establish tokens. This handles MFA prompts:

```bash
# Set credentials (or the CLI will prompt you)
export GARMIN_EMAIL="you@example.com"
export GARMIN_PASSWORD="your-password"

# Interactive login -- prompts for MFA if enabled
uvx mcp-garmin-login
```

### Running the server

The MCP server requires `GARMIN_EMAIL` and `GARMIN_PASSWORD` environment variables. It reuses tokens saved by the login step and refreshes them automatically.

```bash
export GARMIN_EMAIL="you@example.com"
export GARMIN_PASSWORD="your-password"
```

## Configuration

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "garmin": {
      "command": "uvx",
      "args": ["mcp-garmin"],
      "env": {
        "GARMIN_EMAIL": "you@example.com",
        "GARMIN_PASSWORD": "your-password"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add garmin -- uvx mcp-garmin
```

Set `GARMIN_EMAIL` and `GARMIN_PASSWORD` in your shell environment.

## Tools

All date parameters use ISO format (`YYYY-MM-DD`).

### Daily Health

| Tool | Description |
|------|-------------|
| `get_daily_summary` | Steps, calories, distance, active minutes |
| `get_heart_rates` | Heart rate data |
| `get_sleep_data` | Sleep stages and metrics |
| `get_stress_data` | Detailed stress levels |
| `get_all_day_stress` | All-day stress summary |
| `get_body_battery` | Body Battery (energy) levels |
| `get_steps_data` | Detailed step data |
| `get_hrv_data` | Heart Rate Variability |
| `get_spo2_data` | Blood oxygen saturation |
| `get_respiration_data` | Respiratory rate |
| `get_training_readiness` | Training readiness score |
| `get_intensity_minutes` | Intensity minutes |
| `get_resting_heart_rate` | Resting heart rate |

### Activities

| Tool | Description |
|------|-------------|
| `get_activities` | List recent activities (paginated) |
| `get_activities_by_date` | Activities within a date range |
| `get_activities_for_date` | All activities for a specific date |
| `get_last_activity` | Most recent activity |
| `get_activity` | Single activity by ID |
| `get_activity_details` | Detailed metrics (laps, charts) |
| `get_activity_splits` | Split/lap data |
| `get_activity_weather` | Weather during activity |
| `get_activity_hr_zones` | Heart rate zone distribution |
| `get_activity_gear` | Equipment used |
| `get_activity_exercise_sets` | Strength training sets |

### Workouts

| Tool | Description |
|------|-------------|
| `get_workouts` | List saved workout templates |
| `get_workout` | Single workout by ID |

### Body Composition

| Tool | Description |
|------|-------------|
| `get_body_composition` | Body composition over a date range |
| `get_weigh_ins` | Weight measurements over a date range |

### Profile & Fitness

| Tool | Description |
|------|-------------|
| `get_user_profile` | Profile information |
| `get_max_metrics` | VO2 max and fitness metrics |
| `get_fitness_age` | Calculated fitness age |
| `get_training_status` | Training status |
| `get_personal_records` | Personal bests |

## Development

```bash
uv sync
uv run pytest tests/ -x -q
uv run ruff check src/ tests/
uv run pyright src/
```
