---
description: Audit the wiki. Tool invocation (run /founder-os:lint). Read-only check across broken cross-references, orphan pages, stale time-sensitive content, provenance gaps, and possible contradictions. Never auto-fixes.
allowed-tools: ["Read", "Glob", "Grep"]
---

# Founder OS lint

Read-only wiki audit. Surfaces issues, never fixes them.

## Procedure

1. Read the lint skill at `skills/lint/SKILL.md` and execute it end to end.

2. The skill owns the scan logic, file reads, and output rendering. This command is a thin trigger.

3. If the skill file is missing, reply: `Lint skill not found at skills/lint/SKILL.md. Restarting Claude Code fixes this most of the time, because it reloads what is installed. If it happens again after a restart, say "update Founder OS".` and stop.

## Rules

- Read-only. Never modify any file.
- Output is a single fenced report block. No commentary before, after, or around it.
- If the install is empty (no `core/identity.md`), reply: `Founder OS not set up here. Say "set up Founder OS" first.` and stop.
- No em dashes or en dashes. Hyphens only.
