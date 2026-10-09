---
name: artifact-fs
description: Mounts Git remotes with ArtifactFS as local working trees without a full clone. Use when asked to mount a remote repo, explain committed state versus dirty overlay state, or mount multiple repos under one daemon.
---

# ArtifactFS Usage

Use this skill to operate ArtifactFS as a consumer. Prefer the CLI workflow and mounted repos. Do not inspect ArtifactFS internals unless the task is about developing ArtifactFS itself.

## FIRST: Verify Prerequisites

Run from the repo root. If either check fails, STOP and fix the environment first.

```bash
test -e /Library/Filesystems/macfuse.fs || test -e /dev/fuse
test -x ./artifact-fs || go build -o artifact-fs ./cmd/artifact-fs
```

## Critical Rules

- **Use a dedicated state root.** Set `ARTIFACT_FS_ROOT`, usually under `/tmp`, so mounts and caches stay isolated.
- **Prefer HTTPS remotes.** For private repos, use Git credential helpers or SSH auth. Do not embed tokens or passwords in the `--remote` URL because `--remote` is a CLI arg and can show up in process listings.
- **`add-repo` does not mount.** It registers a blobless clone and exits. `daemon` mounts all registered repos and stays running.
- **The mounted tree starts from committed Git state.** Remote commits, trees, and refs are the base view. Local edits live in an overlay and appear as dirty state until committed.
- **One daemon can mount many repos.** Register each repo separately, then start one `daemon --root <mount-root>`.

## Quick Reference

| Task | Command |
|------|---------|
| Register one repo | `./artifact-fs add-repo --name <name> --remote <url> --branch <branch> --mount-root /tmp` |
| Mount all registered repos | `./artifact-fs daemon --root /tmp` |
| Check mount and overlay state | `./artifact-fs status --name <name>` |
| List registered repos | `./artifact-fs list-repos` |
| Unmount or remove a repo | `./artifact-fs unmount --name <name>` or `./artifact-fs remove-repo --name <name>` |

## Quick Start: One Repo

```bash
export ARTIFACT_FS_ROOT=/tmp/artifact-fs-demo

./artifact-fs add-repo \
  --name workers-sdk \
  --remote https://github.com/cloudflare/workers-sdk.git \
  --branch main \
  --mount-root /tmp

./artifact-fs daemon --root /tmp &
DAEMON_PID=$!

git -C /tmp/workers-sdk rev-parse HEAD
git -C /tmp/workers-sdk status
./artifact-fs status --name workers-sdk

kill $DAEMON_PID
# If a stale mount remains:
umount /tmp/workers-sdk
```

## Mount Semantics

- Base view = branch `HEAD` from the blobless clone. File contents hydrate on first read.
- Dirty files are overlay state, not part of the base commit. `./artifact-fs status --name <repo>` reports this as `overlay_dirty=true`.
- `git add` and `git commit` inside the mount are supported. After commit or checkout, the watcher re-indexes the new `HEAD` and reconciles stale overlay entries.

## Quick Start: Multiple Repos

```bash
export ARTIFACT_FS_ROOT=/tmp/artifact-fs-demo

./artifact-fs add-repo --name repo-a --remote https://github.com/org/repo-a.git --branch main --mount-root /tmp
./artifact-fs add-repo --name repo-b --remote https://github.com/org/repo-b.git --branch main --mount-root /tmp

./artifact-fs daemon --root /tmp &
DAEMON_PID=$!

ls /tmp/repo-a
ls /tmp/repo-b
./artifact-fs list-repos

kill $DAEMON_PID
umount /tmp/repo-a
umount /tmp/repo-b
```
