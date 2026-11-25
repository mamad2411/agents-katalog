---
name: claude-review
description: Use the local Claude CLI as a second-opinion reviewer for briefs, plans, architecture, and code, then selectively incorporate its feedback. Use when the user invokes $claude-review or asks for an Opus or Claude review.
---

# Claude review

Use Claude to find material gaps in the work and assess possible improvements.
Give it the goal, motivation, constraints, relevant sources, and the question
its review should answer. Keep the review read-only. You remain responsible for
checking its findings and deciding which feedback improves the result.

Run Claude from the current project directory so it shares the project context.
If the task uses Ergo, direct it to `ergo --help` for the installed interface.
Default to `claude-opus-5`; use `claude-sonnet-5` when the user requests Sonnet.

```bash
claude -p \
  --model claude-opus-5 \
  --effort medium \
  --permission-mode auto \
  --tools Read,Glob,Grep,Bash \
  --no-session-persistence \
  --output-format json \
  "<review prompt>"
```

Use automatic permission mode to allow ordinary read-only discovery while
retaining permission checks. Keep that boundary when adding tools the review
needs; avoid `--allowedTools` and permission bypasses for a normal review.

Allow time for the review to finish: Opus at medium effort can take several
minutes. Poll at intervals no longer than 30 seconds and keep the user informed.
Use process state and errors to judge a stalled review; silence alone does not
justify interrupting it.

Assess feedback against the original goal and evidence before incorporating it.
Report material findings and remaining disagreements. Relay token, cache, or
cost metadata when Claude supplies it.
