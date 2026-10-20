---
name: bundle-ts-as-cjs-for-node-require
description: Bundle a TypeScript helper as a single CJS file so it can be loaded via node --require / bun --preload into any arbitrary subprocess without requiring the child to have access to your node_modules.
category: build
version: 1.0.0
version_origin: extracted
tags: [esbuild, cjs, bundle, node-require, preload]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: scripts/electron-build-main.ts
imported_at: 2026-04-18T00:00:00Z
---

# Bundle TS as CJS for node --require

## When to use
- Writing interceptors, shims, or preload helpers that need to run BEFORE any other code in a Node/Bun subprocess.
- Subprocess's cwd doesn't have your `node_modules` (shipped app, different working dir, different user).
- You want a single-file drop-in: `node --require /abs/path.cjs child.js`.

## How it works
1. Author in TypeScript with all imports inline.
2. Bundle with esbuild:
   ```
   esbuild src/interceptor.ts \
     --bundle --platform=node --format=cjs \
     --outfile=dist/interceptor.cjs
   ```
3. `--bundle` inlines every dep (no transitive `require()`). `--platform=node` picks correct semantics. `--format=cjs` produces something `--require` / `--preload` can load.
4. Verify the output by running `node --check dist/interceptor.cjs` after build - catches "used `await` at top level" and similar ESM/CJS mismatches.
5. Wait for file stability (see `file-stability-polling-for-fs-flush`) before shipping.

## Example
```ts
// build step in your package.json scripts or a build script
spawn(['bun', 'run', 'esbuild',
  'packages/shared/src/unified-network-interceptor.ts',
  '--bundle', '--platform=node', '--format=cjs',
  '--outfile=apps/electron/dist/interceptor.cjs',
]);
```

Usage:
```ts
Bun.spawn(['node', '--require', interceptorCjsPath, 'agent.js'], { ... });
// or with bun:
Bun.spawn(['bun', '--preload', interceptorCjsPath, 'agent.ts'], { ... });
```

## Gotchas
- If your source uses top-level `await`, CJS won't work. Rewrite as sync or move into an IIFE.
- Anything you import at build time gets inlined; keep the file focused so the bundle stays small (fast to load per subprocess start).
- Don't mark deps as `external` unless you KNOW the child has them - defeats the purpose of a self-contained drop-in.
- For Electron packaged builds, include the `.cjs` in electron-builder `files:` list so it ships in the app bundle.
- Test on both Node (`--require`) and Bun (`--preload`) if you target both.
