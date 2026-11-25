---
name: context-check
description: Audit current context usage and recommend whether to /clear, /compact, or delegate to a subagent. Use when output quality drops, when switching tasks, or when context feels heavy.
allowed-tools: Bash, Read
---

# Context check

Surfaces what's loaded into context and recommends the right next move.

## Steps

1. **Inventory loaded context**:
   - Project root CLAUDE.md (always loaded)
   - `.claude/rules/*.md` (auto-loaded)
   - Component CLAUDE.md (loaded when working in that dir)
   - Files Read this session
   - Subagent results merged back in

2. **Estimate budget**: rough heuristic — main CLAUDE.md ~2–5KB, each rule ~1–2KB, each file Read counts as its byte size.

3. **Recommend**:
   - **`/clear`** — switching to an unrelated task; current context is mostly noise for the next thing.
   - **`/compact <focus>`** — staying on the same task but losing focus; summarize and continue.
   - **Delegate to a subagent** — the next step is exploration/research; offload to keep main context lean.
   - **No action** — context is healthy, keep going.

## Decision rules

| Situation | Recommendation |
|---|---|
| Output quality drops, lots of repetition | `/compact` with a focus statement |
| Starting a new feature unrelated to current work | `/clear` then `/prime` |
| About to read 10+ files for research | spawn a researcher subagent instead |
| Working on the same task and trending well | nothing — keep going |

## Why this exists

The model can't reliably self-assess context health when context is already noisy. This skill gives a clean, scoped read on the situation.
