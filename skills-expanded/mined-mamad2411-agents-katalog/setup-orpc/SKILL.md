---
name: follow-lib-orpc-setup-orpc
description: Install oRPC, router/procedure basics, zod integration, and the server handler
argument-hint: "[runtime-or-scope]"
related:
  - follow-lib-orpc
  - follow-lib-zod
  - follow-lib-effect-ts
  - learn
  - resolve-errors
---

## Goal

Install oRPC and create a router/procedure with Zod validation + a server handler so API calls actually work — first-time setup only

## Scope

- use when the project has no oRPC yet (if it exists already → verify only)
- covers: install, the `os` builder, procedures + zod `.input()`/`.output()`, `RPCHandler` mounting
- does not cover client, middleware, OpenAPI, TanStack Query — see the parent `SKILL.md`

## Execute

### 1. Check Precondition

> Goal: check the environment before setup

1. read `package.json` — if `@orpc/server` is already present → skip to verify; check the version (v1 stable vs v2 beta differ — see Version Notes in the parent)
2. identify the runtime/framework (Bun, Node, TanStack Start, Next.js) — pick the matching handler package
3. if there is no `zod` → run `/follow-lib-zod` first (oRPC uses Zod as its primary validator)

### 2. Install

> Goal: install the minimum packages

1. run `bun add @orpc/server` (add `@orpc/client` if a same-repo client needs it)
2. confirm it lands in `dependencies`; `zod` must already be present

### 3. Define Procedures And Router

> Goal: a router with zod-validated procedures

1. create the `os` builder: `import { os } from "@orpc/server"` — add `.$context<{ headers: Headers }>()` if initial context is needed
2. procedure: `.input(zodSchema).handler(async ({ input }) => { ... })` — run `/follow-lib-zod` for schemas
3. add `.output(zodSchema)` when the response must be validated; `.errors({...})` when type-safe errors are needed
4. combine procedures into a router: `{ users: { list, create } }`, then `export type Router = typeof router`

### 4. Setup Server Handler

> Goal: the handler can answer requests

1. use `RPCHandler` from `@orpc/server/fetch` (edge/fetch runtimes) or `@orpc/server/node` (Node.js)
2. mount at a route such as `/rpc/*`, then call `handler.handle(request, { prefix: "/rpc", context: { headers: request.headers } })`
3. check `matched` — if false → return `404`/the next handler
4. set `interceptors: [onError((error) => console.error(error))]` for error logging

### 5. Verify

> Goal: call a procedure for real over HTTP

1. Smoke: call a procedure via an HTTP request or test client — input is validated, output is correct
2. Invalid input → a clear error response (zod validation)
3. run `bunx tsc --noEmit` + lint — if it fails → run `/resolve-errors` max 3 rounds, then stop and report; passing → `/suggest-next-action`

## Rules

- Idempotent — if already set up, verify only
- `.input()` on every procedure that takes input — Zod is the primary validator
- Always export `type Router` — client type inference depends on it
- Pick the handler package by runtime (`/fetch` vs `/node`) — if unsure → check the official docs (orpc.unnoq.com)
- Check the version before choosing APIs — v2 beta has breaking changes (`isDefinedError` → `isInferableError`, etc.)

## Expected Outcome

- `@orpc/server` installed, router + procedures with zod validation
- `RPCHandler` mounted at the right route — smoke call passes
- ready to continue with client/middleware per the parent `SKILL.md`
