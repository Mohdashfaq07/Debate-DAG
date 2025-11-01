# Multi-Agent Debate DAG — Mock Offline Release

This package runs a mock-offline debate between two agents (Scientist vs Philosopher)
with memory and a local judge. No OpenAI key is required.

## Quick start

1. Extract the zip.
2. Create a virtual env and activate it:
   python -m venv venv
   venv\Scripts\activate   # windows
   source venv/bin/activate  # mac/linux
3. Install (graphviz system package may be required):
   pip install -r requirements.txt
4. Run:
   python src/debate_graph.py --mock
