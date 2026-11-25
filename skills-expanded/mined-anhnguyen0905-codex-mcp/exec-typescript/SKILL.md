---
name: exec-typescript
description: TypeScript/JavaScript execution idioms to embed into Codex prompts when the target project is TS/JS — type safety, async correctness, and Node/web conventions.
---

# TypeScript / JavaScript Idioms (embed when project is TS/JS)

```
TypeScript standards:
- Explicit param/return types on exported functions; let locals infer. No `any` — use `unknown`
  and narrow, or generics.
- `interface` for extendable object shapes; `type` for unions/intersections; string-literal
  unions over enums.
- Async: always await or return promises — no floating promises; wrap awaits in try/catch where
  the error is handled; never mix .then chains with async/await.
- Narrow caught errors: `catch (error: unknown)` then `instanceof Error` before touching .message.
- Immutable updates via spread/map/filter — no in-place mutation of props, state, or params.
- Prefer const; no var. Strict null handling — no non-null assertions (!) to silence the checker.
- Validate external data with a schema library already in the project (e.g. zod) and infer types
  from the schema.
- ESM/CJS: match the project's module system exactly, including file extensions in imports if the
  project uses them.
- React (if present): typed props, hooks rules (no conditional hooks), keys on lists, effects with
  correct dependency arrays.
```
