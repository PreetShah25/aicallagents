from __future__ import annotations
import re, math
from collections import Counter

_SENT_SPLIT = re.compile(r'(?<=[.!?])\s+')
_WORD = re.compile(r"[A-Za-z0-9']+")
_STOP = set("""a an the and or but if while of for to in on at by with from about as into like through after over between out against during without before under around among is are was were be been being it this that these those he she they we you i me him her them us our your their""".split())

def _sentences(text: str):
    return [s.strip() for s in _SENT_SPLIT.split(text) if s.strip()]

def _tokenize(s: str):
    return [w.lower() for w in _WORD.findall(s)]

def _tfidf_rank(sents, top_k):
    docs = [[w for w in _tokenize(s) if w not in _STOP] for s in sents]
    df = Counter(); [df.update(set(d)) for d in docs]
    N = len(docs); scores = []
    for i,d in enumerate(docs):
        tf = Counter(d); sc = 0.0
        for t,f in tf.items():
            idf = math.log((N+1)/(1+df[t])) + 1.0
            sc += f*idf
        scores.append((sc,i))
    scores.sort(reverse=True); keep=[i for _,i in scores[:max(1,top_k)]]; keep.sort(); return keep

def summarize_extractive(text: str, top_k: int = 7):
    s = _sentences(text)
    if not s: return []
    idx = _tfidf_rank(s, top_k)
    return [s[i] for i in idx]
