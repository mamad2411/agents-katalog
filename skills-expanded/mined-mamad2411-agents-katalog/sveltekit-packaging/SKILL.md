---
name: sveltekit-packaging
description: Use when building a reusable SvelteKit or Svelte component library using @sveltejs/package, including $lib export surface design, package.json exports map, the svelte field, TypeScript declaration generation, and library publishing conventions.
---

# SvelteKit Packaging

## Specialization

Expert guidance for authoring reusable Svelte and SvelteKit libraries using `@sveltejs/package`. Covers the `package` command, `$lib` as the export root, `package.json` `exports` map generation, the `svelte` field for editor tooling, `.d.ts` declaration generation, selective inclusion and exclusion of files, versioning conventions, and publishing to npm or a private registry.

## Trigger Conditions

- Building a reusable Svelte component library to be shared across multiple projects or published to npm.
- Authoring a SvelteKit utility library with server-side and client-side exports that must be tree-shakeable.
- Generating correct `package.json` `exports` map entries for a Svelte library so consumers get types, ESM, and the Svelte source.
- Diagnosing "cannot find module" or missing type errors when consuming a library built with `@sveltejs/package`.
- Setting up the build pipeline for a library package within a monorepo.
- Publishing a Svelte library and ensuring it works with Vite, SvelteKit, and Rollup consumers.

## Scope Boundaries

In scope:

- `@sveltejs/package` CLI: `svelte-package` command, `--watch` mode, `--input` and `--output` options.
- `src/lib` as the package root: all files under `src/lib` are candidates for export.
- `package.json` fields generated or required: `exports`, `svelte`, `types`, `main`, `module`.
- `exports` map structure: `'.'` default export, named subpath exports (`'./components/Button'`), conditional exports (`import`, `require`, `svelte`, `types`).
- `.d.ts` generation from `svelte2tsx` and TypeScript; ensuring `.svelte` files have accompanying `.d.ts`.
- `files` field in `package.json`: controlling what is included in the published package.
- `svelte` field: pointing to the Svelte source entry for tools that understand it.
- Barrel files vs. direct subpath exports: tradeoffs for tree-shaking.
- Version management: `package.json` `version`, semver conventions for Svelte library releases.
- Monorepo integration: workspace linking, `peerDependencies` for `svelte` and `@sveltejs/kit`.
- Testing the library locally with `npm link` or workspace `file:` references before publishing.
- Publishing: `npm publish`, `--access public`, npmrc authentication.

Out of scope:

- SvelteKit application configuration (`svelte.config.js` for apps) — covered by `sveltekit-configuration`.
- Bundler plugin authoring (Vite plugins, Rollup plugins) — out of SvelteKit packaging scope.
- CI/CD release pipeline — covered by `ci-cd-workflows`.
- Monorepo tooling (Turborepo, Nx) configuration beyond workspace linking.

## Inputs

- Library name and intended consumers (SvelteKit apps, plain Svelte, non-Svelte Vite projects).
- Export surface: list of components, utilities, and server-only modules to expose.
- TypeScript usage and strictness level.
- Monorepo vs. standalone package setup.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| `package.json` exports map | Correct `exports`, `svelte`, `types`, and `main` entries for all intended entry points |
| Build script | `svelte-package` command in `package.json` `scripts`; `--watch` variant for development |
| Type declarations | `.d.ts` files generated for all exported `.svelte` and `.ts` files |
| Server/client boundary | Server-only exports isolated under a subpath that signals server-only intent |
| Packaging quality checklist | Pass/fail against the checklist below |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Build a single-component library and confirm it imports correctly in a consuming SvelteKit app | `svelte-package` runs without errors; component imports and renders in the consumer |
| L2 Practical Delivery | Multi-component library with named subpath exports and types | All exports resolvable; types correct; tree-shaking works on named subpaths |
| L3 Specialist Hardening | Server/client split exports and monorepo workspace linking | Server-only subpath tested; workspace linking verified; peer dependency versions documented |
| L4 Expert Standardisation | Production-ready library with versioning, publish pipeline, and consuming-app integration test | `npm publish --dry-run` passes; consuming integration test exists; semver policy documented |

## Workflow

1. Scaffold the library: use `npm create svelte@latest` with the "library" template, or add `@sveltejs/package` to an existing project with `npm install --save-dev @sveltejs/package`.
2. Place all public exports under `src/lib/`; files outside `src/lib/` are not part of the package surface.
3. Add the build script to `package.json`: `"package": "svelte-package"` and `"package:watch": "svelte-package --watch"`.
4. Run `svelte-package`; it generates a `dist/` directory with `.svelte`, `.js`, `.d.ts`, and `package.json` files.
5. Review the generated `package.json` in `dist/`; verify the `exports` map covers:
   - `'.'`: the default entry (typically `src/lib/index.ts`).
   - Named subpaths for every discrete component or utility that consumers may import directly.
   - Conditional export keys: `'svelte'` (source), `'types'` (`.d.ts`), `'import'` (ESM `.js`).
6. For server-only exports (modules that import from `$env/static/private` or use Node APIs), place them under `src/lib/server/`; expose them as a `'./server'` subpath export with no `'svelte'` condition (no browser bundle).
7. Set `peerDependencies` for `svelte` (and `@sveltejs/kit` if hooks or routing APIs are used); specify a version range that matches the minimum supported version.
8. Set the `files` field in the root `package.json` to `['dist']` to prevent publishing source files or dev artifacts.
9. For TypeScript consumers, verify that the `types` condition in each `exports` entry resolves to a `.d.ts` file; run `tsc --noEmit` in a consuming project to confirm.
10. Run the packaging quality checklist; then test with `npm link` or a workspace `file:` reference before publishing.

## Packaging Quality Checklist

- [ ] `exports` map in `dist/package.json` has entries for every intended public import path.
- [ ] Each `exports` entry includes `'svelte'`, `'import'`, and `'types'` conditions.
- [ ] Server-only exports are under a `'./server'` subpath and do not include a browser-compatible entry.
- [ ] `peerDependencies` declares the minimum compatible `svelte` version; `svelte` is not in `dependencies`.
- [ ] `files` in the root `package.json` is set to `['dist']`; source files are not published.
- [ ] `.d.ts` files exist for every `.svelte` and `.ts` export; no `any` leaks at the public API boundary.
- [ ] Barrel file (`index.ts`) re-exports are not used as the sole export strategy; named subpath exports exist for tree-shaking.
- [ ] `npm publish --dry-run` lists only `dist/` contents plus `package.json`, `README.md`, and `LICENSE`.
- [ ] A consuming SvelteKit project can import from the library with no `moduleResolution` errors.
- [ ] Library version follows semver; breaking changes increment the major version.

## Security Notes

- Do not publish files containing secrets, `.env` content, or private keys. Review `npm publish --dry-run` output before every publish.
- Server-only modules (`src/lib/server/`) must not be importable from browser-side code; confirm the `exports` map does not expose a browser-compatible entry for them.
- Pin `peerDependencies` to a minimum version that does not have known security vulnerabilities; update when upstream patches are released.
- Use `npm publish` with `--access public` only for intentionally public packages; private packages require `--access restricted` or a private registry.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Library scaffold | Workflow steps 1–2 |
| Build script setup | Workflow step 3 |
| `exports` map generation | Workflow steps 4–5 |
| Server/client boundary | Workflow step 6 |
| Peer dependencies | Workflow step 7 |
| Publish artifact control | Workflow step 8 |
| TypeScript types | Workflow step 9 |
| Security | Security Notes + checklist |
| Quality validation | Packaging Quality Checklist |

## References

See [references/source-catalog.md](./references/source-catalog.md) for active source tracking.
