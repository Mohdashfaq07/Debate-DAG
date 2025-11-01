# src/nodes/judge_node.py
from typing import List, Dict, Optional
from utils import log, now_ts

class JudgeNode:
    def __init__(self, model_runner=None):
        self.model_runner = model_runner

    def judge(self, transcript: List[Dict], topic: str) -> Dict:
        summary_lines = [f"R{m['round']} {m['speaker']}: {m['text']}" for m in transcript]
        summary = "\n".join(summary_lines)
        if self.model_runner:
            prompt = (
                f"You are a meticulous judge. Topic: {topic}\n\n"
                f"Transcript:\n{summary}\n\n"
                "Provide:\n1) A concise 3-5 sentence debate summary.\n2) Pick a winner: Scientist or Philosopher or Tie.\n3) Provide short logical reasoning for your decision."
            )
            out = self.model_runner(prompt=prompt, role="Judge")
            return {"summary": out, "winner": "Model-declared", "reason": "See summary"}
        else:
            text = summary.lower()
            risk_score = sum(text.count(k) for k in ["risk", "safety", "harm", "regulated", "medical", "clinical", "mitigate"])
            freedom_score = sum(text.count(k) for k in ["freedom", "autonomy", "progress", "innovation", "philosophy", "ethics"])
            if risk_score > freedom_score:
                winner = "Scientist"
                reason = f"Risk-oriented arguments outranked freedom-oriented ones ({risk_score} vs {freedom_score})."
            elif freedom_score > risk_score:
                winner = "Philosopher"
                reason = f"Freedom/innovation-centered arguments outranked risk-oriented ones ({freedom_score} vs {risk_score})."
            else:
                winner = "Tie"
                reason = f"Scores equal ({risk_score} vs {freedom_score})."
            summary_short = " ".join(summary_lines[:8]) + ("\n..." if len(summary_lines) > 8 else "")
            verdict = {"summary": summary_short, "winner": winner, "reason": reason, "ts": now_ts()}
            log(f"[JudgeNode] Verdict: {verdict}")
            return verdict
