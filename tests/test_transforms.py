"""Tests for response transformer functions."""

from garmin_mcp.transforms import (
    trim_activity_list,
    trim_heart_rates,
    trim_hrv,
    trim_respiration,
    trim_sleep,
    trim_stress,
)

# ---------------------------------------------------------------------------
# trim_heart_rates
# ---------------------------------------------------------------------------


class TestTrimHeartRates:
    def test_strips_values_array(self):
        data = {
            "restingHeartRate": 52,
            "maxHeartRate": 180,
            "heartRateValues": [[1000, 60], [2000, 65], [3000, 70]],
            "heartRateValueDescriptors": [{"key": "heartrate", "index": 1}],
        }
        result = trim_heart_rates(data)
        assert "heartRateValues" not in result
        assert "heartRateValueDescriptors" not in result

    def test_keeps_scalar_fields(self):
        data = {
            "restingHeartRate": 52,
            "maxHeartRate": 180,
            "minHeartRate": 48,
            "heartRateValues": [[1000, 60]],
        }
        result = trim_heart_rates(data)
        assert result["restingHeartRate"] == 52
        assert result["maxHeartRate"] == 180
        assert result["minHeartRate"] == 48

    def test_computes_average(self):
        data = {"heartRateValues": [[1000, 60], [2000, 80], [3000, 100]]}
        result = trim_heart_rates(data)
        assert result["averageHeartRate"] == 80

    def test_excludes_zero_from_average(self):
        # 0 bpm = no reading, not a real value
        data = {"heartRateValues": [[1000, 0], [2000, 60], [3000, 90]]}
        result = trim_heart_rates(data)
        assert result["averageHeartRate"] == 75  # (60+90)/2

    def test_no_average_when_no_valid_readings(self):
        data = {"heartRateValues": [[1000, 0], [2000, None]]}
        result = trim_heart_rates(data)
        assert "averageHeartRate" not in result

    def test_empty_values_array(self):
        data = {"restingHeartRate": 52, "heartRateValues": []}
        result = trim_heart_rates(data)
        assert result["restingHeartRate"] == 52
        assert "averageHeartRate" not in result

    def test_passthrough_non_dict(self):
        assert trim_heart_rates([1, 2, 3]) == [1, 2, 3]
        assert trim_heart_rates(None) is None


# ---------------------------------------------------------------------------
# trim_stress
# ---------------------------------------------------------------------------


class TestTrimStress:
    def test_strips_stress_array(self):
        data = {
            "avgStressLevel": 35,
            "stressValuesArray": [[1000, 30], [2000, -1], [3000, 40]],
            "bodyBatteryValuesArray": [],
        }
        result = trim_stress(data)
        assert "stressValuesArray" not in result
        assert "bodyBatteryValuesArray" not in result

    def test_strips_descriptor_list(self):
        data = {
            "stressValueDescriptorsDTOList": [{"key": "stressLevel"}],
            "stressValuesArray": [],
            "bodyBatteryValuesArray": [],
        }
        result = trim_stress(data)
        assert "stressValueDescriptorsDTOList" not in result

    def test_excludes_sentinel_values_from_avg_stress(self):
        # -1 = unmeasured, -2 = during activity — must be excluded
        data = {
            "stressValuesArray": [[1000, -2], [2000, -1], [3000, 20], [4000, 40]],
            "bodyBatteryValuesArray": [],
        }
        result = trim_stress(data)
        assert result["computedAvgStress"] == 30  # (20+40)/2

    def test_computes_body_battery_stats(self):
        data = {
            "stressValuesArray": [],
            "bodyBatteryValuesArray": [
                [1000, 80, "MEASURED"],
                [2000, 60, "MEASURED"],
                [3000, 40, "MEASURED"],
            ],
        }
        result = trim_stress(data)
        assert result["computedAvgBodyBattery"] == 60
        assert result["computedMinBodyBattery"] == 40
        assert result["computedMaxBodyBattery"] == 80

    def test_keeps_scalar_fields(self):
        data = {
            "avgStressLevel": 42,
            "maxStressLevel": 75,
            "startTimestampGMT": "2026-04-07T00:00:00",
            "stressValuesArray": [],
            "bodyBatteryValuesArray": [],
        }
        result = trim_stress(data)
        assert result["avgStressLevel"] == 42
        assert result["maxStressLevel"] == 75
        assert result["startTimestampGMT"] == "2026-04-07T00:00:00"

    def test_no_computed_stats_when_arrays_empty(self):
        data = {"stressValuesArray": [], "bodyBatteryValuesArray": []}
        result = trim_stress(data)
        assert "computedAvgStress" not in result
        assert "computedAvgBodyBattery" not in result

    def test_passthrough_non_dict(self):
        assert trim_stress("raw") == "raw"


# ---------------------------------------------------------------------------
# trim_sleep
# ---------------------------------------------------------------------------


class TestTrimSleep:
    def test_strips_list_values(self):
        data = {
            "dailySleepDTO": {"totalSleepSeconds": 28800, "sleepScores": {}},
            "sleepLevels": [
                {"startGMT": "00:00", "endGMT": "00:30", "activityLevel": 0}
            ],
            "remSleepData": [[1000, 1], [2000, 0]],
            "sleepMovement": [[1000, 0.1]],
        }
        result = trim_sleep(data)
        assert "sleepLevels" not in result
        assert "remSleepData" not in result
        assert "sleepMovement" not in result

    def test_keeps_dict_and_scalar_fields(self):
        data = {
            "dailySleepDTO": {"totalSleepSeconds": 28800},
            "restingHeartRate": 52,
            "avgSleepStress": 18.5,
            "sleepLevels": [[1000, 0]],
        }
        result = trim_sleep(data)
        assert result["dailySleepDTO"] == {"totalSleepSeconds": 28800}
        assert result["restingHeartRate"] == 52
        assert result["avgSleepStress"] == 18.5

    def test_keeps_none_values(self):
        data = {"dailySleepDTO": None, "sleepLevels": []}
        result = trim_sleep(data)
        assert "dailySleepDTO" in result
        assert result["dailySleepDTO"] is None

    def test_passthrough_non_dict(self):
        assert trim_sleep([1, 2]) == [1, 2]


# ---------------------------------------------------------------------------
# trim_respiration
# ---------------------------------------------------------------------------


class TestTrimRespiration:
    def test_strips_raw_values_array(self):
        data = {
            "startTimestampGMT": "2026-04-07T00:00:00",
            "respirationValuesArray": [[1000, 14.5], [2000, 15.0]],
            "respirationAveragesValuesArray": [[0, 14.8]],
        }
        result = trim_respiration(data)
        assert "respirationValuesArray" not in result

    def test_keeps_hourly_averages(self):
        data = {
            "respirationValuesArray": [[1000, 14.5]],
            "respirationAveragesValuesArray": [[0, 14.8], [3600, 15.1]],
        }
        result = trim_respiration(data)
        assert result["respirationAveragesValuesArray"] == [[0, 14.8], [3600, 15.1]]

    def test_keeps_scalar_fields(self):
        data = {
            "avgWakingRespirationValue": 15.2,
            "highestRespirationValue": 18.0,
            "respirationValuesArray": [],
        }
        result = trim_respiration(data)
        assert result["avgWakingRespirationValue"] == 15.2
        assert result["highestRespirationValue"] == 18.0

    def test_passthrough_non_dict(self):
        assert trim_respiration(42) == 42


# ---------------------------------------------------------------------------
# trim_hrv
# ---------------------------------------------------------------------------


class TestTrimHrv:
    def test_strips_readings_array(self):
        data = {
            "startTimestampGMT": "2026-04-07T01:00:00",
            "lastNight": {"avg": 45, "min": 32, "max": 68},
            "hrvReadings": [
                {"hrvValue": 45, "startTimestampGMT": "2026-04-07T01:00:00"}
            ],
        }
        result = trim_hrv(data)
        assert "hrvReadings" not in result

    def test_keeps_summary_fields(self):
        data = {
            "lastNight": {"avg": 45, "min": 32, "max": 68, "status": "BALANCED"},
            "baseline": {"lowUpper": 38, "balancedLow": 40, "balancedUpper": 55},
            "hrvReadings": [],
        }
        result = trim_hrv(data)
        assert result["lastNight"]["avg"] == 45
        assert result["baseline"]["balancedLow"] == 40

    def test_passthrough_non_dict(self):
        assert trim_hrv(None) is None


# ---------------------------------------------------------------------------
# trim_activity_list
# ---------------------------------------------------------------------------


class TestTrimActivityList:
    def test_strips_user_roles_from_list(self):
        activities = [
            {
                "activityId": 1,
                "activityName": "Run",
                "userRoles": ["SCOPE_A", "SCOPE_B"],
            },
            {"activityId": 2, "activityName": "Ride", "userRoles": ["SCOPE_A"]},
        ]
        result = trim_activity_list(activities)
        assert isinstance(result, list)
        assert all("userRoles" not in a for a in result)

    def test_keeps_other_fields_in_list(self):
        activities = [
            {
                "activityId": 1,
                "activityName": "Run",
                "distance": 5000.0,
                "userRoles": [],
            },
        ]
        result = trim_activity_list(activities)
        assert result[0]["activityId"] == 1
        assert result[0]["activityName"] == "Run"
        assert result[0]["distance"] == 5000.0

    def test_strips_user_roles_from_single_dict(self):
        activity = {"activityId": 1, "userRoles": ["SCOPE_A"]}
        result = trim_activity_list(activity)
        assert isinstance(result, dict)
        assert "userRoles" not in result
        assert result["activityId"] == 1

    def test_no_user_roles_key_is_unchanged(self):
        activity = {"activityId": 1, "activityName": "Run"}
        result = trim_activity_list(activity)
        assert result == activity

    def test_empty_list(self):
        assert trim_activity_list([]) == []

    def test_passthrough_non_list_non_dict(self):
        assert trim_activity_list("raw") == "raw"
        assert trim_activity_list(None) is None
