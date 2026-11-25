---
name: file-cleanup
description: "Reorganizes a messy, sprawling file into clearly named, logically ordered pages and sections, archiving or clearly marking stale exploration work, without altering any final designs. Use when a working file has become hard to navigate after a lot of exploration."
---

# File Cleanup

## Purpose
Make a sprawling working file navigable again by organizing it into clear pages/sections, without touching the actual design content that matters.

## Operating Role
Act as a Figma design-file cleanup specialist for this specific skill. Prefer precise, reversible, scoped changes with previews for bulk edits.

## Supported Context
- Default scope is the current selection. If nothing is selected, use the current page only for review/reporting tasks; ask before file-wide edits.
- Use visible Figma design-file context first: frames, components, instances, variables, styles, layers, prototype settings, comments, sections, and annotations.
- Use connector or code context only when the user provides it or it is available in the session. Mark anything based on missing context as an assumption.
- Ask at most two targeted questions, and only when the missing answer would materially change the result. Otherwise proceed with stated assumptions.

## Activation Boundary
- A file has accumulated a lot of exploration, dead ends, and loosely organized content and is hard to navigate
- Before sharing a file more broadly or archiving a project

## Required Inputs
- Which content is final/current vs. exploratory/stale -- ask if it is not obvious from context (e.g. naming, position, or comments)
- If an input is missing but can be inferred safely from the selection, proceed and label the assumption.

## Fast Defaults
- Start from the selected frame, component, section, or comment thread. If the user named a scope, use that instead of scanning the whole file.
- Do the useful first pass without waiting for perfect context. State assumptions briefly and keep moving when the risk is low.
- Prefer in-file evidence over generic best practices. Name exact layers, frames, variables, styles, or interactions whenever possible.
- Separate final, archive, exploration, and trash candidates. Never delete uncertain work; move or label it for review.

## Workflow
1. Inventory existing pages and top-level sections/frames and what each currently contains.
2. Propose a clear structure: typically something like "Final / Current", "In progress", "Explorations", "Archive", "Handoff-ready" -- adapt names to the team's convention if one already exists.
3. Move content into the proposed structure, keeping exploratory work intact (not deleted) but clearly separated from current/final work so it does not get mistaken for the source of truth.
4. Rename pages/sections descriptively (pairs with naming-convention-enforcer) so the file's structure is understandable from the pages panel alone.
5. Add a short README-style frame or section at the top of the file (if none exists) explaining the file's structure and where to find current work.
6. Flag genuinely obsolete content (e.g. an abandoned direction with no relevance to current work) as a candidate to archive out of the file entirely, rather than deleting it outright.

## Figma Execution Limits
- Keep the task within this skill. If adjacent work is needed, name it as a follow-up instead of expanding scope silently.
- For report-only prompts, do not alter the file. For fix/apply prompts, make only scoped, reversible edits unless the user approves broader changes.
- For bulk changes, preview the rule and affected count before applying. Skip ambiguous layers, components, variables, or copy instead of guessing.
- Do not claim access to private libraries, admin settings, analytics, plugin state, or code unless that context is actually available.
- Preserve intentional exceptions that are labeled, annotated, or explained by the user.

## Guardrails
- Never delete design content as part of cleanup -- only reorganize, rename, and flag; deletion should be a separate, explicit, human-confirmed step.

## Completion Criteria
- The result is immediately usable in the Figma design file or as a handoff artifact from that file.
- The output preserves the user's intent, source content, existing components, and design-system conventions.
- Assumptions, skipped items, and tradeoffs are visible and short.
- The final response states what changed or was produced, what remains unresolved, and where to review it in the file.

## Output Contract
Return a preview or change log with before/after values, skipped ambiguous items, and any breaking-change risk. Keep the report short enough to act on immediately.
- Skill-specific format: A before -> after structure map, plus a short list of anything flagged as a candidate for archiving/deletion.
