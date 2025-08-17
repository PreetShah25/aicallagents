from __future__ import annotations
from typing import List, Dict, Optional

class LLMClient:
    def chat(self, messages: List[Dict[str,str]], *, max_tokens: int = 512) -> str:
        raise NotImplementedError

class LocalStub(LLMClient):
    """Deterministic, dependency-free 'LLM' for testing."""
    def chat(self, messages, *, max_tokens: int = 512) -> str:
        last_user = next((m['content'] for m in reversed(messages) if m['role']=='user'), ''))
        # Simple template: mirror + add a cautious caveat
        return (last_user[: max_tokens//2] + "\n(Caveat: synthetic stub, not model output.)").strip()

try:
    import os
    import importlib
    _openai_key = os.environ.get('OPENAI_API_KEY', '')
    if _openai_key:
        from .openai_client import OpenAIClient  # type: ignore
        DefaultClient = OpenAIClient
    else:
        DefaultClient = LocalStub
except Exception:
    DefaultClient = LocalStub
