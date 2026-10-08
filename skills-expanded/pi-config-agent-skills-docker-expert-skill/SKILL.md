---
name: docker-expert
description: 'Docker reference for the docker-expert subagent — Dockerfiles, BuildKit (incl. rootless), multi-stage, multi-platform, secret/cache mounts, Compose v2, container security.'
disable-model-invocation: true
---

# Docker Expert

Read-only reference for Docker guidance — BuildKit features, rootless builds, multi-stage patterns, cache optimization, security, and Compose v2.

## BuildKit Fundamentals

### Enabling BuildKit

| Method | Context |
|---|---|
| `DOCKER_BUILDKIT=1` env var | Legacy Docker Engine (<23.0) |
| Default in Docker Engine 23.0+ | No action needed |
| `docker buildx build` | Always uses BuildKit |

### `# syntax` Directive

```dockerfile
# syntax=docker/dockerfile:1
```

Must be the first line (before any comments or `ARG`). Required for BuildKit-only features like `--mount`. Without it, the legacy builder silently ignores mount flags.

### Version Pinning

| Directive | Behavior |
|---|---|
| `# syntax=docker/dockerfile:1` | Latest 1.x (recommended) |
| `# syntax=docker/dockerfile:1.7` | Pinned minor version |
| `# syntax=docker/dockerfile:1.7.1` | Pinned exact version |

## Rootless BuildKit

Rootless BuildKit is the default pattern for all image builds in this ecosystem. It runs the BuildKit daemon without root privileges.

### Setup

```bash
# Dependencies
sudo apt-get install -y uidmap slirp4netns

# Start rootless buildkitd
rootlesskit buildkitd --oci-worker-no-process-sandbox &

# Or use systemd user service
systemctl --user enable --now buildkit
```

### Socket Path

Rootless: `$XDG_RUNTIME_DIR/buildkit/buildkitd.sock`
System: `/run/buildkit/buildkitd.sock`

### Feature Support

| Feature | Rootless support | Notes |
|---|---|---|
| Image builds | Full | No limitations |
| Cache mounts | Full | — |
| Secret mounts | Full | — |
| Multi-platform (QEMU) | Requires setup | `tonistiigi/binfmt` must be run as root once |
| Overlay filesystem | Requires kernel 5.11+ | Falls back to `fuse-overlayfs` on older kernels |
| Privileged operations | Limited | Cannot bind ports <1024 without sysctl |

### Buildx Integration

```bash
docker buildx create \
  --name rootless \
  --driver remote \
  --driver-opt="addr=unix://$XDG_RUNTIME_DIR/buildkit/buildkitd.sock"
docker buildx use rootless
```

## Secret Mounts

### Usage

```dockerfile
# syntax=docker/dockerfile:1
RUN --mount=type=secret,id=mytoken \
    cat /run/secrets/mytoken | some-command

RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm install
```

```bash
docker buildx build --secret id=mytoken,src=./token.txt .
docker buildx build --secret id=mytoken,env=MY_TOKEN .
```

### Critical Trap

The `--mount=type=secret` syntax requires the `# syntax` directive. Without it, the legacy builder silently ignores the mount — the `RUN` executes but `/run/secrets/mytoken` does not exist. No error, no warning. Security risk if the command falls back to a default value.

Secrets exist only during the `RUN` instruction and are not committed to any layer.

## Cache Mounts

### Common Patterns

| Package manager | Cache target |
|---|---|
| apt | `/var/cache/apt`, `/var/lib/apt/lists` |
| pip | `/root/.cache/pip` |
| npm | `/root/.npm` |
| Go | `/go/pkg/mod`, `/root/.cache/go-build` |

### Sharing Modes

| Mode | Behavior | Use when |
|---|---|---|
| `shared` (default) | Multiple builds read/write concurrently | Most package managers |
| `locked` | Exclusive access, others wait | Compilers with non-atomic writes |
| `private` | Each build gets its own instance | Isolation needed |

### Cache ID

Default cache ID is the target path. Use `id=mycache` to share across different `RUN` instructions or Dockerfiles.

**Trap:** Cache mounts are NOT in the image layer. Data persists on the build host only. In CI, each run starts empty unless using BuildKit remote cache export/import.

## Multi-Stage Builds

### Patterns

| Pattern | Description |
|---|---|
| Builder + runtime | Compile in fat image, copy binary to minimal image |
| Test stage | `FROM builder AS tester` — build with `--target tester` in CI |
| Dev stage | Debug tools, hot-reload; never ship to production |
| Base stage | Shared setup, multiple children `FROM base` |

### `COPY --from` Ordering

Stages build in dependency order, not declaration order. BuildKit parallelizes independent stages. Always use named stages (`AS builder`) — numeric indices (`COPY --from=0`) break if stages are reordered.

## Multi-Platform Builds

### Build Command

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag myapp:latest \
  --push .
```

### Approach Comparison

| Approach | Speed | Complexity |
|---|---|---|
| QEMU emulation | Slow (10-50x) | Automatic with `tonistiigi/binfmt` |
| Cross-compilation | Native speed | Requires cross-compile toolchain |
| Remote native builders | Native speed | Requires remote `buildx create` nodes |

### Platform Variables

```dockerfile
FROM --platform=$BUILDPLATFORM golang:1.22 AS builder
ARG TARGETPLATFORM TARGETOS TARGETARCH
RUN GOOS=$TARGETOS GOARCH=$TARGETARCH go build -o /app .
```

Use `FROM --platform=$BUILDPLATFORM` to pin build stages to host architecture for cross-compilation.

## Security Patterns

### Non-Root USER

```dockerfile
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser
USER appuser
```

Or use distroless images with built-in `nonroot` user (UID 65534).

### COPY vs ADD

- `COPY` — copies from build context. Predictable.
- `ADD` — also extracts tars and fetches URLs. Avoid unless extraction is needed.

### `.dockerignore`

```gitignore
.env
.env.*
*.key
*.pem
credentials/
.git
node_modules
```

### Runtime Security

| Feature | Flag | Effect |
|---|---|---|
| Read-only filesystem | `--read-only` | Prevents writes (use tmpfs for /tmp) |
| No new privileges | `--security-opt=no-new-privileges` | Blocks setuid/setgid |
| Drop capabilities | `--cap-drop=ALL` | Remove all Linux capabilities |
| Add specific caps | `--cap-add=NET_BIND_SERVICE` | Add only what is needed |

## Compose v2

### v1 to v2 Differences

| Aspect | v1 (`docker-compose`) | v2 (`docker compose`) |
|---|---|---|
| Binary | Standalone Python | Docker CLI plugin (Go) |
| Container naming | `project_service_1` | `project-service-1` (hyphens) |
| `depends_on` health | Limited | Full `condition: service_healthy` |
| Profiles | Not supported | Supported |
| `watch` for dev | Not supported | `docker compose watch` |
| BuildKit | Requires env var | Default |

### Health Check Dependencies

```yaml
services:
  db:
    image: postgres:16
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
  app:
    depends_on:
      db:
        condition: service_healthy
```

### Profiles

```yaml
services:
  debug:
    image: busybox
    profiles: ["debug"]
    # Only starts with: docker compose --profile debug up
```

## Dockerfile Best Practices

### Layer Ordering

1. Base image (changes rarely)
2. System dependencies (changes occasionally)
3. Application dependency files (lockfile copy)
4. Dependency install (cached unless lockfile changes)
5. Application code (changes frequently)
6. Runtime config (USER, EXPOSE, CMD)

### `ARG` Scoping

`ARG` before `FROM` is available in the `FROM` line only. `ARG` after `FROM` is available in that build stage. Pre-FROM ARGs must be redeclared (without default) after `FROM` to use them in the stage.

### Heredoc Syntax

```dockerfile
# syntax=docker/dockerfile:1
RUN <<EOF
apt-get update
apt-get install -y nginx
rm -rf /var/lib/apt/lists/*
EOF
```

### HEALTHCHECK

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1
```
