
import pytest

from app.engine.what_if import simulate_delivery


def test_simulates_six():
    result = simulate_delivery(
        runs=156,
        wickets=5,
        balls_completed=108,
        target=190,
        outcome="six"
    )

    assert result["hypothetical_score"] == "162/5"
    assert result["runs_required"] == 28
    assert result["remaining_balls"] == 11
    assert result["required_run_rate"] == 15.27


def test_simulates_wicket():
    result = simulate_delivery(
        runs=156,
        wickets=5,
        balls_completed=108,
        target=190,
        outcome="wicket"
    )

    assert result["hypothetical_score"] == "156/6"
    assert result["remaining_wickets"] == 4


def test_rejects_invalid_outcome():
    with pytest.raises(ValueError):
        simulate_delivery(156, 5, 108, 190, "three")


def test_rejects_completed_innings():
    with pytest.raises(ValueError):
        simulate_delivery(156, 10, 120, 190, "six")


def test_rejects_negative_runs():
    with pytest.raises(ValueError):
        simulate_delivery(-1, 5, 108, 190, "six")
