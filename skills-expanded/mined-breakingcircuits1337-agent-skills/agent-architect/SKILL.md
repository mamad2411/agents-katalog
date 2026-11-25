---
name: agent-architect
description: Scaffolds new AI agent projects with standard directory structures, configuration, and boilerplate code. Use when you need to create a new sub-agent, specialized worker, or experimental bot.
---

# Agent Architect

## Overview
The Agent Architect acts as a factory for spawning new AI agent projects. It handles the boilerplate of setting up directory structures, python environments, and basic agent code.

## Usage

### Create a New Agent
Run the scaffolder script to generate a new agent:

```bash
python3 scripts/scaffold_agent.py <agent_name> --instructions "Your instructions" --model <model_id>
```

**Parameters:**
- `agent_name`: Snake_case name (e.g., `research_bot`).
- `--instructions`: The core system prompt.
- `--model`: (Optional) The LLM model to use (default: `gemini-2.5-flash`).
- `--out`: (Optional) Target directory (default: `./agents`).

**Example:**
```bash
python3 scripts/scaffold_agent.py code_reviewer \
  --instructions "You review Python code for security flaws." \
  --out ./src/agents
```

### Generated Structure
```
agents/
└── code_reviewer/
    ├── main.py        # Executable entry point
    ├── config.json    # Model and tool config
    └── README.md      # Usage instructions
```

## Resources
- `scripts/scaffold_agent.py`: The generator script.
- `references/patterns.md`: Architectural guidelines for the generated agents.