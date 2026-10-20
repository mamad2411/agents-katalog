---
name: infra-docker-images
description: Use when choosing or writing Dockerfiles — base-image strategy, multi-stage builds, distroless, scratch, size vs supply-chain.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [infra-docker-compose, infra-docker-swarm, ci-github-actions, ci-gitlab-ci]
---

# Infra Docker Images

**Iron Law: Debian by default. Multi-stage always. Distroless or `scratch` for the runtime stage of static binaries. Pin to digests in highest-stakes envs. NEVER `:latest` in any non-local file.**

**Versions:** Docker Engine `27.x` (current) · BuildKit (default since 23.0) · Compose v2 plugin.

## Base-image default: Debian, not Alpine

Reach for Debian (`*-slim`, `*-trixie-slim`, `python:3.X-slim`, `node:22-slim`) first. Alpine is acceptable only after you've audited compatibility. The reasoning, in priority order:

| Concern          | Debian                                                                         | Alpine                                                                                                                             |
| ---------------- | ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| libc             | glibc — what every prebuilt binary, manylinux wheel, and Go cgo target expects | musl — incompatible with manylinux wheels; rebuilds from source on `pip install`                                                   |
| Python wheels    | install in seconds                                                             | `psycopg`, `pillow`, `pyvips`, `numpy`, `scipy`, `cryptography` rebuild from source unless `*-musllinux` wheels exist (many don't) |
| Go cgo           | `CGO_ENABLED=1` linking just works                                             | musl static-link gymnastics; DNS resolver edge cases (`GODEBUG=netdns=cgo+2` doesn't apply)                                        |
| DNS / networking | glibc NSS, `/etc/resolv.conf` works                                            | musl's resolver doesn't read `search`, no parallel A/AAAA, bugs around CNAME chains                                                |
| Image size       | `*-slim` is 50-80 MB; `distroless-debian12` is 20-30 MB                        | 5-15 MB                                                                                                                            |
| Supply chain     | Debian security team is large, fast, mature                                    | Alpine team is smaller; CVE fix cadence varies                                                                                     |
| TLS roots        | `ca-certificates` package present                                              | present but `apk add --no-cache ca-certificates` step often forgotten                                                              |
| Debugging        | `bash`, `apt`, `procps`, `coreutils` available in `-slim`                      | `ash`/`busybox`; missing flags trip you up under load                                                                              |

**When Alpine is fine:**

- Pure-static Go binary going into Alpine for the cert bundle (or use `scratch` + manual cert copy)
- Pure-JS Node app with no native deps (no `bcrypt`, no `sharp`, no `better-sqlite3`)
- You measured and image size dominates everything else (rare; pull bandwidth is cheap, build time isn't)

**When Alpine is wrong** (don't argue, just use Debian):

- Anything Python with `numpy`/`pandas`/`polars`/`scipy`/`pillow`/`pyvips`/`psycopg`/`cryptography`
- Anything Node with `node-gyp`-built deps (`bcrypt`, `sharp`, `canvas`, `better-sqlite3`)
- Anything cgo-linked Go (sqlite via `mattn/go-sqlite3`, image libs)
- Anything that has to do DNS to AWS/GCP private zones

## Multi-stage: always

```dockerfile
# syntax=docker/dockerfile:1.7   # buildkit features

# ---- builder ----
FROM golang:1.26-trixie AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go mod download
COPY . .
RUN --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /out/api ./cmd/api

# ---- runtime ----
FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=builder /out/api /api
USER nonroot
EXPOSE 8080
ENTRYPOINT ["/api"]
```

- BuildKit cache mounts (`--mount=type=cache`) — keep module/build caches across builds without committing them to layers.
- Pin builder base by major/minor (`golang:1.26-trixie`). Pin runtime by digest in prod (`gcr.io/distroless/static-debian12@sha256:...`).
- `CGO_ENABLED=0` if you can — gives you `scratch`/distroless runtime targets.

## Runtime image picker

| Workload                                              | Use                                                                               | Why                                                           |
| ----------------------------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Static Go / Rust binary                               | `gcr.io/distroless/static-debian12:nonroot` or `scratch` (with manual CA bundle)  | ~20 MB, no shell, no package manager — minimal attack surface |
| Go/Rust with TLS to public internet                   | `gcr.io/distroless/static-debian12:nonroot`                                       | ca-certificates already present                               |
| Go cgo / C extensions                                 | `gcr.io/distroless/base-debian12:nonroot`                                         | glibc + libssl + ca-certificates                              |
| Python app                                            | `gcr.io/distroless/python3-debian12:nonroot` for prod, `python:3.14-slim` for dev | distroless if no `apt install` at runtime                     |
| Node app                                              | `gcr.io/distroless/nodejs22-debian12:nonroot` for prod, `node:22-slim` for dev    | distroless drops npm, shell, package manager                  |
| Anything needing a shell (cron entrypoint, debugging) | `python:3.14-slim` / `node:22-slim` / `debian:trixie-slim`                        | accept the size; you need `sh`                                |

Distroless `:debug` tag includes busybox — only for triage, never the default.

## `scratch` for the truly minimal

```dockerfile
FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /out/api /api
ENTRYPOINT ["/api"]
```

`scratch` = nothing. No `/tmp`, no `/etc/passwd`, no DNS resolver config (Go uses cgo+netdns by default — set `GODEBUG=netdns=go` or stick to distroless). Use only when you've measured and the ~20 MB savings vs distroless matter.

## `.dockerignore` is required

```
.git
.github
.gitlab-ci.yml
node_modules
__pycache__
.venv
dist
build
.next
target
*.md
tests/fixtures/large/
```

Without `.dockerignore` you ship the entire repo into the build context — slow uploads, larger images, secrets leaks (think `.env`, `.git/config`).

## Reproducibility

```dockerfile
# Pin by digest, not tag, when reproducibility matters
FROM debian:trixie-slim@sha256:8c25c5e7ee...
```

Tags move. Digests don't. Use [Docker scout / Trivy / grype] to scan the digest you pinned, not the tag you read.

## Buildx for multi-arch

```bash
docker buildx create --use --name multiarch
docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/me/api:v1.4.2 --push .
```

Always test on both arches if you have any chance of running on Apple Silicon dev → x86 prod. Native compilation per platform; QEMU emulation is slow but works.

## Common patterns

**Python with `uv`:**

```dockerfile
FROM python:3.14-slim AS builder
# Prod: pin by digest (the Iron Law). `0.5` works for local dev but a force-pushed
# tag would compromise this build stage (which runs with mounted secrets).
COPY --from=ghcr.io/astral-sh/uv@sha256:<resolve-with-`docker buildx imagetools inspect ghcr.io/astral-sh/uv:0.5`> /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project
COPY . .
RUN uv sync --frozen --no-dev

FROM python:3.14-slim
COPY --from=builder /app /app
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT ["python", "-m", "myapp"]
```

**Node with pnpm:**

```dockerfile
FROM node:22-slim AS builder
RUN corepack enable && corepack prepare pnpm@latest --activate
WORKDIR /app
COPY pnpm-lock.yaml package.json ./
RUN --mount=type=cache,target=/root/.local/share/pnpm/store pnpm install --frozen-lockfile
COPY . .
RUN pnpm build

FROM gcr.io/distroless/nodejs22-debian12:nonroot
COPY --from=builder /app/dist /app
WORKDIR /app
CMD ["index.js"]
```

## Anti-patterns

- `FROM ubuntu:latest` + 14 `RUN apt install` lines + `COPY . .` at the top — one-stage, no cache, no slim base, no pin
- `:latest` anywhere outside local dev
- `RUN apt-get update && apt-get install -y X` without `&& rm -rf /var/lib/apt/lists/*`
- Running as root in the runtime image — every distroless image has a `:nonroot` variant; use it
- Forgetting `.dockerignore` and shipping `.git`/`node_modules`/`.venv` into the image
- Alpine + manylinux Python wheels — debugging musl-resolver weirdness in prod at 3am
- Pinning by tag (`postgres:17`) but never running `docker pull` in CI — stale layers diverge from prod
- One giant `RUN` doing 30 things — layer cache invalidates entire chain on any change

## Red flags

| Thought                                  | Reality                                                                                                                   |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| "Alpine is 5MB smaller, let's use it"    | You'll spend 4 hours on a musl-resolver bug; the 5MB cost less than 0.01% of your egress bill                             |
| "We don't need distroless, slim is fine" | Slim has `bash`, `apt`, `dpkg`. Distroless removes the attack surface for free. Use distroless unless you need the shell. |
| "I'll add `.dockerignore` later"         | `.env` is already in your registry; rotate everything                                                                     |
| "Just one `RUN` to keep layers down"     | Cache invalidates on every change; build time goes from 30s to 5min                                                       |
| "Multi-arch is overkill"                 | First Apple Silicon dev clone says otherwise                                                                              |

## Hand-off

For compose/swarm wiring of these images: `Skill(infra-docker-compose)`, `Skill(infra-docker-swarm)`. For build pipelines: `Skill(ci-github-actions)`, `Skill(ci-gitlab-ci)`. For supply-chain scanning (SBOM, secrets): `Skill(security)`.
