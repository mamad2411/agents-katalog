# Module: `crate::ops::git`

**Layer:** ops (layer 1, bottom)
**Single responsibility:** Git repository operations — cleanliness check, context capture for receipts.
**Was:** standalone crate `shipper-git` + in-tree `shipper/src/git.rs` shim wrapper (both absorbed during decrating Phase 2).

## Public-to-crate API

Re-exported at `shipper::git` (preserved backward compatibility with the old shim):

- `collect_git_context() -> Option<crate::types::GitContext>` — populate a
  `GitContext` for the current working directory. Returns `None` when the CWD
  is not inside a git repo. Defined in `mod.rs`.
- `is_git_clean(repo_root: &Path) -> anyhow::Result<bool>` — porcelain-status
  check. Treats any untracked, staged, or modified file as dirty.
- `ensure_git_clean(repo_root: &Path) -> anyhow::Result<()>` — fail fast if
  the working tree is dirty. Error phrasing:
  `"git working tree is not clean; commit/stash changes or use --allow-dirty"`
  (pinned by the `shipper-cli` snapshot tests).

Crate-internal helpers live in the sibling sub-modules:

- `cleanliness.rs` — `is_git_clean`/`ensure_git_clean` (canonical CLI error
  phrasing) plus `ensure_git_clean_legacy` (the original shipper-git error
  wording, still referenced by the preserved snapshot tests).
- `context.rs` — commit/branch/tag/changed-files/remote queries and the
  aggregator `get_git_context`. Also retains the ORIGINAL shipper-git
  `is_git_clean` / `ensure_git_clean` with the legacy error phrasing (used by
  this module's own tests; the outer facade in `cleanliness.rs` supersedes
  them for public callers).
- `bin_override.rs` — `SHIPPER_GIT_BIN` routing: `git_program`, `is_repo_root`,
  `local_is_git_clean`, plus parallel implementations of commit / branch / tag /
  dirty helpers that honor the override.

## Invariants

- **`SHIPPER_GIT_BIN` env var** overrides the git executable path (useful for
  tests and sandboxed environments). `git_program()` returns the env value
  verbatim (including empty strings, to preserve pre-absorption behavior).
- **Error-text compatibility.** The outer `is_git_clean` wrapper prefixes the
  underlying error with an extra `git status failed:` string; the CLI snapshot
  tests assert against the doubled prefix (`git status failed: git status
  failed: …`). Do not change this wording without updating
  `crates/shipper-cli/tests/snapshots/e2e_expanded__preflight_*.snap`.
- **Short commit slicing.** `GitContext::short_commit` on `shipper-types`
  slices by BYTE index (not char index). This matches the original
  `shipper-git` crate — commit hashes are always ASCII hex so byte = char, but
  arbitrary inputs shorter than 7 bytes are returned verbatim.
- **Collector is override-strict.** When `SHIPPER_GIT_BIN` is set,
  `collect_git_context` uses only the override helpers; there is no silent
  fallback to the default `git` binary for any sub-query.
- **`is_dirty()` default.** When `GitContext::dirty` is `None`, `is_dirty()`
  returns `true` (treat unknown as dirty) — matches the safe-by-default
  semantics pre-absorption.

## Architectural notes

- Layer-1 pure I/O. Must not import from `engine`, `plan`, `state`, or
  `runtime` (enforced by `.github/workflows/architecture-guard.yml`).
- Depends only on `crate::types::GitContext` (re-exported from
  `shipper-types`) and external crates (`anyhow`).
- All subprocess spawning uses `std::process::Command` directly (pre-existing
  behavior; migration to `crate::ops::process` is out of scope for this
  absorption).
