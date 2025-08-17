"""
Lightweight API (Flask) exposing run-sim and run-agents for demos.
"""
from flask import Flask, request, jsonify
from pathlib import Path
from ace_pro.simulator import simulate_call
from ace_pro.agent_loop import run_agent_call
from ace_pro.tools.redaction import redact_text, default_redaction_config
from ace_pro.tools.summarize import summarize_extractive

app = Flask(__name__)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/run-sim")
def run_sim():
    data = request.get_json(force=True)
    scenario_text = data.get("scenario_text")
    if not scenario_text:
        return {"error":"scenario_text required"}, 400
    p = Path("tmp_scenario.yaml"); p.write_text(scenario_text, encoding="utf-8")
    transcript = simulate_call(str(p))
    return {"transcript": transcript}

@app.post("/run-agents")
def run_agents():
    data = request.get_json(force=True)
    intro = data.get("intro", "System: Demo intro")
    turns = int(data.get("turns", 4))
    transcript = run_agent_call(intro, knowledge_index=None, turns=turns)
    red = redact_text(transcript, default_redaction_config())
    bullets = summarize_extractive(transcript, top_k=7)
    return {"transcript": transcript, "redacted": red, "bullets": bullets}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
