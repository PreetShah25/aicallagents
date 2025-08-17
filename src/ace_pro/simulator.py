from __future__ import annotations
from pathlib import Path
import yaml

def simulate_call(yaml_path: str) -> str:
    data = yaml.safe_load(Path(yaml_path).read_text(encoding='utf-8'))
    inv = data.get('investor', {'name':'Investor'})
    exp = data.get('expert', {'name':'Expert'})
    agenda = data.get('agenda', [])
    style = data.get('style', {'tone':'concise','depth':'practical'})
    L=[]; L.append(f"System: Simulated call. Tone={style.get('tone')}, Depth={style.get('depth')}.");
    L.append(f"Investor: Thanks {exp.get('name')}, quick intro then agenda?"); L.append("Expert: Sounds good.")
    for item in agenda:
        q=item.get('q','Can you expand?'); a=item.get('a','Here is my perspective.')
        L.append(f"Investor: {q}"); L.append(f"Expert: {a}")
        for fq in item.get('followups', []):
            L.append(f"Investor: {fq}"); L.append(f"Expert: {a} Adding risks and implementation details.")
    L.append("Investor: Anything we missed?"); L.append("Expert: That covers it. Thanks.")
    return "\n".join(L)
