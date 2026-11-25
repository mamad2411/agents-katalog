---
name: list-agents
description: Discover and inspect existing agents, skills, and workflows. Use when the user wants to see what agents are available, what skills they have, or explore agent capabilities.
user-invocable: true
---

# List Agents — Discovery and Inspection

Find and display existing agents, skills, and workflows across the workspace.

## Process

### Step 1: Scan for Agents

Search these locations for agent definitions:

```
# Primary location
~/.talon/agents/*/AGENT.yaml

# Standalone skills
~/.talon/skills/*/SKILL.md

# Standalone workflows
~/.talon/workflows/*.yaml
```

### Step 2: Display Agent Summary

For each agent found, show:

```
Agent: <name>
  Description: <from AGENT.yaml>
  Model: <model>
  Backend: <backend or "default">
  Skills: <count> (<skill-1>, <skill-2>, ...)
  Workflows: <count> (<workflow-1>, ...)
  Identity: <first line of SOUL.md>
```

### Step 3: Detailed Inspection (if requested)

If the user asks about a specific agent, show:

1. **Full SOUL.md** — identity and philosophy
2. **AGENT.yaml** — complete configuration
3. **Skills list** — each skill's name, description, and step count
4. **Workflow diagram** — text representation of state machine:
   ```
   [planning] → [implementation] → [review] → [done]
                       ↑                |
                       └── (rejected) ──┘
   ```
5. **Launch command** — how to run this agent via dispatch

### Step 4: Gap Analysis (optional)

If the user asks "what's missing?" or wants to improve an agent:

- Check if SOUL.md exists and has substance (not just template placeholders)
- Check if skills have validation steps
- Check if workflows pass validation
- Check if AGENT.yaml references skills/workflows that actually exist
- Suggest improvements based on domain best practices

## Output Format

**Summary view (default):**
```
Found 3 agents:

  analyst         Financial research agent (opus)
                  Skills: dcf-valuation, fundamental-analysis, sec-filing-reader
                  Workflows: research-pipeline

  sentinel        Security audit agent (sonnet, default)
                  Skills: dependency-scan, owasp-check, secret-detection

  scribe          Documentation agent (haiku, default)
                  Skills: api-doc-gen, changelog-writer
```

**No agents found:**
```
No agents found in this workspace.

To create one: /create-agent
```

$ARGUMENTS
