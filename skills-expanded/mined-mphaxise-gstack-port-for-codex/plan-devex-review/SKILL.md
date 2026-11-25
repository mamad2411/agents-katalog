---
name: plan-devex-review
description: Pre-implementation developer-experience review for Codex. Use when a plan is for APIs, CLIs, SDKs, docs, or developer-facing platforms.
---

# Plan DevEx Review

Use this skill when the product is for developers and the plan should be judged on onboarding, clarity, and time-to-value before implementation starts.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Read the plan and identify the target developer persona.
2. Trace the intended first-run journey:
   - discovery
   - install or setup
   - hello world
   - first real success
3. Stress-test the plan for:
   - time to first working result
   - documentation clarity
   - API or CLI ergonomics
   - failure handling and error messages
   - magical moment versus tedious setup
4. Rewrite the plan to reduce friction and expose the real adoption bottlenecks.

## Guardrails

- Do not confuse backend complexity with good developer experience.
- Prefer concrete journey steps over abstract DX slogans.
- Name the highest-friction step explicitly.

## Outputs

Always include:

- target developer persona
- expected hello-world path
- biggest friction points
- revised DevEx direction
- what to test after implementation
- next 1-3 actions
