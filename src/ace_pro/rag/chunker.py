from __future__ import annotations
from typing import List, Tuple
def simple_chunks(text: str, chunk_size: int = 800, overlap: int = 120) -> List[str]:
    out=[]; i=0
    while i < len(text):
        out.append(text[i:i+chunk_size])
        i += max(1, chunk_size - overlap)
    return out
