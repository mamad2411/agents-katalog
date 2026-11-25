---
name: hash-based-worktree-port
description: Deterministically pick a unique TCP port per git-worktree path by hashing the path to a fixed offset range, so parallel dev servers don't collide.
category: bun
version: 1.0.0
version_origin: extracted
tags: [bun, worktree, port-allocation, dev-server, determinism]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/coleam00/Archon.git
source_ref: dev
source_commit: d89bc767d291f52687beea91c9fcf155459be0d9
source_project: Archon
imported_at: 2026-04-18T00:00:00Z
---

# Hash-Based Deterministic Port per Git Worktree

## When to use

- Your tool is developed in a polyrepo / parallel-worktree style (multiple git worktrees of the same repo checked out at once).
- Each worktree runs its own dev server (`bun run dev`, Vite, Hono, etc.).
- You want each worktree to get a **stable, deterministic, unique** port so you can script `curl localhost:<port>` or have editor integrations remember per-worktree URLs.
- Randomizing or auto-increment-on-EADDRINUSE is awkward because the port changes between dev-server restarts.

## Steps

1. **Detect worktree-ness** first. Use `git rev-parse --show-toplevel` or a `isWorktreePath(cwd)` helper that checks whether CWD's `.git` is a **file** (worktree pointer) vs. a directory (main clone). Skip the hash and use your base port when not in a worktree.
2. **Honor an explicit `PORT` env var override** with full validation (must be integer, 1–65535). Log-and-exit on invalid rather than silently defaulting, so misconfigured CI surfaces loudly.
3. **Compute the offset from an MD5 hash** of the absolute worktree path. Take the first 2 bytes of the digest as a uint16 and map into a fixed 900-wide window:

   ```ts
   function calculatePortOffset(path: string): number {
     const hash = createHash('md5').update(path).digest();
     return (hash.readUInt16BE(0) % 900) + 100; // 100..999
   }
   ```

   Final port = `basePort + offset`. With `basePort = 3090`, Archon allocates into `3190..4089`.

4. **Log the allocation on startup** as structured fields (`{ cwd, port, basePort, offset }`) — this is the developer's first and only signal about which port is active.
5. **Co-locate the logic in a utility module** (`port-allocation.ts`) separate from the server entry so tests can import it without triggering app boot.

MD5 is the right primitive here: it's cheap, stable across runtimes, produces uniform distribution on arbitrary path strings, and has no cryptographic sensitivity (nobody is attacking your port choice).

## Counter / Caveats

- **Collisions exist.** 900 slots means the birthday bound is ~37 paths before a collision is >50% likely. In practice a single developer rarely has >10 active worktrees; if you do, fall back to a list of known worktrees and assign sequentially.
- The port changes if you **move** a worktree (e.g. rename the parent directory). That is usually desirable — a moved worktree is essentially a new worktree — but document it so users don't panic.
- Pair this with a frontend proxy fallback: Archon's Vite config in `packages/web/vite.config.ts` defaults to `3090` so the web dev-server still works when the backend isn't running in a worktree.
- Don't use the hash allocation when `PORT=` is set — explicit beats derived.

## Evidence

- `packages/core/src/utils/port-allocation.ts` (62 lines): full implementation including MD5 hash + `isWorktreePath` detection + PORT env var validation.
- Range: 3190..4089 (`basePort = 3090`, offset 100..999). Base rationale: it matches the Vite proxy fallback in `packages/web/vite.config.ts`.
- `CLAUDE.md`:507-536 (section "Running the App in Worktrees"): docs the pattern with a sample log line "Auto-allocated port: 3637 (base: 3090, offset: +547)".
- Commit SHA: d89bc767d291f52687beea91c9fcf155459be0d9.
