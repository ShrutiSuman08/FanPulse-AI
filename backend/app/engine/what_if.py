
def simulate_delivery(
    runs: int,
    wickets: int,
    balls_completed: int,
    target: int,
    outcome: str,
    total_overs: int = 20
):
    """
    Simulate one hypothetical delivery.

    Supported outcomes:
    dot, single, double, four, six, wicket
    """

    outcomes = {
        "dot": 0,
        "single": 1,
        "double": 2,
        "four": 4,
        "six": 6,
        "wicket": 0
    }

    if outcome not in outcomes:
        raise ValueError("Invalid delivery outcome")

    if not 0 <= wickets <= 10:
        raise ValueError("Wickets must be between 0 and 10")

    if not 0 <= balls_completed <= total_overs * 6:
        raise ValueError("Invalid number of balls completed")

    if runs < 0 or target < 0:
        raise ValueError("Runs and target cannot be negative")

    if wickets >= 10:
        raise ValueError("The innings is already over")

    if balls_completed >= total_overs * 6:
        raise ValueError("The innings is already over")

    if outcome == "wicket":
        wickets += 1
    else:
        runs += outcomes[outcome]

    balls_completed += 1

    remaining_balls = max(
        0, total_overs * 6 - balls_completed
    )

    runs_required = max(0, target - runs)

    remaining_wickets = max(0, 10 - wickets)

    required_run_rate = (
        round(runs_required / (remaining_balls / 6), 2)
        if remaining_balls > 0
        else 0
    )

    return {
        "hypothetical_score": f"{runs}/{wickets}",
        "runs": runs,
        "wickets": wickets,
        "balls_completed": balls_completed,
        "overs": f"{balls_completed // 6}.{balls_completed % 6}",
        "runs_required": runs_required,
        "remaining_balls": remaining_balls,
        "remaining_wickets": remaining_wickets,
        "required_run_rate": required_run_rate,
        "outcome": outcome
    }
