---
name: prune-sync-assets
description: Use when decommissioning sync-managed assets that are no longer present in source manifests, with explicit approval and safe-delete controls.
---

# Prune Sync Assets

## Specialization

Decommission obsolete sync-managed assets that were previously imported but are now missing from the current source manifest.

This skill is intentionally narrow: removal planning and approval-gated decommission only.

## Self-Containment Requirement

- REQUIRED: Keep execution self-contained within this skill.
- REQUIRED: Do not reference or delegate to sibling skills.

## Trigger Conditions

Use this skill when:

- A sync plan reports `hold` items with reason `missing-in-source`.
- A team needs to retire previously managed artifacts no longer distributed by source.
- Manual cleanup must be traceable and approval-gated.

## Inputs

Required:
- `TargetRepoRoot`: Target repository root path.
- `PlanPath`: Path to a sync plan JSON containing per-artifact actions.
- `ApprovedRemovals`: Comma-separated `artifactId` values approved for decommission.
- `PruneReportPath`: Caller-specified output report path.

Optional:
- `WhatIf`: Preview proposed file deletions only.

## Required Outputs

1. Decommission execution report JSON with:
   - `planId`
   - `requestedAt`
   - `removedCount`
   - `skippedCount`
   - Per-artifact disposition (`removed`, `skipped-not-approved`, `skipped-missing-file`, `skipped-not-hold`)
2. Deterministic summary table (`artifactId`, `path`, `decision`, `reason`).
3. No out-of-scope mutation beyond approved removals.

## Safety Rules (Non-Negotiable)

- Never remove assets unless explicitly listed in `ApprovedRemovals`.
- Only remove artifacts with plan action `hold` and reason `missing-in-source`.
- Never remove local-owned assets (`source=local` or `ownershipMode=local`).
- Never remove non-compendium source assets (`source != sourceRepo`).
- Always emit a prune report even when no deletions occur.
- Support preview mode (`WhatIf`) before destructive execution.

## Workflow

1. Load and validate plan JSON.
2. Filter candidates to `hold` + `missing-in-source`.
3. Exclude protected items (`local`, `non-compendium-source`, missing path).
4. Intersect candidates with `ApprovedRemovals`.
5. In preview mode, report planned deletions without file mutation.
6. In execution mode, delete approved candidate files and record outcomes.
7. Write report JSON and render table summary.

## Companion Script

- [Invoke-PruneSyncAssets.ps1](./references/scripts/Invoke-PruneSyncAssets.ps1): Executes approval-gated decommission from a sync plan; supports `-WhatIf` preview.

## Execution Example

```powershell
./.github/skills/prune-sync-assets/references/scripts/Invoke-PruneSyncAssets.ps1 \
   -PlanPath .github/skills/prune-sync-assets/references/.prune/input-plan.json \
   -TargetRepoRoot . \
   -ApprovedRemovals artifact-a,artifact-b \
   -PruneReportPath .github/skills/prune-sync-assets/references/.prune/prune-report.json \
   -WhatIf
```

## Done Criteria

- Candidate set is deterministic from plan input.
- No unapproved deletions occur.
- Protected ownership modes are preserved.
- Report is written to caller-specified path.
- All outcomes are attributable to explicit approval.
