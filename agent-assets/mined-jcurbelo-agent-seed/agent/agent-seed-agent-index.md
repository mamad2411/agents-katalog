---
title: Agent Registry
description: Routing table for all available agents
max_lines: 150
---

# Agent Registry

Agents are specialized sub-processes with scoped tools and model tiers.
Each agent has a `.md` file in this folder with YAML frontmatter.

## Routing Table

| User intent | Agent | Model | When to use |
|-------------|-------|-------|-------------|
| Research a topic | [researcher](researcher.md) | haiku | Looking up info, web search |
| Write or edit code | [coder](coder.md) | sonnet | Creating, modifying, debugging code |
| Review code | [reviewer](reviewer.md) | sonnet | PR reviews, code quality checks |
| Manage todos | [todo-manager](todo-manager.md) | haiku | Creating, updating daily tasks |
| Self-improvement | [reflection](reflection.md) | haiku | Capturing learnings after sessions |

## Adding New Agents

The `/learn` skill can detect gaps and propose new agents via PR.
You can also create agents manually:

1. Create `.claude/agents/<name>.md`
2. Add YAML frontmatter: `model`, `tools`, `permissionMode` (required)
3. Add the agent to this routing table
4. Run `scripts/check-markdown-policy.sh` to validate

## Frontmatter Reference

```yaml
---
name: agent-name              # Unique identifier
description: What it does     # One line
model: haiku                  # haiku | sonnet | opus
tools:                        # Allowed tools list
  - Read
  - Write
  - Edit
permissionMode: default       # default | bypassPermissions
maxTurns: 10                  # Max conversation turns
memory: project               # Optional: persist learnings
---
```

## Model Tiering Guide

- **haiku** — fast, cheap: lookups, reads, searches, simple tasks
- **sonnet** — capable: code analysis, writing, drafting, medium complexity
- **opus** — powerful: orchestration, complex reasoning, multi-step planning
