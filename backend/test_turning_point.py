
from app.engine.turning_point import detect_turning_points


def test_detects_wicket():
    result = detect_turning_points(
        100, 4, 100,
        [{"runs": 0, "wicket": True}],
        190
    )

    assert result["final_wickets"] == 5
    assert result["events"][0]["type"] == "wicket"
    assert result["events"][0]["severity"] == "high"


def test_detects_boundary():
    result = detect_turning_points(
        150, 4, 102,
        [{"runs": 6, "wicket": False}],
        190
    )

    boundaries = [
        e for e in result["events"]
        if e["type"] == "boundary"
    ]

    assert len(boundaries) == 1
    assert boundaries[0]["severity"] == "medium"


def test_detects_scoring_burst():
    result = detect_turning_points(
        140, 3, 100,
        [{"runs": 6}, {"runs": 4}, {"runs": 6}],
        190
    )

    bursts = [
        e for e in result["events"]
        if e["type"] == "scoring_burst"
    ]

    assert len(bursts) == 1


def test_final_match_state():
    deliveries = [
        {"runs": 1},
        {"runs": 4},
        {"runs": 0},
        {"runs": 6},
        {"runs": 0, "wicket": True},
        {"runs": 0}
    ]

    result = detect_turning_points(
        145, 4, 102, deliveries, 190
    )

    assert result["final_score"] == "156/5"
    assert result["final_balls"] == 108
    assert result["final_required_run_rate"] == 17.0
