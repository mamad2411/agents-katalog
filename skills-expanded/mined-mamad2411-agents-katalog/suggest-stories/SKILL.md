---
name: suggest-stories
description: Suggest remaining candidate stories for one active epic by reading the epic plus existing stories and bugfixes, without creating files until the user accepts specific suggestions. Use after `validate-epic`, and any time while the epic is active, to plan or revisit the story set needed to fulfill an epic, find missing story coverage, or choose the next independently implementable value slices.
---

# Suggest Stories

## Core Rule

Suggest remaining candidate story boundaries for exactly one active epic by comparing the epic goals against existing stories and bugfixes; do not create or modify story files unless the user explicitly accepts one or more suggestions and asks you to proceed with `add-story`. This skill separates story coverage review from story artifact creation and can be rerun while the epic remains active. Follow [references/clarification-policy.md](references/clarification-policy.md).

## Workflow

1. Select exactly one active epic:
   - If the user provided a specific epic path or slug, use that as the candidate epic.
   - If the user did not provide a specific epic, run this skill's `scripts/list-active-epics.sh <target-repo-root>` to list active epics and validation decisions, then choose or ask for exactly one row from that output.
   - Do not read child stories, bugfixes, code, or broad Product Vision context for multiple epics. Stop and ask the user to choose when more than one epic is plausible and there is no clear single requested epic.
   - Confirm the selected epic is under `docs/epics/active/<epic>/epic.md`.

2. Load context from the selected epic:
   - Read only the selected `docs/epics/active/<epic>/epic.md`.
   - Read the source Product Vision when present.
   - Run this skill's `scripts/list-epic-child-work.sh <epic-slug-or-path> <target-repo-root>`, then read the existing `story_*.md` and `bugfix_*.md` files in the epic that are relevant to coverage, sequencing, gaps, or overlap.
   - Read relevant `docs/knowledge/` concern specs and inspect code, tests, or docs enough to understand current system boundaries.

3. Analyze epic fulfillment:
   - Map the epic's intent, in-scope items, Product Vision coverage role, risks, rollout, and validation gaps to existing stories and bugfixes.
   - Identify already-planned work, partial coverage, missing value slices, sequencing constraints, regression boundaries, and duplicated ownership.
   - Distinguish planned value slices from corrective defect work. Recommend `add-bugfix` for defects that need root cause and regression preservation.

4. Suggest candidates:
   - Propose the smallest useful remaining story set that can fulfill the epic's in-scope outcome.
   - For each candidate, include purpose, user or system value, in-scope and out-of-scope behavior, acceptance criteria themes, regression boundaries, dependencies, sequencing, verification approach, and overlap risk.
   - Keep each candidate independently implementable and validatable by `validate-change-plan`.
   - Do not force a complete story breakdown if the user asked only for the next story or a specific area.

5. Ask for acceptance:
   - Ask the user which candidate to create, revise, defer, or drop.
   - If accepted, use `add-story` for each accepted candidate, one story at a time.
   - If a candidate is actually a defect fix, recommend `add-bugfix` instead of creating a story.
   - If rejected or changed, revise suggestions before writing any artifact.

## Validation Checklist

- [ ] Exactly one active epic was analyzed.
- [ ] Exactly one active epic was selected before child work, code, or broad Product Vision context was loaded.
- [ ] Existing stories and bugfixes in the epic were checked for coverage and overlap.
- [ ] Suggestions are independently implementable planned value slices, not technical task buckets.
- [ ] Defect fixes are routed to `add-bugfix`.
- [ ] Each suggestion maps to specific epic scope, Product Vision items when present, and acceptance criteria themes.
- [ ] Gaps, overlap, dependencies, sequencing, regression boundaries, and open questions are explicit.
- [ ] No files were created or modified unless the user accepted a suggestion and requested creation.
