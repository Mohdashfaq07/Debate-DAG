# src/debate_graph.py
import os
import sys
# ensure src dir is on path so relative imports work
sys.path.append(os.path.dirname(__file__))
from utils import log
from nodes.user_input_node import UserInputNode
from nodes.agent_node import AgentNode
from nodes.memory_node import MemoryNode
from nodes.judge_node import JudgeNode

from graphviz import Digraph

def generate_dag_diagram(output_path=None):
    if output_path is None:
        output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dag_diagram")
    dot = Digraph(comment="Debate DAG")
    dot.attr("node", shape="box")
    dot.node("UserInput", "UserInputNode")
    dot.node("AgentA", "AgentNode: Scientist")
    dot.node("AgentB", "AgentNode: Philosopher")
    dot.node("Memory", "MemoryNode")
    dot.node("Judge", "JudgeNode")
    dot.edge("UserInput", "AgentA")
    dot.edge("AgentA", "Memory")
    dot.edge("Memory", "AgentB")
    dot.edge("AgentB", "Memory")
    dot.edge("Memory", "AgentA")
    dot.edge("Memory", "Judge")
    dot.edge("AgentA", "Judge")
    dot.edge("AgentB", "Judge")
    dot.format = "png"
    dot.render(filename=output_path, cleanup=True)
    log(f"[debate_graph] DAG diagram generated at {output_path}.png")

def run_debate(topic: str):
    user_node = UserInputNode()
    mem = MemoryNode()
    agent_a = AgentNode(name="Scientist", persona="A practical scientist focusing on safety and evidence", model_runner=None)
    agent_b = AgentNode(name="Philosopher", persona="A philosopher valuing autonomy, progress, and ethical reflection", model_runner=None)
    judge = JudgeNode(model_runner=None)

    user_data = user_node.run(topic)
    rounds = 8
    for r in range(1, rounds + 1):
        speaker_turn = agent_a if (r % 2 == 1) else agent_b
        mem_summary = mem.summarize_for(speaker_turn.name)
        msg = speaker_turn.generate_argument(topic=user_data["topic"], round_number=r, memory=mem_summary)
        mem.append(msg)

    verdict = judge.judge(mem.transcript, topic=user_data["topic"])
    log("=== Final Transcript ===")
    log(mem.full_transcript())
    log("=== Judge Verdict ===")
    log(f"Winner: {verdict.get('winner')}")
    log(f"Reason: {verdict.get('reason')}")
    generate_dag_diagram()
    return {"transcript": mem.transcript, "verdict": verdict}

if __name__ == "__main__":
    import argparse
    from rich import print
    parser = argparse.ArgumentParser(description="Run Multi-Agent Debate DAG (CLI).")
    parser.add_argument("--topic", type=str, help="Debate topic (wrap in quotes).", required=False)
    parser.add_argument("--mock", action="store_true", help="Use mock agents (no OpenAI).")
    args = parser.parse_args()
    if not args.topic:
        topic = input("Enter topic for debate: ").strip()
    else:
        topic = args.topic
    print(f"Starting (mock) debate on: {topic}")
    run_debate(topic=topic)
    print("Debate finished. Log saved to logs/debate_log.txt and DAG diagram generated.")
