# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Check compilation
cargo check -p rocket-git

# Run all tests for this crate
cargo test -p rocket-git

# Run a specific test
cargo test -p rocket-git <test_name>

# Run tests with output
cargo test -p rocket-git -- --nocapture
```

## Architecture

`rocket-git` is a pure domain crate — no I/O wiring, no Tauri, no async. It defines the git abstraction layer used by the broader Rocket API client.

### Trait + Implementation pattern

`GitService` (`service.rs`) is the public trait used by consumers. `Git2Service` (`git2_service.rs`) is the only implementation, backed by `libgit2` via the `git2` crate (with SSH support).

All methods take a `path: &str` argument — the repository root on disk. There is no persistent repository handle; `Repository::open()` is called per-operation.

### Domain types

Each module owns its types and re-exports them via `lib.rs`:

| Module | Types |
|---|---|
| `status` | `GitStatus` (enum), `FileStatus`, `RepoStatus` |
| `diff` | `FileDiff`, `DiffHunk`, `DiffLine`, `LineType` |
| `branch` | `Branch`, `BranchList` |
| `commit` | `CommitInfo` |
| `stash` | `StashEntry` |
| `conflict` | `ConflictFile`, `ConflictResolution` |
| `credentials` | `GitCredentials` (enum: SshKey, SshAgent, UserPass, Token) |
| `remote` | `RemoteInfo` |

All types derive `Serialize`/`Deserialize` with `camelCase` field names (for Tauri IPC). Enums use `lowercase` variant names.

### Key implementation details

- **Status**: A file with both staged and unstaged changes emits two separate `FileStatus` entries (one with `staged: true`, one with `staged: false`).
- **Diff**: Uses a simplistic all-removals-then-all-additions approach in a single hunk (`build_simple_diff`). Not a proper Myers diff.
- **Commit signature**: Requires git config user identity (user.name and user.email) — no fallback. If missing, operations return a `DomainError::Internal`.
- **Pull**: Implements fetch + fast-forward or merge commit. On conflicts, writes the index and returns `Ok(())`, leaving the repo in merge-in-progress state for the frontend to resolve.
- **Conflict resolution**: `ConflictResolution` supports `Ours`, `Theirs`, or `Custom { content }`. Resolution writes the file, stages it, and clears the conflict marker in the index.

### Testing

Tests live in `#[cfg(test)]` blocks within each module. All integration tests use `tempfile::TempDir` for ephemeral repos. The `setup_repo()` helper in `git2_service.rs` creates a repo with an initial commit on `main` — call it directly in new tests rather than duplicating the setup.
