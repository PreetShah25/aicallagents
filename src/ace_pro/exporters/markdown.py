from __future__ import annotations
from pathlib import Path

def export_markdown(bullets, transcript, out_dir: str):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    md = "\n".join(["# Notes","","## Highlights", *["- "+b for b in bullets], "", "## Transcript", "```", transcript, "```"])
    (out/"notes.md").write_text(md, encoding="utf-8")
    return str(out/"notes.md")
