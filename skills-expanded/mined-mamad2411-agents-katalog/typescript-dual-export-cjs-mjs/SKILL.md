---
name: typescript-dual-export-cjs-mjs
description: TypeScript package builds dual CJS + ESM outputs (dist/cjs, dist/mjs) and uses the package.json `exports` field to route imports/requires correctly.
category: bindings
version: 1.0.0
version_origin: extracted
confidence: medium
tags: [magika, bindings]
source_type: extracted-from-git
source_url: https://github.com/google/magika.git
source_ref: main
source_commit: 0a8cb9626bbf76c2194117d9830b23e9052a1548
source_project: magika
imported_at: 2026-04-18T00:00:00Z
---

# Typescript Dual Export Cjs Mjs

**Trigger:** Publishing a TS library that must work in legacy CJS Node, modern ESM Node, and bundlers (webpack/vite).

## Steps

- Set up two tsconfigs: tsc --module commonjs --outDir dist/cjs and tsc --module esnext --outDir dist/mjs.
- In package.json: "exports": { ".": { "import": "./dist/mjs/index.js", "require": "./dist/cjs/index.js", "types": "./dist/mjs/index.d.ts" } }.
- Add a separate ./node entrypoint for Node-specific code (fs access) so browser bundles stay slim.
- Emit .d.ts to both outputs so TS consumers get types under either resolution.
- Use .js extensions in source imports — required for ESM, harmless for CJS.
- CI test: import from a CJS test file and an ESM test file to catch mis-routing.

## Counter / Caveats

- Dual builds roughly double compile time; use tsc --build for incremental.
- Source maps need separate handling for each output; tools must pick the right one.
- Circular imports behave differently in CJS vs ESM; design to avoid them.
- Tree-shaking works well with ESM but bundlers may struggle with CJS — document for users.

## Source

Extracted from `magika` (https://github.com/google/magika.git @ main).

Files of interest:
- `js/package.json:7-17`
- `js/tsconfig.json:1-30`
