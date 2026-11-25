---
name: ts-react-antipatterns
description: Forbidden TypeScript/React patterns — XSS, eval, localStorage tokens, hook bugs, floating Promises. Applies when editing TS/TSX files.
paths: ["**/*.js","**/*.jsx","**/*.ts","**/*.tsx"]
user-invocable: false
---

# TypeScript / React anti-patterns — do not write these

Checks run automatically after each edit. Findings reference the IDs below.

## Blockers
- AP-TS-SEC-001 — Never set `innerHTML`/`dangerouslySetInnerHTML` from user data; use DOMPurify for rich text.
- AP-TS-SEC-002 — No `eval`/`new Function`/`setTimeout(string)`; use a static dispatch map.
- AP-TS-SEC-004 — Validate that user-supplied URLs have an `https:` or `http:` scheme before rendering.
- AP-TS-SEC-005 — Server-side secrets stay on the server; expose only through a backend proxy endpoint.

## Errors
- AP-TS-SEC-003 — Store session tokens in `HttpOnly; Secure; SameSite` cookies, not `localStorage`.
- AP-TS-PERF-001 — List every value the effect reads in `deps`; compute derived state in the render, not in effects.
- AP-TS-PERF-003 — Define components at module scope; memoize context values with `useMemo`.
- AP-TS-MAINT-002 — Await every Promise or chain `.catch()`; mark intentional fire-and-forget with `void`.
- AP-TS-MAINT-003 — Replace `@ts-ignore` with `@ts-expect-error // reason: <≥10 chars>`.

## Warnings
- AP-TS-PERF-004 — Cancel fetches on cleanup with `AbortController`; prefer a data-fetching library.
- AP-TS-PERF-005 — Never copy or spread the accumulator in `reduce`; mutate in place (`acc[key] = val; return acc`).
- AP-TS-MAINT-001 — Validate external data at the boundary (e.g. zod); avoid `any`, `!`, unsafe `as`, and never `as unknown as T`.
- AP-TS-MAINT-005 — No chained `as` casts; put `// SAFETY: <reason>` above every type assertion.
- AP-TS-MAINT-006 — Don't widen a known value to `unknown` to assert it into another type; use the original type.
- AP-TS-MAINT-007 — No `unknown`/`object` parameters, returns, or aliases; use named interfaces and validate at boundaries.
- AP-TS-MAINT-008 — Replace `Reflect.get`/`Reflect.apply` with direct property access and typed function calls.
- AP-TS-MAINT-009 — Replace `jest.mock`/`vi.mock` full-module replacement with `vi.spyOn`/`jest.spyOn` on specific exports.

Details for any ID: `reference/<ID>.md`
