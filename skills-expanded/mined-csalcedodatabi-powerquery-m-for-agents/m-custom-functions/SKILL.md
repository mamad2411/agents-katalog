---
name: m-custom-functions
description: Use when writing a custom Power Query M function — typed and optional parameters, return types, recursion with @, functions that take functions, attaching Documentation metadata with Value.ReplaceType so the function shows a description and examples in the editor, or turning a query into a reusable function. Triggers on "M custom function", "Power Query function parameters", "optional parameter M", "Value.ReplaceType", "document my function", "Documentation.Name", "recursive function Power Query", "invoke custom function".
---

# M Custom Functions

> **Status.** Stub. Scope fixed in
> [the design spec](../../docs/superpowers/specs/2026-09-28-powerquery-m-for-agents-design.md)
> (§4).

## Planned contents

| File | Covers |
|---|---|
| `references/syntax.md` | `(x as number, optional y as nullable text) as table =>`, what `optional` really implies for the type |
| `references/documentation-metadata.md` | `Value.ReplaceType` with `Documentation.*` — the same metadata `m-reference` reads from `#shared` |
| `references/recursion.md` | `@` scoping, and when `List.Generate` is the better answer |
| `references/function-values.md` | Passing functions, `each` as sugar for `(_) =>`, closures over `let` variables |

## Related skills

- **`m-reference`** — check a library function does not already do it.
- **`m-iteration`** — loops without recursion.
