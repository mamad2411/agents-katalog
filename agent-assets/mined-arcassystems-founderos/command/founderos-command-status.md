---
description: Check OS readiness. Say "check my OS readiness", "what's my OS state", or "readiness check" (or run /founder-os:status). Returns a weighted score across six buckets (Core, Voice and Brand, Cadence, Business Context, Brain Layer, Queue) plus the next 3 high-impact moves. For a full health audit, use /founder-os:audit. Read-only.
allowed-tools: ["Read", "Glob", "Grep"]
---

# Founder OS status

Read-only readiness check. Reads the OS state and returns a single fenced score block.

## Procedure

1. Read the readiness skill at `skills/readiness-check/SKILL.md` and execute it end to end.

2. The skill owns the scoring logic, file reads, and output rendering. This command is a thin trigger.

3. If the skill file is missing, reply: `Readiness skill not found at skills/readiness-check/SKILL.md. Restarting Claude Code fixes this most of the time, because it reloads what is installed. If it happens again after a restart, say "update Founder OS".` and stop.

## Rules

- Read-only. Do not write to any file.
- Output is a single fenced block. No commentary before, after, or around it.
- If the install is empty (no `core/identity.md`), reply: `Founder OS not set up here. Say "set up Founder OS" first.` and stop.
- No em dashes or en dashes. Hyphens only.
