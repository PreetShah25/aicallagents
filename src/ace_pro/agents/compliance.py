from __future__ import annotations
import re

MNPI = re.compile(r"\b(non[-\s]?public|material non[-\s]?public|mnpi|inside(?:r)? information)\b", re.I)
PII_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PII_PHONE = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})\b")

class ComplianceAgent:
    def check(self, text: str) -> str:
        flags = []
        if MNPI.search(text): flags.append("MNPI-like keyword")
        if PII_EMAIL.search(text): flags.append("email present")
        if PII_PHONE.search(text): flags.append("phone present")
        if not flags: return "OK"
        return "; ".join(flags)
