---
name: debug
description: >-
  Systematic debugging of a reported problem: reproduce, gather evidence from
  logs, hypothesize, fix, verify. Trigger on "it is broken", "figure out why",
  "debug", a pasted stack trace, or a prod incident report.
---

# Debug

Evidence first, fix second. Never patch a symptom you haven't reproduced or
traced.

## Steps

1. **Reproduce or trace**: run the failing flow locally, or pull the real
   error from logs:
   - Fly apps: `fly logs -a <app>` (see fly-ops/fly-logs for filtering).
   - Local: dev server output, `.dev.log`, pytest output.
   - Browser: console + network tab via Playwright/devtools if it's frontend.
2. **Locate**: from the stack trace / log line, read the actual code path.
   Check recent commits touching it (`git log -p -- <file>`).
3. **Hypothesize** one cause, state what evidence would confirm/refute it,
   check that evidence. Repeat until confirmed. Don't shotgun fixes.
4. **Known local pitfalls** to rule out early: FEATURE_COLS drift between
   repos (shape-mismatch 500s), Docker --reload not picking up host edits,
   FastF1 data lag producing nonsense seed grids, port collisions
   (8001/8000/5180), predictor not loaded for race_laps.
5. **Fix + verify**: apply the minimal fix, re-run the failing flow, confirm
   the log/error is gone. Add a regression test if the project has a suite.
6. Report: root cause, fix, proof it works (actual output).
