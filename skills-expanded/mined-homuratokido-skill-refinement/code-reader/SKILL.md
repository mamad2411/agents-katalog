---
name: code-reader
description: >
  Reusable method for reading code without changing it. Use when locating
  definitions, tracing references, checking source against docs, or compressing
  source facts into a report.
---

# Code Reader Skill

Use this when the work is source understanding, not source modification.

## Method

1. Restate the exact question and allowed scope.
2. Search before reading.
3. Read narrow slices; expand only when needed.
4. Separate fact from inference.
5. Return file paths, line anchors, and uncertainty.

## Avoid

- Bulk-reading without a routed question.
- Treating old docs as source truth.
- Making final architecture decisions.

## Output

```text
Question:
Scope searched:
Findings:
Evidence:
Uncertainty:
Suggested next check:
```
