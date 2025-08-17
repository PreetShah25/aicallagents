from __future__ import annotations
import re
from dataclasses import dataclass

@dataclass
class RedactionConfig:
    redact_emails: bool = True
    redact_phones: bool = True
    redact_names: bool = False
    redact_mnpi_keywords: bool = True

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})\b")
MNPI = re.compile(r"\b(non[-\s]?public|material non[-\s]?public|mnpi|inside(?:r)? information)\b", re.I)

def default_redaction_config() -> RedactionConfig:
    return RedactionConfig()

def redact_text(text: str, cfg: RedactionConfig) -> str:
    out = text
    if cfg.redact_emails: out = EMAIL.sub('[REDACTED_EMAIL]', out)
    if cfg.redact_phones: out = PHONE.sub('[REDACTED_PHONE]', out)
    if cfg.redact_mnpi_keywords: out = MNPI.sub('[SENSITIVE]', out)
    return out
