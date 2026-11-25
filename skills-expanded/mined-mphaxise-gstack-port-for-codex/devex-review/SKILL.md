---
name: devex-review
description: Live developer-experience audit for Codex. Use when docs, setup, onboarding, CLI, API, or SDK workflows should be tested as a real user would experience them.
---

# DevEx Review

Use this skill when a developer-facing product or workflow should be tested end to end instead of only discussed abstractly.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Identify the target onboarding or usage path.
2. Follow the docs or expected setup steps as literally as possible.
3. Measure the real developer experience:
   - time to first working result
   - confusing steps
   - missing prerequisites
   - error quality
   - help text and recovery path
4. Record evidence and score the experience.
5. Fix the highest-value DX issues when the user wants changes; otherwise report them cleanly.

## Guardrails

- Test the workflow the way a new developer would, not the way an expert maintainer would.
- Prefer evidence and concrete repro steps over vague DX impressions.
- If setup is blocked by missing credentials or environment, say so explicitly.

## Outputs

Always include:

- path tested
- time-to-first-working-result estimate
- biggest DX blockers
- fixes made or recommended
- follow-up tests still needed
