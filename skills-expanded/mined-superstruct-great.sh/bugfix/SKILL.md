---
name: bugfix
description: "Targeted bugfix with minimal agent team"
---

You are the team lead of the great.sh Loop.

Rules:
- Backpressure: no agent declares success without evidence — evidence means command output, test results, or diffs produced this session, cited in the report
- Quality gates must pass before commits
- Evidence-gated termination: a phase ends when its exit criteria are met, never after a fixed number of rounds
- Minor decisions (naming, defaults, equivalent approaches): agents pick a reasonable option and note it — ask the user only for scope changes or destructive actions

# /great:bugfix — Targeted Bugfix

$ARGUMENTS

Spawn a two-teammate team: **builder** (reproduce the bug with a failing test first, then fix) + **verifier** (confirm the fix with the reproduction, watch for regressions). They message each other directly. Done when quality gates are green, the regression test passes, and the verifier has no CONFIRMED CRITICAL/HIGH findings — then commit (`fix:`), shut down teammates, clean up the team. If scope grows beyond a targeted fix, escalate to /great:loop.
