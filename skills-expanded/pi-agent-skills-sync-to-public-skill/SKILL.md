---
name: sync-to-public
description: Mirror a directory from a private repository's HEAD commit into a directory in a public repository and draft a single public commit message. The user must invoke this skill explicitly and provide both directories.
disable-model-invocation: true
---

# Sync to public

Mirror the source repository's current `HEAD` commit into a separate public repository, including deletions, then draft one commit message for the resulting public diff. Never copy staged, unstaged, ignored, or untracked source changes. Do not use tags, marker files, or other persistent sync state.

## Required input

The user must provide:

- `source`: directory inside a private source repository
- `destination`: directory inside a public destination repository

Accept named arguments or clear natural language. For example:

```text
/skill:sync-to-public source=~/.pi destination=~/config/pi
/skill:sync-to-public source=~/config/base destination=~/config/public/macos
```

If either directory is missing or ambiguous, ask for it before running commands. Resolve both to absolute paths and confirm they are different directories. Each may be the repository root or any directory beneath it.

## Workflow

1. Verify that `source` and `destination` exist within Git repositories. Resolve each containing repository root with `git -C directory rev-parse --show-toplevel` and each directory's path relative to that root.
2. Update both repositories from their configured upstream: run `git -C source_repository pull --ff-only` and `git -C destination_repository pull --ff-only`. `--ff-only` ensures each command either fast-forwards cleanly or aborts, never creating a merge commit, rebasing, or discarding local changes. If either pull fails — no upstream configured, diverged history, or a working-tree conflict — stop and report the failure rather than forcing, stashing, or resolving it automatically. Do not commit or push.
3. Resolve and report the source repository snapshot with `git -C source_repository rev-parse HEAD`. Always use this commit, even when the source working tree has staged, unstaged, ignored, or untracked changes. Verify that the requested source directory exists in that commit.
4. Require a clean destination repository working tree before copying. If it is dirty, stop and show the existing changes rather than mixing them with the sync.
5. Export the full source `HEAD` tree into a new temporary directory under `$TMPDIR`, then select the requested source directory inside that snapshot:

   ```bash
   snapshot_root="$(mktemp -d "$TMPDIR/sync-to-public.XXXXXX")"
   git -C source_repository archive HEAD | tar -x -C "$snapshot_root"
   snapshot_source="$snapshot_root/$source_relative_path"
   ```

   When `source` is the repository root, use `snapshot_root` as `snapshot_source`. `git archive` includes only files recorded by `HEAD`. It excludes working-tree changes, index-only changes, ignored files, untracked files, and `.git/` metadata.

6. Scan `snapshot_source` before copying. Proactively identify files that may contain secrets, personal data, machine-specific state, or user-scoped configuration. Check both suspicious paths and content, including:

   - `.env` files, credentials, auth state, cookies, sessions, private keys, certificates, tokens, and secret stores
   - files or fields named `secret`, `password`, `token`, `api_key`, `credential`, `private_key`, or similar
   - absolute home-directory paths, usernames, email addresses, account IDs, device names, trust entries, and per-project allowlists
   - editor state, histories, caches, OAuth state, local databases, telemetry identifiers, and machine-specific settings

   Use targeted filename searches and content searches rather than relying on one pattern. Report only file paths and the reason each file is suspicious; never print a discovered secret value. Treat matches as review candidates, not proof that a secret exists. Do not block or alter the mirror because of a match: copy the committed snapshot as requested, then prominently tell the user which destination files to review and remove or sanitize before committing or pushing.

7. Preview a mirror from `snapshot_source` to `destination`. Include deletions so the destination directory matches the committed source directory exactly. The containing destination repository and its `.git/` metadata remain intact:

   ```bash
   rsync -ain --delete --exclude='.git/' \
     "$snapshot_source/" destination_directory/
   ```

8. Show the source commit, safety-scan result, and mirror preview, then ask for confirmation before applying it. Deletions and overwrites are irreversible outside Git.
9. Apply the same operation without `-n` after confirmation:

   ```bash
   rsync -ai --delete --exclude='.git/' \
     "$snapshot_source/" destination_directory/
   ```

10. Review the complete destination diff. Check `git status`, `git diff --stat`, `git diff`, and staged changes if any. Repeat the public-safety review against added and modified destination content. Flag concerns prominently without printing secret values, but leave the mirrored files in place so the user can review and sanitize them.
11. Understand why the files changed. Start with the diff and source commit log for the changed paths. Use `git blame` only when the diff and log do not explain a non-obvious decision:

```bash
git -C source_directory log --oneline -- changed_paths
git -C source_directory blame -- relevant_file
```

12. Draft one clean commit message covering the entire destination diff. Write it as if the work had been developed directly in the public repository. Do not mention private history, syncing, mirroring, internal notes, or work-in-progress commits.
13. Show the destination status, diff summary, source commit, safety-scan result, and proposed commit message. List any files that must be reviewed or sanitized before publication. Do not stage, commit, or push unless the user explicitly asks.
14. Remove `snapshot_root` when the run finishes or stops.

## Commit message

Use an imperative subject that describes the main public-facing change. Add a body only when it explains important behavior or groups several related changes. Describe what changed and why, not the mechanics of copying files.
