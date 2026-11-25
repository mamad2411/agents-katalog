---
name: write-description
version: 1.1.0
description: Use when opening or updating a pull request, writing or fixing a PR description or body, running `gh pr create` or `gh pr edit`, when asked to "write the PR description", or when an existing PR body is stale, a wall of text, or narrates the diff file-by-file.
---

# Writing PR Descriptions

## The one rule

A PR description carries **only what the diff cannot show**: the *why*, the *shape* of the change,
and *what to look at first*. The reviewer reads the code for the *how*. Every sentence that restates
the implementation is noise; cut it.

Write for a reviewer scanning in fifteen seconds. Short is the target, not a constraint. Size to the
number of distinct ideas, not the file count: a 50-file rename is one idea and earns a tiny
description.

## Pre-flight (before writing a word)

Read the change: `git diff <base>...HEAD` and `git log <base>..HEAD`. Every path, name, and count in
the description must match what you just read. That is what keeps it from going stale.

## The shape

Lead with a **visual when the change has one**, then the four sections. Most are one line.

### Visual first (when it applies)

- The change is a **mapping, rename, enumeration, or set of values** -> show a **table**.
- The change is a **flow, topology, lifecycle, or state machine of 3+ parts** -> show a **diagram**
  (`mermaid`; an inline `A -> B -> C` for a plain 3-box chain).
- Neither -> skip this; no decorative diagram.

Draw the data once, here. The sections below must not re-narrate what the visual already shows.

### 1. TL;DR

One sentence: `<what changed at the system level> so that <why it matters>`. The why is required. The
PR title is the conventional-commit summary; the TL;DR is the sentence version, not a copy of it.

### 2. Goal

One line, first match wins: (a) link the tracker ticket; (b) else name the task and link its
plan/spec doc; (c) else one plain sentence. If the TL;DR already carries the why and there is no
ticket or doc, fold Goal into the TL;DR rather than pad an empty line.

### 3. What changed

Three to five bullets, **one line each**. Each bullet is a **decision, capability, or consequence the
reviewer cannot read off the diff**, not the mechanism.

- A bullet that names types, fields, or call chains is restating the code. Rewrite it as the decision
  behind them.
- When a visual already carries the change, the bullets cover only what it cannot: the why, the
  migration, the blast radius.

> BAD (restates the diff): *Tier now carries a `TierId` and `rank`; the names live in `TIER_CONTENT`
> and resolve by id via `tierLabel`.*
> GOOD (the decision): *Tier names are now content, resolved by id, off the domain type like every
> other label.*

### 4. Verify

What you ran (test count and checks) and the one repro path a reviewer follows. One or two lines.

## Conditional sections: default to omitting

Add one **only** when its trigger fires, and keep it to a line. When unsure, leave it out. Describe
what the change *is*; do not catalogue what it is not.

- **Key decisions** - only when a reviewer would expect a different choice: `<choice> because
  <constraint>`. A choice already obvious from the TL;DR is not one.
- **Out of scope** - only when a missing piece would otherwise read as a bug. Not a dumping ground for
  everything you did not do.
- **Docs** - only to link a canonical doc the PR should not duplicate: a link plus a short gloss.

## Final scrub

Strip the AI tells, **keep the structure**. Remove em/en dashes (`—`, `–`), any bot sign-off, AI
vocabulary, and filler; keep a neutral voice. Tables, bold lead-ins, code, and identifiers stay; they
are the format, not noise. Run `writing:humanize` for the prose pass and require it to preserve the shape
above.

## Handoff

Print the draft. Publishing is outward-facing, so apply only after the owner approves.

- New PR: `gh pr create --base <main> --title "<conventional-commit summary>" --body-file <path>`
- Edit a PR: `gh pr edit <N> --body-file <path>`. If it fails on the Projects deprecation, use
  `gh api --method PATCH "repos/{owner}/{repo}/pulls/<N>" -f body=@<path>`.

## Example

Renames the five difficulty tiers from metals to an ability scale and moves their display names out of
the domain core, so the core stores only a stable id and rank.

| rank | id | en | pt-BR | was |
|---|---|---|---|---|
| 1 | `novice` | Novice | Novato | Silver |
| 2 | `intermediate` | Intermediate | Intermediário | Gold |
| 3 | `advanced` | Advanced | Avançado | Platinum |
| 4 | `expert` | Expert | Especialista | Diamond |
| 5 | `master` | Master | Mestre | Master |

**Why:** tier names are content, not domain, the same rule as exercise and ladder labels
(`spec/glossary.md`).

**What changed**
- Tier names moved to the content layer, resolved by id; the `core` type keeps only id and rank.
- Stored events migrate on read (schema v1->v2 upcaster), so existing logs stay valid.
- Catalog data, the reference docs, and the rank-ramp tokens follow the new scale.

**Verify:** `pnpm typecheck && pnpm test`: 115 pass, including the upcaster and label tests.
