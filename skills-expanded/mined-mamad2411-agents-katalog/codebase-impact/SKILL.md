---
name: codebase-impact
description: Use before multi-file, unfamiliar, public-contract, or shared-behavior code changes to build a bounded impact set without reading the whole repository or editing from a single file view.
---

# Codebase Impact Adapter

Use map -> slice -> expand -> impact set -> delta review.

## Map

Use fast search, file lists, project rules, symbols, routes, and related tests. Avoid full-repo reads and generated/vendor files.

## Slice

Read likely edit files, same-pattern implementations, related tests, and relevant config. Start small, usually 3-8 files.

## Expand

Expand only when contracts, callers, tests, security/data boundaries, or project rules require it.

## Output

- Files likely to edit
- Callers/consumers
- Tests/checks
- Config/docs
- Risks/unknowns
- Stop condition
