---
name: follow-lib-orpc
description: Develop APIs with oRPC 1.15+ type-safe per official best practices
argument-hint: "[scope]"
related:
  - follow-lib-zod
  - follow-best-practice
  - use-my-packages-on-registry
  - setup-cicd
  - deep-test
  - run-api-docs
  - follow-tool-bruno

---

## Goal

Develop APIs with the latest oRPC version, fully type-safe, per official best practices

## Scope

Use for projects that use oRPC as the API layer (both standalone and inside TanStack Start/Next.js)

- Install oRPC packages (server, client, openapi, tanstack-query)
- Create procedures with input/output validation and type-safe errors
- Configure middleware, server handler, client
- Use TanStack Query and OpenAPI if needed
- No own CLI — used via programmatic API (thus none)

## Execute

### Workflows

| Topic | Workflow |
|-------|----------|
| Setup | `workflows/setup-orpc/SKILL.md` — install, router/procedure basics, zod, server handler |
| Contract-first design | `workflows/define-contracts/SKILL.md` — `oc` builder, `.input`/`.output`/`.errors`/`.route` |
| Procedures + router impl | `workflows/define-procedures/SKILL.md` — `implement()`, handlers, context, lazy routers |
| Client + TanStack Query | `workflows/connect-client/SKILL.md` — `createORPCClient`, `RPCLink`, query options |
| Middleware + auth | `workflows/use-middleware/SKILL.md` — `.use()`, context extension, interceptors |
| Serve + OpenAPI/docs | `workflows/serve-openapi/SKILL.md` — `RPCHandler`/`OpenAPIHandler`, spec gen, CORS | 
### 1. Install Packages

> Goal: install oRPC packages and dependencies

1. Install `bun add @orpc/server@1.15.0 @orpc/client` or `bun add @orpc/server @orpc/client` (latest stable)
2. If using OpenAPI, install `bun add @orpc/openapi`
3. If using TanStack Query, install `bun add @orpc/tanstack-query`
4. If you want contract-first, install `bun add @orpc/contract`
5. Use Zod for schema validation (do `/follow-lib-zod`)

### 2. Define Procedures

> Goal: create procedures with input validation and error handling

1. Create the `os` builder from `@orpc/server`
2. Use `.$context<{ headers: Headers }>()` for initial context
3. Use `.meta(...)` for OpenAPI metadata if needed
4. Use `.input(zodSchema)` for input validation
5. Use `.output(zodSchema)` for output validation if needed
6. Use `.errors({ CODE: { data: zodSchema } })` for type-safe error definitions
7. Use `.handler(async ({ input, context, errors }) => { ... })` for business logic
8. Use `.use(middleware)` for auth, logging, or resource injection
9. Export `type Router` for client-side type inference

### 3. Setup Middleware

> Goal: configure middleware for auth and resource injection

1. Use `.$context<{ ... }>()` before `.use()` to declare dependent context
2. Use `next({ context: { ... } })` to inject execution context (auth, db, etc.)
3. Use `throw new ORPCError('CODE')` for guards and error throwing
4. Use inline middleware with `.use(async ({ context, next }) => { ... })` for simple cases
5. Use `.mapInput()` on middleware if you need a different input shape

### 4. Setup Server Handler

> Goal: configure the server handler for the runtime

1. Use `RPCHandler` from `@orpc/server/fetch` (or `@orpc/server/node` for Node.js)
2. Use `OpenAPIHandler` from `@orpc/openapi/*` if OpenAPI/REST support is needed
3. Configure `interceptors: [onError((error) => console.error(error))]`
4. Use `handler.handle(request, { context: { headers: request.headers } })` for initial context
5. Check `matched` before returning the response
6. If using TanStack Start, use `createFileRoute` with `server.handlers`

### 5. Create Client

> Goal: create a type-safe client for calling procedures

1. Use `RPCLink` from `@orpc/client/fetch` to create a link
2. Use `createORPCClient(link)` with the `RouterClient<typeof router>` type
3. Use `headers: () => ({ ... })` for dynamic headers (e.g. auth token)
4. Use `interceptors: [onError((error) => { ... })]` for client-side error logging
5. If using TanStack Start, use `createIsomorphicFn` for environment-specific config

### 6. Handle Errors

> Goal: handle errors type-safely with `safe()` and `isDefinedError`

1. Use `.errors()` in the procedure to define type-safe errors
2. Use `safe()` from `@orpc/client` instead of try/catch for tuple destructuring
3. Use `isDefinedError(error)` from `@orpc/client` to narrow error types from `.errors()`
4. Use `createSafeClient` to auto-wrap every procedure call with `safe()`
5. Never put sensitive information in `message` or `data` (they are sent to the client)

### 7. Integrate TanStack Query

> Goal: configure TanStack Query if needed

1. Use `createTanstackQueryUtils` from `@orpc/tanstack-query`
2. Use `orpc.<path>.queryOptions({ input: { ... } })` for type-safe queries
3. Use `orpc.<path>.mutationOptions({ ... })` for mutations
4. Use `isDefinedError` in `onError` callbacks for type-safe error handling

### 8. OpenAPI And Contracts

> Goal: create OpenAPI docs and contract-first APIs if needed

1. Use `OpenAPIHandler` from `@orpc/openapi/fetch` or the adapter matching the runtime
2. Set `prefix` to match the route handler
3. Use `OpenAPIGenerator` from `@orpc/openapi` to generate an OpenAPI spec document from the router — use that spec with `/run-api-docs` (Scalar serve), `/deep-test api` (import into Bruno via `bru import openapi` or fuzz with Schemathesis)
4. Use `@orpc/contract` to define the contract before implementing
5. Use `ContractRouterClient<typeof contract>` for a client from the contract

## Rules

### 1. Procedure Design

- Use `.$context<{ ... }>()` for initial context (environment-specific dependencies)
- Use `.input(zodSchema)` for every procedure that accepts input (do `/follow-lib-zod`)
- Use `.output(zodSchema)` when you want to validate responses and OpenAPI
- Use `.errors()` for application-specific errors that need type safety
- Use common error codes (`UNAUTHORIZED`, `NOT_FOUND`) without defining a schema each time
- Export `type Router` for client-side type inference

### 2. Middleware Design

- Use `.$context` before `.use()` to declare dependent context
- Use `next({ context: { ... } })` to inject execution context
- Use `throw new ORPCError('CODE')` for guards
- Check the context before initializing a resource (dedup if it already exists)

### 3. Server Setup

- Use `RPCHandler` from the package matching the runtime (`/fetch`, `/node`)
- Use `OpenAPIHandler` if OpenAPI/REST support is needed
- Configure `interceptors` for error logging
- Pass initial context via `handler.handle(request, { context: { ... } })`
- Check `matched` before returning the response

### 4. Client Setup

- Use `RPCLink` from `@orpc/client/fetch`
- Use `RouterClient<typeof router>` for a type-safe client
- Use `headers: () => ({ ... })` for dynamic headers
- Use `createIsomorphicFn` for SSR/CSR environment-specific config
- Use `createSafeClient` if you use `safe()` often

### 5. Error Handling

- Use `safe()` instead of try/catch in client code
- Use `isDefinedError(error)` to narrow typed errors
- Never put sensitive information in `message` or `data`
- Use `.errors()` only for application-specific cases, not common errors
- Use `ORPCError` directly in utility functions without access to the `errors` object

### 6. Context Management

- Use initial context for environment-specific values (headers, env vars, db URLs)
- Use execution context for runtime data (auth, db connections)
- Combine both: initial context for static deps, middleware for dynamic deps
- Don't pass sensitive data through context that isn't needed

### 7. TanStack Query Integration

- Use `createTanstackQueryUtils` instead of building custom query utils
- Use `.queryOptions()`, `.mutationOptions()` for type-safe options
- Use `isDefinedError` in `onError` callbacks

### 8. Version Notes

- Latest stable: `@orpc/server@1.15.4` / `@orpc/client@1.15.4` (verified 2026-09-24)
- oRPC v2 beta: `@orpc/server@beta @orpc/client@beta` (2.0.0-beta.35) has breaking changes such as `route`/`prefix`/`tag` → `meta(openapi(...))`, `isDefinedError` → `isInferableError`, `safe` returns `[error, data, inferableError]`, `eventIterator` → `asyncIteratorObject`
- Check the version in `package.json` before choosing APIs

- Use `/follow-lib-zod` if using Zod as the validator
- Use `/follow-best-practice` if needed
- Use `/use-my-packages-on-registry` if needed
- Use `/setup-cicd` if needed
- Use /follow-tool-bruno if needed


- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- A fully type-safe API (server → client)
- Type-safe error handling with `safe()` and `isDefinedError`
- Middleware for auth, logging, resource injection
- Schema validation with Zod for every input/output
- A client that calls procedures like local functions with auto-completion
- Consistent with official oRPC documentation
