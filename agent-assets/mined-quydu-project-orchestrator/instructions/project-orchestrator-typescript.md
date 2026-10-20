---
applyTo: "**/*.ts,**/*.tsx,**/*.js,**/*.mjs,**/*.cjs"
description: TypeScript and JavaScript authoring standards.
---

# TypeScript and JavaScript Instructions

- TypeScript `strict` mode is required. `any` requires a comment justifying it.
- Use ES modules. No `require` in new code.
- Prefer `const`; use `let` only when reassignment is required. Never `var`.
- Model absence explicitly. Do not use `null` and `undefined` interchangeably.
- Validate external data at the boundary with a schema; do not cast unknown input to a type.
- Every `Promise` is awaited or explicitly handled. No floating promises.
- Catch narrowly and rethrow with context. Never `catch {}`.
- Release resources in `finally`, including file handles, timers, listeners, and abort controllers.
- No dynamic code execution: no `eval`, no `new Function`, no string-bodied timers.
- Never spawn a process with shell interpretation enabled or with unvalidated arguments.
- Keep modules focused. Extract a function when a block needs a comment to explain what it does.
