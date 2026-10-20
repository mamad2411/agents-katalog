---
name: follow-create-elysia-plugin
description: Create an Elysia plugin with TypeScript/Bun, type safe, with lifecycle hooks
argument-hint: "[scope]"
related:
  - follow-create-bun-cli
  - follow-create-sdk
  - follow-lang-typescript
  - run-test
  - deep-review-codebase
  - report

---
## Goal

Create an Elysia plugin package with TypeScript/Bun that can be `.use()`-ed in an Elysia app, with decorators, state, hooks, routes, and tests

## Scope

Use for creating a reusable Elysia plugin for the Bun/Node runtime, supporting typed context, lifecycle hooks, prefix, scope, and package build

- Always confirm the latest `elysia` version with `/deep-research` + `/follow-best-practice` (don't pin it in files — per `/update-devin-global-skills`) — peerDeps must include `typescript >=5` and `@sinclair/typebox`

## Execute

### 1. Review Tech Stack

> Goal: verify the tech stack before creating

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest `elysia` plugin API, then run `/deep-review-codebase` to summarize the tech stack
2. Record the rationale for the chosen stack and libraries for future reference (create elysia plugin)
3. Record the rationale for the chosen stack and libraries for future reference (create elysia plugin)

### 2. Setup Project

> Goal: create the plugin package structure

1. Create the `packages/{plugin-name}/` directory
2. Create `package.json` with `name: elysia-{plugin-name}`
3. Create `tsconfig.json` with `strict: true`
4. Run `bun init` or `npm init`

### 3. Create Plugin

> Goal: implement the Elysia plugin

1. Create `src/index.ts` with a function returning `new Elysia({ name, seed })`
2. Add `.state()`, `.decorate()`, `.derive()` for shared context
3. Add routes with `.get()`, `.post()` as needed
4. Add lifecycle hooks with `.onBeforeHandle()`, `.onAfterHandle()`, `.onError()`

### 4. Configure Plugin Options

> Goal: support options and type safety

1. Take an options object as a parameter
2. Use `asconst` or Zod to validate options
3. Pass generic types through `Elysia<...>` if needed
4. Use `seed` for deduplication

### 5. Build Package

> Goal: build for npm

1. Install `tsup` or `bun build`
2. Set the output to `cjs` and `esm`
3. Mark `elysia` as external in `package.json`
4. Declare `types`, `main`, `exports` in `package.json`

### 6. Add Tests

> Goal: test the plugin

1. Create `test/plugin.test.ts`
2. Create an Elysia app, then `.use(plugin({ ... }))`
3. Call `app.handle(new Request('http://localhost/...'))` to test
4. Run `bun test`

### 7. Add Examples

> Goal: create usage examples

1. Create `examples/basic.ts`
2. Create `examples/with-options.ts`
3. Run the examples to make sure they pass

### 8. Ship

> Goal: deliver the work

1. Run `/ship`
2. If `ship` fails → report the status

## Rules

- Use a function returning `new Elysia()` as the starting pattern
- `elysia` must be in `peerDependencies`, not bundled in
- Name the plugin `elysia-{name}`
- Use lifecycle hooks for cross-cutting concerns
- Test with `app.handle()` without listening on a port

- Use /follow-create-bun-cli when needed
- Use /follow-create-sdk when needed
- Use /follow-lang-typescript when needed
- Use /run-test when needed
- Use /report when needed

## Expected Outcome

- The Elysia plugin package builds successfully
- The plugin can be `.use()`-ed in an Elysia app
- Context type inference works
- Tests pass
- Examples run

