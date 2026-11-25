---
name: edit
description: "Visually edit existing Agent Teams configuration. Use to change agents, workflows, or skills."
user-invocable: true
allowed-tools: Bash(npx:*), Bash(cd:*), Read, Glob
---

# /edit

Interactively edit an existing agent-system.config.yaml configuration.

## Usage

```bash
npx create-agent-system edit [--target <path>]
```

## Flow

1. Load current configuration (agent-system.config.yaml required)
2. Display current settings summary
3. Select section to edit:
   - **Agents** — Enable/disable agents
   - **Workflow** — Review rounds, QA mode, Visual QA, EPIC-based
   - **Skills** — Enable/disable skills
   - **All** — Edit everything
4. Display change diff
5. Choose save method:
   - Save config only
   - Save config + re-scaffold
   - Cancel

## Prerequisites

An `agent-system.config.yaml` file must exist. If not, create one first with `/scaffold --save-config`.
