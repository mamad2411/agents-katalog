---
name: fw-ship-lite
description: "Use for branch finishing, release documentation, and release-readiness reporting without default deploy actions."
manifest_hash: sha256:f8601b037062d68df84a78fa341053fa326ad90c46b5ab3d8e93b790c69d8e12
generated_from: workflow.manifest.yaml
---

# fw-ship-lite

Generated wrapper skill for the curated gstack + Superpowers workflow.

## Stage Contract

- Stage: ship-lite
- Owner: codex-orchestrator
- Role: Conditional
- Primary method: mixed
- Methods: superpowers, gstack
- Contract: Report readiness only. Do not default to deploy, land, canary, merge, or release side effects.

## Inputs

- Reviewed branch, verification evidence, and release documentation context.

## Outputs

- Branch finishing status, release-readiness report, documentation notes, and explicit next gate.

## Required References

- adapters/superpowers/finish-readiness.md
  - Read: `../../references/adapters/superpowers/finish-readiness.md`
- superpowers/skills/finishing-a-development-branch/SKILL.md
  - Read active materialization: `../../references/upstreams/superpowers/commits/6fd4507659784c351abbd2bc264c7162cfd386dc/skills/finishing-a-development-branch/SKILL.md`
- adapters/gstack/common-safety.md
  - Read: `../../references/adapters/gstack/common-safety.md`
- gstack/document-release/SKILL.md
  - Read active materialization: `../../references/upstreams/gstack/commits/c7ae63201ab193a7dc7fb7e0d81238645111ffac/document-release/SKILL.md`
- adapters/gstack/ship-readiness.md
  - Read: `../../references/adapters/gstack/ship-readiness.md`

## Conditional References

- None

## Suppressed Routes

- gstack/ship/SKILL.md
- gstack/land-and-deploy/SKILL.md
- gstack/canary/SKILL.md


## Policy Notes

- Release, deploy, canary, merge, and push requests route to readiness reporting unless a separate explicit release gate is present.

## Execution Rules

- Read this wrapper first, then read every required reference listed above before acting.
- Read conditional references only when the user request reaches that gate.
- If an active upstream materialization is unavailable, report that the wrapper is blocked on upstream sync instead of guessing from installed skills.
- Treat installed skills as callable surfaces, not source-of-truth project documentation.
- Keep one execution owner for the current task.

## Workflow-Run JSON Output

Every run of this wrapper should be able to produce a machine-readable stage artifact with this shape:

```json
{
  "wrapper": "fw-ship-lite",
  "stage": "ship-lite",
  "owner": "codex-orchestrator",
  "primary_method": "mixed",
  "methods": [
    "superpowers",
    "gstack"
  ],
  "status": "success|needs-user|blocked|failed",
  "manifest_hash": "sha256:f8601b037062d68df84a78fa341053fa326ad90c46b5ab3d8e93b790c69d8e12",
  "inputs": [],
  "outputs": [],
  "references_read": [],
  "suppressed_routes": [
    "gstack/ship/SKILL.md",
    "gstack/land-and-deploy/SKILL.md",
    "gstack/canary/SKILL.md"
  ],
  "policy_notes": [
    "Release, deploy, canary, merge, and push requests route to readiness reporting unless a separate explicit release gate is present."
  ],
  "verification": {
    "commands": [],
    "artifacts": []
  },
  "next_action": null
}
```
