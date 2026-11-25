---
name: docker-entrypoint-gosu-bind-mount
description: Write a Docker ENTRYPOINT that `mkdir -p`s required subdirs on first run, `chown`s them, then drops from root to a non-root user with `gosu` — so bind mounts "just work" and named volumes keep their inherited perms.
category: docker
version: 1.0.0
version_origin: extracted
tags: [docker, entrypoint, gosu, bind-mount, non-root, privileges]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/coleam00/Archon.git
source_ref: dev
source_commit: d89bc767d291f52687beea91c9fcf155459be0d9
source_project: Archon
imported_at: 2026-04-18T00:00:00Z
---

# Docker ENTRYPOINT: `mkdir -p` Subdirs + `gosu` Drop to Non-Root

## When to use

- You ship a Docker image that expects a persistent data directory (e.g. `/.archon/`) and users mount it via **either** named volume **or** bind mount.
  - Named volumes inherit the image-layer's perms/ownership on first use — fine.
  - Bind mounts do **not** — they start with whatever perms the host directory has. Subdirs that the image baked in are **gone**, and your container's non-root user typically can't write them.
- A naive fix "run container as root" is a security regression. Tools like Claude Code explicitly refuse to run as root with `--dangerously-skip-permissions`.
- You want one image that boots correctly under both mount styles, for root and non-root container invocations.

## Steps

1. **Install `gosu`** in the image (Debian-based: `apt-get install -y gosu`). It's a minimal setuid-like helper that drops privileges cleanly — unlike `su` / `sudo`, it doesn't fork a subshell or interfere with signals.

2. **Write `docker-entrypoint.sh`** that (in order):
   - `set -e` for strict error handling.
   - `mkdir -p` every subdirectory your app needs inside the mount point. This is the whole point — named volumes copy these from the image, bind mounts don't.
   - Detect whether we're root: `if [ "$(id -u)" = "0" ]`. If yes:
     - `chown -Rh <user>:<user> /mount` (with a clear error message on failure: "volume may be read-only or mounted with incompatible options"; `exit 1`).
     - Set `RUNNER="gosu appuser"`.
   - Otherwise (already non-root via `--user` or K8s `securityContext`):
     - Set `RUNNER=""`.

3. **Do any auth / setup steps as the target user** via `$RUNNER`:
   - `$RUNNER git config --global …` — configure git as appuser if you need per-user settings.
   - `$RUNNER bun run setup-auth` — run one-shot auth setup.

4. **`exec $RUNNER <main-command>`** — the `exec` replaces the shell so the main process becomes PID 1 and receives SIGTERM directly, enabling graceful shutdown. Without `exec`, the shell swallows signals.

5. **Handle CRLF on Windows hosts.** `COPY docker-entrypoint.sh /usr/local/bin/` followed by `RUN sed -i 's/\r$//' /usr/local/bin/docker-entrypoint.sh && chmod +x`. This prevents `/bin/bash^M: bad interpreter` errors when the repo is cloned on Windows without `core.autocrlf=input`.

6. **Pre-configure `safe.directory`** for git operations if the mount will contain git repos owned by a different UID than the container user. Example:

   ```dockerfile
   RUN gosu appuser git config --global --add safe.directory '/.archon/workspaces' \
    && gosu appuser git config --global --add safe.directory '/.archon/workspaces/*' \
    && gosu appuser git config --global --add safe.directory '/.archon/worktrees' \
    && gosu appuser git config --global --add safe.directory '/.archon/worktrees/*'
   ```

   This prevents "fatal: detected dubious ownership" errors when bind mounts have non-appuser UIDs.

7. **Use a credential helper for tokens**, not `~/.gitconfig`. Archon embeds a bash function so `GH_TOKEN` stays in env, never in a file:

   ```bash
   $RUNNER git config --global credential."https://github.com".helper \
     '!f() { echo "username=x-access-token"; echo "password=${GH_TOKEN}"; }; f'
   ```

## Counter / Caveats

- Don't `chown` every file on the volume — `-R` on a large mount (many GB) adds seconds to boot. `-Rh` follows no symlinks, which is usually what you want. If boot time matters, chown **only** the known subdirs you `mkdir`ed.
- `gosu` is **not** `su` and **not** `sudo`. It doesn't run PAM, doesn't spawn a login shell, doesn't alter env vars. That's the feature, not a bug.
- If you want the container to run fully read-only (`docker run --read-only`), the entrypoint's `mkdir -p` needs a writable subdirectory (tmpfs mount on `/mount/tmp`), or you need to pre-create everything in the image and skip the chown step.
- When running in Kubernetes with `securityContext.fsGroup`, the cluster may already fix ownership on bind-equivalent mounts, making your chown redundant but not harmful. Keep the check for portability.
- Don't call `chown -R` when the mount might be read-only (ConfigMap / secrets volume). Guard with `if ! chown … 2>/dev/null` and exit with a clear message.

## Evidence

- `docker-entrypoint.sh` (32 lines): full script with `set -e`, `mkdir -p`, root-detect + `chown -Rh`, `RUNNER=""` fallback, credential-helper-as-bash-function for GH_TOKEN, `exec $RUNNER`.
- `Dockerfile`:
  - `gosu` in system install at line 67-77.
  - Non-root user creation + data-dir perms at lines 119-126.
  - `safe.directory` pre-configuration at lines 175-179.
  - CRLF strip at lines 182-185.
- Commit SHA: d89bc767d291f52687beea91c9fcf155459be0d9.
