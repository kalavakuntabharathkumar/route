import json
import os
import re
from .tools import TOOLS


def _tracking_ids(text: str):
    return re.findall(r"RT-\d{5}", text.upper())


def deterministic_plan(query: str) -> list[dict]:
    ids = _tracking_ids(query)
    if not ids:
        return [{"tool": "search_routes", "args": {"query": query}}]
    steps = [{"tool": "lookup_shipment", "args": {"tracking_id": ids[0]}}]
    if any(word in query.lower() for word in ("risk", "delay", "late")):
        steps.append({"tool": "delay_risk", "args": {"tracking_id": ids[0]}})
    return steps


def _openai_plan(query: str):
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = "Return JSON array only. Choose tools from lookup_shipment, delay_risk, search_routes. Each item has tool and args. User query: " + query
    response = client.responses.create(model=os.getenv("OPENAI_MODEL", "gpt-5"), input=prompt)
    return json.loads(response.output_text)


def run_agent(query: str) -> dict:
    plan = _openai_plan(query) if os.getenv("OPENAI_API_KEY") else deterministic_plan(query)
    results = []
    for step in plan:
        tool = step.get("tool")
        if tool not in TOOLS:
            results.append({"tool": tool, "error": "unsupported tool"})
            continue
        results.append({"tool": tool, "result": TOOLS[tool](**step.get("args", {}))})
    return {"query": query, "plan": plan, "results": results}
