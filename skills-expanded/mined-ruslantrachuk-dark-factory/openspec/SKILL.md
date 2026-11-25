---
name: openspec
description: >
  Use when writing or editing a change under openspec/changes/<slug>/ — the proposal (with
  WHEN/THEN acceptance scenarios), the design of a large change, or tasks.md — or when you need
  the folder layout and the format of these files.
user-invocable: true
---

# OpenSpec — the format used here

> Canonical template (templates/base). Needs no configuration. How a project applies it (surfaces,
> scope fallback, SHIPPED.md) — its `openspec/README.md`. Whether a piece of work needs a spec at
> all, and how big — the `size-task` skill. Turning an approved spec into queue tasks — `openspec-to-beads`.

Agree on what to build before writing code. A change is a folder of plain Markdown files, edited by
hand; there is no CLI, no living spec and no archive. Changes stay in `openspec/changes/` as the
record of why something was done; git log says when.

## Layout

```
openspec/changes/<slug>/
├── proposal.md   # always (small and large)
├── design.md     # large changes only
└── tasks.md      # always
```

- `<slug>` is lowercase words with hyphens and is unique: it is taken if the folder exists. It is the
  branch slug and the bd epic's label `change:<slug>`.
- The tracker ID, when there is one, goes in the proposal header, not in the folder name.

## proposal.md

```markdown
# <Title>

Tracker: DMP-123            <!-- or "none" -->
Type: feat                  <!-- feat | fix | ui | refactor | chore | docs -->

## Problem
What is wrong or missing now, and for whom.

## Scope
- In: …
- Not in: …   (deferrals matter as much as the scope)

## Acceptance scenarios
- **WHEN** a user sends a voice message **THEN** the bot replies with its transcript
- **WHEN** the audio is longer than 60 s **THEN** the bot asks for a shorter one

## Interaction surfaces
(user-visible features — the table from `openspec/README.md` §0)

## Decisions
Made, not to be revisited.

## Risks
Each with a fallback: what to drop or do if it does not work out.
```

Acceptance scenarios are observable facts in WHEN/THEN form, one per behaviour; each becomes at least one
test at the entry point.

## design.md (large changes)

Only the **delta** against the code as it is: decisions and trade-offs, the mapping to the project's
layers, and the **transition tree** — every entry, every state and where each action leads, including
"back", cancel and errors, with no dead ends. Needed when the data model, an API contract or a user flow
changes.

## tasks.md

Phases, each sliced **end to end**: after its commit the phase works from the entry point to the
result and has an entry-level test. Never split by layers.

```markdown
## Phase 1 — <what the user can do after it>
- [ ] RED: test <entry-level test name>
- [ ] GREEN: <the smallest implementation>
- [ ] REFACTOR, commit
```

Each phase is its own branch and PR: a separate tracker card with its own ID (preferred), or the
slug with a `-p<K>` suffix when there is no tracker.

## Common mistakes

- Code before `tasks.md` exists for a small or large change.
- Acceptance written as "everything works" instead of WHEN/THEN facts.
- Phases cut by layer ("data", then "API", then "UI") — the feature stays unwired between them.
- A slug that is already taken, or one that reuses an old folder's name.
