# src/nodes/agent_node.py
import hashlib
from utils import log, now_ts
from typing import Dict, List, Optional

class AgentNode:
    def __init__(self, name: str, persona: str, model_runner=None):
        self.name = name
        self.persona = persona
        self.history: List[Dict] = []
        self.seen_hashes = set()
        self.model_runner = model_runner

    def _hash_text(self, text: str):
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def generate_argument(self, topic: str, round_number: int, memory: Optional[str]=None):
        prompt = (
            f"You are {self.name}, a {self.persona}.\n"
            f"Topic: {topic}\n"
            f"Round: {round_number}\n"
            f"Memory summary (only what is relevant to you):\n{memory or 'None'}\n\n"
            "Make a short, original argument (1-3 sentences)."
        )
        if self.model_runner:
            text = self.model_runner(prompt=prompt, role=self.name)
        else:
            text = f"[Mock-{self.name}] (round {round_number}) argument about '{topic}'."
        h = self._hash_text(text)
        if h in self.seen_hashes:
            text += " (additional nuance)"
            h = self._hash_text(text)
        self.seen_hashes.add(h)
        msg = {"speaker": self.name, "round": round_number, "text": text, "ts": now_ts()}
        self.history.append(msg)
        log(f"[{self.name}] {text}")
        return msg
