from __future__ import annotations
from typing import List
from .common import Message, as_chat
from ..llm.base import DefaultClient

SYS = """You are ModeratorAgent. Goal: run a rigorous expert call.
- Ask concise, high-signal questions.
- Use provided context and citations.
- Avoid MNPI; ask for public, experiential evidence.
- After an answer, propose one sharp follow-up.
Return: `QUESTION:` and `FOLLOW_UP:` lines only."""

class ModeratorAgent:
    def __init__(self):
        self.llm = DefaultClient()

    def next(self, transcript: str, context: str = "") -> str:
        messages = [
            {"role":"system","content": SYS},
            {"role":"user","content": f"Context:\n{context}\n\nTranscript so far:\n{transcript}\n"}
        ]
        return self.llm.chat(messages, max_tokens=400)
