---
name: follow-lib-esm-sh
description: Use the esm.sh CDN to load ES Modules in the browser without a bundler
argument-hint: "[scope]"
related:
  - follow-lib-animejs
  - follow-lib-arktype
  - follow-lib-better-auth
  - follow-best-practice
  - use-my-packages-on-registry
  - setup-cicd

---

## Goal

Use the `esm.sh` CDN to load `ES Modules` from `npm`, `JSR`, `GitHub`, and `pkg.pr.new` in the `browser`, `Deno`, or `Node.js` without a `bundler`

## Scope

For `import`ing modules via `HTTPS URL` with automatic `tree-shaking`, `bundling`, `dependency rewriting`, and `import maps`

- Use this skill only when loading modules via CDN URLs with no bundler (browser, Deno, no-build setups) — if the project has `package.json` + a bundler → install the package normally instead
- Other CDNs: jsDelivr (`cdn.jsdelivr.net`), JSPM (`jspm.io`) — see official docs via `/learn-from-web`
- `esm.sh` has a CLI for managing import maps in `index.html` — see `references/cli.md`

## Execute

### 1. Import Modules

> Goal: load ES Modules via `esm.sh`

1. Use the URL format `https://esm.sh/{package}@{version}/{subpath}`
2. Supports `npm` (default), `JSR` (`/jsr/`), `GitHub` (`/gh/`), and `pkg.pr.new` (`/pr/`)
3. Examples:
   - `import React from 'https://esm.sh/react@19.3.0'`
   - `import { encodeBase64 } from 'https://esm.sh/jsr/@std/encoding@1.0.0/base64'`
   - `import tslib from 'https://esm.sh/gh/microsoft/tslib@v2.8.1'`

### 2. Configure Dependencies And Build Options

> Goal: control dependencies and build options

1. Use `?deps=PACKAGE@VERSION,PACKAGE2@VERSION` to lock dependency versions
2. Use `?external=PACKAGE` or the `*` prefix, e.g. `https://esm.sh/*react-dom`, to mark all external dependencies
3. Use `?alias=PACKAGE:ALIAS` to change what a package resolves to, e.g. `?alias=react:preact/compat`
4. Use `?bundle=false` to disable default bundling, `?standalone` to bundle every dependency (except `peerDependencies`)
5. Use `?exports=a,b` to `tree-shake` down to only the needed exports
6. Use `?dev` for a development build, `?target=es2022` for a build target, `?conditions=...` for conditional exports

### 3. Use Import Maps

> Goal: use bare specifiers with `import maps`

1. Create a `<script type="importmap">` and map specifiers to `esm.sh` URLs
2. For trailing slashes, change `?` to `&` after the version, e.g. `https://esm.sh/react-dom@19.3.0&dev/`
3. Combine `?external` with `import maps` so the `browser` resolves the dependency itself
4. Use the `esm.sh` CLI (`npx esm.sh add <pkg>`, `npx esm.sh tidy`) to automatically add/clean imports in the `<script type="importmap">` of `index.html` — see `references/cli.md`

### 4. Use Advanced Features

> Goal: use esm.sh extra features as appropriate

1. Use `?worker` to load a module as a `Web Worker`
2. Use `?css` to import `CSS` that a package imports in JS
3. Use `?raw` or `https://raw.esm.sh/<PATH>` to fetch a source file untransformed
4. Use `?no-dts` to disable `TypeScript` type declarations in `Deno`
5. Use `esm.sh/run` (`<script type="module" src="https://esm.sh/run"></script>`) for `JSX/TSX` in HTML with no build (experimental)

### 5. Ensure Stability

> Goal: keep production stable

1. Always pin versions, e.g. `https://esm.sh/react@19.3.0` instead of `latest` or a bare package
2. Date (`yyyy-mm-dd`) versioning is supported since v137, e.g. `https://esm.sh/my-package@2026-01-02`
3. Since build v136 the system no longer uses the build version prefix (`/v135/...`) and `?pin` is ignored; since v137_2 the legacy build server is shut down — old pinned URLs redirect to the new routes
4. Test the URL in the `browser` or `Deno` before deploying
5. Follow the changelog at `https://github.com/esm-dev/esm.sh/releases` (latest build: v138, 2026-08-24 — verified 2026-09-13)

## Rules

- Use the URL format `https://esm.sh/{package}@{version}/{subpath}`
- Use `?deps` to lock dependency versions
- Use `?external` or the `*` prefix for external dependencies
- Use `?bundle=false` when bundling causes duplicate shared modules
- Use `?exports` to `tree-shake` to only the used parts
- Pin every version in URLs for production
- Use `&` instead of `?` when combining query params with a trailing slash
- Use `?target` to set the ES target
- Use `?dev` for development builds only
- Use `?no-dts` if CDN type declarations make `Deno` type-check incorrectly

- jsDelivr serves as a `multi-CDN` alternative — see official docs via `/learn-from-web`
- JSPM serves as an `import maps package manager` — see official docs via `/learn-from-web`
- Use /follow-lib-animejs if needed
- Use /follow-lib-arktype if needed
- Use /follow-lib-better-auth if needed
- Use /follow-best-practice if needed
- Use /use-my-packages-on-registry if needed
- Use /setup-cicd if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- `ES Modules` load without a `bundler`
- `Bundle size` reduced via `tree-shaking` and `?exports`
- `Dependency resolution` is clear and stable with version pinning
- `Development workflow` is simpler with `import maps` and `?dev`
