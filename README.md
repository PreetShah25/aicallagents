# ai-call-exchange-pro

Advanced **AI-based expert call exchange** toolkit with *agents*, *GenAI integration*, offline **simulator**, **RAG** (document ingestion + retrieval), **compliance redaction**, and **structured notes**. Built to prototype Third Bridge–style calls with automated agenda planning, dynamic follow‑ups, and exportable notes.

> ⚠️ **Compliance**: If you connect to real calls, ensure explicit consent, avoid MNPI, and comply with privacy laws in each jurisdiction.

## Key Capabilities
- **Agent loop**: `ModeratorAgent` (plans & probes), `ExpertAgent` (answers), `ComplianceAgent` (flags), `NotesAgent` (summarizes).
- **GenAI**: Pluggable LLM provider (`OPENAI_API_KEY` optional). Fallback to deterministic local stub when no key is set.
- **RAG**: Local TF‑IDF vector store over `.txt/.md` knowledge; cite snippets during the call.
- **Offline simulator**: Reproducible transcripts from YAML scenarios (personas + agenda).
- **Redaction**: Emails/phones/MNPI keywords, with optional name redaction toggle.
- **Artifacts**: `transcript.txt`, `redacted_transcript.txt`, `notes.md`, `notes.json`.
- **CLI**: `ingest`, `run-sim`, `run-agents`, `redact`, `make-notes`.
- **CI/Tests**: GitHub Actions runs flake8 + pytest on 3.10/3.11.

## Install
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Optional: enable GenAI
export OPENAI_API_KEY=sk-...  # or set in your shell profile
```

## Quickstarts
### 1) Offline simulation (no LLM needed)
```bash
python -m ace_pro.cli run-sim examples/scenario.yaml --out out_sim
```

### 2) RAG + Agent loop (uses LLM if key present)
```bash
# Ingest local notes into a vector store
python -m ace_pro.cli ingest data/knowledge --index .ace_index.pkl

# Run agents using a scenario + knowledge index
python -m ace_pro.cli run-agents examples/scenario.yaml --index .ace_index.pkl --out out_agents
```

### 3) Generate notes from a transcript
```bash
python -m ace_pro.cli make-notes out_agents/transcript.txt --out out_notes
```

## Repo Map
```
src/ace_pro/
  agents/        # Moderator, Expert, Compliance, Notes
  llm/           # LLM provider abstraction + OpenAI client + local stub
  rag/           # TF-IDF vector store + ingestion
  tools/         # redaction, utils
  simulator.py   # deterministic offline transcript generator
  cli.py         # command-line interface
examples/
tests/
```

## Real-time Plumbing (future work)
- Telephony (Twilio/WebRTC), streaming ASR (Whisper/Deepgram), streaming TTS.
- Turn the agent loop into a real-time orchestration with partial summaries, handoff to researcher, and compliance gating.
