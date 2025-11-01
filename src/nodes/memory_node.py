# src/nodes/memory_node.py
from typing import List, Dict
from utils import log

class MemoryNode:
    def __init__(self):
        self.transcript: List[Dict] = []

    def append(self, msg: Dict):
        self.transcript.append(msg)
        log(f"[MemoryNode] Appended: {msg['speaker']} (R{msg['round']})")

    def summarize_for(self, recipient_name: str) -> str:
        if not self.transcript:
            return "No prior arguments."
        last_two = self.transcript[-2:] if len(self.transcript) >= 2 else self.transcript[:]
        lines = []
        for m in last_two:
            lines.append(f"R{m['round']} {m['speaker']}: {m['text']}")
        combined = " ".join([m["text"] for m in self.transcript])
        theme = " / ".join(list({w.strip(".,()").lower() for w in combined.split() if len(w) > 5})[:5])
        summary = f"Recent: {' | '.join(lines)}\nThemes: {theme or 'general points'}"
        log(f"[MemoryNode] Summary for {recipient_name}: {summary}")
        return summary

    def full_transcript(self) -> str:
        return "\n".join([f"R{m['round']} [{m['speaker']}] {m['text']}" for m in self.transcript])
