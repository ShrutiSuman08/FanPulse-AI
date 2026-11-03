<div align="center">

# 🏏 FanPulse AI
### Your AI-powered companion for understanding the match beyond the scoreboard.

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Open_FanPulse_AI-1f9d72?style=for-the-badge)](https://fan-pulse-ai-psi.vercel.app/)
[![API Docs](https://img.shields.io/badge/API-Interactive_Swagger-1686c7?style=for-the-badge)](https://fanpulse-ai-backend.onrender.com/docs)
[![Backend Health](https://img.shields.io/badge/Backend-Health_Check-6c63ff?style=for-the-badge)](https://fanpulse-ai-backend.onrender.com/api/health)
[![GitHub](https://img.shields.io/badge/Source-GitHub-24292f?style=for-the-badge&logo=github)](https://github.com/ShrutiSuman08/FanPulse-AI)

**A fan-first cricket intelligence demo built with React, FastAPI, LangChain, LangGraph and Groq.**

</div>

---

## ✨ Explore the Demo

| Experience | What You Can Try |
|---|---|
| 🏟️ **Match Context** | Explore the current simulated match state and understand the chase situation. |
| 📍 **Turning Points** | Review important match events and understand why a moment can change the pressure of a game. |
| 💬 **Ask the AI Analyst** | Ask cricket questions in natural language and get context-aware explanations. |
| 🔮 **What-If Scenarios** | Explore how a hypothetical delivery or event could change the match equation. |

<div align="center">

### ▶️ [LAUNCH FANPULSE AI](https://fan-pulse-ai-psi.vercel.app/)

</div>

### 🎮 A Quick Fan Walkthrough

1. Open the [live app](https://fan-pulse-ai-psi.vercel.app/).
2. Scan the match situation and note the score, overs, target and required run rate.
3. Explore the turning-point timeline to understand the match narrative.
4. Ask the AI analyst a question such as:
   - What is putting the chasing team under pressure?
   - Which factor matters most in the final overs?
   - Explain the current required run rate in simple terms.
5. Open the what-if feature and try a hypothetical event, such as a boundary or a wicket. Compare the revised match equation and explanation.

<details>
<summary><strong>💡 More prompts to try</strong></summary>

- Summarise the match situation for a casual fan.
- What should the batting team prioritise from here?
- How would a wicket change the pressure?
- What happens to the equation if the next ball is a six?
- Explain why the required run rate is important.

</details>

> **Demo-data notice:** The match state and events in this public demo are simulated for demonstration. FanPulse AI is not connected to a live cricket-data provider, and its outputs should not be treated as live scores, betting advice, or guaranteed match predictions.

---

## 🎯 The Fan Problem

A scoreboard tells fans **what** is happening, but it does not always explain **why** the match is shifting.

During a tense chase, fans may want to understand the pressure, the significance of a wicket, or how one delivery changes the equation.

FanPulse AI turns match context into explanations that are easier to follow and explore.

## 🧠 How FanPulse AI Helps

- **Context, not just numbers:** Converts match state into plain-language explanations.
- **Moment-led storytelling:** Surfaces turning points so fans can follow the match narrative.
- **Ask in your own words:** Lets fans ask questions without navigating statistics manually.
- **Explore alternate outcomes:** Lets fans test hypothetical events and inspect the changed equation.

---

## 🏗️ Architecture

```mermaid
flowchart TD
    A[Cricket fan] --> B[React + Vite frontend]
    B -->|REST API requests| C[FastAPI backend]
    C --> D[Match engine]
    D --> D1[Current match context]
    D --> D2[Turning-point timeline]
    D --> D3[What-if simulation]
    C --> E[AI analyst service]
    E --> F[LangChain / LangGraph workflow]
    F --> G[Groq-hosted LLM]
    G --> E
    D1 --> C
    D2 --> C
    D3 --> C
    E --> C
    C -->|JSON response| B
