---
name: careful
description: Write a checklist of destructive commands the user wants to think twice about (rm -rf, force push, hard reset, db drop, etc.) to .dragoon/CAREFUL.md. dragoon does NOT block commands at runtime - this is a discipline tool, a list the agent reads before risky operations. Use to set explicit guardrails for an AI agent or new contributor. Run as `node ~/.claude/skills/dragoon/skills/careful/scripts/careful.js`.
version: 1.0.0
---

# /careful

Discipline-tool checklist for destructive commands.

## When to use

- Setting up a new project or onboarding an agent
- After a destructive accident, codify the rule
- The user says "set up guardrails", "what should the agent not do"

## What it writes

`.dragoon/CAREFUL.md` with two sections:
- destructive commands to confirm before running (rm -rf, force push, etc.)
- destructive commands the agent should NEVER run without explicit user prompt

This is **not** a runtime block. It's a read-before-act discipline aid.

## Run it

```
dragoon careful --apply
dragoon careful --show
```
