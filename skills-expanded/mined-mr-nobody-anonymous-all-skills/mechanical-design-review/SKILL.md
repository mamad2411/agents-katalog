---
name: mechanical-design-review
description: Review mechanical structures for function, load paths, manufacturability, assembly, safety, and verification planning.
source: "https://github.com/aa15107688191-collab/codex-mechanical-engineering-skills"
source_repository: "aa15107688191-collab/codex-mechanical-engineering-skills"
source_path: "skills/mechanical-design-review/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Mechanical Design Review

## Purpose

Provide a structured mechanical design review for parts, assemblies, mechanisms, prototypes, or course projects. The skill helps identify unclear requirements, weak load paths, stress concentrations, assembly risks, tolerance issues, maintainability problems, and missing tests.

It is advisory only. A qualified engineer, instructor, or responsible reviewer must confirm the final design.

## When to Use

Use this skill when the user wants to:

- Review a mechanical structure before CAD detailing or fabrication.
- Identify likely failure modes and design risks.
- Check assembly, fasteners, bearings, shafts, pins, clearances, and service access.
- Prepare a design review memo for a course or prototype.
- Compare alternative concepts using explicit criteria.

## Required Inputs

- Design objective and operating environment.
- Sketch, CAD description, drawing, or mechanism explanation.
- Materials and manufacturing process.
- Loads, motion, constraints, and duty cycle assumptions.
- Critical interfaces and assembly requirements.
- Applicable standards, course requirements, or safety constraints if known.

## Workflow

1. Restate the intended function and boundary conditions.
2. Identify load paths, constraints, and likely failure modes.
3. Review geometry for stress concentrations, stiffness, stability, wear, and clearance risks.
4. Review manufacturability, assembly sequence, inspection, and maintenance.
5. Rank issues by severity and uncertainty.
6. Recommend calculations, simulations, prototypes, or tests needed for confirmation.
7. State that final decisions require qualified engineering review.

## Expected Outputs

- Design review summary.
- Risk table with severity and recommended action.
- Open questions and missing data.
- Verification and test plan.
- Design improvement suggestions.

## Acceptance Criteria

- Recommendations are tied to stated assumptions.
- Safety-critical unknowns are escalated.
- The review includes manufacturability and assembly considerations.
- The response does not claim certification or guaranteed performance.
- Final confirmation by a qualified engineer, instructor, or responsible reviewer is stated.

## Failure Handling

- If loads are missing, provide a load-assumption template and avoid strength claims.
- If geometry is unclear, request sketches, dimensions, or screenshots.
- If a design may affect safety, recommend formal calculation, simulation, prototype testing, and responsible approval.
- If requirements conflict, identify the conflict and propose tradeoff options.

## Engineering Limitations

This skill cannot replace finite element validation, hand calculations by a responsible engineer, physical testing, standards compliance review, or inspection. It cannot guarantee safe or optimal designs. A qualified engineer, instructor, or responsible reviewer must confirm the final design before fabrication or use.

## Example Invocations

- "Use `mechanical-design-review` to review a PETG-FDM universal joint demonstration model."
- "Review this clamp design for load path, assembly, and FDM risks."
- "Create a design review checklist for a student mechanical mechanism project."
