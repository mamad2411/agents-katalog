---
name: lazy-auto-detect-server-entry
description: Walk up from import.meta.dir looking for a sentinel file (packages/server/src/index.ts) so monorepo CLIs don't need config, hardcoded paths, or environment variables to find the server they should spawn.
category: cli
version: 1.0.0
version_origin: extracted
tags: [monorepo, auto-detect, cli, sentinel-file]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: apps/cli/src/server-spawner.ts
imported_at: 2026-04-18T00:00:00Z
---

# Auto-detect monorepo sibling entry point

## When to use
- A CLI package inside a monorepo needs to find a sibling package's file (e.g. `packages/server/src/index.ts`).
- Don't want to hardcode "../../packages/..." - breaks when the CLI is symlinked / published / copied.
- Avoid forcing users to pass `--server-entry` every time.

## How it works
1. Start from `import.meta.dir` (the dir of the running CLI file).
2. Walk upward step by step (`resolve(dir, '..')`), bounded to ~10 levels.
3. At each level, test whether a known monorepo sentinel exists (`packages/server/src/index.ts`).
4. Return the first hit.
5. If nothing found after N levels, throw with a *helpful* message pointing at the `--server-entry` override.

## Example
```ts
import { resolve, join } from 'node:path';

function findServerEntry(): string {
  let dir = import.meta.dir;
  for (let i = 0; i < 10; i++) {
    const candidate = join(dir, 'packages', 'server', 'src', 'index.ts');
    if (Bun.file(candidate).size > 0) return candidate;
    dir = resolve(dir, '..');
  }
  throw new Error(
    'Could not auto-detect server entry. ' +
    'Pass --server-entry or ensure the monorepo layout includes packages/server/src/index.ts'
  );
}
```

## Gotchas
- `Bun.file(path).size > 0` is fast (no read) and handles missing-file without throwing. In Node, use `existsSync(path)` + `statSync(path).size > 0`.
- Bound the walk - broken installs shouldn't probe all the way to `/`.
- The sentinel must be unique to your repo (NOT something like `package.json` that exists everywhere).
- In packaged builds, the CLI is often at a non-monorepo path; keep the `--server-entry` escape hatch.
- Write a test that runs with `cwd` changed to an unrelated dir and confirms the error message fires.
