import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.engine.match_engine import calculate_match_state
from app.engine.turning_point import detect_turning_points
from app.engine.what_if import simulate_delivery
from app.services.ai_analyst import ask_match_analyst


# --------------------------------------------------
# APP CONFIGURATION
# --------------------------------------------------

app = FastAPI(
    title="FanPulse AI",
    description="AI-powered cricket match companion",
    version="1.0.0"
)

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# SIMULATED MATCH DATA
# --------------------------------------------------

MATCH = {
    "match_id": "match_001",
    "team_a": "Mumbai Indians",
    "team_b": "Chennai Super Kings",
    "batting_team": "Chennai Super Kings",
    "runs": 156,
    "wickets": 5,
    "overs_completed": 18,
    "balls_completed": 0,
    "target": 190
}

DELIVERIES = [
    {"runs": 1, "wicket": False},
    {"runs": 4, "wicket": False},
    {"runs": 0, "wicket": False},
    {"runs": 6, "wicket": False},
    {"runs": 0, "wicket": True},
    {"runs": 0, "wicket": False}
]


# --------------------------------------------------
# REQUEST MODELS
# --------------------------------------------------

class AnalystRequest(BaseModel):
    question: str


class WhatIfRequest(BaseModel):
    outcome: str


class WhatIfExplanationRequest(BaseModel):
    outcome: str


# --------------------------------------------------
# HOME AND HEALTH ROUTES
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to FanPulse AI",
        "status": "running"
    }


@app.get("/api/health")
def health():
    return {"status": "healthy"}


# --------------------------------------------------
# CURRENT MATCH API
# --------------------------------------------------

@app.get("/api/match/current")
def get_current_match():

    state = calculate_match_state(
        runs=MATCH["runs"],
        wickets=MATCH["wickets"],
        overs_completed=MATCH["overs_completed"],
        balls_completed=MATCH["balls_completed"],
        target=MATCH["target"]
    )

    return {
        "match": MATCH,
        "match_state": state,
        "data_mode": "simulated"
    }


# --------------------------------------------------
# AI CRICKET ANALYST API
# --------------------------------------------------

@app.post("/api/analyst/ask")
def ask_analyst(request: AnalystRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Please enter a question."
        )

    match_state = calculate_match_state(
        runs=MATCH["runs"],
        wickets=MATCH["wickets"],
        overs_completed=MATCH["overs_completed"],
        balls_completed=MATCH["balls_completed"],
        target=MATCH["target"]
    )

    match_context = {
        "match": MATCH,
        "match_state": match_state
    }

    try:
        answer = ask_match_analyst(
            question=question,
            match_context=match_context
        )

        return {
            "question": question,
            "answer": answer,
            "data_mode": "simulated"
        }

    except Exception as e:
        print("AI ANALYST ERROR:", repr(e))

        raise HTTPException(
            status_code=502,
            detail="AI analyst is temporarily unavailable. Check backend terminal."
        )


# --------------------------------------------------
# TURNING POINTS API
# --------------------------------------------------

@app.get("/api/match/timeline")
def get_match_timeline():

    result = detect_turning_points(
        initial_runs=145,
        initial_wickets=4,
        initial_balls=102,
        deliveries=DELIVERIES,
        target=190
    )

    return {
        "match_id": MATCH["match_id"],
        "events": result["events"],
        "final_score": result["final_score"],
        "final_required_run_rate": result[
            "final_required_run_rate"
        ],
        "data_mode": "simulated"
    }


# --------------------------------------------------
# WHAT-IF SIMULATOR API
# --------------------------------------------------


@app.post("/api/match/what-if")
def what_if_simulation(request: WhatIfRequest):
    try:
        # 1. Calculate hypothetical delivery
        simulation = simulate_delivery(
            runs=MATCH["runs"],
            wickets=MATCH["wickets"],
            balls_completed=(
                MATCH["overs_completed"] * 6
                + MATCH["balls_completed"]
            ),
            target=MATCH["target"],
            outcome=request.outcome
        )

        # 2. Calculate actual match situation
        actual_state = calculate_match_state(
            runs=MATCH["runs"],
            wickets=MATCH["wickets"],
            overs_completed=MATCH["overs_completed"],
            balls_completed=MATCH["balls_completed"],
            target=MATCH["target"]
        )

        # 3. Prepare match context for AI
        match_context = {
            "actual_score": (
                f'{MATCH["runs"]}/{MATCH["wickets"]}'
            ),
            "actual_runs_required": actual_state["runs_required"],
            "actual_remaining_balls": actual_state["remaining_balls"],
            "actual_required_run_rate": actual_state["required_run_rate"],
            "hypothetical_score": simulation["hypothetical_score"],
            "hypothetical_runs_required": simulation["runs_required"],
            "hypothetical_remaining_balls": simulation["remaining_balls"],
            "hypothetical_required_run_rate": simulation["required_run_rate"],
            "selected_outcome": request.outcome
        }

        # 4. Generate AI explanation
        question = """
        You are FanPulse AI, a cricket match analyst.

        Compare the actual and hypothetical match situations.
        Explain how the selected delivery changes the chase.
        Mention whether the chase remains challenging.

        Use only the supplied match data.
        Do not invent player statistics or winning probabilities.
        Do not change or recalculate the supplied numbers.
        Keep the explanation simple, engaging and concise.
        Write 3-5 sentences.
        """

        explanation = ask_match_analyst(
            question=question,
            match_context=match_context
        )

        # 5. Return everything in one response
        return {
            "actual_score": match_context["actual_score"],
            "actual_runs_required": actual_state["runs_required"],
            "actual_remaining_balls": actual_state["remaining_balls"],
            "simulation": simulation,
            "explanation": explanation,
            "data_mode": "simulated"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        print("WHAT-IF ERROR:", repr(e))

        raise HTTPException(
            status_code=502,
            detail="Unable to complete What-If analysis."
        )


# --------------------------------------------------
# AI-POWERED WHAT-IF EXPLANATION API
# --------------------------------------------------

@app.post("/api/match/what-if/explain")
def explain_what_if(request: WhatIfExplanationRequest):

    try:
        # Step 1: Calculate hypothetical delivery
        simulation = simulate_delivery(
            runs=MATCH["runs"],
            wickets=MATCH["wickets"],
            balls_completed=(
                MATCH["overs_completed"] * 6
                + MATCH["balls_completed"]
            ),
            target=MATCH["target"],
            outcome=request.outcome
        )

        # Step 2: Calculate actual match situation
        actual_state = calculate_match_state(
            runs=MATCH["runs"],
            wickets=MATCH["wickets"],
            overs_completed=MATCH["overs_completed"],
            balls_completed=MATCH["balls_completed"],
            target=MATCH["target"]
        )

        # Step 3: Prepare verified context
        match_context = {
            "actual_score": (
                f'{MATCH["runs"]}/{MATCH["wickets"]}'
            ),
            "actual_runs_required": actual_state[
                "runs_required"
            ],
            "actual_remaining_balls": actual_state[
                "remaining_balls"
            ],
            "actual_required_run_rate": actual_state[
                "required_run_rate"
            ],
            "hypothetical_score": simulation[
                "hypothetical_score"
            ],
            "hypothetical_runs_required": simulation[
                "runs_required"
            ],
            "hypothetical_remaining_balls": simulation[
                "remaining_balls"
            ],
            "hypothetical_required_run_rate": simulation[
                "required_run_rate"
            ],
            "selected_outcome": request.outcome
        }

        # Step 4: Ask AI to explain the comparison
        question = """
        You are FanPulse AI, a cricket match analyst.

        Explain the hypothetical delivery outcome to a cricket fan.

        Compare the actual and hypothetical match situations.
        Explain how the selected delivery changes the chase.
        Mention whether the chase remains challenging.

        Use only the supplied match data.
        Do not invent player statistics or winning probabilities.
        Do not change or recalculate the supplied numbers.

        Keep the explanation simple, engaging and concise.
        Write 3-5 sentences.
        """

        answer = ask_match_analyst(
            question=question,
            match_context=match_context
        )

        # Step 5: Return explanation and calculations
        return {
            "outcome": request.outcome,
            "explanation": answer,
            "simulation": simulation,
            "match_context": match_context,
            "data_mode": "simulated"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        print("WHAT-IF EXPLANATION ERROR:", repr(e))

        raise HTTPException(
            status_code=502,
            detail="Unable to generate the AI explanation. Check backend terminal."
        )
