---
name: update-libra
description: Syncs Libra-style docs (docs/decisions, docs/specs, docs/design, docs/plans) after meaningful conversations. Use when the user asks to sync docs, or at end of session when conversation produced decisions, constraints, scope changes, or progress worth recording.
---

# update-libra

Single-purpose workflow: keep `/docs` current. Run **in-stream** as part of the current conversation.

## Step 1 — Determine what changed

Review the conversation. Identify anything in these categories:
- Architectural or technical decisions (new or changed)
- Feature scope additions, removals, or pivots
- Constraints a coding agent must respect
- Open questions that are unresolved but relevant to upcoming work
- Plan progress (tasks completed, new tasks, phase changes)

Then check `git status`:
- If there are no meaningful changes outside `docs/`, `.cursor/`, and `.claude/`, respond briefly ("Nothing to sync") and stop.
- If there are meaningful changes, continue.

If nothing in the conversation falls into these categories, respond briefly ("Nothing to sync") and stop.

## Step 2 — Read before writing

For each doc you plan to update, read it first with your available file-read tool. Never write a doc without reading it — you will lose existing content.

Always read:
- `docs/decisions/INDEX.md` if you're adding or updating any decision
- The specific ADR file if you're superseding an existing one
- `docs/plans/INDEX.md` and active plan files if task status changed

## Step 3 — Write only what changed

Make surgical edits — do not rewrite unchanged sections. Build the full updated file content in memory, then present it to the user for review.

**For new ADRs:**
- New file at `docs/decisions/adr-NNN-[slug].md` — format: context → options considered → decision → rationale → consequences
- Update `docs/decisions/INDEX.md` with the new entry
- ADR numbers are sequential — check the index for the next number

**For plan updates:**
- Mark completed tasks `[x]`
- Add new tasks if scope changed
- Update phase status if it changed

**For new or updated product specs:**
- Create or update `docs/specs/[feature-name].md`
- Update `docs/specs/INDEX.md`

**For design docs:**
- Update `docs/design/[topic].md` when principles or design rationale changed
- Keep `docs/design/INDEX.md` in sync

**For plans index updates:**
- Keep `docs/plans/INDEX.md` as a short map of active/completed plans
- Do not let indexes become narrative docs

**Doc format:**
```
---
title: "..."
date: YYYY-MM-DD
status: ...
---
```

Conventions:
- Every doc file has frontmatter
- Cross-link with wiki links: `[[adr-005]]`, `[[spec:auth-flow]]`, `[[design:core-beliefs]]`
- Keep indexes named `INDEX.md` (caps)
- Keep docs under 300 lines
- High-signal, short, cross-linked

## Rules

- Read every doc before writing it
- Only modify files under `docs/`
- Do not create new doc paths without updating the relevant index file
- When done, summarize what was updated and why
