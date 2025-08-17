from __future__ import annotations
from typing import Optional
from .agents.moderator import ModeratorAgent
from .agents.expert import ExpertAgent
from .agents.compliance import ComplianceAgent
from .rag.store import VectorStore

def run_agent_call(scenario_intro: str, knowledge_index: Optional[VectorStore] = None, turns: int = 6) -> str:
    mod = ModeratorAgent(); exp = ExpertAgent(); comp = ComplianceAgent()
    transcript = scenario_intro.strip() + "\n"
    for t in range(turns):
        # RAG context
        ctx = ""
        if knowledge_index:
            q_hint = transcript[-500:]
            hits = knowledge_index.query(q_hint, k=2)
            ctx = "\n\n".join([f"[score={s:.3f}] {snip}" for s,_,snip in hits])
        # Moderator asks question
        mod_out = mod.next(transcript, context=ctx)
        transcript += f"Moderator: {mod_out}\n"
        # Expert answers
        ans = exp.answer(mod_out, context=ctx)
        transcript += f"Expert: {ans}\n"
        # Compliance pass
        flags = comp.check(ans)
        if flags != "OK":
            transcript += f"Compliance: {flags}\n"
    return transcript
