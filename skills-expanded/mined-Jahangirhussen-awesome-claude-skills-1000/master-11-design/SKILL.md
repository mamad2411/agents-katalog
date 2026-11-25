---
name: master-11-design
description: 11-DESIGN domain of the master skills library (UI, UX, accessibility, design systems, graphics and branding). Use when the task needs interface, visual or brand design work and no more specific installed skill matches. Not when the task is backend logic.
---

# 11-DESIGN

## Purpose
Index for UI, UX, accessibility, design systems, graphics and branding: imported skills (read in place) and a pointer to the installed skills in this domain.

## When to use
The task needs interface, visual or brand design work.

## When NOT to use
- The task is backend logic.
- Another domain fits better (see `../ROUTER.md`).

## Inputs
The task, project context, and constraints; domain is inferred by the orchestrator.

## Core workflow
1. Check the imported skills below; if one fits, open its `SKILL.md` and follow it.
2. Otherwise open `INSTALLED.md` in this folder (installed skills per subdomain) and invoke the matching skill with the Skill tool.
3. For cross-domain needs follow `../DEPENDENCIES.md` instead of duplicating instructions.
4. Execute, verify, report.

## Decision rules
- Prefer the most specific skill; prefer installed canonical skills over imported generic ones.
- Open one skill at a time; do not read the whole folder.

## Edge cases and failure handling
- No fitting skill -> use general capability and say no adequate skill exists; do not invent one.
- Imported skill depends on an unavailable external service -> use the nearest installed alternative.

## Validation
Check the chosen skill's instructions match the task and that its output is verified with the matching testing/validation approach.

## Output requirements
The task result as a short `DONE`; no routing narration.

## Example
Request in this domain -> orchestrator selects the skill from the list below or `INSTALLED.md` -> follow its steps -> verify -> report.

## Imported skills (read the SKILL.md at the path when relevant)
- `graphic-design/image-enhancer/SKILL.md` - Improves the quality of images, especially screenshots, by enhancing resolution, sharpness, and clarity. Perfect for preparing images for pr
- `ui/artifacts-builder/SKILL.md` - Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS,

## Related skills
`../ROUTER.md`, `../DEPENDENCIES.md`, `../RULES.md`, `INSTALLED.md`.
