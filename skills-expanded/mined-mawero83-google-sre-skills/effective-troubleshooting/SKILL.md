---
name: effective-troubleshooting
description: >-
  Run structured troubleshooting: problem statement, hypothesis tree, divide-and-conquer, and evidence logging per Google SRE. Use during incidents or deep production debugging.
---

# Effective Troubleshooting

**Domain:** `operations`  
**Sources:** SRE Book 1e Ch12

## When to use

- Active incident investigation
- Mysterious production behavior
- Coaching juniors on debug method

## Principles

- Start with a clear problem statement (what, since when, impact, scope).
- Form falsifiable hypotheses; test the cheapest discriminating checks first.
- Change one variable at a time when experimenting.
- Write down what you tried — future you (and AI helpers) need the trail.

## Workflow

1. Write problem statement in incident doc.
2. Establish blast radius and timeline of changes.
3. Build hypothesis list ordered by likelihood × ease of test.
4. Gather telemetry (golden signals, traces, logs) against hypotheses.
5. Mitigate user impact in parallel when possible.
6. Capture learnings for postmortem even if 'just a blip'.

## Decision guide

- If recent change correlates → roll forward/back consideration early.
- If data contradicts pet theory → kill the theory.

## Output template

```markdown
# Troubleshooting log
- Problem statement:
- Impact / scope:
- Recent changes:
- Hypotheses + tests + results:
- Current best theory:
- Next action:
```

## Anti-patterns

- Random restarting without hypothesis.
- Tunnel vision on one layer.

## Related skills

`incident-management`, `monitoring-observability`, `ai-supports-sre`

## Canonical references

- [Effective Troubleshooting](https://sre.google/sre-book/effective-troubleshooting/)

## Agent notes

- Prefer live data (metrics, tickets, pages) over generic advice.
- Cite which Google SRE source informed a recommendation when useful.
- Keep outputs tactical: decisions, owners, next actions.
