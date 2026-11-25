---
name: fw-debug
description: "Use for bugs and unexpected behavior; use Superpowers root-cause debugging before conditional gstack investigation."
manifest_hash: sha256:f8601b037062d68df84a78fa341053fa326ad90c46b5ab3d8e93b790c69d8e12
generated_from: workflow.manifest.yaml
---

# fw-debug

Generated wrapper skill for the curated gstack + Superpowers workflow.

## Stage Contract

- Stage: debug
- Owner: codex-orchestrator
- Role: Conditional
- Primary method: superpowers
- Methods: superpowers, gstack
- Contract: Find root cause before fixing. Use gstack investigation only as conditional support.

## Inputs

- Bug report, failing test, unexpected behavior, or repro evidence.

## Outputs

- Root cause, fix, regression verification, and any conditional investigation findings.

## Required References

- superpowers/skills/systematic-debugging/SKILL.md
  - Read active materialization: `../../references/upstreams/superpowers/commits/6fd4507659784c351abbd2bc264c7162cfd386dc/skills/systematic-debugging/SKILL.md`
- adapters/gstack/common-safety.md
  - Read: `../../references/adapters/gstack/common-safety.md`
- gstack/investigate/SKILL.md
  - Read active materialization: `../../references/upstreams/gstack/commits/c7ae63201ab193a7dc7fb7e0d81238645111ffac/investigate/SKILL.md`

## Conditional References

- None

## Suppressed Routes

- None


## Policy Notes

- None

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
  "wrapper": "fw-debug",
  "stage": "debug",
  "owner": "codex-orchestrator",
  "primary_method": "superpowers",
  "methods": [
    "superpowers",
    "gstack"
  ],
  "status": "success|needs-user|blocked|failed",
  "manifest_hash": "sha256:f8601b037062d68df84a78fa341053fa326ad90c46b5ab3d8e93b790c69d8e12",
  "inputs": [],
  "outputs": [],
  "references_read": [],
  "suppressed_routes": [],
  "policy_notes": [],
  "verification": {
    "commands": [],
    "artifacts": []
  },
  "next_action": null
}
```
