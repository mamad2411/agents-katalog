---
name: bun-multi-platform-server-packager
description: Assemble a self-contained cross-platform Bun server distribution by scanning imports, copying the transitive dep tree, bundling platform-specific native modules, and emitting entry scripts + Dockerfile.
category: build
version: 1.0.0
version_origin: extracted
tags: [bun, packaging, cross-platform, distribution]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: scripts/build-server.ts
imported_at: 2026-04-18T00:00:00Z
---

# Bun multi-platform server packager

## When to use
- Shipping a Bun/Node server as a self-contained tarball (no npm install on target).
- Monorepo where workspace packages must be resolved at runtime via symlinks.
- Targeting multiple OS/arch combinations (darwin/linux x x64/arm64) with bundled runtime + native deps.
- Want Docker/systemd/start scripts generated alongside the tarball.

## How it works
1. **Download the runtime**: `downloadBunForServer()` (`scripts/build-server.ts:232`) drops a matching `bun` binary under `vendor/bun/` per target arch. Same for `uv` under `resources/bin/uv`.
2. **Build MCP subprocess servers** into CJS with `bun build --target=node --format=cjs` (see `packages/session-mcp-server`, `packages/pi-agent-server`).
3. **Scan source imports, not just `package.json`**: regex-walk every `.ts/.js` in `SERVER_PACKAGES` looking for `from '...'`, `require('...')`, `import('...')` (lines 314-343). Skip relative / `node:` / workspace (`@craft-agent/*`) specifiers. Union with declared `dependencies` + `peerDependencies`. This catches hoisted + dynamically required deps that `package.json` alone misses.
4. **Copy the transitive tree**: `copyDependencyTree()` recursively reads each copied package's `package.json` and pulls in its declared deps. Tracked via a `visited` Set to dedupe.
5. **Add platform-specific natives** explicitly (sharp, sharp-libvips). They ship as `optionalDependencies` so they don't appear in normal import scans.
6. **Filter platform binaries inside deps** - e.g. strip all `ripgrep/<arch-os>` subdirs inside `@anthropic-ai/claude-agent-sdk/vendor/ripgrep/` except the target's. Saves tens of MB.
7. **Emit workspace shims**: write a minimal root `package.json` (`workspaces: ["packages/*"]`) + `tsconfig.json` with path maps, then `symlinkSync` each `packages/<pkg>` to `node_modules/@craft-agent/<short>/` so Bun resolves workspace imports at runtime.
8. **Generate entry scripts** (`bin/craft-server`, `start.sh`, `install.sh`) that set `CRAFT_BUNDLED_ASSETS_ROOT`, `CRAFT_UV`, `CRAFT_SCRIPTS`, prepend `resources/bin` + `vendor/bun` to `PATH`, then `exec "$ROOT/vendor/bun/bun" run "$ROOT/packages/server/src/index.ts" "$@"`.
9. **Optionally tar.gz**: `tar -czf craft-server-<ver>-<platform>-<arch>.tar.gz -C <outputDir> .`.

## Example
```ts
// Scan .ts files for external imports (paraphrase of scripts/build-server.ts)
const importRe = /(?:from\s+['"]|require\s*\(\s*['"]|import\s*\(\s*['"])([^'"]+)['"]/g;
for (const match of content.matchAll(importRe)) {
  const spec = match[1];
  if (spec.startsWith('.') || spec.startsWith('node:') || spec.startsWith('@craft-agent/')) continue;
  const parts = spec.split('/');
  const pkgName = spec.startsWith('@') ? `${parts[0]}/${parts[1]}` : parts[0];
  packages.add(pkgName);
}
// Then: copyDependencyTree(pkg, node_modules_src, node_modules_dst, visited)
```

## Gotchas
- Don't rely on `package.json` deps alone - monorepo hoisting hides real runtime requirements.
- Workspace symlinks MUST use relative target (`../../packages/<pkg>`) so the tarball stays portable.
- On Windows you cannot use POSIX symlinks without admin; this packager is darwin/linux only.
- `bun install --production` is NOT used here because it drops workspace deps; the manual copy pattern is the workaround.
