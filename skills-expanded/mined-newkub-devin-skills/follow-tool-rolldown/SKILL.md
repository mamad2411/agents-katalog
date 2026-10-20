---
name: follow-tool-rolldown
description: Set up and use Rolldown for high-speed JavaScript/TypeScript bundling
argument-hint: "[scope]"
related:
  - follow-tool-vite
  - follow-create-plugins
  - follow-tool-tsdown
  - follow-tool-turborepo
  - follow-lang-typescript
  - follow-tool-vite-devtools
---

## Goal

Set up and use Rolldown for high-speed JavaScript/TypeScript bundling, supporting migration from Rollup and picking the right plugins in the ecosystem

## Scope

Use for JavaScript/TypeScript projects that want a fast bundler, code splitting/tree-shaking, or migration from Rollup/Vite

- Use standalone `rolldown` when bundling outside Vite (e.g. libraries, custom toolchain); if the project already uses Vite 8, Rolldown is its built-in bundler — go to `follow-tool-vite`
- Use `follow-tool-tsdown` for library builds that want zero-config on Rolldown (dts, dual format) instead of hand-written config

- Latest: `rolldown@1.2.11` (verified 2026-09-26) — 1.0 stable since May 2026 and the default bundler of Vite 8; requires Node.js `^20.19.0 | >=22.12.0`

## Execute

### 1. Installation

> Goal: install Rolldown on the environment

1. Check `package.json` and the package manager the project uses
2. Install `rolldown` with `bun add -D rolldown`
3. Verify the version with `bunx rolldown --version`
4. See more details in 

### 2. Project Analysis

> Goal: assess the project and pick a migration path or setup strategy

1. Check the existing bundler from `package.json` scripts and config files
2. If `rollup.config.*` exists → analyze current plugins, input, output
3. Identify entry points, output formats (esm/cjs/iife/umd), and the target environment
4. See ecosystem and official resources in 

### 3. Configuration

> Goal: create a correct `rolldown.config.ts`

1. Create `rolldown.config.ts` at the project root
2. Use `defineConfig` from `rolldown` for type safety
3. Define `input`, `output.dir`, `output.format`, `treeshake`, `plugins`
4. Enable `clear: true` for production builds if needed
5. Read the top-level options in 

### 4. Build and Watch

> Goal: run build and watch mode, then check the output

1. Run the build with `bunx rolldown`
2. Use `bunx rolldown --watch` for development
3. Check the output in `dist/` or the configured `output.dir`
4. Run `bun run build` via the package script if present
5. See output option details in 

### 5. Migration from Rollup

> Goal: move from Rollup to Rolldown without breaking behavior

1. Compare `rollup.config.*` with `rolldown.config.ts`
2. Replace Rollup plugins with Rolldown-compatible plugins (`@rolldown/*` or verified Rollup plugins)
3. Adjust `output` options, `manualChunks`, `external`, `globals`
4. Run the build and test suite to verify the output
5. See migration guidance in `workflows/migrate-from-rollup-*.md`

### 6. Plugin and Ecosystem Selection

> Goal: pick suitable plugins and libraries from the Rolldown ecosystem

1. Check the official plugins: `@rolldown/plugin-commonjs`, `@rolldown/plugin-node-resolve`, `@rolldown/plugin-terser`
2. Check community plugins are active and compatible with the Rolldown version
3. Use `rolldown-plugin-dts` if type definitions must be generated
4. Refresh the plugin list periodically against the official docs
5. See the plugin list in 

### Workflows

> Goal: dispatch specialized work to the right workflow

| Topic | Workflow |-------|----------| first-time setup (install, config, entry/output) | `workflows/setup-rolldown/SKILL.md` | optimize bundle (splitting, treeshaking, advancedChunks) | `workflows/optimize-bundle/SKILL.md` | migrate from Rollup | `workflows/migrate-from-rollup/SKILL.md` 
## Rules

### 1. Installation

- Use `bun add -D rolldown` for the local install
- Use `bunx rolldown` for a one-off build
- Check the version and Node.js compatibility before use (Rolldown 1.x needs Node `^20.19.0 | >=22.12.0`)
- If the project already uses Vite 8, Rolldown is its built-in bundler — use standalone `rolldown` only when bundling outside Vite (e.g. libraries)

### 2. Configuration

- Always use `rolldown.config.ts` with `defineConfig`
- Define `input`, `output.dir`, `output.format` explicitly
- Keep `treeshake` enabled by default unless there's a specific reason

### 3. Migration

- Don't rewrite source code for the migration
- Compare output against the previous Rollup build before deploy
- Verify sourcemap and chunking behavior

### 4. Plugins

- Prefer official plugins over community plugins
- Check maintenance status and compatibility
- Don't hard-code paths or secrets in config

- Use /follow-tool-vite if needed
- Use /follow-create-plugins (vite) if needed (tool rolldown)
- Use /follow-tool-tsdown if needed
- Use /follow-tool-turborepo if needed
- Use /follow-lang-typescript if needed

## References

- [CLI reference](references/cli.md)


- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Rolldown installed and building
- `rolldown.config.ts` is correct and maintainable
- Migration from Rollup goes smoothly
- The output bundle performs better
- Plugins are chosen appropriately

