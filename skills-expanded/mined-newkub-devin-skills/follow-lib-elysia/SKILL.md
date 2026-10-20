---
name: follow-lib-elysia
description: Develop type-safe APIs with Elysia 1.4+ on Bun, following official best practices
argument-hint: "[scope]"
related:
  - use-bun-native-api
  - follow-lib-zod
  - follow-best-practice
  - setup-cicd
  - use-my-packages-on-registry

---

## Goal

Develop APIs with the latest Elysia version on the Bun runtime, fully type-safe, following official best practices

## Scope

For projects using Elysia as the web framework on the Bun runtime — pick the workflow by phase:

- First-time setup (install, `new Elysia()`, basic routes/plugins) → `workflows/setup-elysia/SKILL.md`
- Production deploy (`bun build`, env config, platform targets) → `workflows/deploy-elysia/SKILL.md`
- This skill covers the full reference — if the task is a general Bun HTTP server without Elysia → use `/use-bun-native-api` instead

- Install Elysia, Eden, and the needed plugins
- Define routes, handlers, validation, lifecycle hooks
- Use Standard Schema (Zod, Valibot, ArkType, Effect Schema, Yup, Joi)
- Build a type-safe client via Eden
- Generate OpenAPI docs with `@elysia/openapi`

## Execute

### Workflows

| Topic | Workflow |
|-------|----------|
| Setup | `workflows/setup-elysia/SKILL.md` — install, `new Elysia()`, `.listen()`, basic routes/plugins |
| Routing | `workflows/define-routes/SKILL.md` — methods, params/wildcards, `.group`/`.guard`/`.mount`, `.ws` |
| Validation | `workflows/validate-requests/SKILL.md` — TypeBox `t.*` schemas, coercion, shared models, Standard Schema |
| Lifecycle/hooks | `workflows/use-lifecycle/SKILL.md` — hook order, `derive`/`decorate`/`resolve`, `onError`, scoping |
| Eden client | `workflows/use-eden/SKILL.md` — `treaty`, typed calls, WS subscriptions |
| Plugins | `workflows/use-plugins/SKILL.md` — `@elysiajs/*` openapi/cors/jwt/static/cron + custom plugins |
| Deploy | `workflows/deploy-elysia/SKILL.md` — `bun build`, env config, platform targets | 
### 1. Install And Setup

> Goal: install Elysia and set up on the Bun runtime

1. Install `bun add elysia` or `bun add elysia@1.4.30` (latest stable)
2. For end-to-end type safety, install `bun add @elysia/eden`
3. Create a new project with `bun create elysia app`
4. Use `bun --hot` for hot reloading in development
5. Use Bun as the runtime only (do `/use-bun-native-api`)
6. Create a `new Elysia()` instance and `.listen(port)`

### 2. Define Routes

> Goal: define routes with HTTP verb methods and path parameters

1. Use HTTP verb methods: `.get()`, `.post()`, `.put()`, `.patch()`, `.delete()`
2. Use dynamic path parameters: `/users/:id`, `/posts/:category/:slug`
3. Use wildcards: `/files/*` for catch-all
4. Use `.group()` for route grouping and prefix
5. Use custom methods with `.route(method, path, handler)`

### 3. Handle Context

> Goal: handle request context and response headers

1. Use `context.body`, `context.query`, `context.params`, `context.headers`, `context.cookie`, `context.request`
2. Use `context.store` for global mutable state
3. Use `context.set.headers` to set response headers
4. Use `context.set.status` or `context.status(code, value)` for type-safe status codes
5. Use `context.redirect(path)` for redirects

### 4. Validate With Schema

> Goal: validate input with schema validation

1. Use `Elysia.t` (TypeBox) for built-in schema validation
2. Standard Schema (Zod, Valibot, ArkType, Effect Schema, Yup, Joi) works by importing it and passing it to the route handler
3. Define schemas in route options: `body`, `query`, `params`, `headers`, `cookie`, `response`
4. Use `.model()` for reusable named schemas
5. Use `.guard()` to apply schemas and validation in a scoped way
6. Do `/follow-lib-zod` if Zod is the validator

### 5. Use Lifecycle Hooks

> Goal: use lifecycle hooks for the request/response pipeline

1. Use `.onRequest()` to notify a new request
2. Use `.onParse()` for custom body parsing
3. Use `.onTransform()` to modify context before validation
4. Use `.onBeforeHandle()` for custom validation before the handler
5. Use `.onAfterHandle()` to tweak the returned value
6. Use `.onMapResponse()` to map the returned value into an HTTP response
7. Use `.onError()` to handle errors in the life-cycle
8. Use `.onAfterResponse()` for cleanup after the response is sent
9. Use `.derive()` or `.resolve()` to derive additional context values

### 6. Use Plugins

> Goal: use plugins for a modular architecture

1. Use `.use(plugin)` to register a plugin
2. Declare dependencies explicitly: the main instance must `.use(auth)` before using `Auth`
3. Use `.decorate()` to inject custom properties into context
4. Use `.state()` to inject mutable state
5. Use `.guard()` for scoped validation and schemas
6. Use `.scope()` to control plugin merge behavior (local, scoped, global)

### 7. Setup Eden Client

> Goal: set up the Eden Client if needed

1. Export `type App` from the server: `export type App = typeof app`
2. Use `treaty<App>(url)` from `@elysia/eden` (recommended)
3. Call the API type-safely: `app.users({ id: 1 }).get()`
4. Use `edenFetch<App>(url)` for a fetch-like syntax
5. Handle errors with `{ data, error }` destructuring

### 8. OpenAPI And Production

> Goal: generate OpenAPI docs and prepare for production

1. Install `@elysia/openapi` with `bun add @elysia/openapi`
2. Use `app.use(openapi())` to generate the OpenAPI spec and docs UI
3. Use `fromTypes()` if you want to generate OpenAPI directly from TypeScript types
4. Use `@elysia/swagger` if you want Swagger UI
5. Run production with `bun run start` and verify `Bun.version` supports Elysia

## Rules

### 1. Project Setup

- Use Bun as the runtime only (do `/use-bun-native-api`)
- Use `bun add elysia` to install
- Use `Bun.serve` only through the Elysia `.listen()`
- Use `bun --hot` for hot reloading in development

### 2. Route Definition

- Use HTTP verb methods (`.get()`, `.post()`, etc.) to define routes
- Use dynamic params with the `:param` syntax
- Use `.group()` for route prefix and organization
- Route order: static paths before dynamic paths

### 3. Handler Patterns

- Use `context.status(code, value)` or `context.set.status` for type-safe status (v1.4)
- Use `context.set.headers` for response headers
- Use `context.store` for mutable global state
- Use `context.cookie` for cookie management
- Use `context.redirect()` for redirects

### 4. Validation

- Use `Elysia.t` (TypeBox) as the default validator
- Standard Schema (Zod, Valibot, ArkType, Effect Schema, Yup, Joi) is fine if the project already uses it
- Define schemas for `body`, `query`, `params`, `headers`, `response`
- Use `.model()` for reusable schemas
- Use `.guard()` for scoped validation

### 5. Lifecycle Hooks

- Use `.onBeforeHandle()` for auth and custom validation
- Use `.onAfterHandle()` to transform responses
- Use `.onError()` for centralized error handling
- Use `.derive()` to derive additional context values (recommended for v2)
- Use `.resolve()` to resolve values before the handler (still available in v1.4)
- Hook order: Request → Parse → Transform → Before Handle → Handler → After Handle → Map Response → After Response

### 6. Plugin Design

- Declare dependencies explicitly (Dependency Injection pattern)
- Use `.decorate()` to inject services into context
- Use `.state()` to inject mutable state
- Use `.guard()` for scoped schemas and validation
- Use `.scope()` to control merge behavior
- Split logic into small, reusable plugins

### 7. Eden Type Safety

- Export `type App` from the server
- Use `treaty<App>()` (recommended) over `edenFetch`
- Handle errors with `{ data, error }` destructuring
- Use Eden for type-safe unit tests

### 8. Error Handling

- Use `.onError()` for centralized error handling
- Use `context.status(code, message)` instead of throw where possible (v1.4)
- Use a custom error class when needed, then handle it in `.onError()`
- Return meaningful error messages without leaking sensitive info

### 9. Version Notes

- Latest stable: `elysia@1.4.30`, `@elysia/eden@1.4.10`, `@elysia/openapi@1.4.16` (verified 2026-09-16)
- Elysia 2.0 beta "DayDream": `bun add elysia@next` (2.0.0-beta.14) or migrate with `bunx @elysia/codemod@latest` (verified 2026-09-16)
- v2.0 has breaking changes: route hooks/schemas must come before the handler, `resolve` → `derive`, `as: 'scoped'` → `'plugin'`, use `problem` for RFC 9457 errors instead of `status`
- v2.0 drops the `on` prefix from lifecycle hooks (`onRequest` → `request`, `onBeforeHandle` → `beforeHandle`, `onError` → `error`) and WebSocket becomes an opt-in plugin, `.ws()` takes 3 args `(path, options, handler)` with generator `yield` instead of `ws.send`
- Check the version in `package.json` before choosing APIs

- Use /use-bun-native-api if needed
- Use /follow-lib-zod if Zod is the validator
- Use /follow-best-practice if needed
- Use /setup-cicd if needed
- Use /use-my-packages-on-registry if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- A fully type-safe API (server → client via Eden)
- Validation across every layer (body, query, params, headers, response)
- A modular, reusable plugin architecture
- Centralized, type-safe error handling
- OpenAPI docs generated automatically from code
- Aligned with the official ElysiaJS documentation
- Bun native APIs used per `/use-bun-native-api`
