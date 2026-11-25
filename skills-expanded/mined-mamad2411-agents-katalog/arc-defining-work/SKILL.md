---
name: arc-defining-work
description: Destination router for new work-item creation across GitHub Issues, Linear, or Agile Accelerator. Use when asked to create stories, build a backlog, define work from codebase analysis, or convert requirements into tracked work items and the destination tracker is not yet fixed. Do not use for implementation planning of existing work.
---
# Arc Defining Work

Route new-work requests to the right creation skill. The leading word is **destination-first**: ask where to create work before analysis or mutation, then delegate to the destination specialist. This skill creates work items itself only for Agile Accelerator.

## Steps

1. **Choose destination before analysis.**
   - Ask: GitHub Issues, Linear, or Agile Accelerator?
   - Do not infer the destination from repo context.
   - Wait for the user's answer before creating or deeply analyzing work items.

   Completion criterion: the run has one explicit destination, or it stops with the destination question.

2. **Detect source mode.**
   - Codebase analysis mode: user wants backlog/stories from observed gaps or next-phase improvements.
   - PRD breakdown mode: user wants requirements converted into vertical-slice work items.

   Completion criterion: the output states the selected mode and source material.

3. **Route to the destination specialist.**

   | Destination | Source | Continue with |
   |---|---|---|
   | GitHub Issues | PRD | `arc-prd-to-issues` (tracer-bullet slices + granularity quiz) |
   | GitHub Issues | codebase/ideas | `arc-creating-user-stories` |
   | Linear | any | `arc-linear-issue-creator` (for PRD sources, slice per `arc-prd-to-issues/SLICE_FORMAT.md` before bulk creation) |
   | Agile Accelerator | any | steps 4–5 below |

   All destinations share the story contract in `arc-creating-user-stories/STORY_FORMAT.md` (job story + verifiable checklist acceptance criteria + W-numbering).

   Completion criterion: for GitHub or Linear, the run hands off to the specialist skill with destination and source mode stated; for Agile Accelerator, it proceeds to step 4.

4. **Agile Accelerator: draft work items for approval.**
   - Follow `arc-creating-user-stories/STORY_FORMAT.md` for story bodies, metadata, and acceptance-criteria rules; for PRD sources, slice per `arc-prd-to-issues/SLICE_FORMAT.md`.
   - Do not create records before user approval unless the user explicitly asked to create without review.

   Completion criterion: every draft item is independently implementable or explicitly marked blocked/HITL.

5. **Agile Accelerator: create and verify records.**
   - Load [AGILE_ACCELERATOR_DESTINATION.md](AGILE_ACCELERATOR_DESTINATION.md) for `sf` commands.
   - Let Salesforce assign `Name` and query it after creation.
   - Report record IDs, assigned `W-` numbers, and any failed items.

   Completion criterion: every approved item exists in Agile Accelerator with its queried `W-` number reported, or exact tooling/permission blockers are reported.

## Boundaries

- Use `arc-planning-work` for implementation plans for existing work items.
- Go directly to `arc-creating-user-stories`, `arc-prd-to-issues`, or `arc-linear-issue-creator` when the user has already fixed the destination; this router adds value only while the destination is open.
- Use `arc-bug-finder` for defect intake; this skill defines feature/backlog work.
