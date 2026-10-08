---
description: Compute item statistics (P-value, D-index, Rit, distractor analysis) from a response CSV. Explicit shortcut into the test-builder analysis mode.
argument-hint: <responses.csv>
disable-model-invocation: true
---

Read `${CLAUDE_PLUGIN_ROOT}/skills/test-builder/SKILL.md` and follow its
analysis mode (Steps 8–10).

Response data: $ARGUMENTS
(a CSV path — rows = takers, columns = items, plus a `KEY` row with the
correct answers; or an already-scored 0/1/points matrix, then add --scored).

From the user's project directory, run:

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/test-builder/scripts/psychometrics.py" <csv> --out report.md
```

Then interpret the report against the guide's interval tables in
`${CLAUDE_PLUGIN_ROOT}/skills/test-builder/references/psychometrics.md`:
per-item verdicts (bank / revise / retire), dead distractors, negative
discrimination, keying anomalies, whole-test reliability, and whether the
test was too hard or too easy for this group. State the small-sample caveat
when n < 20.
