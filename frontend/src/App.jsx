
import { useEffect, useState } from "react";
import "./App.css";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function App() {
  const [match, setMatch] = useState(null);
  const [matchState, setMatchState] = useState(null);
  const [error, setError] = useState("");
  const [timeline, setTimeline] = useState([]);

  // What-If Simulator states
  const [whatIfOutcome, setWhatIfOutcome] = useState("six");
  const [whatIfResult, setWhatIfResult] = useState(null);
  const [whatIfLoading, setWhatIfLoading] = useState(false);
  const [whatIfError, setWhatIfError] = useState("");

  // AI What-If Explanation state
  const [whatIfExplanation, setWhatIfExplanation] = useState("");

  // AI Analyst states
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState("");

  // Fetch match data and turning points
  useEffect(() => {
    const fetchMatch = async () => {
      try {
        const response = await fetch(
          `${API_BASE_URL}/api/match/current`
        );

        if (!response.ok) {
          throw new Error("Unable to fetch match");
        }

        const data = await response.json();

        setMatch(data.match);
        setMatchState(data.match_state);
        setError("");
      } catch {
        setError("Backend connection failed. Check FastAPI.");
      }
    };

    const fetchTimeline = async () => {
      try {
        const response = await fetch(
          `${API_BASE_URL}/api/match/timeline`
        );

        if (!response.ok) {
          throw new Error("Unable to fetch timeline");
        }

        const data = await response.json();
        setTimeline(data.events || []);
      } catch (err) {
        console.error("Timeline error:", err);
      }
    };

    fetchMatch();
    fetchTimeline();

    const interval = setInterval(fetchMatch, 5000);

    return () => clearInterval(interval);
  }, []);

  // Ask the AI cricket analyst
  const askFanPulse = async (event) => {
    event.preventDefault();

    if (!question.trim() || aiLoading) return;

    setAiLoading(true);
    setAiError("");
    setAnswer("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/analyst/ask`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: question.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "AI analyst request failed"
        );
      }

      setAnswer(data.answer);
    } catch (err) {
      setAiError(
        err.message || "Unable to reach FanPulse AI."
      );
    } finally {
      setAiLoading(false);
    }
  };

  // Run What-If simulation and generate AI explanation
  // Both are handled by ONE backend API call.
  const runWhatIfSimulation = async () => {
    if (!whatIfOutcome || whatIfLoading) return;

    setWhatIfLoading(true);
    setWhatIfError("");
    setWhatIfResult(null);
    setWhatIfExplanation("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/match/what-if`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            outcome: whatIfOutcome,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "What-If analysis failed"
        );
      }

      // Store simulation and AI explanation
      setWhatIfResult(data);
      setWhatIfExplanation(data.explanation || "");
    } catch (err) {
      console.error("What-If error:", err);

      setWhatIfError(
        err.message || "Unable to complete What-If analysis."
      );
    } finally {
      setWhatIfLoading(false);
    }
  };

  // Reset What-If simulation
  const resetWhatIfSimulation = () => {
    setWhatIfOutcome("six");
    setWhatIfResult(null);
    setWhatIfError("");
    setWhatIfExplanation("");
    setWhatIfLoading(false);
  };

  // Loading and error states
  if (error && !matchState) {
    return <div className="loading">{error}</div>;
  }

  if (!match || !matchState) {
    return (
      <div className="loading">
        Loading FanPulse AI...
      </div>
    );
  }

  return (
    <div className="app">

      {/* NAVBAR */}
      <header className="navbar">
        <div className="brand">
          <span className="brand-icon">F</span>
          FanPulse <strong>AI</strong>
        </div>

        <span className="demo-tag">
          SIMULATED MATCH · DEMO
        </span>
      </header>

      <main className="dashboard">

        {/* WELCOME */}
        <section className="welcome">
          <p className="eyebrow">
            YOUR INTELLIGENT CRICKET COMPANION
          </p>

          <h1>Every ball tells a story.</h1>

          <p className="subtitle">
            Understand the game beyond the scoreboard.
          </p>
        </section>

        {/* MATCH SCORECARD */}
        <section className="match-card">
          <div className="match-header">
            <span>CRICKET MATCH CENTER</span>
            <span>SECOND INNINGS</span>
          </div>

          <div className="teams">
            <div className="team">
              <div className="team-logo mi">MI</div>
              <h2>{match.team_a}</h2>
            </div>

            <span className="versus">VS</span>

            <div className="team">
              <div className="team-logo csk">CSK</div>
              <h2>{match.team_b}</h2>
            </div>
          </div>

          <div className="score-section">
            <div>
              <p className="score-label">
                CURRENT SCORE
              </p>

              <div className="score">
                {matchState.runs}/{matchState.wickets}
              </div>

              <p className="overs">
                Overs {matchState.overs}
              </p>
            </div>

            <div className="target-box">
              <p>TARGET</p>
              <h2>{matchState.target}</h2>
              <span>To win</span>
            </div>
          </div>

          <div className="match-status">
            {matchState.runs_required} runs needed from{" "}
            {matchState.remaining_balls} balls
          </div>
        </section>

        {/* MATCH STATISTICS */}
        <section className="stats-section">
          <p className="eyebrow">
            THE NUMBERS BEHIND THE GAME
          </p>

          <h2>Match situation</h2>

          <div className="stats-grid">
            <div className="stat-card">
              <span>🎯</span>
              <p>Runs required</p>
              <h3>{matchState.runs_required}</h3>
            </div>

            <div className="stat-card">
              <span>⏱️</span>
              <p>Balls remaining</p>
              <h3>{matchState.remaining_balls}</h3>
            </div>

            <div className="stat-card">
              <span>📈</span>
              <p>Required run rate</p>
              <h3>{matchState.required_run_rate}</h3>
            </div>

            <div className="stat-card">
              <span>🏏</span>
              <p>Current run rate</p>
              <h3>{matchState.current_run_rate}</h3>
            </div>
          </div>
        </section>

        {/* MATCH INSIGHT */}
        <section className="insight-card">
          <p className="eyebrow">
            ✦ FANPULSE INTELLIGENCE
          </p>

          <h2>What's happening in the match?</h2>

          <p>
            {matchState.runs_required} runs are needed from{" "}
            {matchState.remaining_balls} balls. The required run
            rate is {matchState.required_run_rate}, compared
            with the current run rate of{" "}
            {matchState.current_run_rate}.
          </p>

          <small>
            Verified calculations from the match engine.
          </small>
        </section>

        {/* TURNING POINTS TIMELINE */}
        <section className="timeline-section">
          <p className="eyebrow">
            ✦ MATCH MOMENTS
          </p>

          <h2>Turning Points</h2>

          <p className="chat-description">
            Important events detected by FanPulse AI's match engine.
          </p>

          {timeline.length === 0 ? (
            <p>No important events detected yet.</p>
          ) : (
            <div className="timeline-list">
              {timeline.map((event, index) => (
                <div
                  className="timeline-item"
                  key={`${event.delivery}-${index}`}
                >
                  <div
                    className={`timeline-icon ${event.type}`}
                  >
                    {event.type === "wicket"
                      ? "🏏"
                      : event.type === "boundary"
                      ? "🔥"
                      : "⚡"}
                  </div>

                  <div className="timeline-content">
                    <div className="timeline-top">
                      <strong>
                        {event.type
                          .replace("_", " ")
                          .toUpperCase()}
                      </strong>

                      <span>{event.overs} overs</span>
                    </div>

                    <p>{event.description}</p>

                    <div className="timeline-meta">
                      <span>
                        Score: {event.score}
                      </span>

                      <span>
                        RRR: {event.required_run_rate}
                      </span>

                      <span
                        className={`severity ${event.severity}`}
                      >
                        {event.severity.toUpperCase()}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          <small>
            Simulated match events · Rule-based detection
          </small>
        </section>

        {/* WHAT-IF SIMULATOR */}
        <section className="whatif-section">
          <p className="eyebrow">
            ✦ EXPLORE ALTERNATE SCENARIOS
          </p>

          <h2>What If?</h2>

          <p className="chat-description">
            What if the next delivery had a different outcome?
            Explore how one ball could change the match.
          </p>

          <div className="whatif-outcomes">
            {[
              { label: "Dot Ball", value: "dot", icon: "0" },
              { label: "Single", value: "single", icon: "1" },
              { label: "Double", value: "double", icon: "2" },
              { label: "Four", value: "four", icon: "4" },
              { label: "Six", value: "six", icon: "6" },
              { label: "Wicket", value: "wicket", icon: "W" },
            ].map((item) => (
              <button
                key={item.value}
                type="button"
                className={`whatif-outcome ${
                  whatIfOutcome === item.value
                    ? "selected"
                    : ""
                }`}
                onClick={() => {
                  setWhatIfOutcome(item.value);
                  setWhatIfResult(null);
                  setWhatIfError("");
                  setWhatIfExplanation("");
                }}
              >
                <strong>{item.icon}</strong>
                <span>{item.label}</span>
              </button>
            ))}
          </div>

          <button
            type="button"
            className="whatif-run-button"
            onClick={runWhatIfSimulation}
            disabled={whatIfLoading}
          >
            {whatIfLoading
              ? "Analyzing Scenario..."
              : "Simulate This Delivery →"}
          </button>

          {whatIfError && (
            <div className="ai-error">
              {whatIfError}
            </div>
          )}

          {/* SIMULATION RESULTS */}
          {whatIfResult && (
            <div className="whatif-result">
              <p className="eyebrow">
                ✦ SIMULATION RESULT
              </p>

              <div className="whatif-comparison">
                <div className="whatif-score-card">
                  <span>ACTUAL MATCH</span>

                  <h3>{whatIfResult.actual_score}</h3>

                  <p>
                    {whatIfResult.actual_runs_required} runs needed
                  </p>

                  <small>
                    {whatIfResult.actual_remaining_balls} balls left
                  </small>
                </div>

                <div className="whatif-score-card hypothetical">
                  <span>HYPOTHETICAL MATCH</span>

                  <h3>
                    {whatIfResult.simulation.hypothetical_score}
                  </h3>

                  <p>
                    {whatIfResult.simulation.runs_required} runs needed
                  </p>

                  <small>
                    {whatIfResult.simulation.remaining_balls} balls left
                  </small>
                </div>
              </div>

              <div className="whatif-insight">
                <div>
                  <span>Actual required run rate</span>
                  <strong>
                    {matchState.required_run_rate}
                  </strong>
                </div>

                <div>
                  <span>Hypothetical required run rate</span>
                  <strong>
                    {whatIfResult.simulation.required_run_rate}
                  </strong>
                </div>
              </div>

              <p className="whatif-note">
                This is a hypothetical scenario. The actual
                match score has not been changed.
              </p>

              {/* AI-GENERATED EXPLANATION */}
              <div className="whatif-ai-explanation">
                <h3>✦ FanPulse AI Match Insight</h3>

                {whatIfExplanation ? (
                  <div className="ai-explanation-content">
                    <ReactMarkdown
                      remarkPlugins={[remarkGfm]}
                    >
                      {whatIfExplanation}
                    </ReactMarkdown>
                  </div>
                ) : (
                  <p className="ai-loading">
                    No AI explanation was returned.
                  </p>
                )}
              </div>

              <button
                type="button"
                className="suggestion"
                onClick={resetWhatIfSimulation}
              >
                Reset Simulation
              </button>
            </div>
          )}
        </section>

        {/* AI CRICKET ANALYST */}
        <section className="ai-chat-card">
          <p className="eyebrow">
            ✦ TALK TO YOUR AI CRICKET ANALYST
          </p>

          <h2>Ask FanPulse AI</h2>

          <p className="chat-description">
            Ask anything about the current match situation
            and get an AI-powered explanation.
          </p>

          {/* SUGGESTED QUESTIONS */}
          <div className="suggested-questions">
            {[
              "Is CSK in a good position to win?",
              "What does CSK need to do now?",
              "Explain the required run rate.",
            ].map((suggestion) => (
              <button
                type="button"
                className="suggestion"
                key={suggestion}
                onClick={() => setQuestion(suggestion)}
              >
                {suggestion}
              </button>
            ))}
          </div>

          {/* QUESTION INPUT */}
          <form
            onSubmit={askFanPulse}
            className="chat-form"
          >
            <input
              type="text"
              value={question}
              onChange={(event) =>
                setQuestion(event.target.value)
              }
              placeholder="Ask your cricket question..."
              disabled={aiLoading}
            />

            <button
              type="submit"
              disabled={aiLoading || !question.trim()}
            >
              {aiLoading ? "Thinking..." : "Ask AI →"}
            </button>
          </form>

          {aiLoading && (
            <p className="ai-loading">
              FanPulse AI is analyzing the match...
            </p>
          )}

          {aiError && (
            <div className="ai-error">
              {aiError}
            </div>
          )}

          {answer && (
            <div className="ai-answer">
              <p className="eyebrow">
                ✦ AI MATCH ANALYSIS
              </p>

              <div className="answer-content">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                >
                  {answer}
                </ReactMarkdown>
              </div>

              <small>
                AI-generated analysis · Simulated match data
              </small>
            </div>
          )}
        </section>

        {/* FOOTER */}
        <footer>
          <span>FanPulse AI</span>
          <span>Built for cricket fans.</span>
        </footer>

      </main>
    </div>
  );
}

export default App;
