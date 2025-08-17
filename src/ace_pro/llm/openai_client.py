from __future__ import annotations
from typing import List, Dict
import os

class OpenAIClient:
    """Thin wrapper; requires `openai` package and OPENAI_API_KEY set."""
    def __init__(self, model: str = None):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise RuntimeError('OPENAI_API_KEY not set')
        try:
            from openai import OpenAI  # type: ignore
        except Exception as e:
            raise RuntimeError('Install `openai` package to use OpenAIClient') from e
        self._client = OpenAI(api_key=api_key)
        self._model = model or os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

    def chat(self, messages: List[Dict[str,str]], *, max_tokens: int = 512) -> str:
        resp = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.3,
        )
        return resp.choices[0].message.content.strip()
