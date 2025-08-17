from __future__ import annotations
import argparse, os
from pathlib import Path
from .simulator import simulate_call
from .agent_loop import run_agent_call
from .rag.store import VectorStore
from .tools.redaction import redact_text, default_redaction_config
from .tools.summarize import summarize_extractive

def _ensure_out(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def cmd_ingest(args):
    vs = VectorStore()
    n = vs.ingest(args.folder)
    vs.save(args.index)
    print(f"Indexed {n} documents → {args.index}")

def cmd_run_sim(args):
    out = Path(args.out or 'out_sim'); _ensure_out(out)
    transcript = simulate_call(args.scenario)
    (out/'transcript.txt').write_text(transcript, encoding='utf-8')
    print(f"Wrote {out/'transcript.txt'}")

def cmd_run_agents(args):
    out = Path(args.out or 'out_agents'); _ensure_out(out)
    intro = Path(args.scenario).read_text(encoding='utf-8').splitlines()[0]
    vs=None
    if args.index and Path(args.index).exists():
        vs = VectorStore(); vs.load(args.index)
    transcript = run_agent_call(intro, knowledge_index=vs, turns=args.turns)
    (out/'transcript.txt').write_text(transcript, encoding='utf-8')
    # Redact + notes
    red = redact_text(transcript, default_redaction_config())
    (out/'redacted_transcript.txt').write_text(red, encoding='utf-8')
    bullets = summarize_extractive(transcript, top_k=args.top_k)
    (out/'notes.md').write_text("\n".join(["# Notes","","## Highlights",*['- '+b for b in bullets]]), encoding='utf-8')
    print(f"Artifacts in {out}")

def cmd_make_notes(args):
    out = Path(args.out or 'out_notes'); _ensure_out(out)
    text = Path(args.transcript).read_text(encoding='utf-8')
    bullets = summarize_extractive(text, top_k=args.top_k)
    (out/'notes.md').write_text("\n".join(["# Notes","","## Highlights",*['- '+b for b in bullets]]), encoding='utf-8')
    print(f"Wrote {out/'notes.md'}")

def cmd_redact(args):
    out = Path(args.out or 'out_redact'); _ensure_out(out)
    text = Path(args.transcript).read_text(encoding='utf-8')
    red = redact_text(text, default_redaction_config())
    (out/'redacted_transcript.txt').write_text(red, encoding='utf-8')
    print(f"Wrote {out/'redacted_transcript.txt'}")

def main():
    ap = argparse.ArgumentParser(prog='ace-pro')
    sub = ap.add_subparsers(required=True)

    p = sub.add_parser('ingest', help='Ingest a folder of .txt/.md docs into a vector store')
    p.add_argument('folder'); p.add_argument('--index', default='.ace_index.pkl')
    p.set_defaults(func=cmd_ingest)

    p = sub.add_parser('run-sim', help='Run offline simulated call (deterministic)')
    p.add_argument('scenario'); p.add_argument('--out')
    p.set_defaults(func=cmd_run_sim)

    p = sub.add_parser('run-agents', help='Run agent loop (uses LLM if OPENAI_API_KEY set)')
    p.add_argument('scenario'); p.add_argument('--index'); p.add_argument('--turns', type=int, default=6)
    p.add_argument('--top-k', type=int, default=7); p.add_argument('--out')
    p.set_defaults(func=cmd_run_agents)

    p = sub.add_parser('make-notes', help='Generate notes from transcript')
    p.add_argument('transcript'); p.add_argument('--top-k', type=int, default=7); p.add_argument('--out')
    p.set_defaults(func=cmd_make_notes)

    p = sub.add_parser('redact', help='Redact a transcript')
    p.add_argument('transcript'); p.add_argument('--out')
    p.set_defaults(func=cmd_redact)

    args = ap.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
