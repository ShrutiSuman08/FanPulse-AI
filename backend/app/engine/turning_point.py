def detect_turning_points(
    initial_runs: int,
    initial_wickets: int,
    initial_balls: int,
    deliveries: list,
    target: int,
    total_overs: int = 20
):
    runs = initial_runs
    wickets = initial_wickets
    balls = initial_balls
    events = []
    recent_runs = []

    total_balls = total_overs * 6

    def get_rrr(current_runs, current_balls):
        remaining_runs = max(0, target - current_runs)
        remaining_balls = max(0, total_balls - current_balls)

        if remaining_balls == 0:
            return 0.0 if remaining_runs == 0 else float("inf")

        return round((remaining_runs / remaining_balls) * 6, 2)

    previous_rrr = get_rrr(runs, balls)

    for delivery in deliveries:
        delivery_runs = delivery.get("runs", 0)
        is_wicket = delivery.get("wicket", False)
        is_legal = delivery.get("legal", True)

        runs += delivery_runs

        if is_wicket:
            wickets += 1

        if is_legal:
            balls += 1
            recent_runs.append(delivery_runs)

            if len(recent_runs) > 3:
                recent_runs.pop(0)

        current_rrr = get_rrr(runs, balls)
        rrr_improvement = round(previous_rrr - current_rrr, 2)

        overs = f"{balls // 6}.{balls % 6}"

        runs_required = max(0, target - runs)
        wickets_remaining = max(0, 10 - wickets)

        if is_wicket:
            events.append({
                "type": "wicket",
                "severity": "high",
                "delivery": balls,
                "score": f"{runs}/{wickets}",
                "overs": overs,
                "runs_required": runs_required,
                "required_run_rate": current_rrr,
                "rrr_change": rrr_improvement,
                "description": (
                    f"A wicket has fallen at {overs} overs. "
                    f"The batting side now has {wickets_remaining} "
                    "wickets remaining, increasing pressure on the chase."
                )
            })

        elif is_legal and delivery_runs in (4, 6):
            severity = (
                "high" if rrr_improvement >= 2.0
                else "medium" if rrr_improvement >= 0.75
                else "low"
            )

            if severity != "low":
                events.append({
                    "type": "boundary",
                    "severity": severity,
                    "delivery": balls,
                    "score": f"{runs}/{wickets}",
                    "overs": overs,
                    "runs_required": runs_required,
                    "required_run_rate": current_rrr,
                    "rrr_change": rrr_improvement,
                    "description": (
                        f"A {delivery_runs}-run boundary at {overs} overs "
                        f"reduced the required run rate by "
                        f"{rrr_improvement} runs per over."
                    )
                })

        # Detect a scoring burst across the last three legal deliveries.
        if len(recent_runs) == 3 and sum(recent_runs) >= 12:
            burst_improvement = round(
                previous_rrr - current_rrr, 2
            )

            severity = (
                "high" if burst_improvement >= 2.0
                else "medium" if burst_improvement >= 0.75
                else "low"
            )

            events.append({
                "type": "scoring_burst",
                "severity": severity,
                "delivery": balls,
                "score": f"{runs}/{wickets}",
                "overs": overs,
                "runs_required": runs_required,
                "required_run_rate": current_rrr,
                "rrr_change": burst_improvement,
                "description": (
                    f"The batting side scored {sum(recent_runs)} runs "
                    f"across the last three legal deliveries."
                )
            })

        previous_rrr = current_rrr

        if runs >= target or wickets >= 10 or balls >= total_balls:
            break

    final_rrr = get_rrr(runs, balls)

    return {
        "events": events,
        "final_score": f"{runs}/{wickets}",
        "final_runs": runs,
        "final_wickets": wickets,
        "final_balls": balls,
        "final_required_run_rate": final_rrr
    }