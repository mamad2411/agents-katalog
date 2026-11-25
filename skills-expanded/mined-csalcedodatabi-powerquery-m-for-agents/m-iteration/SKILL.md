---
name: m-iteration
description: Use when a Power Query M task needs looping or state across rows — List.Generate, List.Accumulate, running totals, paginating a REST API until the last page, Table.Buffer or List.Buffer to stop repeated evaluation, GroupKind.Local for sorted groups, or deciding between these for performance. Triggers on "loop in Power Query", "List.Generate", "List.Accumulate", "pagination Power Query", "running total M", "Table.Buffer", "List.Buffer", "GroupKind.Local", "iterate API pages".
---

# M Iteration

> **Status.** Stub. Scope fixed in
> [the design spec](../../docs/superpowers/specs/2026-09-28-powerquery-m-for-agents-design.md)
> (§4).

## Planned contents

| File | Covers |
|---|---|
| `references/list-generate.md` | The four arguments, the off-by-one on the last page, returning records as state |
| `references/list-accumulate.md` | When it is fine and when it is quadratic |
| `references/buffering.md` | `Table.Buffer` / `List.Buffer`: what they fix, and that they stop folding |
| `references/pagination.md` | Next-link, offset and cursor pagination patterns |
| `references/group-local.md` | `Table.Group(..., GroupKind.Local)` on sorted data |

## Related skills

- **`m-reference`** — signatures.
- **`m-folding`** — buffering ends folding; know the trade.
