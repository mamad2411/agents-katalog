---
name: fix-bug
description: "Reproduce a defect, isolate root cause, add regression coverage and make the smallest responsible fix. Use when bug report, failing behavior, runtime defect."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "delivery"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Fix Bug

Reproduce a defect, isolate root cause, add regression coverage and make the smallest responsible fix.

## Activate when

- bug report
- failing behavior
- runtime defect

## Focus

- Primary mission: Reproduce a defect, isolate root cause, add regression coverage and make the smallest responsible fix.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Read project instructions, nearby implementation patterns, tests, and the intended behavior before changing code.
2. Establish a failing signal, acceptance check, or preservation baseline appropriate to the work.
3. Make the smallest coherent change that addresses the actual requirement or root cause.
4. Preserve public contracts and unrelated behavior unless change is explicitly in scope.
5. Add or update tests at the cheapest layer that reliably proves the changed behavior.
6. Run focused checks first, then the broader affected build/test/lint suite required by the repository.
7. Inspect the final diff for accidental scope, stale code, generated junk, configuration/docs drift, and unverified claims.

## Deliverables

- Minimal code/config change
- Appropriate regression or preservation tests
- Fresh verification evidence
- A result that directly satisfies: Reproduce a defect, isolate root cause, add regression coverage and make the smallest responsible fix.

## Common failure modes

- Fixing symptoms without understanding the failing mechanism
- Mixing unrelated cleanup into a targeted change
- Claiming tests passed from stale or partial output
- Hiding uncertainty instead of stating what was not inspected, reproduced, measured, or verified.

## Composition

Use `skill-router` when this task needs multiple specialties. Prefer composition over copying another skill's workflow into this one.

## Exit criteria

- The requested decision, change, test, or review is supported by concrete evidence.
- Important residual risks, limitations, and unknowns are explicit.
- The output is specific enough for another engineer or agent to act on without reconstructing hidden reasoning.
