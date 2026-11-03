
def calculate_match_state(
    runs: int,
    wickets: int,
    overs_completed: int,
    balls_completed: int,
    target: int,
    total_overs: int = 20
):
    """Calculate the state of a cricket run chase."""

    total_balls_bowled = (
        overs_completed * 6 + balls_completed
    )

    total_balls = total_overs * 6

    remaining_balls = max(
        0, total_balls - total_balls_bowled
    )

    runs_required = max(0, target - runs)

    remaining_wickets = max(0, 10 - wickets)

    current_run_rate = (
        runs / (total_balls_bowled / 6)
        if total_balls_bowled > 0 else 0
    )

    required_run_rate = (
        runs_required / (remaining_balls / 6)
        if remaining_balls > 0 else 0
    )

    return {
        "runs": runs,
        "wickets": wickets,
        "overs": f"{overs_completed}.{balls_completed}",
        "target": target,
        "runs_required": runs_required,
        "remaining_balls": remaining_balls,
        "remaining_wickets": remaining_wickets,
        "current_run_rate": round(current_run_rate, 2),
        "required_run_rate": round(required_run_rate, 2)
    }
