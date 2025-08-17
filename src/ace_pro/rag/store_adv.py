from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from .chunker import simple_chunks

@dataclass
class ChunkRef:
    path: str
    start: int
    end: int
    text: str

class VectorStoreAdv:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=30000)
        self.chunks: List[ChunkRef] = []
        self.mat = None

    def ingest(self, folder: str, extensions=('.txt','.md')) -> int:
        self.chunks.clear()
        for p in Path(folder).rglob('*'):
            if p.suffix.lower() in extensions:
                raw = p.read_text(encoding='utf-8', errors='ignore')
                offset = 0
                for ch in simple_chunks(raw):
                    self.chunks.append(ChunkRef(str(p), offset, offset+len(ch), ch))
                    offset += len(ch)
        if not self.chunks:
            self.mat = None; return 0
        corpus = [c.text for c in self.chunks]
        self.mat = self.vectorizer.fit_transform(corpus)
        return len(self.chunks)

    def query(self, text: str, k: int = 3) -> List[Tuple[float, ChunkRef]]:
        if self.mat is None: return []
        qv = self.vectorizer.transform([text])
        sims = (qv @ self.mat.T).toarray()[0]
        idx = np.argsort(-sims)[:k]
        return [(float(sims[i]), self.chunks[i]) for i in idx]
