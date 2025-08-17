from __future__ import annotations
import argparse
from pathlib import Path
from .simulator import simulate_call
from .agent_loop import run_agent_call
from .rag.store import VectorStore
from .rag.store_adv import VectorStoreAdv
from .tools.redaction import redact_text, default_redaction_config
from .tools.summarize import summarize_extractive
from .exporters.markdown import export_markdown
from .exporters.notion import export_notion_simple

def _ensure_out(p: Path): p.mkdir(parents=True, exist_ok=True)

def cmd_ingest(args):
    if args.adv:
        vs = VectorStoreAdv(); n = vs.ingest(args.folder); vs_path = Path(args.index)
        vs_path.write_text("adv", encoding="utf-8")  # marker
        print(f"Indexed {n} chunks with VectorStoreAdv → {args.index} (marker)")
    else:
        vs = VectorStore(); n = vs.ingest(args.folder); print(f"Indexed {n} docs")
        import pickle; pickle.dump(vs, open(args.index, "wb"))

def _load_index(path: str):
    p = Path(path)
    if not p.exists(): return None, None
    try:
        if p.read_text(encoding="utf-8") == "adv":
            return "adv", VectorStoreAdv()  # empty but signals adv; user should re-ingest in same run
    except Exception:
        pass
    import pickle
    vs = pickle.load(open(path, "rb"))
    return "basic", vs

def cmd_run_sim(args):
    out = Path(args.out or 'out_sim'); _ensure_out(out)
    transcript = simulate_call(args.scenario)
    (out/'transcript.txt').write_text(transcript, encoding='utf-8')
    print(f"Wrote {out/'transcript.txt'}")

def cmd_run_agents(args):
    out = Path(args.out or 'out_agents'); _ensure_out(out)
    intro = Path(args.scenario).read_text(encoding='utf-8').splitlines()[0]
    kind, vs = _load_index(args.index) if args.index else (None, None)
    transcript = run_agent_call(intro, knowledge_index=vs, turns=args.turns)
    (out/'transcript.txt').write_text(transcript, encoding='utf-8')
    red = redact_text(transcript, default_redaction_config())
    (out/'redacted_transcript.txt').write_text(red, encoding='utf-8')
    bullets = summarize_extractive(transcript, top_k=args.top_k)
    export_markdown(bullets, transcript, str(out))
    print(f"Artifacts in {out}")

def cmd_make_notes(args):
    out = Path(args.out or 'out_notes'); _ensure_out(out)
    text = Path(args.transcript).read_text(encoding='utf-8')
    bullets = summarize_extractive(text, top_k=args.top_k)
    export_markdown(bullets, text, str(out))
    print(f"Wrote {out/'notes.md'}")

def cmd_redact(args):
    out = Path(args.out or 'out_redact'); _ensure_out(out)
    text = Path(args.transcript).read_text(encoding='utf-8')
    red = redact_text(text, default_redaction_config())
    (out/'redacted_transcript.txt').write_text(red, encoding='utf-8')
    print(f"Wrote {out/'redacted_transcript.txt'}")

def cmd_export_notion(args):
    text = Path(args.transcript).read_text(encoding='utf-8')
    bullets = summarize_extractive(text, top_k=args.top_k)
    page_id = export_notion_simple(args.title, bullets, text, args.parent_page)
    print(f"Created Notion page: {page_id}")

def main():
    ap = argparse.ArgumentParser(prog='ace-pro')
    sub = ap.add_subparsers(required=True)

    p = sub.add_parser('ingest', help='Ingest docs into a vector store'); p.add_argument('folder')
    p.add_argument('--index', default='.ace_index.pkl'); p.add_argument('--adv', action='store_true')
    p.set_defaults(func=cmd_ingest)

    p = sub.add_parser('run-sim', help='Run offline simulation'); p.add_argument('scenario'); p.add_argument('--out')
    p.set_defaults(func=cmd_run_sim)

    p = sub.add_parser('run-agents', help='Run agent loop (LLM if OPENAI_API_KEY set)')
    p.add_argument('scenario'); p.add_argument('--index'); p.add_argument('--turns', type=int, default=6)
    p.add_argument('--top-k', type=int, default=7); p.add_argument('--out')
    p.set_defaults(func=cmd_run_agents)

    p = sub.add_parser('make-notes', help='Generate notes from transcript')
    p.add_argument('transcript'); p.add_argument('--top-k', type=int, default=7); p.add_argument('--out')
    p.set_defaults(func=cmd_make_notes)

    p = sub.add_parser('redact', help='Redact a transcript'); p.add_argument('transcript'); p.add_argument('--out')
    p.set_defaults(func=cmd_redact)

    p = sub.add_parser('export-notion', help='Export notes to Notion page')
    p.add_argument('transcript'); p.add_argument('parent_page'); p.add_argument('--title', default='AI Call Notes')
    p.add_argument('--top-k', type=int, default=7); p.set_defaults(func=cmd_export_notion)

    args = ap.parse_args(); args.func(args)

if __name__ == '__main__': main()
