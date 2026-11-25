---
name: opt-debt
description: >-
  Scans the codebase for deliberate YAGNI shortcut markers (shortcut:, opt:)
  and compiles an actionable technical debt ledger with revisit triggers.
license: MIT
metadata:
  origin: AI Optimizer
  maintainer: Airshell (https://github.com/airshell)
---

# YAGNI Shortcut Ledger (`opt-debt`)

When developers and AI coding agents follow strict YAGNI principles, they write the minimum code required for the current task and defer speculative complexity. That trade is honest only when tracked. Every deliberate simplification carries a `shortcut:` comment naming its ceiling and the trigger to revisit. Older code may carry the previous `opt:` prefix — this skill harvests both into an actionable ledger.

## When to Use

- Before code review or major release milestones
- When asked to "list shortcuts", "show technical debt", or "what did we defer"
- To audit which temporary simplifications need scheduled follow-ups

## Marker Syntax

The standardized convention is `shortcut: <ceiling>, <trigger>`:

```python
# shortcut: in-memory aggregation ceiling 10k records, migrate to indexed SQLite
```

```javascript
// shortcut: synchronous fs read for single-user CLI, async stream if multi-tenant server introduced
```

## Scan

```bash
P='(#|//|--|/\*) ?(shortcut|opt):'
if git rev-parse --git-dir >/dev/null 2>&1; then git grep --untracked -nE "$P"
else grep -rnE "$P" . --exclude-dir={node_modules,.git,dist,build,vendor}; fi
```

## Output Format

One row per marker, grouped by file:

`<file>:<line> — <what was simplified>. ceiling: <the limit>. trigger: <when to revisit>.`

Tag any marker with no clear revisit condition as `no-trigger` — a ceiling without a revisit condition is the shape that rots.

End with:
`<N> markers, <M> with no trigger.`

Nothing found:
`No shortcut debt. Clean ledger.`

## Boundaries

- **Report only.** Do not refactor, fix, or remove markers — the user decides what to pay down.
- **Do not invent debt.** Generic `TODO`/`FIXME` comments are not `shortcut:` markers.
- **Data-first presentation.** Save judgements for one closing line, only if something is genuinely alarming.

