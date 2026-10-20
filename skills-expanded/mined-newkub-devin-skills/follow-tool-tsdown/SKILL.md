---
name: follow-tool-tsdown
description: Set up tsdown as a library bundler for TypeScript with Rolldown
argument-hint: "[scope]"
related:
  - follow-tool-rolldown
  - follow-tool-vite
  - follow-tool-bunup
  - follow-create-plugins
  - follow-tool-turborepo
  - follow-lang-typescript
  - follow-tool-vitest
  - follow-test
---

## Goal

Set up tsdown as a TypeScript library bundler on Rolldown, with type declarations and multiple output formats

## Scope

Use for TypeScript library projects that need bundling to ESM/CJS/IIFE with `.d.ts` generation

- Boundary: use tsdown when bundling a library (publish to a registry) — app bundling/dev server → `/follow-tool-vite`; raw bundler tuning → `/follow-tool-rolldown`; an alternative library bundler → `/follow-tool-bunup`; migrating from `tsup` → `workflows/migrate-from-tsup`
- Latest: `tsdown@0.23.0` (verified 2026-09-13) — requires Node.js `^22.18.0 | ^24.11.0 | >=26.0.0` at build time (output target can be lower via `target`)

## Execute

### 1. Project Analysis

> Goal: Confirm the project fits tsdown

1. Confirm it is a TypeScript library project
2. Check `package.json` and the Node.js version `^22.18.0 | ^24.11.0 | >=26.0.0`
3. Identify the wanted output formats
4. Check `src/index.ts` or the entry files

### 2. Installation

> Goal: Install tsdown

1. Install with `bun add -D tsdown`, or scaffold a new project with `bun create tsdown@latest`
2. Verify the version with `bunx tsdown --version`
3. Use `bunx tsdown --help` to see CLI options
4. See details in 

### 3. Configuration

> Goal: Create `tsdown.config.ts` for the project

1. Create `tsdown.config.ts` at the root
2. Use `defineConfig` from `tsdown`
3. Set `entry`, `format`, `dts`, `outDir`, `clean`
4. Configure `platform` as `node`, `browser`, or `neutral`
5. See config options in 

### 4. Build Scripts

> Goal: Add package scripts for building

1. Add `"build": "tsdown"` to `package.json`
2. Add `"build:watch": "tsdown --watch"`
3. Add `"dev": "tsdown --watch"` if needed
4. Verify the scripts work on Bun

### 5. Plugins and Validation

> Goal: Add plugins and validate the package

1. Add Rolldown/Rollup/unplugin plugins to the `plugins` array
2. Enable `publint: true` and `attw: true` when validation is wanted
3. Run `bun run build`, then check `dist/`
4. Verify the `.d.ts` files are all generated

### 6. Validate Output

> Goal: Check the output and watch mode

1. Check `dist/*.mjs`, `dist/*.cjs`, `dist/*.d.ts`
2. Run `bunx tsdown --watch` to test watch mode
3. Test importing the output in another project
4. Do `/follow-test` to run tests after build

### Workflows

> Goal: Dispatch specialized work to the right workflow

| Topic | Workflow |-------|----------| first-time setup (install, config, entry/dts/sourcemap) | `workflows/setup-tsdown/SKILL.md` | migrate from tsup | `workflows/migrate-from-tsup/SKILL.md` 
## Rules

### 1. Installation

- Use `bun add -D tsdown` for a local install
- Check the Node.js version first
- Use `bunx tsdown` for one-off runs

### 2. Configuration

- Use `tsdown.config.ts` with `defineConfig`
- Specify `entry` as an array or a string
- Set `format` to `['esm', 'cjs']` when both are wanted

### 3. Build

- Enable `clean: true`
- `treeshake` is enabled by default
- Check the `dist/` output after building

### 4. Type Declarations

- Enable `dts: true`
- Use the `vue` or `react` dts option when working with a framework
- Verify all `.d.ts` files are generated

### 5. Migration

- Use `bunx tsdown-migrate` to migrate from `tsup`
- Verify the output stays the same after migration
- Fix incompatible config

- Use /follow-tool-rolldown if needed
- Use /follow-tool-vite if needed
- Use /follow-tool-bunup if needed
- Use /follow-create-plugins (vite) if needed (tool tsdown)
- Use /follow-tool-turborepo if needed
- Use /follow-lang-typescript if needed
- Use /follow-tool-vitest if needed

## References

- [CLI reference](references/cli.md)


## File Structure

Canonical file structure + layer table: [templates/file-structure-lib.md](templates/file-structure-lib.md)

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Correct `tsdown.config.ts`
- package.json has build scripts
- `dist/` contains bundled files and `.d.ts`
- Watch mode works
- Validation (`publint`, `attw`) passes

