---
skill_id: roadmap_plan
name: roadmap-plan
description: Create or restructure a persistent milestone-based roadmap under .spec-driven/roadmap/.
author: auto-spec-driven
type: agent_skill
version: 1.0.0
---

You are helping the user create or restructure the repository roadmap.

## Prerequisites

The `.spec-driven/` directory must exist at the **project root**. Before
proceeding, verify:
```
ls .spec-driven/
```
If this fails, the project is not initialized. Run `/spec-driven-init` first.

If `.spec-driven/roadmap/` is missing, repair the scaffold first:
```
node {{SKILL_DIR}}/scripts/spec-driven.js init
```

## Steps

1. **Read roadmap context first** — before proposing milestone structure, read:
   - `.spec-driven/config.yaml`
   - `.spec-driven/roadmap/INDEX.md` if it exists
   - every existing file under `.spec-driven/roadmap/milestones/`
   - `.spec-driven/specs/INDEX.md` and any main spec files that are clearly
     relevant to the user's planning scope
   - active and archived changes under `.spec-driven/changes/` as evidence of
     what is already in progress or complete

2. **Understand the planning goal** — determine:
   - whether the user wants to create a brand-new roadmap or restructure an
     existing one
   - what major phases or stage goals the roadmap should express
   - whether there are existing changes that already belong to specific
     milestones

3. **Converge on milestone boundaries before writing** — help the user settle:
   - milestone names and ordering
   - each milestone's goal and done criteria
   - which concrete `Planned Changes` belong in each milestone
   - key dependencies, risks, and sequencing

4. **Confirm the roadmap shape** — before editing files, summarize the intended
   milestone structure and ask for explicit confirmation.

5. **Write roadmap assets** — update:
   - `.spec-driven/roadmap/INDEX.md`
   - `.spec-driven/roadmap/milestones/<milestone>.md` for each milestone in scope

6. **Preserve roadmap rules** — in every milestone file:
   - use these standard section headings:
     - `## Goal`
     - `## Done Criteria`
     - `## Planned Changes`
     - `## Dependencies / Risks`
     - `## Status`
   - treat `Planned Changes` as the milestone's only work list and keep it
     limited to concrete approved change work
   - derive milestone completion from archived planned changes rather than
     manual toggles

7. **Validate roadmap size before finish** — run:
   ```
   node {{SKILL_DIR}}/scripts/spec-driven.js verify-roadmap
   ```
   - If validation reports a milestone is too large, stop and tell the user to
     split it into smaller milestones
   - Do not present the roadmap as ready while size validation fails

8. **Summarize the result** — report the milestone structure created or changed,
   what planned work was assigned to each milestone, and any remaining planning
   gaps.

## Rules

- This is a planning/documentation skill only — do not change product code
- Read roadmap files and relevant change history before restructuring anything
- Do not collapse multiple milestones into one oversized roadmap document
- Do not mark a milestone complete manually if its planned changes are not all
  archived
