---
name: fw-ceo-review
description: "Use after office-hours confirms direction to run gstack CEO-level scope, ambition, and premise review before planning."
manifest_hash: sha256:f8601b037062d68df84a78fa341053fa326ad90c46b5ab3d8e93b790c69d8e12
generated_from: workflow.manifest.yaml
---

# fw-ceo-review

Generated wrapper skill for the curated gstack + Superpowers workflow.

## Stage Contract

- Stage: ceo-review
- Owner: codex-orchestrator
- Role: Core
- Primary method: gstack
- Methods: gstack
- Contract: Run gstack plan-ceo-review only, then stop for user confirmation before fw-plan. Do not write implementation specs or plans inside this wrapper.

## Inputs

- User-confirmed office-hours direction, scope notes, and unresolved premise risks.

## Outputs

- CEO-level scope challenge, ambition and premise notes, and explicit user confirmation or block before fw-plan.

## Required References

- adapters/gstack/common-safety.md
  - Read: `../../references/adapters/gstack/common-safety.md`
- adapters/gstack/section-reference.md
  - Read: `../../references/adapters/gstack/section-reference.md`
- gstack/plan-ceo-review/SKILL.md
  - Read active materialization: `../../references/upstreams/gstack/commits/c7ae63201ab193a7dc7fb7e0d81238645111ffac/plan-ceo-review/SKILL.md`

## Conditional References

- gstack/plan-ceo-review/sections/review-sections.md
  - Read active materialization: `../../references/upstreams/gstack/commits/c7ae63201ab193a7dc7fb7e0d81238645111ffac/plan-ceo-review/sections/review-sections.md`

## Suppressed Routes

- superpowers/brainstorming


## Policy Notes

- Common-safety applies to conditional gstack references before raw conditional material is read.
- Allowlisted gstack section files are reference-only and must be read only when the parent skill's section index applies to the active wrapper stage.
- fw-ceo-review must not write specs or plans; stop for user confirmation before fw-plan.

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
  "wrapper": "fw-ceo-review",
  "stage": "ceo-review",
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
  "suppressed_routes": [
    "superpowers/brainstorming"
  ],
  "policy_notes": [
    "Common-safety applies to conditional gstack references before raw conditional material is read.",
    "Allowlisted gstack section files are reference-only and must be read only when the parent skill's section index applies to the active wrapper stage.",
    "fw-ceo-review must not write specs or plans; stop for user confirmation before fw-plan."
  ],
  "verification": {
    "commands": [],
    "artifacts": []
  },
  "next_action": null
}
```
