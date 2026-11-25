---
name: quality-enhance
description: "Create reversible, quality-gated game asset or scene enhancements with preserved originals and before-and-after evidence."
---

# Quality Enhance

## Outcome

Improve a specific measurable weakness without silently changing style, behavior, rights, or performance budgets.

## Required inputs

- source asset or scene
- approved quality target
- locked properties, performance budget, and acceptable transformations

Ask for missing information only when it changes the route materially. Otherwise
state conservative assumptions and proceed with read-only analysis.

## Workflow

1. Diagnose concrete defects and define measurable acceptance criteria before proposing a transformation.
2. Copy originals to a recoverable location and inventory all dependent files and references.
3. Prepare a plan showing the exact enhancement route, tools, license implications, files, previews, and rollback.
4. Wait for explicit confirmation before running transformations.
5. Produce variants beside originals and create controlled before-and-after comparisons.
6. Validate format, visual fidelity, temporal behavior, runtime budget, playability, and project integration before requesting replacement approval.

## Expected artifacts

- defect diagnosis
- approved enhancement plan
- preserved originals
- candidate variants
- before-and-after evidence
- rollback record

## Workflow-specific gates

- Never overwrite or replace a source asset without a final human choice made after previewing evidence.
- Reject improvements that introduce identity drift, style drift, seams, artifacts, broken dependencies, or budget regressions.
- Keep the enhancement reproducible by recording tools, versions, settings, prompts, seeds, and manual edits.

## Production completion gate

Before recommending production use, complete and report all seven gates:

1. Rights, consent, code/model/dataset/output license, and generation-provenance checks.
2. Technical format, naming, scale, color, metadata, and target-import validation.
3. Visual and temporal consistency review across representative views and states.
4. Runtime memory, frame-time, draw-call, streaming, and asset-budget checks.
5. Playability and interaction smoke tests in the target runtime.
6. Screenshot, capture, diff, or artifact-regression evidence with reproducible settings.
7. Human approval before replacing source assets or promoting generated output.

Unknown rights, missing consent, unsupported hardware, conflicting host adapters,
or failed quality gates block production promotion. Preserve originals and make
fallbacks explicit.
