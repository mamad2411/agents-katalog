---
name: benchmark
description: Performance baseline and regression workflow for Codex. Use when load time, resource size, or user-facing performance should be measured and compared over time.
---

# Benchmark

Use this skill when the repo needs a repeatable performance baseline or a before-and-after comparison.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Define the target page or flow to measure.
2. Capture the available performance signals:
   - load time
   - resource size
   - Core Web Vitals or equivalent
   - regressions relative to a prior run
3. Save a comparable report when the user wants trend tracking.

## Guardrails

- Be explicit about the measurement method and limitations.
- Compare like with like: same route, same environment, same scope.
- Do not overstate precision if the environment only supports rough measurements.
