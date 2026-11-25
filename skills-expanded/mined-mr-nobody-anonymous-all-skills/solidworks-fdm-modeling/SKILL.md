---
name: solidworks-fdm-modeling
description: Plan and draft SolidWorks VBA/API automation for FDM-friendly mechanical part models.
source: "https://github.com/aa15107688191-collab/codex-mechanical-engineering-skills"
source_repository: "aa15107688191-collab/codex-mechanical-engineering-skills"
source_path: "skills/solidworks-fdm-modeling/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# SolidWorks FDM Modeling

## Purpose

Help users plan SolidWorks VBA/API automation and draft reviewable macro code for FDM-oriented mechanical models. The skill focuses on parameterized sketches, features, naming, units, and manufacturability-aware geometry.

Generated macros are drafts. A qualified engineer or responsible reviewer must confirm the geometry, requirements, dimensions, and safe use before production.

## When to Use

Use this skill when the user wants to:

- Create or revise a SolidWorks VBA macro for a mechanical part.
- Convert a concept into a parameterized SolidWorks modeling workflow.
- Add FDM-oriented geometry such as fillets, chamfers, ribs, bosses, reliefs, and print-friendly holes.
- Review a macro for unit, selection, rebuild, and feature-naming risks.

Do not use it to claim automatic generation of a perfect engineering model.

## Required Inputs

- Target SolidWorks version when known.
- Unit system and key dimensions.
- Part purpose and loading assumptions.
- FDM process assumptions such as material, nozzle size, layer height, orientation, and support policy.
- Required features, interfaces, fasteners, and keep-out zones.
- Any company, course, or drawing constraints that are allowed to share.

## Workflow

1. Restate the modeling goal and identify missing inputs.
2. Define parameters with units, names, safe defaults, and expected ranges.
3. Create a feature plan before drafting code.
4. Draft VBA/API code in small, reviewable sections.
5. Include rebuild checks, selection checks, and comments for manual verification.
6. Add FDM review notes for wall thickness, overhangs, layer direction, tolerances, and support access.
7. Tell the user to test the macro on a disposable file and inspect the final model manually.

## Expected Outputs

- A parameter table.
- A SolidWorks feature construction plan.
- Reviewable VBA/API macro draft or pseudocode.
- FDM design notes and risk list.
- Manual verification checklist.

## Acceptance Criteria

- Units and major parameters are explicit.
- The macro draft avoids hidden personal or proprietary file paths.
- Feature names and rebuild checkpoints are included.
- FDM constraints are stated as assumptions, not guarantees.
- The response reminds the user that a qualified engineer or responsible reviewer must confirm the model.

## Failure Handling

- If dimensions or constraints are missing, produce a safe parameter template and list open questions.
- If the requested feature depends on unavailable API behavior, provide a manual SolidWorks workflow alternative.
- If a macro may modify important files, require backup and disposable-file testing.
- If safety-critical use is implied, stop short of approval and recommend formal engineering review.

## Engineering Limitations

This skill cannot verify real loads, material properties, fatigue life, fit, regulatory compliance, printer calibration, or SolidWorks rebuild behavior in the user's environment. It cannot promise a perfect CAD model or production-ready part. Final confirmation must come from a qualified engineer, instructor, or responsible reviewer.

## Example Invocations

- "Use `solidworks-fdm-modeling` to draft a VBA macro for a PETG-FDM bracket with parameterized hole spacing."
- "Review this SolidWorks macro for FDM printability and rebuild risks."
- "Create a feature plan for a universal joint yoke model before writing the VBA."
