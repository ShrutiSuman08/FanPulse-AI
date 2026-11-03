
from app.engine.match_engine import calculate_match_state


def test_calculates_current_match_state():
    result = calculate_match_state(
        runs=156,
        wickets=5,
        overs_completed=18,
        balls_completed=0,
        target=190
    )

    assert result["runs"] == 156
    assert result["wickets"] == 5
    assert result["runs_required"] == 34
    assert result["remaining_balls"] == 12
    assert result["remaining_wickets"] == 5
    assert result["current_run_rate"] == 8.67
    assert result["required_run_rate"] == 17.0


def test_calculates_match_at_start():
    result = calculate_match_state(
        runs=0,
        wickets=0,
        overs_completed=0,
        balls_completed=0,
        target=190
    )

    assert result["runs_required"] == 190
    assert result["remaining_balls"] == 120
    assert result["remaining_wickets"] == 10
    assert result["current_run_rate"] == 0


def test_match_with_no_balls_remaining():
    result = calculate_match_state(
        runs=180,
        wickets=8,
        overs_completed=20,
        balls_completed=0,
        target=190
    )

    assert result["remaining_balls"] == 0
    assert result["runs_required"] == 10
    assert result["required_run_rate"] == 0
