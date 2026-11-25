---
name: getting-started
description: Onboarding guide for the LinkLore MCP tools (brief, show, add, edit) — an AI-native memory of decisions, pitfalls, and docs for this codebase. Use this when starting a new session in a project that has LinkLore set up, when unsure which LinkLore tool to call, or when a user asks how LinkLore works.
---

# Getting started with LinkLore

LinkLore is a memory layer that AI agents read and write directly — not a passive
docs folder. It stores two kinds of items in a local `.linklore/` store (SQLite,
no account required):

- **lore** (`lr-` ids) — decisions, pitfalls, fixes, local rules. Has a
  `status` (`open`/`done`/`rule`).
- **doc** (`dc-` ids) — specs, system documentation, checklists/catalogs via
  `items`.

Both link bidirectionally (`link`) and can attach to files, so `show(file=...)`
surfaces the decisions and pitfalls relevant to the file you're about to edit.

LinkLore is free and local by default. An optional paid backend
(linklore.io) adds team sync, cross-project sharing, and cloud backup — this
skill and the bundled MCP server work fully offline without it.

## Core flow

1. **Start of session — call `brief`.** It returns open items, recent
   activity, and hotspots in a few hundred tokens. Do this before reading
   the codebase at large; it's the cheapest way to load context.
2. **Before changing code — call `show`.** Search by `file=`, `query=`,
   `tag=`, or `status=` to find decisions or pitfalls tied to the area
   you're about to touch. Reading this first avoids repeating a mistake
   someone (or a previous session) already made.
3. **While working — call `add` or `edit`.**
   - After a decision, bug fix, or pitfall: `add(type='lore',
     status='done')` to leave a regression guard for future sessions.
   - For a new system or feature: prefer `add(type='doc', ...)` over
     writing a standalone `.md` file — LinkLore docs get automatic
     bidirectional links and code context that plain markdown doesn't.
   - Connect related items at creation time with `links=['dc-x', 'lr-y']`
     rather than a separate linking call.
4. **If the project has no `.linklore/` yet — call `init`.** This creates
   the local store; it does not require login or the paid backend.

## When to use each tool

| Situation | Tool |
| --- | --- |
| Starting a session, want context fast | `brief` |
| About to edit a file, want related history | `show(file='path')` |
| Searching for a decision or doc by topic | `show(text=...)`, `show(tag=...)` |
| Just made a decision, fixed a bug, hit a pitfall | `add(type='lore', ...)` |
| Documenting a new feature or system | `add(type='doc', ...)` |
| Updating an existing item | `edit(...)` |
| First time in this project | `init` |

## Notes

- Humans are the governor: they describe what happened in words; the AI
  records it in LinkLore. Don't ask a human to hand-author lore/doc entries.
- Scope creep during a task ("that's separate, follow-up") should become
  `add(type='lore', status='open')` immediately — a commit message is not a
  backlog.
