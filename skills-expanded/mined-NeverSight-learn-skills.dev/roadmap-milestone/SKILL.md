---
skill_id: roadmap_milestone
name: roadmap-milestone
description: Refine one roadmap milestone's goal, planned changes, and derived status.
author: auto-spec-driven
type: agent_skill
version: 1.0.0
---

You are helping the user refine a single roadmap milestone.

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

1. **Choose the milestone** — determine whether the user wants to edit an
   existing milestone or create a new one under `.spec-driven/roadmap/milestones/`.

2. **Load milestone context** — read:
   - `.spec-driven/config.yaml`
   - `.spec-driven/roadmap/INDEX.md`
   - the target milestone file when it already exists
   - any nearby milestone files needed to preserve ordering or avoid overlap
   - active and archived changes that the milestone already references or might
     need to reference
   - whether the target milestone uses a legacy structure, such as an extra
     `## Candidate Ideas` section, a combined `## Dependencies / Risks`
     section, or missing `## In Scope`, `## Out of Scope`, or `## Notes`
     sections

3. **Refine only one milestone at a time** — help the user settle:
    - the milestone `Goal`
    - `In Scope`
    - `Out of Scope`
    - `Done Criteria`
    - `Planned Changes`
    - `Dependencies`
    - `Risks`
    - derived `Status`
    - `Notes`
    Use these standard section headings in the file:
     - `## Goal`
     - `## In Scope`
     - `## Out of Scope`
     - `## Done Criteria`
     - `## Planned Changes`
     - `## Dependencies`
     - `## Risks`
     - `## Status`
     - `## Notes`
     Milestone declared statuses are limited to:
     - `proposed`
     - `active`
     - `blocked`
     - `complete`
     Write each `Planned Changes` item with a canonical first line,
     `- \`<change-name>\` - Declared: <status> - <summary>`.
     Planned change declared statuses are limited to:
     - `planned`
     - `complete`
     Default new or unfinished planned changes to `Declared: planned`.
     Keep the full planned change description on that same line and do not add
     indented continuation lines below it. If the milestone needs richer local
     detail, move that context into another section such as `## Notes` rather
     than attaching multiline detail under `## Planned Changes`.
    If the milestone starts in a legacy format and the user wants a one-file
    migration instead of a whole-roadmap restructure, preserve clearly
    recoverable content, carry forward useful leftover context into `## Notes`
    when needed, and surface ambiguity instead of guessing silently.

4. **Write the milestone file** — create or update the milestone markdown file
   and keep it focused on that milestone only. If the file started in a legacy
   format, rewrite it into the canonical section set while preserving intent
   conservatively.

5. **Update roadmap index if needed** — if the milestone is new, add it to
   `.spec-driven/roadmap/INDEX.md` in the correct sequence.

6. **Enforce milestone status rules** — if listed planned changes are not all
   archived, the milestone is not complete. Do not add manual completion
   overrides.

7. **Validate roadmap size before finish** — run:
   ```
   node {{SKILL_DIR}}/scripts/spec-driven.js verify-roadmap
   ```
   If validation reports that the milestone is too large, stop and tell the user
   to split it instead of presenting the milestone as ready.

8. **Report the result** — summarize what changed in the milestone and identify
   any follow-up planning gaps that still need decisions before new planned
   changes are added.

## Rules

- This is a planning/documentation skill only — do not change product code
- Keep `Planned Changes` limited to concrete approved roadmap work
- Keep milestone scope bounded; do not turn this into a whole-roadmap rewrite
- Milestone completion is derived from archive state, not user preference
