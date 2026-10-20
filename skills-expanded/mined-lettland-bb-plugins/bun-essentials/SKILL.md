---
name: bun-essentials
description: Use when working with Bun — install/run/test/bundle, native Bun APIs, bunx, monorepo gotchas, migration from Node.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: runtime
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [node-essentials, pnpm-essentials, typescript]
---

# Bun Essentials

**Iron Law: Bun for new TS/JS projects in 2026. Migration from Node mostly drop-in; check the Bun.\* API gaps before betting on it.**

**Versions:** Current `1.2.x` · No LTS series — _`bun build --compile` ships standalone executables; first-class TS without tsc; `bun --hot` HMR; `bun install --frozen-lockfile`; `Bun.serve` rivals raw uWebSockets in latency._

## What Bun is

A JS/TS runtime + package manager + bundler + test runner + transpiler in one binary, written in Zig. Aims for Node-API compatibility plus its own native APIs that are faster than Node equivalents.

## One binary, four tools

```bash
bun install          # package manager (pnpm-class speed)
bun run script       # task runner (reads package.json scripts)
bun test             # test runner (Jest-compatible API)
bun build ./entry.ts # bundler — ahead-of-time, esbuild-class output (no HMR)
bun ./server.ts      # runtime — PROD path (executes TS/JSX directly, no transpile, no watcher)
bun --hot ./server.ts # runtime — DEV path (same execution + HMR/watch on top)
bun upgrade          # self-update
```

No `tsc`, `vitest`, `tsx`, `esbuild`, `npm` needed in a Bun-only stack. Less surface area, fewer version mismatches.

## Bun vs Node tradeoffs

|                                       | Bun                                            | Node                                |
| ------------------------------------- | ---------------------------------------------- | ----------------------------------- |
| TS/JSX execution                      | native (no transpile)                          | needs `tsx`/`ts-node`/`tsc`         |
| Test runner                           | built-in (`bun test`)                          | external (vitest, jest)             |
| Package install speed                 | ~5–20× faster than npm                         | baseline                            |
| Bundler                               | built-in                                       | external (esbuild, rollup, webpack) |
| Native APIs (`Bun.serve`, `Bun.file`) | yes, faster                                    | n/a                                 |
| Node compat                           | high but not 100% (some `node:*` APIs partial) | 100% (it's Node)                    |
| Native modules (`.node`)              | partial — N-API support improving              | full                                |
| Production maturity                   | improving — workloads pass at most scales      | battle-tested                       |
| Memory footprint                      | lower (Zig allocator)                          | baseline                            |

**Choose Bun for:** new projects, internal tools, scripts, edge functions, dev experience, monorepo speed.
**Choose Node for:** apps using specific native modules with no Bun build, very long-tail Node API usage (cluster module edge cases, some `worker_threads` patterns), regulated environments mandating Node LTS.

## Native APIs that beat Node

```typescript
// HTTP server — ~3× faster than node:http
Bun.serve({
  port: 3000,
  idleTimeout: 30, // seconds; default 10. RAISE proportionally if `maxRequestBodySize` is raised for uploads — a 100 MB upload on a 10 Mbps link takes 80s+ and a low timeout kills the connection mid-stream.
  maxRequestBodySize: 1024 * 1024, // 1 MB cap; default 128 MB. Drop unless you accept uploads.
  fetch(req) {
    return new Response("hi");
  },
  websocket: {
    open(ws) {
      ws.subscribe("room");
    },
    message(ws, msg) {
      ws.publishText("room", String(msg));
    },
  },
});

// File I/O — lazy, streaming
const f = Bun.file("./big.json"); // doesn't read yet
const text = await f.text(); // streams
const stream = f.stream();
await Bun.write("./out.txt", "hello"); // string, Blob, ArrayBuffer, Response

// Password hashing (argon2id by default)
const hash = await Bun.password.hash("secret");
const ok = await Bun.password.verify("secret", hash);

// SQLite (no driver install)
import { Database } from "bun:sqlite";
const db = new Database(":memory:");
db.query("CREATE TABLE t(id INTEGER)").run();

// Hashing
const h = Bun.hash("data"); // wyhash
const sha = new Bun.CryptoHasher("sha256").update("x").digest("hex");
```

These aren't polyfills — they're the reason to use Bun. Default to native APIs in new code; reach for `node:*` only when portability matters.

## `bunx` vs `npx`

```bash
bunx prettier --write .         # like npx but uses Bun's resolver/runtime
bunx --bun vite                 # force-run with Bun (some tools default to Node)
```

- Caches package installs aggressively; subsequent runs are near-instant.
- `--bun` forces the target tool to run on Bun's runtime — some tools (Vite, jest) spawn Node by default.
- Don't pin a `bunx` invocation to a moving tag in production scripts; pin the exact version. For production tooling that runs repeatedly, prefer `bun add --exact tool && bun run tool` over `bunx` — the lockfile then guards against registry-mirror or post-publish artifact swaps, which a version-only pin doesn't.

## Monorepo — the parent `node_modules` gotcha

Bun walks up the directory tree looking for `node_modules` and `package.json`. **If a parent directory has a `node_modules`, Bun in your subproject will resolve packages from there**, even if you ran `bun install` in the subproject.

This bites you when:

- A workspace's `node_modules` was deleted but a higher monorepo root still has one
- Two projects share a parent and one was installed with npm
- A `tsconfig.json` in a parent picks up resolution rules

**Mitigations:**

- Use workspaces (`workspaces:` in root `package.json`) — Bun handles them properly and creates a single hoisted `node_modules`.
- For unrelated projects under one folder, keep an empty `node_modules` (or `.npmrc` with `root=true`-equivalent) at each project root, or move projects out from under any parent `node_modules`.
- `bun pm ls` lists installed packages and versions (top-level by default; pipe through `--json` for the full tree). For _which-parent-won_ resolution detail, inspect `bun.lock` directly — it records the resolution graph.

## Migration from Node

For most apps, the migration is:

```bash
rm -rf node_modules package-lock.json
bun install
bun run dev          # or bun ./src/index.ts
bun test
```

**Checklist before betting prod on it:**

| Concern                                      | Check                                                                                                |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Native modules (`.node` files)               | does each work under Bun? `bun pm ls --json \| jq -r '..\|.name? // empty' \| grep node-` and verify |
| Worker threads                               | Bun supports `node:worker_threads`; test your worker-heavy code                                      |
| Cluster module                               | partial support; use `Bun.serve` + reuse-port instead                                                |
| Custom loaders / `--experimental-vm-modules` | Bun has its own plugin API                                                                           |
| `process.binding(...)` (deep internals)      | not supported; refactor                                                                              |
| Async hooks for context propagation (OTel)   | works; verify your specific instrumentation                                                          |
| CI runs npm                                  | switch CI to `bun install` AND `bun test` together; mixed CI breaks lockfiles                        |

**Don't** mix `bun install` locally with `npm ci` in CI — `bun.lock` and `package-lock.json` will drift; one or the other rules.

## When NOT to use Bun

- Deep monorepos with conflicting parent `node_modules` you can't fix
- Heavy `.node` native modules with no Bun-compatible build (older `bcrypt`, some database drivers — check before committing)
- Regulated platforms that mandate Node LTS specifically
- "Just because it's faster" on a project that's already shipped on Node and works fine — migration risk usually exceeds dev-time win

## Anti-patterns

- `bun install` locally + `npm ci` in CI → divergent lockfiles, "works on my machine"
- Running Bun in a directory under a parent `node_modules` you forgot about
- Using `Bun.*` native APIs in a library intended for Node users — breaks portability
- Expecting 100% Node compat for niche APIs (`vm`, deep `process.*`, certain `dgram` flags)
- Treating Bun's test runner as drop-in Jest — most matchers work, some Jest plugins don't
- Pinning `bunx tool@latest` in CI — re-runs become non-deterministic

## Red flags

| Thought                          | Reality                                                                      |
| -------------------------------- | ---------------------------------------------------------------------------- |
| "It's just like Node"            | 95%. The 5% will be the one you depend on. Test first.                       |
| "Bun's native APIs are optional" | They're the point. If you only use `node:*`, why pay the compat risk?        |
| "Lockfile compatibility is fine" | npm/yarn/pnpm/bun lockfiles do **not** interchange. Pick one.                |
| "It'll work in our CI"           | Test on the exact CI runner OS. Bun was Linux/macOS first; Windows is newer. |

## Hand-off

For Node-specific topics (event loop, ESM/CJS interop, profiling): `Skill(node-essentials)`. For pnpm in monorepos that aren't Bun-native: `Skill(pnpm-essentials)`. For TS config and types: `Skill(typescript)`.
