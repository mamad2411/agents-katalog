---
name: skill-optimizer
description: Improve a skill through benchmarked, validation-gated edits instead of ad hoc prompt polishing.
---

# Skill Optimizer

Use this skill when the user asks to optimize, tune, or improve an existing skill against examples or a benchmark.

This port is adapted from `garrytan/gbrain` at commit `814258dda67945ffec9457a1e73980e947b7e462`.

## Workflow

1. Pick the target skill and read its `SKILL.md`.
2. Establish an evaluation set before editing:
   - existing examples, tests, or benchmark JSONL
   - user-provided success criteria
   - at least a small held-out set for bundled skills
3. Make the smallest body-only change likely to improve behavior.
4. Preserve frontmatter routing fields unless the user explicitly asked to change routing.
5. Validate before accepting:
   - repo tests
   - relevant skill-specific checks
   - manual comparison against held-out tasks
6. Record what improved, what was rejected, and remaining risk.

## Codex Adaptation

- Prefer deterministic local tests and review tasks over upstream `gbrain skillopt` unless that CLI is installed and the user approved its cost/runtime.
- For bundled skills in this repo, default to proposed edits plus validation rather than automatic mutation loops.
- Do not call external model optimization services unless the user explicitly approves the cost and network use.

## Guardrails

- Do not optimize against a vague preference; write the benchmark first.
- Do not mutate frontmatter in a quality-tuning pass.
- Do not accept a change that only improves the training examples while regressing held-out tasks.
- Do not present an unvalidated rewrite as an optimization.
