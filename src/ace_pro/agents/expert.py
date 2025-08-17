from __future__ import annotations
from ..llm.base import DefaultClient

SYS = """You are ExpertAgent. Answer as a seasoned operator with practical detail, not hype.
- No MNPI. Cite experience and public knowledge.
- Be specific: metrics, processes, risks.
"""

class ExpertAgent:
    def __init__(self):
        self.llm = DefaultClient()

    def answer(self, question: str, context: str = "") -> str:
        messages = [
            {"role":"system","content": SYS},
            {"role":"user","content": f"Context (snippets):\n{context}\n\nQuestion:\n{question}"}
        ]
        return self.llm.chat(messages, max_tokens=450)
