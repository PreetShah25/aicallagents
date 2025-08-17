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


## Streamlit UI
```bash
streamlit run src/ace_pro/app/streamlit_app.py
```

## Exporters
- Markdown (default): saved in the output folder.
- Notion (skeleton): set `NOTION_TOKEN` and provide parent page ID
```bash
export NOTION_TOKEN=secret
python -m ace_pro.cli export-notion out_agents/transcript.txt <parent_page_id> --title "AI Call Notes"
```

## Live Adapters (stubs)
- Twilio: `src/ace_pro/live/twilio_adapter.py` (requires env and hosting a TwiML URL).
- WebRTC: `src/ace_pro/live/webrtc_stub.py` (design placeholder).
- ASR/TTS stubs: replace with your providers.

## Advanced RAG
Use `--adv` to signal advanced chunk/citation store. (Note: for simplicity the example uses a marker file.)


## Docker
```bash
docker compose up --build
# UI -> http://localhost:8501
# API -> http://localhost:8000/health
# Twilio demo server -> http://localhost:8001/health
```

## Twilio (demo)
- Point a public URL (ngrok or your domain) to the `twilio` service `/voice` endpoint.
- Use `/outbound` to initiate calls (requires env vars).

## API
- `POST /run-sim` { "scenario_text": "<yaml>" }
- `POST /run-agents` { "intro": "System: ...", "turns": 4 }

## Notebook
Open `notebooks/ACE_Pro_Demo.ipynb` in VS Code or Jupyter and run all cells.
