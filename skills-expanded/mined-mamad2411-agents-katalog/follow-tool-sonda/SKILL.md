---
name: follow-tool-sonda
description: Set up the Sonda bundle analyzer to analyze real bundles via source maps
argument-hint: "[scope]"
related:
  - report-bundle
  - run-build
  - follow-tool-vite
  - optimize
---

## Goal

Set up and use Sonda to analyze and visualize the bundle of the bundler/framework the project uses — treemap, dependency tree, compression sizes, and a JSON report for automation

## Scope

For JS/TS projects bundled with Vite, Rollup, Rolldown, esbuild, webpack, Rspack, or frameworks (Next.js, Nuxt, Astro, SvelteKit, Angular CLI)

- Boundary: Sonda analyzes source maps of the final output — sourcemaps must be enabled in the build config; if the target is inspecting the whole `node_modules` tree → `/follow-tool-node-modules-inspector`
- Used in `/report-bundle` to get per-asset and per-dependency sizes from a real report instead of `du` estimates
- Latest: `sonda@0.14.0` (verified 2026-10-03)

## Execute

### 1. Install And Enable Sourcemaps

> Goal: Install sonda and enable source maps

1. Install with `bun add -D sonda`
2. Enable sourcemaps in the build config (e.g. `build.sourcemap: true` in `vite.config.ts`) — Sonda works from the final source maps
3. If the report is incomplete, check that other plugins generate source maps too

### 2. Register Plugin

> Goal: Wire Sonda into the bundler or framework in use

1. Pick the entry point per bundler: `sonda/vite`, `sonda/rollup`, `sonda/rolldown`, `sonda/esbuild`, `sonda/webpack`, `sonda/rspack`
2. Framework integrations have dedicated entries (Next.js, Nuxt, Astro, SvelteKit, Angular CLI) — see the official docs per framework
3. Vite example:

   ```ts
   import { defineConfig } from 'vite'
   import Sonda from 'sonda/vite'

   export default defineConfig({
     build: { sourcemap: true },
     plugins: [Sonda()],
   })
   ```

4. See all options in [API reference](references/apis.md)

### 3. Configure Options

> Goal: Set the report to match the use case

1. `format: ['html', 'json']` — html for the interactive treemap, json for automation/CI
2. `gzip: true`, `brotli: true` — report compressed sizes (adds build time)
3. `deep: true` — break dependencies down into their original source files via their source maps
4. `sources: true` — embed source code in the report (careful with proprietary code when sharing)
5. `open: false` for CI; `outputDir`/`filename` set the report destination (default `.sonda/`, `sonda_[index]`)

### 4. Generate And Read Report

> Goal: Get real bundle data from the report

1. Run the build normally via `/run-build` — Sonda generates the report every time
2. Open `.sonda/sonda_*.html` — treemap per asset, dependency tree, deep view, code inspection
3. Use the JSON format as input for `/report-bundle` tables and CI assertions

## Rules

### 1. Sourcemaps Required

- No source maps → no report; always enable them in the build config before use
- Vite: CSS files have no source maps → CSS is not in the report (upstream limitation, vitejs/vite#2830)

### 2. Performance

- Enable only the options you need — `deep`, `sources`, `gzip`, `brotli` add build time and report size
- In CI use `format: 'json'` + `open: false`

### 3. Privacy

- `sources: true` embeds source code in the report — never share the report if the code is proprietary

- Use /report-bundle if needed
- Use /run-build if needed
- Use /follow-tool-vite if needed
- Use /optimize bundle if needed

## References

- [API and config options](references/apis.md)

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- The Sonda plugin wired into the bundler/framework with sourcemaps enabled
- Every build produces an HTML/JSON report in `.sonda/`
- Treemap, dependency tree, and compressed sizes ready to use in `/report-bundle` and CI
