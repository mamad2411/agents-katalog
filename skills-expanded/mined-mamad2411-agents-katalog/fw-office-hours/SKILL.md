---
name: fw-office-hours
description: "Use for gstack office-hours idea intake, demand reality, product direction, and problem framing before CEO review."
manifest_hash: sha256:f8601b037062d68df84a78fa341053fa326ad90c46b5ab3d8e93b790c69d8e12
generated_from: workflow.manifest.yaml
---

# fw-office-hours

Generated wrapper skill for the curated gstack + Superpowers workflow.

## Stage Contract

- Stage: office-hours
- Owner: codex-orchestrator
- Role: Core
- Primary method: gstack
- Methods: gstack
- Contract: Run gstack office-hours only, then stop for user confirmation before fw-ceo-review. Do not run CEO review or planning inside this wrapper.

## Inputs

- Raw idea, product question, demand signal, or scope uncertainty.

## Outputs

- Office-hours notes, demand reality assessment, direction options, and explicit user confirmation or block before fw-ceo-review.

## Required References

- adapters/gstack/common-safety.md
  - Read: `../../references/adapters/gstack/common-safety.md`
- adapters/gstack/section-reference.md
  - Read: `../../references/adapters/gstack/section-reference.md`
- gstack/office-hours/SKILL.md
  - Read active materialization: `../../references/upstreams/gstack/commits/c7ae63201ab193a7dc7fb7e0d81238645111ffac/office-hours/SKILL.md`

## Conditional References

- gstack/office-hours/sections/design-and-handoff.md
  - Read active materialization: `../../references/upstreams/gstack/commits/c7ae63201ab193a7dc7fb7e0d81238645111ffac/office-hours/sections/design-and-handoff.md`

## Suppressed Routes

- superpowers/brainstorming


## Policy Notes

- Common-safety applies to conditional gstack references before raw conditional material is read.
- Allowlisted gstack section files are reference-only and must be read only when the parent skill's section index applies to the active wrapper stage.
- fw-office-hours must not automatically continue to plan-ceo-review; stop for user confirmation before fw-ceo-review.

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
  "wrapper": "fw-office-hours",
  "stage": "office-hours",
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
    "fw-office-hours must not automatically continue to plan-ceo-review; stop for user confirmation before fw-ceo-review."
  ],
  "verification": {
    "commands": [],
    "artifacts": []
  },
  "next_action": null
}
```
