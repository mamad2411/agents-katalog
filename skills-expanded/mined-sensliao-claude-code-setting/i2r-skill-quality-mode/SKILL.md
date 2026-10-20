---
name: i2r-skill-quality-mode
description: Meta-mode that keeps I2R itself testable and iterable via skill-TDD — observe naive failure, build evals pipeline, add pressure scenarios. Internal I2R authoring mode.
when_to_use: When authoring or modifying any i2r-* skill/agent/schema, or when running `i2r.py evals.run` to verify a skill behaves correctly before it enters a production agent.
user-invocable: false
---

# i2r-skill-quality-mode

## Purpose

This mode governs the quality loop for I2R **itself** — not the requirements it produces. It encodes skill-TDD: before trusting any i2r-* skill inside an agent, you must observe how a naive agent behaves without it, build evals that catch the failure, then verify the skill closes the gap. Sources: Anthropic skill-creator pattern; Superpowers writing-skills eval discipline.

**Vendor-not-install:** patterns are extracted from those sources and implemented as local i2r-* logic. No runtime calls to external skills.

---

## Core principle: skill-TDD

1. **Observe naive failure first.** Run the target task without the candidate skill. Record what goes wrong (implementation leak, vague NFR, etc.).
2. **Write a failing eval.** Add a pressure scenario under `evals/pressure-scenarios/` that reproduces the failure.
3. **Author/fix the skill.** Update the SKILL.md or its `references/`.
4. **Verify the eval passes.** Run `i2r.py evals.run` — all stages of the pipeline must turn green before the skill ships.
5. **Gate on description-trigger accuracy.** Run `evals/trigger-tests/` to confirm the skill fires on the right prompts and not on near-misses.

---

## Evals pipeline (`i2r.py evals.run`)

Six sequential stages — a stage gates the next:

```
bad-prompts
  → good-prompts
    → trigger-tests
      → schema-tests
        → downstream-GSD-readiness-tests
          → description-trigger-accuracy-tests
```

See `references/skill-evals.md` for what each stage checks and what a PASS looks like.

---

## Pressure scenarios

Each scenario lives at `evals/pressure-scenarios/<slug>.md` and must specify:
- **Input:** the raw idea or artifact handed to the agent
- **Expected failure (naive):** what a skill-less agent does wrong
- **Pass condition:** what the skill-armed agent must produce instead
- **Defect class(es) caught:** from CONTRACT.md §7 enum

Five seed scenarios are documented in `references/pressure-test-rules.md`.

---

## Description + trigger accuracy

Every i2r-* skill's `description` and `when_to_use` must pass a trigger-accuracy test: given 10 should-trigger prompts and 10 near-miss should-not-trigger prompts, the skill must be auto-invoked on ≥9/10 and not-invoked on ≥9/10. Rules and test format: `references/trigger-accuracy.md`.

---

## What this mode does NOT do

- Does not produce requirements (WHAT/WHY boundary holds).
- Does not modify `raw/` or any run artifact.
- Does not call external evals frameworks at runtime.
