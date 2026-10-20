---
name: follow-create-vite-plugin
description: Build Vite plugins with the standard Plugin API
argument-hint: "[scope]"
related:
  - follow-create-sdk
  - deep-review-codebase
  - follow-tool-vite
  - ship
  - follow-tool-vite-devtools

---
## Goal

Build Vite plugins with the standard Plugin API, with Rolldown compatibility support

## Scope

Use `follow-create-vite-plugins` for the specifically covered tasks and workflows (create vite plugins)

- Packages: `vite` (8.x uses Rolldown as the default bundler — universal hooks are per-environment via `this.environment`), `rolldown`, `typescript` — always confirm the latest versions with `/deep-research` + `/follow-best-practice` (not pinned in this file — per `/update-devin-global-skills`)

## Execute

### 1. Review Tech Stack

> Goal: Review the tech stack before building

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, then run `/deep-review-codebase` to summarize the tech stack
3. Record the rationale for the chosen stack and libraries for future reference (create vite plugins)

### 2. Setup

> Goal: Prepare the initial folder structure and config

1. Create the `packages/{plugin-name}/` folder structure
2. Create `package.json` with dependencies and scripts
3. Create `tsconfig.json` for TypeScript configuration

### 3. Create Plugin

> Goal: Create the plugin implementation with hooks per the Vite Plugin API (Rolldown-compatible)

1. Create `src/index.ts` with the plugin implementation — the plugin object must have `name` (required, used in error/debugging) and optional `enforce`/`apply`
2. Define the plugin function returning an object with hooks
3. Use TypeScript for type safety

### 4. Configure Build

> Goal: Configure the library-mode build per Vite `build.lib`

1. Create `vite.config.ts` for the library-mode build — `build.lib`: `entry` (`resolve(import.meta.dirname, 'lib/main.ts')` or a map of multiple entries), `name` (UMD global), `fileName`; default formats: single entry = `es`+`umd`, multiple entries = `es`+`cjs`
2. Mark external deps that shouldn't be bundled via `build.rolldownOptions.external` (+ `output.globals` for UMD)
3. Externalize vite from the bundle

### 5. Add Examples

> Goal: Create basic and advanced usage examples

1. Create `examples/basic/` with a basic example
2. Create `examples/advanced/` with an advanced example
3. Test that the examples actually work

### 6. Add Tests

> Goal: Create unit and integration tests for the plugin

1. Create `test/` with unit and integration tests
2. Run `build` to verify the build process
3. Run `test` to verify functionality

### 7. Ship

> Goal: Deliver the work

1. Run `/ship`
2. If `ship` fails → report the status

## Rules

### 1. Plugin Naming

- Use `vite-plugin-{name}` for Vite-specific plugins
- Use `rolldown-plugin-{name}` for Rolldown-compatible plugins
- Use `vite-plugin-{framework}-{name}` for framework-specific plugins

### 2. Universal Hooks

- Use Rolldown-compatible hooks for dev and build
- Hooks: options, buildStart, resolveId, load, transform, buildEnd, closeBundle
- Avoid the `moduleParsed` hook in dev mode (Vite doesn't do a full AST parse; output-generation hooks except `closeBundle` aren't called in dev)
- Use hook filters (Rolldown/Rollup 4.38+) to reduce overhead between the Rust↔JS runtime
- Use `normalizePath` from `vite` to convert paths to POSIX separators
- Check the runtime via `this.meta.viteVersion` and `this.meta.rolldownVersion` (Rolldown-powered Vite 8+)

### 3. Vite Specific Hooks

- Use Vite-specific hooks only when necessary
- Hooks: config, configResolved, configureServer, configurePreviewServer, closeServer (`{ reason: 'restart' | 'close' }` — dispose resources created in `configureServer`), transformIndexHtml, handleHotUpdate
- Use the `hotUpdate` hook (per-environment, receives `HotUpdateOptions` with `type: 'create' | 'update' | 'delete'`) for the new HMR flow — `handleHotUpdate` is planned for deprecation
- Universal hooks are per-environment — access the current environment via `this.environment` inside a hook

### 4. Plugin Ordering

- Use `enforce: 'pre'` to run before Vite core plugins
- Use `enforce: 'post'` to run after Vite build plugins
- Don't set enforce for ordering between Vite core and build plugins

### 5. Conditional Application

- Use `apply: 'build'` for build-only plugins
- Use `apply: 'serve'` for dev-only plugins
- Use the function form `(config, { command }) => command === 'build'` for complex logic

### 6. Library Mode

- Use Vite library mode for building plugins (browser-oriented) — for non-browser/advanced cases use `tsdown` or Rolldown directly
- Configure build.lib with entry, name, fileName (+ `cssFileName` if there is CSS — export `"./style.css"` in package.json)
- Use formats: ['es', 'cjs'] — `.js` output becomes `.mjs` and `.cjs` becomes `.js` according to `type: module`
- `package.json`: `"files": ["dist"]`, subpath `exports` per entry (`import`/`require`); build types separately with `tsc --emitDeclarationOnly` (Vite doesn't emit declarations)
- `import.meta.env.*` is static-replaced at build time but `process.env.*` is not — if you need it, define it in the `define` config
- Externalize vite from the bundle

- Use /follow-create-sdk when needed
- Use /follow-tool-vite when needed

## Expected Outcome

- Plugin created with the correct naming convention
- Plugin uses universal hooks for Rolldown compatibility
- Plugin builds successfully with library mode
- Examples and tests are fully created
