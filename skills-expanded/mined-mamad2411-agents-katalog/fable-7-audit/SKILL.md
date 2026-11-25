---
name: fable-7-audit
description: >-
  Fable7 framework audit for over-engineering. Scoped to tools/ and fable/ only.
  Forbidden on campaigns/. Fork of ponytail-audit for Fable framework evolution.
version: 7.0.0
allowed-tools: [Read, Grep, Glob, Bash]
---

# Fable 7 Audit

Repo-wide over-engineering audit **scoped to framework paths only**:

- `tools/` (not `tools/reconnaissance/` shims unless noting deletion)
- `fable/`, `bin/`, `Workflow/`, `hooks/`, `docs/`

**FORBIDDEN:** `campaigns/` — operator data.

## Tags

`delete:` `stdlib:` `native:` `yagni:` `shrink:` `duplicate:`

## Output

One line per finding, ranked biggest cut first. End with `net: -N lines possible.`

Prioritize: duplicate utilities (reconnaissance shims), root-level copies, stale v5/v6 refs.

Lean already on framework → `Lean already. Ship.`
