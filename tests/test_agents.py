from ace_pro.agent_loop import run_agent_call
from ace_pro.rag.store import VectorStore

def test_agent_loop_runs(tmp_path):
    vs = VectorStore(); # no docs, still runs
    transcript = run_agent_call("System: Test intro", knowledge_index=None, turns=2)
    assert "Moderator:" in transcript and "Expert:" in transcript
