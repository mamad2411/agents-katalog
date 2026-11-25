---
name: orc-bugfix
description: "Reproduce a reported defect, trace its root cause, fix affected callers and verify with a regression check."
---

# Debug a defect

Use the shared orc-worker-base lifecycle, including knowledge lookup before work
and orc-memory-review before any outcome.

1. Read the report and recent feedback. Identify expected behavior, actual behavior
   and the triggering input. Read related memories and search knowledge bases.
2. Reproduce with a focused test or the actual failing interface before editing.
   If reproduction is unavailable, record exactly what is missing and report the
   declared blocked outcome; do not claim a speculative fix is verified.
3. Trace the full affected path and callers. State the root cause with evidence,
   separating established facts from hypotheses.
4. Fix the cause at its owner with the smallest complete change. Preserve validation
   and error handling. Add a meaningful regression check that fails before and passes
   after the fix. Run the affected integration, lint and compile checks.
5. Deliver root cause, fix, regression evidence, risks and knowledge results using
   the shared summary, then report your node's outcome and stop.

Repeated failed fixes sharing one premise require revisiting that premise, not
another guard that suppresses the symptom. Preserve out-of-scope findings as
short memories or task notes without expanding the fix.
