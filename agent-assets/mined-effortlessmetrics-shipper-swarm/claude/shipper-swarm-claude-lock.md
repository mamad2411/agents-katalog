# Module: `crate::ops::lock`

**Layer:** ops (layer 1, bottom)
**Single responsibility:** Advisory file-based lock that prevents concurrent `shipper` runs from operating on the same workspace/state directory.
**Was:** standalone crate `shipper-lock` (absorbed during decrating Phase 2).

The lock is a JSON file in the state directory (default `.shipper/lock`) that
records the PID, hostname, `acquired_at` timestamp, and optional `plan_id` of
the holder. Acquisition is via atomic `File::create` + `fs::rename` after a
check-then-create. Release happens on `Drop` (best effort) or via
`LockFile::release()`. A stale-lock timeout path (`acquire_with_timeout`) lets
callers reclaim locks whose holders died without releasing.

## Public-to-crate API

Re-exported at `shipper::lock` (preserved backward compatibility with the old
`shipper-lock` public surface; callers in `shipper-cli` and the integration
tests use the `shipper::lock::*` path).

- `LOCK_FILE` — default lock filename constant.
- `LockInfo` — serde struct written to the lock file.
- `LockFile` — RAII handle; `acquire`, `acquire_with_timeout`, `release`,
  `set_plan_id`, `is_locked`, `read_lock_info`.
- `lock_path(state_dir, workspace_root)` — resolves the concrete lock path,
  with an optional `DefaultHasher`-derived suffix when `workspace_root` is
  `Some` (so multiple workspaces sharing a state dir don't collide).

## Invariants & gotchas

- **Not a true atomic mutex.** `acquire` does a check-then-create which races
  under concurrent contention. The engine relies on workspace-level cooperation,
  not OS-level file locking. See `concurrent_acquire_only_one_succeeds` — at
  least one thread is guaranteed to win, but more than one *may* succeed in a
  tight race. Callers that need strict mutual exclusion should layer their own
  guard on top (or switch to OS advisory locks — a deliberate future option).
- **Write-then-rename** is used to publish the lock atomically inside a single
  filesystem. `fsync` of the parent dir is attempted but ignored on failure.
- **`Drop` is best-effort.** If the file is externally removed, `release`
  silently succeeds; `set_plan_id` on a released lock returns an error.
- **Stale-lock detection is wall-clock based.** `acquire_with_timeout`
  compares `Utc::now() - acquired_at` to the configured timeout. A lock whose
  age is *exactly* the timeout is NOT considered stale (strictly `>`). Corrupt
  lock files are treated as stale by `acquire_with_timeout` but as errors by
  plain `acquire`.
- **`lock_path` hash is `DefaultHasher`.** Stable for a single Rust build but
  NOT guaranteed across versions; collisions are extremely rare but possible.
  This is fine for the workspace-disambiguation use case it serves.

## Architectural notes

- Layer-1 pure I/O. Must not import from `engine`, `plan`, `state`, or
  `runtime` (enforced by `.github/workflows/architecture-guard.yml`).
- No async. Synchronous filesystem calls only.
- Dependencies: `anyhow`, `serde`, `serde_json`, `chrono`, `gethostname`.
