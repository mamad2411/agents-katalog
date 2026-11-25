---
name: forge-intro
description: >-
  Onboard to Agent Forge pipeline. Use when first using this repo, asking how
  agent workflow works, or what skills to run.
---
# Forge Intro

Agent Forge is this repo's **memory-governed** pipeline â€” different from generic skill packs:

- **Recall / Remember** use MCP `ratary` (persistent handoffs)
- Stages map to docs-ai Knowledge OS governance (constitution, ADR, phases)
- Skills live in `.cursor/skills/forge-*`

## Read first

1. [docs-ai/cross-cutting/agent-forge/PIPELINE.md](../../docs-ai/products/ratary/phases/07.1-agent-forge/PIPELINE.md)
2. [.ai/START-HERE.md](../../docs-ai/INDEX.md)
3. [.ai/TASK_PROMPT.md](../../docs-ai/NOW.md) if active work exists

## Stage cheat sheet

| You are about toâ€¦ | Skill |
|-------------------|-------|
| Start a session | `forge-recall` |
| Explore a vague idea | `forge-intent` |
| Code after design OK | `forge-isolate` â†’ `forge-blueprint` â†’ `forge-execute` |
| Write/fix tests | `forge-prove` |
| Review between tasks | `forge-inspect` |
| Finish a branch | `forge-land` |
| End session | `forge-remember` |
| Debug a failure | `forge-diagnose` |

Rules are **mandatory**, not suggestions â€” see `.cursor/rules/agent-forge.mdc`.
