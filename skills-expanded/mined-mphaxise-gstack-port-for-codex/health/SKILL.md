---
name: health
description: Codebase health-check workflow for Codex. Use when the repo should be scored or summarized across tests, linting, type checks, and structural quality signals.
---

# Health

Use this skill when the user wants to know how healthy the codebase is right now, not just whether one command passed.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Run the repo's real checks when available:
   - tests
   - linting
   - type checks
   - package or skill validation
2. Summarize the major quality signals:
   - broken or passing checks
   - stale docs
   - risky hotspots
   - missing verification
3. Report the biggest next improvements instead of a vague health label.

## Guardrails

- Do not invent a fake precision score if the repo has little instrumentation.
- Prefer meaningful signals over a noisy checklist.
- Reuse `testing` and `maintain` patterns when those already fit the repo.
