from __future__ import annotations
from ..tools.summarize import summarize_extractive

class NotesAgent:
    def summarize(self, transcript: str, top_k: int = 7):
        return summarize_extractive(transcript, top_k=top_k)
