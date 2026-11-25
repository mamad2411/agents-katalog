---
name: image-pipeline
description: Use when implementing or validating RAW decode and color/edit processing order, including non-destructive parameter application and visual regression checks.
---

# Image Pipeline

## Use This Skill When
- Changing RAW decode flow or edit operation order.
- Introducing new image adjustments or tuning defaults.
- Diagnosing color shifts, clipping, banding, or highlight recovery issues.

## Required Inputs
- Pipeline stage being changed.
- Expected visual behavior and tolerance.
- Test image set or sample corpus path.

## Workflow
1. Document exact processing order before changes.
2. Implement change in one stage at a time.
3. Validate with golden images or reference snapshots.
4. Confirm edits stay parameter-only (non-destructive).
5. Record known visual deltas and rationale.

## Guardrails
- Do not mutate source RAW files.
- Keep parameter mapping stable across preview and export.
- Reject mixed color-space assumptions across stages.

## Output Contract
- Pipeline code change and updated stage documentation.
- Regression comparison notes (pass/fail per test image).
