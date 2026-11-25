---
name: cli-serve-blocking-exit
description: In a CLI that wraps a long-running server, block on SIGINT/SIGTERM with a Promise instead of `process.exit(0)` so the underlying Bun.serve/Hono event loop keeps running.
category: cli
version: 1.0.0
version_origin: extracted
tags: [cli, signal-handling, bun, server, lifecycle]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/coleam00/Archon.git
source_ref: dev
source_commit: d89bc767d291f52687beea91c9fcf155459be0d9
source_project: Archon
imported_at: 2026-04-18T00:00:00Z
---

# `archon serve`-Style: Block CLI on Signals Instead of Returning

## When to use

- You have a CLI whose typical subcommand returns an exit code (`0`/`1`) and that's fine.
- One subcommand starts a long-running server (`serve`, `run`, `daemon`). If this subcommand returns and the CLI's outer switch calls `process.exit(exitCode)`, the server dies with it — even though `Bun.serve()` / Node `http.createServer().listen()` would normally keep the process alive.
- You want Ctrl+C and SIGTERM to cleanly unblock, do any teardown, and only then `process.exit(0)`.

## Steps

1. **Write the subcommand as `async`** and return a number like any other command — but **before** returning, `await` on a promise that only resolves on signals:

   ```ts
   await new Promise<void>(resolve => {
     process.once('SIGINT', resolve);
     process.once('SIGTERM', resolve);
   });
   return 0;
   ```

   Use `once` (not `on`) so the handler auto-removes after firing — prevents double-teardown if both signals arrive.

2. **Start the server first**, then await the signal promise. On unblock, the Promise resolves, `return 0` runs, and the outer CLI switch can do its own cleanup (close DB, shutdown telemetry) before `process.exit`.

3. **Don't install SIGINT handlers during server import.** The subcommand module owns the signal handlers; installing them elsewhere makes lifecycle confusing.

4. **Validate arguments before doing the long-running work.** Range-check ports etc., and return `1` on invalid input — failing early is cheap, failing after the server binds is expensive and confusing.

5. **Guard binary-only subcommands** with a compile-time flag. Archon's `serveCommand` checks `BUNDLED_IS_BINARY` and rejects with a helpful message in dev mode:

   ```ts
   if (!BUNDLED_IS_BINARY) {
     console.error('Error: `archon serve` is for compiled binaries only.');
     console.error('For development, use: bun run dev');
     return 1;
   }
   ```

## Counter / Caveats

- You need to return a value (even if always 0) so the type system / outer switch stay consistent.
- If your server's internal code calls `process.exit()` on fatal errors, it will bypass this mechanism. Audit for stray `process.exit()` calls in the server path.
- Multiple `once` handlers on the same signal are fine, but don't stack `on` — Node will call all registered handlers, which can fire cleanup multiple times.
- For a web server that receives cleanup requests via HTTP (K8s preStop hook), you may want an additional in-band shutdown path in addition to signals.
- On Windows, SIGTERM doesn't fire on `taskkill`; you get SIGBREAK from Ctrl+Break and SIGINT from Ctrl+C. Consider adding `SIGBREAK` to the listener set if you target Windows.

## Evidence

- `packages/cli/src/commands/serve.ts:74-77`:
  ```ts
  await new Promise<void>(resolve => {
    process.once('SIGINT', resolve);
    process.once('SIGTERM', resolve);
  });
  ```
  with comment "Block forever — Bun.serve() keeps the event loop alive, but the CLI's process.exit(exitCode) would kill it."
- Binary-only guard at `serve.ts:29-33` using `BUNDLED_IS_BINARY` from `@archon/paths`.
- Port validation at `serve.ts:21-27` returns `1` before any server work.
- Commit SHA: d89bc767d291f52687beea91c9fcf155459be0d9.
