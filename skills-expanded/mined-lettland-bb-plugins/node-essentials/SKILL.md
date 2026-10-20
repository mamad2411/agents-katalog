---
name: node-essentials
description: Use when working with Node.js — event loop, ESM/CJS interop, performance profiling, common bottlenecks.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: runtime
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [bun-essentials, pnpm-essentials, typescript]
---

# Node Essentials

**Iron Law: don't block the event loop. ESM-only for new code. Profile before optimizing — clinic.js or `--inspect`.**

**Versions:** LTS Active `22` · Current `24` · Next `26` (LTS Oct 2026) — _Node 20 reached EOL on 2026-04-30 — do not start new work on it. Baseline raised from 18; `--permission` model, built-in test runner (`node --test`), built-in `fetch`, `--watch`, native ESM, type-stripping (`--experimental-strip-types`) all in 22+. 26 will land `node:sqlite` and `node:test` upgrades._

## The event loop — phases that actually run

```
┌──────────────────────────────────────────────┐
│   timers       (setTimeout, setInterval)     │  ← expired callbacks fire here
├──────────────────────────────────────────────┤
│   pending      (some I/O system errors)      │
├──────────────────────────────────────────────┤
│   poll         (I/O callbacks: fs, net, etc) │  ← most time spent here
├──────────────────────────────────────────────┤
│   check        (setImmediate)                 │
├──────────────────────────────────────────────┤
│   close        (socket 'close', etc)         │
└──────────────────────────────────────────────┘
       ↑
   between each phase: microtasks drain (Promises + queueMicrotask)
```

| Phase  | What runs                                  | Use for                                 |
| ------ | ------------------------------------------ | --------------------------------------- |
| timers | due `setTimeout` / `setInterval` callbacks | delayed work                            |
| poll   | I/O completion callbacks                   | the bulk of an HTTP server's work       |
| check  | `setImmediate` callbacks                   | run after current I/O, before next poll |
| close  | `'close'` events                           | cleanup                                 |

**Microtasks (`Promise.then`, `queueMicrotask`, `process.nextTick`) run between phases and after each macrotask.** A tight `nextTick` chain starves the loop entirely.

### Macrotasks vs microtasks — visibly

```typescript
setTimeout(() => console.log("timer"), 0);
setImmediate(() => console.log("immediate"));
process.nextTick(() => console.log("nextTick"));
Promise.resolve().then(() => console.log("promise"));
console.log("sync");

// sync → nextTick → promise → timer or immediate (order depends)
```

`process.nextTick` runs before promises, before any phase. Abuse and you starve I/O.

### What blocks the loop

- Sync I/O: `fs.readFileSync`, `crypto.pbkdf2Sync`, sync DNS — never in request paths
- CPU-bound work: image processing, big regexes, JSON.parse on huge strings, ZIP unpacking
- A pathologically long microtask chain (`while`-loop building promises)

**Symptoms:** rising p95 latency under load even though CPU isn't pinned, `loop.checkLagMs` climbing, healthchecks timing out.

**Fixes:**

- Move CPU work to `worker_threads`
- Use streaming APIs (`createReadStream` over `readFileSync`)
- Chunk long loops with `setImmediate` or `setTimeout(..., 0)` between batches
- Use the async crypto/zlib APIs (libuv thread pool, default size 4 — bump `UV_THREADPOOL_SIZE` if I/O-bound on them)

## ESM/CJS interop

**Modern Node is ESM-first.** Authoring new code in CJS is a self-inflicted wound — async imports, `import.meta`, top-level await, tree shaking all require ESM.

```json
// package.json — make the package ESM
{
  "type": "module",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "require": "./dist/index.cjs", // only if you ship dual
      "types": "./dist/index.d.ts"
    }
  }
}
```

### The interop matrix

| Caller | Importing            | Works?                                                                               |
| ------ | -------------------- | ------------------------------------------------------------------------------------ |
| ESM    | ESM                  | ✅                                                                                   |
| ESM    | CJS                  | ✅ — default export is `module.exports`, named exports only if statically detectable |
| CJS    | CJS                  | ✅                                                                                   |
| CJS    | ESM (sync `require`) | ✅ as of Node 22.12 (`require(esm)`) — **only if the ESM has no top-level await**    |
| CJS    | ESM (older Node)     | ❌ — need dynamic `import()`                                                         |

`require(esm)` (Node 22.12+) lets CJS consumers `require()` ESM packages synchronously — finally. Top-level `await` in the ESM disqualifies. Verify with `node --print 'process.versions.node'` ≥ 22.12 before relying on it.

### Common ESM pitfalls

- `__dirname` / `__filename` don't exist in ESM. Use:
  ```typescript
  import { fileURLToPath } from "node:url";
  const __dirname = fileURLToPath(new URL(".", import.meta.url));
  ```
- Imports must include the `.js` extension (even when source is `.ts`) — TS resolves the source, Node resolves the build output.
- JSON imports need `with { type: "json" }`:
  ```typescript
  import pkg from "./package.json" with { type: "json" };
  ```
- `node:*` prefix on builtins (`node:fs`, `node:path`) — strongly recommended, eslint-enforceable. Bare `'fs'` still resolves at runtime but `node:` is the forward-compatible form and disambiguates from any same-named userland package.

## Performance — measure first

```bash
# Quick CPU profile (Chrome DevTools URL printed). Use --inspect to attach without pausing,
# --inspect-brk to pause on the first line (waits for the debugger).
node --inspect ./server.js               # or --inspect-brk; combining both is redundant

# Clinic.js suite — quick visual diagnosis (substitute bunx if you're on Bun)
npx clinic doctor -- node server.js          # high-level
npx clinic flame -- node server.js           # flame graph
npx clinic bubbleprof -- node server.js      # async ops
npx clinic heapprofiler -- node server.js    # heap allocations

npx 0x -- node server.js                     # alternative flame-graph tool

# Built-in (Node 18+)
node --cpu-prof --cpu-prof-dir=./profiles server.js
# → open .cpuprofile in Chrome DevTools → Performance
```

### Common bottlenecks

| Symptom                           | Likely cause                                      | Fix                                                  |
| --------------------------------- | ------------------------------------------------- | ---------------------------------------------------- |
| p95 latency under load, CPU < 50% | event loop blocked                                | profile microtasks; move sync work off-loop          |
| Memory growing forever            | retained refs in closures, big caches without TTL | heap snapshot; weak refs; bounded LRU                |
| Slow JSON parsing                 | huge response body                                | stream parse (`stream-json`, `clarinet`) or paginate |
| Slow DB queries                   | N+1 in ORM, missing index                         | log queries; explain plans; batch with DataLoader    |
| GC stalls (long pauses)           | huge short-lived allocations                      | object pooling, avoid massive arrays in hot paths    |
| `EMFILE` errors                   | file descriptor leak                              | ensure streams `.destroy()`, raise `ulimit -n`       |
| Slow startup                      | sync `require` chain on cold start                | lazy-import non-critical modules                     |

### `--inspect` in production (carefully)

```bash
NODE_OPTIONS="--inspect=127.0.0.1:9229" node server.js
# DO NOT bind 0.0.0.0 — opens RCE
```

Use a SIGUSR1 to enable on demand:

```bash
kill -USR1 <pid>     # toggles inspector on Linux
```

## A few rules that pay off forever

- **Always handle `error` on streams.** Unhandled → process crash.
- **AbortController for cancellation.** `fetch`, `setTimeout`, most async APIs accept `signal`. Cancel on request close.
- **`for await (const x of stream)`** instead of accumulating into memory.
- **One Node version per repo** via `.nvmrc` / `engines.node`. CI must enforce.
- **`NODE_OPTIONS=--enable-source-maps`** in prod so stack traces map back to TS source.

## Anti-patterns

- `readFileSync` / `cryptoSync` / sync DNS in request paths
- `process.nextTick(loop)` recursion → starves I/O
- Catching `error` events nowhere → process death
- `JSON.parse` on multi-MB strings without streaming
- Binding `--inspect` to `0.0.0.0` in production
- ESM without `.js` extension in imports → resolution fails at runtime
- CJS-only library shipped in 2026 without a reason
- "Optimizing" without a profile — vibe-driven perf work
- Unbounded in-memory caches → OOM at the worst moment
- **Shelling out via `child_process` with shell mode enabled** (`exec(cmd)` or `spawn(cmd, args, { shell: true })`) on any string built from user input → command injection (OWASP A03). Use `execFile(bin, [arg, arg])` or `spawn(bin, [arg, arg])` without `shell: true` — args bypass the shell, no quoting bugs, no injection

## Red flags

| Thought                                     | Reality                                                                           |
| ------------------------------------------- | --------------------------------------------------------------------------------- |
| "It's I/O so it can't be blocking"          | `readFileSync` is I/O. So is sync crypto. So is huge regex on a long string.      |
| "We need worker_threads"                    | 90% of the time you need streaming + better algorithm. Measure first.             |
| "ESM is too painful"                        | Painful for a week. Then forever better.                                          |
| "Promises are always faster than callbacks" | Same event loop; promises add microtask overhead. Often invisible, sometimes not. |

## Hand-off

For Bun as a Node alternative (and migration playbook): `Skill(bun-essentials)`. For monorepo package management: `Skill(pnpm-essentials)`. For TypeScript-specific config: `Skill(typescript)`.
