---
name: bundle-size-reduction
description: Analyzes a JavaScript bundle, splits code and replaces heavy dependencies, and reports byte counts before and after every change it makes.
---

# Bundle size reduction

Numbers first. Do not change anything until you have a baseline and a ranked list.

## Steps

1. Build for production and record total, gzip and brotli size per chunk. Generate a treemap with the project's bundler (`npx vite-bundle-visualizer`, `webpack-bundle-analyzer`, `npx source-map-explorer dist/*.js`, or `ANALYZE=true` for Next).
2. List the ten largest modules and who imports them. Look specifically for: full-library imports (`import _ from 'lodash'`, `import * as`), moment or other locale-heavy date code, duplicate versions of one package (`npm ls <pkg>`), polyfills for browsers you do not support, and icon sets imported whole.
3. Fix in order of bytes saved:
   - Replace heavy libraries with native APIs or small ones (`Intl.DateTimeFormat`, `structuredClone`, `date-fns` named imports).
   - Use named, tree-shakeable imports and check `sideEffects: false` in the package.
   - Dedupe versions with the package manager.
   - Lazy-load what is not needed on first paint: routes, modals, charts, editors, with `import()`.
4. Rebuild after every change and note the delta.
5. Check the result still works: run the tests and load the lazy parts once.

## Rules

- Do not remove a dependency still used elsewhere. Search before you delete.
- Never trade a size win for broken browser support listed in the project's browserslist.
- Stop when a change saves under 2 KB gzipped.

## Report

A table of change, bytes before, bytes after. Then what remains and why you left it.
