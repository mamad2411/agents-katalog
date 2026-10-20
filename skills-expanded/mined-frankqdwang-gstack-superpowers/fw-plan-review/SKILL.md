---
name: fw-plan-review
description: "Use after fw-plan to run gstack plan-eng-review and conditional plan-design-review before build."
manifest_hash: sha256:f8601b037062d68df84a78fa341053fa326ad90c46b5ab3d8e93b790c69d8e12
generated_from: workflow.manifest.yaml
---

# fw-plan-review

Generated wrapper skill for the curated gstack + Superpowers workflow.

## Stage Contract

- Stage: plan-review
- Owner: codex-orchestrator
- Role: Gate
- Primary method: gstack
- Methods: gstack
- Contract: Run gstack plan-eng-review as the planning gate, use plan-design-review only for UI/UX-affecting plans, then stop before fw-build.

## Inputs

- Completed Superpowers spec, linked implementation plan, and relevant repo context.

## Outputs

- Plan review verdict, engineering risks, conditional design review notes, and explicit user confirmation or block before fw-build.

## Required References

- adapters/gstack/common-safety.md
  - Read: `../../references/adapters/gstack/common-safety.md`
- adapters/gstack/section-reference.md
  - Read: `../../references/adapters/gstack/section-reference.md`
- gstack/plan-eng-review/SKILL.md
  - Read active materialization: `../../references/upstreams/gstack/commits/c7ae63201ab193a7dc7fb7e0d81238645111ffac/plan-eng-review/SKILL.md`

## Conditional References

- gstack/plan-eng-review/sections/review-sections.md
  - Read active materialization: `../../references/upstreams/gstack/commits/c7ae63201ab193a7dc7fb7e0d81238645111ffac/plan-eng-review/sections/review-sections.md`
- gstack/plan-design-review/SKILL.md
  - Read active materialization: `../../references/upstreams/gstack/commits/c7ae63201ab193a7dc7fb7e0d81238645111ffac/plan-design-review/SKILL.md`
- gstack/plan-design-review/sections/review-sections.md
  - Read active materialization: `../../references/upstreams/gstack/commits/c7ae63201ab193a7dc7fb7e0d81238645111ffac/plan-design-review/sections/review-sections.md`

## Suppressed Routes

- None


## Policy Notes

- Common-safety applies to conditional gstack references before raw conditional material is read.
- Allowlisted gstack section files are reference-only and must be read only when the parent skill's section index applies to the active wrapper stage.
- fw-plan-review owns the gstack planning gate: run plan-eng-review, use plan-design-review only when UI/UX is affected, and stop for user confirmation before fw-build.

## Execution Rules

- Read this wrapper first, then read every required reference listed above before acting.
- Read conditional references only when the user request reaches that gate.
- Common-safety applies to conditional gstack references before raw conditional material is read.
- If an active upstream materialization is unavailable, report that the wrapper is blocked on upstream sync instead of guessing from installed skills.
- Treat installed skills as callable surfaces, not source-of-truth project documentation.
- Keep one execution owner for the current task.

## Workflow-Run JSON Output

Every run of this wrapper should be able to produce a machine-readable stage artifact with this shape:

```json
{
  "wrapper": "fw-plan-review",
  "stage": "plan-review",
  "owner": "codex-orchestrator",
  "primary_method": "gstack",
  "methods": [
    "gstack"
  ],
  "status": "success|needs-user|blocked|failed",
  "manifest_hash": "sha256:f8601b037062d68df84a78fa341053fa326ad90c46b5ab3d8e93b790c69d8e12",
  "inputs": [],
  "outputs": [],
  "references_read": [],
  "suppressed_routes": [],
  "policy_notes": [
    "Common-safety applies to conditional gstack references before raw conditional material is read.",
    "Allowlisted gstack section files are reference-only and must be read only when the parent skill's section index applies to the active wrapper stage.",
    "fw-plan-review owns the gstack planning gate: run plan-eng-review, use plan-design-review only when UI/UX is affected, and stop for user confirmation before fw-build."
  ],
  "verification": {
    "commands": [],
    "artifacts": []
  },
  "next_action": null
}
```
