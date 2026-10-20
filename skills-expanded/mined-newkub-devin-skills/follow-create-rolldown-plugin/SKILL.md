---
name: follow-create-rolldown-plugin
description: Build Rolldown plugins with TypeScript for the Rust-based bundler
argument-hint: "[scope]"
related:
  - follow-create-bun-cli
  - follow-create-sdk
  - follow-create-plugins
  - follow-lang-typescript
  - run-test
  - deep-review-codebase
  - report

---
## Goal

Build Rolldown plugins with TypeScript that work with the Rolldown bundler, supporting universal hooks, hook filters, virtual modules, and package builds

## Scope

Use for building JavaScript/TypeScript plugins for Rolldown or Vite 8+, covering the plugin object, hooks, filters, build, and tests

- Packages: `rolldown` (the main bundler in Rolldown-powered `vite`), `vite` — always confirm the latest versions with `/deep-research` + `/follow-best-practice` (not pinned in this file — per `/update-devin-global-skills`); 1.x has hook filters (`rolldown/filter`: `exactRegex`, `prefixRegex`); external `rolldown`/`vite` in the plugin build

## Execute

### 1. Review Tech Stack

> Goal: Inspect the tech stack before creating

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, then run `/deep-review-codebase` to summarize the tech stack
2. Run `/deep-review-codebase` to review the tech stack, dependencies, and library design (create rolldown plugins)
3. Record the reasons for choosing the stack and libraries for later reference (create rolldown plugins)

### 2. Setup Project

> Goal: Create the plugin package

1. Create the `packages/{plugin-name}/` directory
2. Create `package.json` named `rolldown-plugin-{name}` or `unplugin-{name}`
3. Install `rolldown`, `typescript`, `@types/bun`
4. Create `tsconfig.json`

### 3. Create Plugin Object

> Goal: Implement the plugin factory

1. Create `src/index.ts` with a factory function
2. Return an object with the required `name` — type it with `Plugin` from `rolldown`
3. Use hook filters to reduce overhead

### 4. Add Hooks

> Goal: Use the Rolldown plugin API

1. `options` — modify input options
2. `buildStart` — start the build
3. `resolveId` — resolve imports
4. `load` — load a module
5. `transform` — transform code
6. `buildEnd` / `closeBundle` — cleanup

### 5. Configure Hook Filters

> Goal: Reduce overhead between Rust and JS

1. Use `filter: { id: regex }` in `resolveId`, `load`, `transform`
2. Use helpers from `rolldown/filter` such as `exactRegex`, `prefixRegex` for patterns faster than general regex
3. Return `null` early when there is no match

### 6. Build Package

> Goal: Build for npm

1. Install `tsdown` (recommended — uses rolldown internally) or `bun build`
2. Externalize `rolldown`
3. Output `esm` and `cjs`
4. Declare `types`, `main`, `exports` in `package.json`

### 7. Add Tests

> Goal: Test the plugin

1. Create `test/plugin.test.ts`
2. Use `rolldown.build(...)` with the plugin
3. Check the output bundle
4. Run `bun test`

### 8. Add Examples

> Goal: Create usage examples

1. Create `examples/basic/` with a basic plugin
2. Create `examples/virtual-module/` with resolveId + load
3. Run the examples until they pass

### 9. Ship

> Goal: Deliver the work

1. Run `/ship`
2. If `ship` fails → report the status

## Rules

- Use a unique `name` for the plugin
- Use `rolldown-plugin-{name}` for Rolldown-specific plugins
- Use `unplugin-{name}` if supporting multiple bundlers
- Avoid the `moduleParsed` hook in dev mode
- Use hook filters for `resolveId`, `load`, `transform`
- Externalize `rolldown` and `vite` in the build

- Use /follow-create-bun-cli if needed
- Use /follow-create-sdk if needed
- Use /follow-create-vite-plugin if needed (create rolldown plugins)
- Use /follow-lang-typescript if needed
- Use /run-test if needed
- Use /report if needed
- Use /follow-create-plugins if needed


## Expected Outcome

- Rolldown plugin builds successfully
- The plugin runs with `rolldown.build`
- Hook filters reduce overhead
- Tests and examples pass
- Usable with Vite 8+

