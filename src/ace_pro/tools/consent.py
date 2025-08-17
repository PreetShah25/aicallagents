from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class ConsentPolicy:
    region: str  # e.g., "US-CA", "US-NY", "EU-DE"
    require_two_party: bool = True
    recording_notice: str = "This call may be recorded for note-taking. Do you consent?"

def consent_prompt(policy: ConsentPolicy) -> str:
    if policy.region.startswith("US-CA"):
        return policy.recording_notice + " (California two-party consent.)"
    if policy.region.startswith("EU"):
        return policy.recording_notice + " (GDPR applies.)"
    return policy.recording_notice
