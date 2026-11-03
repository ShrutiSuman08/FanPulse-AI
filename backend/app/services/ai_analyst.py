
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
model_name = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from .env")

llm = ChatGroq(
    model=model_name,
    api_key=api_key,
    temperature=0.3
)


class AnalystState(TypedDict):
    question: str
    match_context: dict
    answer: str


def analyze_match(state: AnalystState):
    question = state["question"]
    context = state["match_context"]

    prompt = f"""
    You are FanPulse AI, an intelligent cricket match analyst.

    Explain cricket situations clearly to everyday fans.

    VERIFIED MATCH DATA:
    {context}

    FAN QUESTION:
    {question}
        Instructions:
    1. Use only the supplied match data for factual claims.
    2. Never invent player statistics, match events, historical records,
       win percentages, or probabilities.
    3. Only provide numerical calculations supported by the supplied data.
    4. Clearly distinguish verified facts from tactical opinions.
    5. Explain the situation in simple language for cricket fans.
    6. Keep the answer concise and structured.
    7. If information is unavailable, explicitly say so.
        8. Do not recalculate or alter supplied match statistics.
    9. Do not confuse overs with balls. One over contains six legal balls.
    10. Never claim historical win percentages without a supplied source.
    11. Use Markdown headings, bullet points, and tables where useful.
    12. Verify all arithmetic in examples before presenting them.
13. Ensure illustrative scoring combinations match the exact
    number of runs required. Do not include unnecessary runs.
    14. Never state a minimum number of boundaries unless it has
    been mathematically verified.
15. Consider different scoring combinations, including singles,
    doubles, triples, fours and sixes.
16. Do not present tactical possibilities as guaranteed outcomes.
17. Do not make unsupported claims about match-winning probabilities.


    Answer:
    """

    response = llm.invoke(prompt)

    return {"answer": response.content}


graph_builder = StateGraph(AnalystState)

graph_builder.add_node("analyze_match", analyze_match)

graph_builder.add_edge(START, "analyze_match")
graph_builder.add_edge("analyze_match", END)

analyst_graph = graph_builder.compile()


def ask_match_analyst(question: str, match_context: dict):
    result = analyst_graph.invoke({
        "question": question,
        "match_context": match_context,
        "answer": ""
    })

    return result["answer"]
