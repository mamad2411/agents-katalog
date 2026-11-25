---
name: use-agent
description: Load and activate a domain agent directly in Claude Code. Reads the agent's SOUL.md identity, skills, and workflows from ~/.talon/agents/ and applies them to the current session. Use when the user says "use <agent-name>", "load agent X", "be <agent-name>", "activate agent", or wants to switch to a domain agent persona.
user-invocable: true
---

# Use Agent — Load a Domain Agent in Claude Code

Load an agent from `~/.talon/agents/<name>/` and activate its identity, skills, and workflows in the current Claude Code session.

## Process

### Step 1: Identify the Agent

If the user specified an agent name (e.g., `/use-agent my-agent`), use that.
Otherwise, scan `~/.talon/agents/` and list available agents for the user to pick.

$ARGUMENTS

### Step 2: Load Agent Files

Read these files from `~/.talon/agents/<name>/`:

1. **AGENT.yaml** — Parse configuration (model, tools, skills list)
2. **SOUL.md** — Read the full identity document

### Step 3: Load Skills

For each skill listed in AGENT.yaml (or found in `skills/` directory):
- Read the `skills/<skill-name>/SKILL.md` file
- Present the skill name and description to understand capabilities

### Step 4: Load Workflows (if any)

For each workflow in `workflows/`:
- Read the YAML file
- Summarize the state machine (states and transitions)

### Step 5: Activate

Present the loaded agent to the user:

```
Agent loaded: <name>
Identity: <first line of SOUL.md>
Model: <model from AGENT.yaml>
Skills: <list of skill names with one-line descriptions>
Workflows: <list of workflow names>
```

Then tell the user:

> "I'm now operating as **<agent-name>**. My identity, skills, and workflows are loaded.
> Ask me anything in my domain and I'll use my specialized skills to help.
>
> Available skills:
> - `/skill-1` — description
> - `/skill-2` — description
>
> To stop: just ask me to 'stop being <agent-name>' or start a new session."

### Step 6: Follow the Identity

From this point forward in the conversation:

- **Adopt the SOUL.md persona** — tone, values, philosophy
- **Use loaded skills** when the user's query matches a skill's trigger description
- **Follow workflow states** if a workflow is active
- **Stay in character** — respond as the agent would, not as a generic assistant

## Important

- The agent's identity is applied through conversation context, not system prompt override
- Skills are available as reference — invoke them by reading the SKILL.md when the trigger matches
- This works in any Claude Code session, no dispatch needed
- The agent persists for the current conversation only
