
🚀 Quick Start

Prerequisites

1. Install Ollama: Download from ollama.ai.
2. Pull a Model: Start with a coding powerhouse:
ollama pull codellama

Installation

# Clone the repository
https://github.com/arasbey4/CodeGarden-agent
cd CodeGarden-agent

# Install dependencies
pip install -r requirements.txt

Execution

python main.py

---

🛠️ Command Reference

┌───────────────┬───────────────────────────────────────────┐
│    Command    │                Description                │
├───────────────┼───────────────────────────────────────────┤
│ /models       │ List all installed local models.          │
├───────────────┼───────────────────────────────────────────┤
│ /cloud-models │ View recommended high-performance models. │
├───────────────┼───────────────────────────────────────────┤
│ /pull <name>  │ Download a model from the Ollama library. │
├───────────────┼───────────────────────────────────────────┤
│ /model <name> │ Change the active AI model.               │
├───────────────┼───────────────────────────────────────────┤
│ /cd <path>    │ Change the project working directory.
├───────────────┼───────────────────────────────────────────┤
│ /clear        │ Reset the conversation history.
├───────────────┼───────────────────────────────────────────┤
│ /help         │ Show all available commands.
├───────────────┼───────────────────────────────────────────┤
│ /exit         │ Exit the garden.
└───────────────┴───────────────────────────────────────────┘

---

🪴 How it Works

CodeGarden connects to the Ollama API and implements a Reasoning-Action (ReAct) loop. When you give it a task, the agent:
1. Analyzes the request.
2. Selects the best tool (read, write, execute, or cd).
3. Executes the tool and observes the result.
4. Repeats this process until the goal is achieved.

---
