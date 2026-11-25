---
name: story
description: "Break a plan into executable Issues using vertical slices. Accepts an existing PRD or a direct feature description. Use when the user wants to convert a plan to Issues, create implementation tickets, or decompose work into subtasks. Trigger words: breakdown, story, 拆分, Issues, tasks, subtasks, decompose."
---

# Story: Break Plan Into Issues

🥷 Vertical slices, each issue is end-to-end.

Break plan into independently actionable issues using vertical slices (tracer bullets). Accepts an existing PRD or a direct feature description.

## Outcome Contract

- **Outcome**: Set of Issues, each executable independently, covering the full plan
- **Done when**: All issues created with dependencies mapped; PRD created or updated with child issues
- **Evidence**: Created Issues with proper acceptance criteria, PRD (created or updated) with child issue links
- **Output**: Issue count list, PRD created/updated, next step to `/implement` (for automated orchestration) or `/tdd` (for per-issue TDD)

## Prerequisites

- **Input**: an existing PRD at `docs/prd/PRD-NNNN-<title>.md`, or a direct feature description from the user
- Apply the [Skill Entry Protocol](../rules/entry-protocol.md) to locate domain docs and issue tracker config
- `docs/agents/issue-tracker.md` — read for issue creation convention
- `docs/agents/triage-labels.md` — read for label mapping
- Missing tracker config → the Entry Protocol's fallback applies; `/story` then either creates the missing config files for the tracker the user names, or suggests `/setup-project` for full interactive setup

## Process Summary

**Step 0**: Read project configuration — apply the [Skill Entry Protocol](../rules/entry-protocol.md); read `docs/agents/issue-tracker.md` and `triage-labels.md` for tracker convention and label mapping (see Prerequisites for fallback when missing)

**Step 1**: Determine input source — locate existing PRD, or capture feature description from user

**Step 2**: Extract requirements — from PRD or from user description + codebase exploration

**Step 3**: Ensure PRD exists — if not, create a minimal PRD capturing the requirements (run the PRD Conflict Check first; see think/REFERENCE.md)

**Step 4**: Explore codebase (optional) — understand current state, use domain glossary, respect ADRs

**Step 5**: Draft vertical slices — each is a thin vertical slice through all layers (schema, API, UI, tests)

**Step 6**: Present to user — show title, type (HITL/AFK), blocked-by, user stories; self-check granularity/dependencies first, then ask one approval question

**Step 7**: Publish issues in dependency order (blockers first). Issue title format: `[PRD-NNNN] <slice-description> — <core-behavior>`. Issue body includes a `Meta` section (PRD reference, Type, Siblings).

**Step 8**: Update PRD with child issues; set `Status` to `Sliced` in the PRD metadata line. Update the `## Traceability` `Sliced into` field with the child issues list (number, title, type, status).

**Step 9**: Sync Issue (if parent exists). Update the parent Issue body, append child issues list.

**Slice Types:**
- **HITL**: Human-in-the-loop — requires human judgment (architecture, design, UX). Agent pauses at decision points for input.
- **AFK**: Away-from-keyboard — implementable end-to-end without human interaction.

See [STORY-FORMAT.md](STORY-FORMAT.md) for the issue title/body template (single source) and [REFERENCE.md](REFERENCE.md) for input handling, slicing detail, and examples.

## Gotchas

| What happened | Rule |
|---|---|
| Horizontal slicing (all schema, then all API) | Use vertical slices through all layers |
| Slices too thick | Prefer many thin slices over few thick ones |
| Dependencies wrong | Publish in dependency order (blockers first) |
| PRD/parent issue not updated | Step 8/9: Update PRD and sync Issue |
| Input too vague for slicing | Suggest `/think` — do not run a full brainstorming session yourself |
| Forced a wide refactor (rename shared column, retype shared symbol) into tracer bullets | Vertical Slice Rules: slice it expand → migrate batches → contract; a slice that can't land green alone isn't a slice |
| Same topic got two PRDs (e.g. PRD-0001 + PRD-0002) | Step 3 (Ensure PRD Exists): run PRD Conflict Check (see think/REFERENCE.md §PRD Conflict Check) before creating |

## Vertical Slice Rules

- Each slice traces one narrow but **complete** path through every layer
- Completed slice is demonstrable or verifiable on its own
- Prefer many thin slices over few thick ones
- Avoid file paths or code snippets — they become stale

**Wide refactors are the exception.** A wide refactor is one mechanical change (rename a shared column, retype a shared symbol) whose blast radius spans the whole codebase — no vertical slice can land green on its own. Don't force it into tracer bullets; slice it as **expand → migrate → contract**: (1) one ticket adds the new form beside the old so nothing breaks; (2) migration tickets move call sites in batches sized by blast radius (per package/directory), each batch keeping the suite green because the old form still exists, each blocked by the expand; (3) one contract ticket deletes the old form, blocked by every migrate batch. See [REFERENCE.md](REFERENCE.md) for the sequence diagram.

## Output

```
Story complete.

Created issues:
* #<issue-1> — <title> (AFK)
* #<issue-2> — <title> (HITL, blocked by #1)

Updated files:
- docs/prd/PRD-NNNN-<title>.md — child issues updated (Status → Sliced)

Next: Run `/implement` to orchestrate implementation across all issues, or `/tdd` to implement a single issue.
```

## Example

```
PRD: User subscription (PRD-0003-subscription)

Proposed:
1. Create subscription data model (AFK) — schema + API + tests
2. Payment flow integration (AFK, blocked by #1) — gateway + webhooks + tests
3. Management UI (HITL, blocked by #2) — design review + components + E2E

User: granularity looks right, proceed → [Create 3 issues, Update PRD]
```
