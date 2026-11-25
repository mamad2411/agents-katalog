---
name: session-bootstrap
description: "Confirm the evolution layer is active at session start and report what was injected. Use at the start of any session where behavior may have recently changed, or when the user asks what guidance is active. Read-only — does not modify stable/."
---

# session-bootstrap

## When to use
- The user asks "what's loaded?" or "what rules apply?"
- A new session just started and you want to confirm the evolution contract landed.
- Troubleshooting why Claude is/isn't following a stable learning.

## What to do
1. Run: `bash ~/.claude/evolution/bin/evolve-status.sh`
2. Show the user:
   - kill-switch state
   - number of stable learnings in effect (grep `^- ` in `~/.claude/evolution/stable/global.md`)
   - any project-scoped stable file matching `basename $(pwd)`
   - last 3 session records
3. If the hook didn't fire (no recent `sessions.jsonl` record), flag it and suggest checking `settings.json` for the `SessionStart` hook.

## What NOT to do
- Do not read raw records (`corrections.jsonl`, `outcomes.jsonl`) and treat them as operating rules. Those are evidence, not stable guidance.
- Do not edit `stable/global.md` or any file under `~/.claude/evolution/stable/`. Changes go through `/evolution promote`.
- Do not bloat the output. The dashboard is terse on purpose.

## Inputs / outputs
- **Inputs:** none (reads `~/.claude/evolution/` state).
- **Outputs:** text dashboard to the user.
