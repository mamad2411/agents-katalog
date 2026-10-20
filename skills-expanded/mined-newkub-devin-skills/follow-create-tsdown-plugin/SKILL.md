---
name: follow-create-tsdown-plugin
description: Build tsdown plugins with the Rolldown API and tsdown-specific hooks
argument-hint: "[scope]"
related:
  - follow-tool-tsdown
  - follow-create-plugins
  - follow-lang-typescript
  - deep-review-codebase
  - follow-tool-turborepo

---
## Goal

Build tsdown plugins with a Rolldown-compatible plugin API plus tsdown-specific lifecycle hooks

## Scope

Use for building plugins for the `tsdown` bundler in TypeScript, covering plugin objects, hooks, build, tests, and the npm package

- Package: `tsdown` (0.x — API may change) — always confirm the latest version with `/deep-research` + `/follow-best-practice` (not pinned in this file — per `/update-devin-global-skills`); `TsdownPlugin` from `tsdown/plugins` + the `tsdownConfig`/`tsdownConfigResolved` hooks on the Rolldown plugin API

## Execute

### 1. Review Tech Stack

> Goal: Review the tech stack before building

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, then run `/deep-review-codebase` to summarize the tech stack
2. Run `/deep-review-codebase` to review the tech stack, dependencies, and library design (create tsdown plugins)
3. Record the rationale for the chosen stack and libraries for future reference (create tsdown plugins)

### 2. Setup Project

> Goal: Create the plugin package

1. Create the `packages/{plugin-name}/` directory
2. Create `package.json` with the name `tsdown-plugin-{name}` or `unplugin-{name}`
3. Install `tsdown`, `rolldown`, `typescript`, `@types/bun`
4. Install a build tool: `bunup` or `tsdown`
5. Create `tsconfig.json` with `strict: true`, `declaration: true`

### 3. Create Plugin Object

> Goal: Implement the plugin factory

1. Create `src/index.ts` with a factory function
2. Import the `TsdownPlugin` type from `tsdown/plugins` if using tsdown hooks
3. Or use the `Plugin` type from `rolldown` for a pure Rolldown plugin
4. Return an object with the required `name`:
   ```ts
   import type { TsdownPlugin } from "tsdown/plugins";
   export function myPlugin(options?: MyOptions): TsdownPlugin {
     return {
       name: "tsdown-plugin-my",
       // hooks
     };
   }
   ```

### 4. Add Rolldown Hooks

> Goal: Use the Rolldown plugin API

1. `options` — modify input options
2. `buildStart` — start the build
3. `resolveId` — resolve imports
4. `load` — load a module
5. `transform` — transform code
6. `buildEnd` / `closeBundle` — cleanup
7. Use hook filters for `resolveId`, `load`, `transform`:
   ```ts
   transform: {
     filter: { id: /\.ts$/ },
     handler(code, id) { ... }
   }
   ```

### 5. Add tsdown-Specific Hooks

> Goal: Use the tsdown-specific lifecycle

1. `tsdownConfig(config, inlineConfig)` — modify `UserConfig` before it is resolved (`inlineConfig` = CLI flags from `build()`)
2. `tsdownConfigResolved` — after the config is resolved (called per output format, read-only)
3. Use mutation on `config.plugins` in `tsdownConfig` — merge instead of replacing the array; don't concat
4. Note that `fromVite` plugins don't receive `tsdownConfig` (but they do receive `tsdownConfigResolved`)
5. Use config-level `hooks` (`build:prepare`, `build:before`, `build:done` — hookable-based) for lifecycle tasks that don't need a full plugin

### 6. Build Package

> Goal: Build the plugin for npm

1. Create `bunup.config.ts` or `tsdown.config.ts`
2. Externalize `tsdown` and `rolldown` from the bundle
3. Output `esm` and `cjs` with `.d.ts`
4. Specify `exports`, `types`, `main` in `package.json`
5. Run `bun run build`

### 7. Add Tests

> Goal: Test the plugin

1. Create `test/plugin.test.ts`
2. Use `tsdown.build(...)` or `rolldown.build(...)` with the plugin
3. Check the bundle output
4. Run `bun test`

### 8. Add Examples

> Goal: Create usage examples

1. Create `examples/basic/` with a basic plugin
2. Create `examples/tsdown-config/` showing the `tsdownConfig` hook in use
3. Run the examples until they pass

### 9. Ship

> Goal: Deliver the work

1. Run `/ship`
2. If `ship` fails → report the status

## Rules

### 1. Naming

- Use `tsdown-plugin-{name}` for tsdown-specific plugins
- Use `unplugin-{name}` if supporting multiple bundlers
- The plugin name in the `name` field must be unique within a build

### 2. Plugin Type

- Use `TsdownPlugin` from `tsdown/plugins` if you need tsdown hooks
- Use `Plugin` from `rolldown` if you don't need tsdown hooks
- Keep compatibility with Rollup plugins where possible

### 3. Hook Filters

- Use `filter` in `resolveId`, `load`, `transform` to reduce overhead
- Return `null` quickly when there is no match
- Use precise regexes such as `/\.ts$/` for TypeScript files

### 4. tsdown Hooks

- `tsdownConfig` can mutate `config.plugins` in place
- Avoid returning a partial config if plugins need to append
- Use `tsdownConfigResolved` to stash the resolved config

### 5. Build And External

- Externalize `tsdown`, `rolldown`, `vite` in the build
- Generate `.d.ts` with `bunup` or `tsdown`
- Use the `exports` field in `package.json`

### 6. Migration

- Use `bunx tsdown-migrate` to migrate from `tsup`
- Check the output after migrating
- Use /follow-create-plugins when needed


## Expected Outcome

- tsdown plugin builds successfully
- Plugin works with `tsdown.build`
- Hook filters reduce overhead between Rust and JS
- Tests and examples pass
- `.d.ts` files are generated completely

## Examples

```text
packages/tsdown-plugin-example/
├── src/
│   └── index.ts
├── test/
│   └── plugin.test.ts
├── examples/
│   ├── basic/
│   └── tsdown-config/
├── package.json
├── tsconfig.json
├── bunup.config.ts
└── README.md
```

## Guide

- `follow-tool-tsdown` — tsdown bundler setup
- `follow-create-rolldown-plugins` — Rolldown plugin patterns
- `follow-create-vite-plugins` — Vite plugin patterns
- `follow-tool-turborepo` — package build pipeline
- `follow-lang-typescript` — TypeScript best practices
- [tsdown Plugin Architecture](https://github.com/rolldown/tsdown/blob/main/docs/advanced/plugins.md)
- [Rolldown Plugin API](https://rolldown.rs/apis/plugin-api)

