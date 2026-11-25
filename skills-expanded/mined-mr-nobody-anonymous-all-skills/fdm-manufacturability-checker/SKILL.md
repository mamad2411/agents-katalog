---
name: fdm-manufacturability-checker
description: Review FDM 3D printing manufacturability risks and design-for-additive-manufacturing assumptions.
source: "https://github.com/aa15107688191-collab/codex-mechanical-engineering-skills"
source_repository: "aa15107688191-collab/codex-mechanical-engineering-skills"
source_path: "skills/fdm-manufacturability-checker/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# FDM Manufacturability Checker

## Purpose

Review a proposed part, drawing, model description, or print plan for FDM manufacturability risks. The skill helps identify likely issues in wall thickness, orientation, supports, tolerances, thermal behavior, material choice, and post-processing.

All recommendations are advisory. A qualified engineer, printer operator, instructor, or responsible reviewer must confirm the final print plan.

## When to Use

Use this skill when the user wants to:

- Check whether a part is likely printable by FDM.
- Review PETG, PLA, ABS, ASA, nylon, TPU, or similar material assumptions.
- Compare orientations or support strategies.
- Prepare a design-for-FDM checklist before CAD revision.
- Review a course project or prototype for printability.

## Required Inputs

- Material and filament brand or grade if known.
- Printer type, nozzle diameter, layer height, and build volume.
- Slicer assumptions such as walls, infill, supports, and temperatures if available.
- Part purpose, approximate dimensions, and critical interfaces.
- Expected loads, cosmetic requirements, and tolerance needs.
- Screenshots, drawings, STL descriptions, or CAD notes if available.

## Workflow

1. Restate the part function and print assumptions.
2. Identify geometry risks: thin walls, unsupported overhangs, bridges, small holes, sharp corners, tall slender features, and trapped supports.
3. Review orientation against strength, accuracy, surface quality, and support removal.
4. Check material-specific risks such as PETG stringing, ABS warping, nylon moisture, or TPU flexibility.
5. Recommend design changes with clear tradeoffs.
6. Provide a pre-print checklist and a prototype-test plan.
7. Require final confirmation by the responsible engineer, instructor, or printer operator.

## Expected Outputs

- Manufacturability risk table.
- Orientation and support recommendations.
- Dimensional tolerance notes.
- Suggested CAD changes.
- Prototype print and inspection checklist.

## Acceptance Criteria

- Assumptions are stated clearly.
- Advice is tied to FDM process constraints.
- Critical unknowns are listed.
- The response avoids guaranteeing successful prints.
- The response reminds the user that final settings and design choices require qualified confirmation.

## Failure Handling

- If no geometry is provided, ask for dimensions or provide a generic checklist.
- If printer settings are unknown, use conservative assumptions and label them clearly.
- If a part appears safety-critical, recommend engineering analysis, inspection, and testing instead of relying on FDM advice alone.
- If tolerances are tight, recommend calibration coupons and measurement before final parts.

## Engineering Limitations

This skill cannot inspect a hidden mesh, verify slicer output, certify strength, or account for all machine-specific behavior. FDM parts are anisotropic and process-dependent. It cannot promise a perfect or successful print. A qualified engineer, instructor, printer operator, or responsible reviewer must approve the final plan.

## Example Invocations

- "Use `fdm-manufacturability-checker` to review this PETG universal joint model concept."
- "Check this bracket for FDM wall thickness, orientation, and support risks."
- "Create a pre-print checklist for a PLA gearbox housing prototype."
