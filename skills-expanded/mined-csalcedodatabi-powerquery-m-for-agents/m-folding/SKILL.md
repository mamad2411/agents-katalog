---
name: m-folding
description: Use when a Power Query M step may or may not fold to the data source — deciding whether a transformation is pushed down as native SQL or evaluated locally, finding which step breaks folding, reading the step folding indicators or View Native Query, using Value.NativeQuery with EnableFolding, or designing a query so it stays foldable for incremental refresh. Triggers on "query folding", "does this fold", "breaks folding", "native query", "Value.NativeQuery", "EnableFolding", "refresh is slow Power Query", "folding indicator", "incremental refresh requires folding".
---

# M Folding

> **Status.** Stub. Scope and structure are fixed in
> [the design spec](../../docs/superpowers/specs/2026-09-28-powerquery-m-for-agents-design.md)
> (§4); content lands in phase 4, each claim backed by a lab query.

## Planned contents

| File | Covers |
|---|---|
| `references/how-folding-works.md` | What the engine pushes down, and when evaluation turns local |
| `references/breakers.md` | Steps that commonly stop folding, per connector family (SQL, OData, SharePoint, files) |
| `references/verify.md` | Step indicators, View Native Query, Query Diagnostics: what each proves and what it does not |
| `references/native-query.md` | `Value.NativeQuery` + `[EnableFolding = true]`, and parameters |
| `references/incremental-refresh.md` | `RangeStart`/`RangeEnd` filters that fold, and the ones that silently do not |

## Rule until then

Do not claim a step folds without a way to check it. Say which verification the user should
run (View Native Query on that step) instead of asserting.

## Related skills

- **`m-reference`** — signatures and host availability.
- **`m-iteration`** — `Table.Buffer`, which stops folding on purpose.
