---
description: Check that Founder OS is healthy. Say "verify the OS" or "health check" (or run /founder-os:verify). Returns a structured report across 9 substrate checks. Read-only. Never auto-fixes.
allowed-tools: ["Read", "Glob", "Grep", "Bash"]
---

# Founder OS verify

Read-only health check. Returns a structured report across 9 substrate checks.

## Procedure

1. Find the verify skill before trying to read it. It ships with the engine, and the
   engine is not always the folder you are standing in - on a plugin install the
   working directory is the founder's own folder. Take the first that exists:
   `${CLAUDE_PLUGIN_ROOT}/skills/verify/SKILL.md`, then `skills/verify/SKILL.md`
   relative to the working directory, then the newest match for
   `~/.claude/plugins/**/skills/verify/SKILL.md`. Read it from wherever it resolved
   and execute it end to end.

2. The skill owns all nine checks, the output format, and the summary footer. This
   command is a thin trigger. The skill runs `python scripts/verify.py` first and
   translates its findings; it never enumerates the file checks itself.

3. If the skill file is missing, reply: `Verify skill not found at skills/verify/SKILL.md.
   Restarting Claude Code fixes this most of the time, because it reloads what is installed. If it happens again after a restart, say "update Founder OS".` and stop.

## Rules

- Read-only. Do not write to any file.
- This command never auto-fixes anything. It only reports.
- No em dashes or en dashes. Hyphens only.
