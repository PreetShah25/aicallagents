from ace_pro.rag.store import VectorStore
import os, tempfile, pathlib

def test_ingest_and_query(tmp_path):
    p = tmp_path / "docs"; p.mkdir()
    (p / "a.txt").write_text("voice ai routing is production ready")
    (p / "b.md").write_text("guardrails evaluation remains weak")
    vs = VectorStore(); n = vs.ingest(str(p)); assert n == 2
    hits = vs.query("guardrails", k=1)
    assert hits and "guardrails" in hits[0][2].lower()
