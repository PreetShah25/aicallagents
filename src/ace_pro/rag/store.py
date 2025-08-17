from __future__ import annotations
from typing import List, Tuple
from dataclasses import dataclass
from pathlib import Path
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def _read_doc(p: Path) -> str:
    txt = p.read_text(encoding='utf-8', errors='ignore')
    # basic cleanup
    return re.sub(r'\s+', ' ', txt).strip()

@dataclass
class DocRef:
    path: str
    text: str

class VectorStore:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=20000)
        self.docs: List[DocRef] = []
        self.mat = None

    def ingest(self, folder: str, extensions=('.txt','.md')) -> int:
        self.docs = []
        for p in Path(folder).rglob('*'):
            if p.suffix.lower() in extensions:
                self.docs.append(DocRef(str(p), _read_doc(p)))
        corpus = [d.text for d in self.docs]
        if not corpus:
            self.mat = None
            return 0
        self.mat = self.vectorizer.fit_transform(corpus)
        return len(self.docs)

    def save(self, path: str):
        import pickle
        with open(path, 'wb') as f:
            pickle.dump({'vocab': self.vectorizer.vocabulary_, 'docs': self.docs, 'idf': self.vectorizer.idf_}, f)

    def load(self, path: str):
        import pickle, scipy.sparse as sp
        data = pickle.load(open(path, 'rb'))
        self.vectorizer = TfidfVectorizer(stop_words='english', vocabulary=data['vocab'])
        # hack: rebuild with stored idf
        self.vectorizer._tfidf._idf_diag = None  # type: ignore
        self.docs = data['docs']
        # Defer matrix construction until first query
        self.mat = None

    def _ensure_matrix(self):
        if self.mat is None and self.docs:
            corpus = [d.text for d in self.docs]
            self.mat = self.vectorizer.fit_transform(corpus)

    def query(self, text: str, k: int = 3) -> List[Tuple[float, DocRef, str]]:
        self._ensure_matrix()
        if self.mat is None:
            return []
        qv = self.vectorizer.transform([text])
        sims = (qv @ self.mat.T).toarray()[0]
        idx = np.argsort(-sims)[:k]
        out = []
        for i in idx:
            doc = self.docs[int(i)]
            score = float(sims[int(i)])
            # return a snippet (first 400 chars around the highest matching ngram not tracked here → fallback to head)
            snippet = doc.text[:400]
            out.append((score, doc, snippet))
        return out
