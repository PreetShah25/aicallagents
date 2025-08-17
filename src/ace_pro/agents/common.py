from __future__ import annotations
from typing import List, Dict
from pydantic import BaseModel, Field

class Message(BaseModel):
    role: str
    content: str

class Turn(BaseModel):
    messages: List[Message] = Field(default_factory=list)

def as_chat(messages: List[Message]) -> List[Dict[str,str]]:
    return [m.model_dump() for m in messages]
