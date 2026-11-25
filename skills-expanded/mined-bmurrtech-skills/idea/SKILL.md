---
name: idea
description: >
  Idea scratch: capture exploratory thoughts under .scratch/ideas/ without
  promoting or publishing. Use when the user says capture this, save this idea,
  brain dump, something to explore later, maybe we should, what if, future idea,
  or don't work on this now — and when intent is ambiguous between thought and
  roadmap.
---

# idea

**Preserve first. Structure later.** Capture brain dumps under
`.scratch/ideas/` so coding sessions can shed thoughts without ceremony.

Promotion to `docs/ROADMAP.md` is **`roadmap`**. External trackers are
**`roadmap`** publish — never this skill.

## Boundaries

- Do **not** modify `docs/ROADMAP.md`.
- Do **not** create GitHub issues, Fizzy cards, PRDs, or handoffs.
- Do **not** implement the idea.
- Do **not** invent Domain / Scope / Boundaries / Constraints the user did not
  imply.
- Do **not** delete or overwrite an existing scratch file without an explicit
  append/replace ask — default is create a new file or append a dated section.

## Workflow

### 1. Confirm capture (not promote)

If the user clearly asked to put the idea on the roadmap / promote / publish,
stop and run **`roadmap`** instead.

If ambiguous → capture here (local safety valve).

**Done when:** branch is capture-only.

### 2. Write scratch file

Ensure `.scratch/ideas/` exists. Choose a kebab-case slug from the working
title (`intelligent-debug-recall.md`). Prefer a new file; if a same-slug file
exists and the user is continuing the same thought, append a `## Capture
{yyyy-MM-dd}` section.

Shape: [references/scratch-template.md](references/scratch-template.md) —
same field spine as the public roadmap, plus internal `Context` / `References` /
`Dev notes`. Prefer raw **Idea** first; fill structured sections only when
obvious. Do not questionnaire the user.

**Done when:** file exists under `.scratch/ideas/`; path reported to the user.

### 3. Stop

Tell the user the absolute path. Mention that promotion requires an explicit
**`roadmap`** invoke.

**Done when:** user has the path; no further artifacts created.
