---
name: publish-release
description: Guidelines for building, packaging, and publishing projects. Use when modifying publishConfig, resolvePluginService, package.json main/types/exports for publishable libraries, checking dist folder generation, or debugging package resolution for released artifacts.
license: MIT
---

# Publish and Release

## Build Output and Publishing

- **Every build writes into its own project's `dist/`** — `packages/logger/dist`,
  `applications/caelundas/dist` — never a top-level one. `dist` is already
  gitignored and in the folder-structure rule's `ignorePatterns`.
- **`configuration/tsconfig.json` sets `declaration: true`**, so every build
  emits `.d.ts` beside its `.js`. Turning it off silently removes the types a
  published package ships.
- **A package's `main`, `types`, and `exports` point at TypeScript sources**, and
  `publishConfig` carries the emitted `dist/` paths beside them — pnpm applies
  those at publish time, so one manifest serves the workspace and a published
  consumer. **Verify a change here by packing, not by reading:** `pnpm pack` in
  the package, then inspect the tarball's `package.json`.
- **`files` must name `dist`.** Without it, packing falls back to the ignore
  files and the tarball ships no build output at all.
- **A plugin entry's `resolvePluginService` must stay a static import.** A
  dynamic `import()` escapes the `@swc-node/register` require hook into Node's
  own ESM resolver, and `nx g` then fails with `Cannot find module
  './modules/plugin/plugin-context.utilities'`.

Why the manifest fields stay on sources, which `publishConfig` fields pnpm
actually applies, and why shrinking the Nx plugin closure buys nothing is
[ADR 0009](../../docs/adr/0009-keep-manifest-fields-on-typescript-sources.md). **Do
not point `main` or `exports` at `dist/`** — it deadlocks the plugin graph load
and breaks `fallow-dead-code` and `vitest`.
