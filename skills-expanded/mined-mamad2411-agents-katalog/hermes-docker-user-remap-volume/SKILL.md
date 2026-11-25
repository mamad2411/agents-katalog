---
name: hermes-docker-user-remap-volume
description: Docker entrypoint that remaps non-root UID/GID to match host volume ownership and bootstraps config files.
category: devops
version: 1.0.0
version_origin: extracted
tags: [docker, uid-gid, entrypoint, gosu, rootless]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/NousResearch/hermes-agent.git
source_ref: main
source_commit: 73bccc94c7af3a07b4002c2a14a4b54f844bd561
source_project: hermes-agent
imported_at: 2026-04-18T00:00:00Z
---

# Docker User-Remap Entrypoint with Volume Bootstrap

## Context

When a Docker image runs as a fixed UID (e.g. `useradd -u 10000`) but the user mounts a volume owned by a different UID, the container either can't write (permission denied) or writes files the host user can't later access. The fix is runtime UID remap + chown, with a safe fallback for rootless Podman.

## When to use

- Your image carries a non-root user with a built-in UID.
- Users mount `~/.myapp` or similar — ownership will vary across hosts.
- You also need to seed default config files (`.env`, `config.yaml`, `SOUL.md`) into the volume if missing.

## Procedure

### 1. Dockerfile installs `gosu` from an official source

```dockerfile
FROM tianon/gosu:1.19-trixie@sha256:... AS gosu_source
...
COPY --chmod=0755 --from=gosu_source /gosu /usr/local/bin/
```

(`Dockerfile:2,21`)

Using a pinned digest + multi-stage copy avoids trusting a mutable tag.

### 2. Bake a default non-root UID

```dockerfile
RUN useradd -u 10000 -m -d /opt/data hermes
ENV HERMES_HOME=/opt/data
VOLUME [ "/opt/data" ]
ENTRYPOINT [ "/opt/hermes/docker/entrypoint.sh" ]
```

### 3. Entrypoint: remap, chown, drop privs

```bash
#!/bin/bash
set -e
HERMES_HOME="${HERMES_HOME:-/opt/data}"
INSTALL_DIR="/opt/hermes"

if [ "$(id -u)" = "0" ]; then
    if [ -n "$HERMES_UID" ] && [ "$HERMES_UID" != "$(id -u hermes)" ]; then
        usermod -u "$HERMES_UID" hermes
    fi
    if [ -n "$HERMES_GID" ] && [ "$HERMES_GID" != "$(id -g hermes)" ]; then
        # -o allows non-unique GID (macOS GID 20 "staff" may exist
        # as "dialout" in the Debian container image)
        groupmod -o -g "$HERMES_GID" hermes 2>/dev/null || true
    fi
    actual_hermes_uid=$(id -u hermes)
    if [ "$(stat -c %u "$HERMES_HOME")" != "$actual_hermes_uid" ]; then
        chown -R hermes:hermes "$HERMES_HOME" 2>/dev/null || \
            echo "Warning: chown failed (rootless container?) — continuing"
    fi
    exec gosu hermes "$0" "$@"
fi
```

(`docker/entrypoint.sh:1-37`)

### 4. Rootless Podman: tolerate chown failure

In rootless Podman, the container's "root" is a host-side unprivileged UID mapped in. `chown` inside will fail — and that's fine; the volume is already owned by the mapped user on the host. The `|| echo Warning…` makes the entrypoint not abort on this expected failure.

### 5. `-o` on `groupmod` for non-unique GIDs

macOS users have GID 20 (`staff`). That collides with the Debian `dialout` group in the container. `groupmod -o` allows the remap anyway. Without it, the entire bind mount becomes unusable for Mac users.

### 6. After privilege drop: bootstrap the volume

Run as `hermes`, activate venv, then seed default files if they don't exist:

```bash
source "${INSTALL_DIR}/.venv/bin/activate"

mkdir -p "$HERMES_HOME"/{cron,sessions,logs,hooks,memories,skills,skins,plans,workspace,home}

[ ! -f "$HERMES_HOME/.env" ]        && cp "$INSTALL_DIR/.env.example"         "$HERMES_HOME/.env"
[ ! -f "$HERMES_HOME/config.yaml" ] && cp "$INSTALL_DIR/cli-config.yaml.example" "$HERMES_HOME/config.yaml"
[ ! -f "$HERMES_HOME/SOUL.md" ]     && cp "$INSTALL_DIR/docker/SOUL.md"       "$HERMES_HOME/SOUL.md"

# Sync bundled skills into the mounted volume without clobbering user edits
python3 "$INSTALL_DIR/tools/skills_sync.py"

exec hermes "$@"
```

Note the `home/` directory: it exists so subprocesses (`git`, `ssh`, `gh`, `npm`) have a per-profile `$HOME` that isn't `/root`. Without it they'd write into ephemeral, shared container state. See `docker/entrypoint.sh:42-49` and referenced issue #4426.

### 7. Place Playwright / large caches outside the volume

```dockerfile
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/hermes/.playwright
```

Volume mounts overlay the image's files at that path, so browsers installed at build time get hidden behind the mount unless you redirect the install path.

## Pitfalls

- **Don't chown inside rootless Podman without the fallback.** It will hard-fail and exit 1.
- **Don't forget `-o` on `groupmod`.** It's the single most common "why doesn't the Mac user's volume work" bug.
- **Keep the default UID stable across releases** — changing 10000 → 1000 later is a breaking change for existing volumes.
- **Do not pre-create cache/app-specific subdirs** in the entrypoint. Let the app populate them on demand so the layout stays in one place (`get_hermes_dir()` in the app code).
