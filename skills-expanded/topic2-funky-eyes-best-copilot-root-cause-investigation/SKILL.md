---
name: root-cause-investigation
description: "Use when failure evidence already exists and the likely file set is narrow. Finds the root cause and guides the smallest safe fix."
---

# Root Cause Investigation

## Steps

1. List 2-3 ranked hypotheses with confidence and falsification signal.
2. Check the highest-confidence hypothesis first.
3. Stop expanding once evidence identifies the root cause.
4. State the fix logic before editing.
5. Verify the exact failure mode after the fix.

## Rules

- Do not patch symptoms without explaining the causal path.
- Use condition-based waits for async or concurrent behavior; avoid arbitrary sleeps where the repo has better primitives.
- If three hypotheses are falsified, stop and ask PM for new evidence.
