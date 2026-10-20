---
description: Investigate a bug using the parallel-hypotheses pattern — 3–5 debuggers race to falsify competing root causes.
argument-hint: [bug description or failing test name]
allowed-tools: Read, Bash, Agent, TodoWrite
---

Investigate this bug with the parallel-hypotheses pattern.

Bug: $ARGUMENTS

## Your plan

1. Brainstorm **3–5 plausible root causes**, each a distinct, testable hypothesis.
2. Spawn one **debugger** sub-agent per hypothesis, in **parallel** (single message, multiple Agent calls). Each debugger:
   - Receives its specific hypothesis as the objective
   - Returns confirmed / refuted / inconclusive with evidence
3. Read all debugger reports.
   - If one confirms: hand off the exact proposed fix to the relevant build specialist (backend-dev / web-frontend-dev / etc.)
   - If all refute: run a second round with new hypotheses based on what the first round ruled out
4. After the fix lands, call **test-engineer** to add a regression test so the bug can't come back.
5. Call **progress-keeper** to log the incident in BUGS.md.

Do **not** debug the bug yourself. Your job is coordination.
