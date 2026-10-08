---
description: Distill a reusable skill from the current session by delegating to the skill-distiller subagent
argument-hint: "[optional focus, e.g. 'the colima ipv6 fix']"
---

Delegate to the `skill-distiller` subagent to capture any reusable, class-level
technique from this session as a `SKILL.md` under `~/.claude/skills/`.

Steps:

1. Determine this session's transcript path: it is `~/.claude/projects/<encoded-cwd>/<session-id>.jsonl`. If you can't resolve it, pass the most recent `.jsonl` in this project's dir.
2. Invoke the subagent:
   ```
   Task(
     subagent_type="skill-distiller",
     description="Distill skill from session",
     prompt="Distill a reusable skill from this work session. " +
            "Transcript: <path>. " +
            ("Focus on: $ARGUMENTS. " if "$ARGUMENTS" else "") +
            "Follow your patch-first decision tree; abort if there's nothing class-level and reusable."
   )
   ```
3. Relay the subagent's one-line result (Patched / Created / No skill) to the user. Do not second-guess a "No skill" verdict — skipping is usually correct.
