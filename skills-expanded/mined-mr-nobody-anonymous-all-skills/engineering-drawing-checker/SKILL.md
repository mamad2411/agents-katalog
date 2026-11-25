---
name: engineering-drawing-checker
description: Check mechanical engineering drawings for completeness, consistency, and review risks.
source: "https://github.com/aa15107688191-collab/codex-mechanical-engineering-skills"
source_repository: "aa15107688191-collab/codex-mechanical-engineering-skills"
source_path: "skills/engineering-drawing-checker/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Engineering Drawing Checker

## Purpose

Review a mechanical drawing description, exported PDF, screenshot, or drawing checklist for completeness and consistency. The skill helps identify missing dimensions, unclear datums, inconsistent tolerances, title block issues, view problems, and manufacturing notes.

It provides review support only. A qualified engineer, instructor, inspector, or responsible reviewer must confirm the final drawing.

## When to Use

Use this skill when the user wants to:

- Check a part or assembly drawing before submission or fabrication.
- Review dimensions, tolerances, notes, views, and title block fields.
- Identify likely ambiguity for machinists, FDM operators, or inspectors.
- Prepare a drawing review checklist for a course project.

## Required Inputs

- Drawing file, screenshot, exported PDF, or text description.
- Drawing standard or course/company requirements if known.
- Unit system and scale.
- Part function and critical interfaces.
- Manufacturing process and inspection expectations.
- Revision status and title block requirements.

## Workflow

1. Identify drawing type: part, assembly, exploded view, detail, or process drawing.
2. Check title block, units, scale, projection, material, finish, and revision fields.
3. Check view coverage and whether geometry is fully described.
4. Review dimensions for completeness, duplication, baseline strategy, and tolerance clarity.
5. Review GD&T or datum usage when present.
6. Check manufacturing and inspection notes.
7. Produce a prioritized issue list and final review checklist.

## Expected Outputs

- Drawing issue table with severity.
- Missing information list.
- Suggested drawing corrections.
- Reviewer questions.
- Final approval checklist.

## Acceptance Criteria

- Issues are specific and actionable.
- The review distinguishes mandatory corrections from optional improvements.
- Unknown standards are treated as assumptions.
- The response does not certify the drawing.
- Final confirmation by a qualified engineer, instructor, inspector, or responsible reviewer is stated.

## Failure Handling

- If the drawing is not visible, request an export or provide a general checklist.
- If the standard is unknown, use standard-neutral drafting expectations and label assumptions.
- If GD&T is complex or safety-critical, recommend formal review by a qualified GD&T reviewer.
- If dimensions conflict, flag the conflict instead of inventing a correction.

## Engineering Limitations

This skill cannot certify compliance with ASME, ISO, GB, company standards, or instructor-specific grading rules. It cannot inspect hidden model geometry or guarantee manufacturability. A qualified engineer, instructor, inspector, or responsible reviewer must approve the final drawing.

## Example Invocations

- "Use `engineering-drawing-checker` to review this FDM part drawing before submission."
- "Check whether my universal joint assembly drawing has enough views and dimensions."
- "Create a drawing review checklist for a PETG printed bracket."
