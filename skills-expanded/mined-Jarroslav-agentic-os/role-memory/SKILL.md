---
name: role-memory
description: >-
  Per-role persistent memory for agents — durable curated facts, preferences, and decisions plus an
  append-only episodic daily log, stored as plain markdown under `.agents/memory/<role>/`. Invoke
  when the user says "remember this", says "log this", or asks "what did you learn yesterday" — and
  whenever you observe a fact, correction, preference, or decision worth carrying across sessions, or
  need to recall what you already know before acting. Uses Read/Write/Edit/Glob only: no CLI, no
  scripts, host-independent (Claude Code, Cursor, Gemini CLI, Windsurf, Copilot CLI, or an external
  supervisor).
  Not for: project or repo documentation (guides own that), task tracking, or storing secrets — plain-markdown per-role memory only.
license: Apache-2.0
version: 0.1.0
authors: agentic-os
---

# role-memory

Give the agent a memory that survives context resets. Each role owns a directory of plain markdown
you manipulate directly with your file tools. No wrapper binary, no shell-path dependence — the
layout is identical on every host.

> Two stores, two costs. The daily log is cheap and episodic: one appended line per observation, no
> promise of lasting value. A curated entry is durable — a fact expected to stay useful for roughly
> six months — and costs one index slot. Spend the expensive store deliberately.

## When to use

- User says **"remember this"**, **"log this"**, or asks **"what did you learn yesterday"**.
- You learn something durable — a preference, a validated correction, a project constraint, a pointer
  to an external system — that a future session would waste effort rediscovering.
- You are about to act and need to recall what this role already knows.

## Role identity

The role is the agent's own `name:` frontmatter value (e.g. `project-manager`, `python-dev`,
`scout`). Every fact below scopes to `<role>`; each role gets its own directory. Never read or write
another role's memory.

## Layout (fixed contract)

`.agents/memory/<role>/` contains:

| Path | What it is |
|------|------------|
| `MEMORY.md` | The curated index — one line per entry. |
| `<slug>.md` | One curated entry (durable fact/preference/decision/pointer). |
| `project_briefing.md` | The scout-seeded `project` entry (stack, conventions, role pitfalls). |
| `daily/YYYY-MM-DD.md` | One episodic log file per day. |
| `snapshot.md` | Supervisor-generated digest — **you never write this**. |

`.agents/` is chosen as an IDE-neutral root so the tree is the same across hosts. Create directories
lazily with `mkdir -p` on first use. You may add role-specific operational files to the directory
(for example a `personal-assistant`'s `people-pending.md`) as long as the core files above keep their
formats.

### Curated entry format

Exactly three frontmatter keys, no extras, one per line — the supervisor's snapshot regenerator
parses these:

```
---
name: <name>
description: <description>
type: <type>
---
```

Body below the frontmatter is free markdown.

### Index format

Header line, then one bullet per entry:

```
# Memory index — <role>
- [<name>](<slug>.md) — <description>
```

### Daily log format

Header line, then one bullet per observation:

```
# Daily log — <today>
- [HH:MM] <text>
```

## Curated types

Every curated entry carries a `type:` — exactly one of these four:

| type | Holds | Notes |
|------|-------|-------|
| `user` | The user's role, expertise, preferences, working style. | |
| `feedback` | Validated corrections. | Record the **why**, not just the rule. |
| `project` | Goals, deadlines, constraints, initiatives. | Fast-decaying; scout-seeded; re-verify before acting. |
| `reference` | Pointers to external systems (Linear projects, Slack channels, dashboards). | |

## Recall

Read only what you need — bounded recall keeps context small.

1. If the import line `@.agents/memory/<role>/snapshot.md` is present near the top of `AGENT.md`,
   memory is already in context. Use it; do **not** re-read the files.
2. Otherwise: read `MEMORY.md`, then the specific `<slug>.md` entries its lines point at, then — via
   `Glob` on `daily/` sorted by filename **descending** — only the **3 newest** daily files.

> Never read the full daily history. The three newest files plus the curated index are the whole
> working set.

## Write a curated entry

Use for anything durable.

1. **Slugify** the name: lowercase it, replace every run of non-alphanumeric characters with `_`, and
   trim leading/trailing underscores. `"User Timezone"` → `user_timezone`.
2. `Write` `<slug>.md` with the exact three-key frontmatter and the body.
3. Create or update the index line in `MEMORY.md`:
   `- [<name>](<slug>.md) — <description>`.

> **Index invariant:** exactly one line per slug. On rewrite, edit that line's description in place —
> never append a duplicate.

## Append to the daily log

Use for cheap, transient observations.

1. Determine `<today>`: read it from the environment context line if present, else run
   `date -u +%Y-%m-%d`.
2. If `daily/<today>.md` is absent, `Write` it with the header `# Daily log — <today>` then the first
   line. Otherwise `Edit`-append one line.
3. Line format: `- [HH:MM] <text>`, 24-hour clock, **one observation per line**. Anything that runs
   to a paragraph belongs in a curated entry instead.

> Daily-log lines are immutable. Corrections are new appended lines — the audit trail is preserved,
> never rewritten.

## Promote, rename, delete

- **Uncertain whether something is durable?** Append it to the daily log. Promotion (log → curated)
  is allowed later; **demotion is never** — a curated entry is not pushed back to log-only.
- **Rename** an entry: write the new `<slug>.md`, delete the old file, and edit its index line.
- **Delete** an entry: remove the file and drop its index line.

## Legacy migration

One-time only, and only when an old path exists **and** the new `<role>` directory does **not**:

| Old path | Action |
|----------|--------|
| `.claude/memory/<role>/` (dir) | `mv` into `.agents/memory/<role>/`. |
| `.octobots/memory/<role>/` (dir) | `mv` into `.agents/memory/<role>/`. |
| `.claude/memory/<role>.md` (flat file) | Read it, then `Write` it as a curated `project_briefing.md` with `type: project`. |

## Snapshot (read-only for you)

The supervisor's launch hook runs `supervisor/skills/memory/scripts/memory.py snapshot`, which merges
the index, every curated body, and the last 3 days of daily logs into `snapshot.md`, then wires the
`@.agents/memory/<role>/snapshot.md` import into `AGENT.md`. Absence is normal — on a stock host with
no supervisor the import silently no-ops and you fall back to on-demand recall. **Never generate or
edit `snapshot.md` yourself.**

## Content routing

| Destination | Content |
|-------------|---------|
| This memory | Agent-facing durable or working notes. |
| User knowledge base (e.g. an obsidian-vault), project docs, issue tracker, code | Anything other humans need. |

## Non-goals

- No CLI, scripts, or shell-path-dependent tooling — file tools only.
- You never author or edit `snapshot.md`.
- Not a home for human-facing documentation, tracker items, or code-level knowledge.
- No editing past daily-log lines; no demoting curated entries back to log-only.
- No unbounded daily-log reads.
