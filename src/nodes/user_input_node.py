# src/nodes/user_input_node.py
from utils import log

class UserInputNode:
    def __init__(self):
        pass

    def run(self, topic: str):
        topic = topic.strip()
        log(f"[UserInputNode] Topic received: {topic}")
        return {"topic": topic}
