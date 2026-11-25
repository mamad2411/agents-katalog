---
name: devops-containers
description: "Container images that are small, safe and reproducible: multi-stage Dockerfiles, base image choice, pinned versions, a non-root user, layer order for caching, .dockerignore, health checks, signals and PID 1, build secrets, multi-arch builds, scanning, and Compose for local development. Read before writing or changing a Dockerfile or a compose file."
---

# Container images

The generated Dockerfile starts `FROM node:latest`, copies the whole folder
(`.git`, `.env` and `node_modules` included) before installing, runs
`npm install` and `npm run dev` as root, bakes an API key into `ENV`, and ships
a 1.5 GB image full of compilers. Every code change reinstalls every
dependency, and `docker stop` waits ten seconds and kills it mid-request. This
is how to build images that rebuild in seconds from cache, run unprivileged,
carry only the runtime, stop cleanly and can be rebuilt the same way next
year. One part of devops; the whole is in the `devops` skill.

## 1. Build stage, runtime stage

A builder stage holds the toolchain, the runtime stage only the artefact and
what it needs to run. `# syntax=docker/dockerfile:1` first (cache and secret
mounts); keep the project's package manager, entry point and port.

```dockerfile
# syntax=docker/dockerfile:1
# Node with pnpm (the pattern from pnpm's docs; its image is Debian trixie)
FROM ghcr.io/pnpm/pnpm:12 AS base
RUN pnpm runtime set node 24 -g
WORKDIR /app
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml* ./

FROM base AS prod-deps
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --prod --frozen-lockfile

FROM base AS build
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile
COPY . .
RUN pnpm run build

FROM node:24-trixie-slim
ENV NODE_ENV=production
WORKDIR /app
COPY --from=prod-deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
COPY package.json ./
USER 1000:1000
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

- The runtime's Debian release matches the build stage's, or native modules
  fail with `GLIBC_2.xx not found`: `node:24-slim` is still bookworm, the pnpm
  image is trixie, so the runtime names `trixie`.
- npm: `npm ci` in the build stage, `npm ci --omit=dev` in the deps stage,
  cache mount `target=/root/.npm`. Workspaces: install after `COPY . .`, then
  `pnpm deploy --filter=<app> --prod /out` and copy `/out`.
- Next.js: `output: "standalone"`, copy `.next/standalone`, `.next/static`
  and `public`, run `node server.js` with `HOSTNAME=0.0.0.0`. Node 24 is the
  active LTS until Node 26 takes over on 28 October 2026.

```dockerfile
# syntax=docker/dockerfile:1
# Python with uv: same base in both stages, the venv is not relocatable
FROM python:3.14-slim AS build
COPY --from=ghcr.io/astral-sh/uv:0.12.20 /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_NO_DEV=1 UV_PYTHON_DOWNLOADS=0
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked

FROM python:3.14-slim
RUN useradd --system --uid 10001 --no-create-home app
WORKDIR /app
COPY --from=build /app /app
ENV PATH="/app/.venv/bin:$PATH"
USER 10001:10001
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# syntax=docker/dockerfile:1
# Go: cross-compiled on the build machine's platform, static, distroless
FROM --platform=$BUILDPLATFORM golang:1.27 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod go mod download
COPY . .
ARG TARGETOS
ARG TARGETARCH
RUN --mount=type=cache,target=/go/pkg/mod --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 GOOS=$TARGETOS GOARCH=$TARGETARCH \
    go build -trimpath -ldflags="-s -w" -o /out/app ./cmd/app

FROM gcr.io/distroless/static-debian13:nonroot
COPY --from=build /out/app /app
EXPOSE 8080
ENTRYPOINT ["/app"]
```

- Rust: cargo-chef caches dependencies (`cargo chef prepare`, then
  `cargo chef cook --release` before `COPY . .`, on
  `lukemathwalker/cargo-chef:0.1.78-rust-1.98.1-trixie`), then
  `cargo build --release --locked`; run on `distroless/cc-debian13:nonroot`.
- Java: build on a JDK image, run on `eclipse-temurin:25-jre` (or 21) or a
  `jlink` runtime of the modules `jdeps` lists, with
  `JAVA_TOOL_OPTIONS=-XX:MaxRAMPercentage=75` so the heap follows the limit.

## 2. Base images

| Base | Use for | Watch out |
|---|---|---|
| `gcr.io/distroless/static-debian13:nonroot` | Static Go or Rust binaries | No shell or package manager; debug with the `:debug` tag |
| `gcr.io/distroless/cc-debian13:nonroot` | Rust or C linked to glibc | Build on the same Debian release |
| `node:24-trixie-slim`, `python:3.14-slim`, `eclipse-temurin:25-jre` | Interpreted and JVM runtimes | Debian with apt; rebuild often for patches |
| Docker Hardened Images (`dhi.io`), Chainguard | Minimal, near zero known CVEs, non-root | DHI is free and open since December 2025; Chainguard's free images carry only `latest` tags |
| `alpine:3.24` | Small tools and static binaries | musl: glibc binaries do not run, some native modules and Python wheels compile from source |
| `scratch` | Fully static binaries | No CA certificates, time zones or users unless copied in |

- Official or vendor images only: Bitnami's free catalogue left Docker Hub in
  September 2025, and `bitnamilegacy` gets no patches.
- Pin the version in the tag and the digest after it:
  `FROM node:24-trixie-slim@sha256:<digest>`. `docker buildx imagetools inspect
  node:24-trixie-slim` prints the digest; Renovate (`docker:pinDigests`)
  keeps both current.

## 3. Layers, cache and context

- Order from least to most changing: manifest and lockfile, install,
  source, build. A source edit then reuses the install layer.
- Cache mounts for package manager caches: npm `/root/.npm`, pnpm
  `/pnpm/store`, uv `/root/.cache/uv`, pip `/root/.cache/pip`, Go
  `/go/pkg/mod` and `/root/.cache/go-build`, apt `/var/cache/apt` with
  `sharing=locked`. They stay out of the image.
- apt in one `RUN`: `apt-get update && apt-get install -y --no-install-recommends
  ca-certificates && rm -rf /var/lib/apt/lists/*`.
- `.dockerignore` keeps the context small and secret-free:

```gitignore
.git
**/node_modules
**/.venv
dist
target
.next
.env
.env.*
!.env.example
*.pem
*.key
```

## 4. User, filesystem, privileges

- A non-root numeric user: `USER 1000:1000` (the `node` user), `10001`
  created in the image, or distroless `nonroot` (65532); Kubernetes'
  `runAsNonRoot` refuses a user given only by name.
- Application files owned by root and read-only to that user; only a data
  directory or `/tmp` writable. Run with `--read-only --tmpfs /tmp`,
  `--cap-drop ALL` and `--security-opt no-new-privileges` (in Compose:
  `read_only`, `tmpfs`, `cap_drop`, `security_opt`).
- Listen on a port above 1024 (3000, 8000, 8080), so no capability is needed.

## 5. Configuration and secrets

- One image for every environment, configured by environment variables at
  runtime (`backend-observability`). `ARG` and `ENV` values show in
  `docker history` and the image config, and a file copied in then deleted
  still sits in its layer: no secret goes in either way.
- Build-time secrets through BuildKit, never in a layer:
  `RUN --mount=type=secret,id=npmrc,target=/root/.npmrc pnpm install --frozen-lockfile`
  with `docker build --secret id=npmrc,src=$HOME/.npmrc .` (or
  `env=NPM_TOKEN` on the mount, or `secrets:` in `docker/build-push-action`);
  private Git over SSH with `--mount=type=ssh` and `docker build --ssh default`.

## 6. PID 1, signals and stopping

- Exec form, the runtime itself: `CMD ["node", "dist/server.js"]`. Shell form
  runs `/bin/sh -c`, which does not pass `SIGTERM` on; `npm start` adds a
  process between the signal and the app.
- PID 1 gets no default signal handlers: an app without a `SIGTERM` handler
  ignores it and is killed at the deadline. Handle it (`backend-observability`)
  or add an init: `docker run --init`, `init: true` in Compose, or `tini` as
  the entrypoint. An init also reaps zombie child processes.
- The deadline after `SIGTERM`: Docker and Compose 10s (`stop_grace_period`),
  Kubernetes 30s, Cloud Run 10s, Render 30s, Fly.io 5s and `SIGINT` unless
  `kill_signal` and `kill_timeout` say otherwise. Shutdown fits inside it.

## 7. Health checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=20s --retries=3 \
  CMD ["node", "-e", "fetch('http://127.0.0.1:3000/healthz').then(r=>process.exit(r.ok?0:1),()=>process.exit(1))"]
```

- A cheap liveness endpoint, never the database (`backend-observability`).
  Docker, Compose and Coolify use it; Kubernetes ignores it for its probes.
  Coolify's dashboard checks run `curl` or `wget` inside the container: slim
  and distroless images need this, or a `healthcheck` subcommand instead.

## 8. Size, architectures, scanning

- Targets: Go or Rust on distroless 10 to 40 MB, Node 150 to 300 MB, Python
  100 to 250 MB, a JRE app 200 to 350 MB; over 1 GB, a toolchain, a cache or
  the repository came along. Size is pull time on every deploy and every
  extra package to patch. Inspect with `docker history --no-trunc` and `dive`.
- Multi-arch: `docker buildx build --platform linux/amd64,linux/arm64 --push`.
  QEMU emulation is many times slower; cross-compile (`--platform=$BUILDPLATFORM`
  with `TARGETOS`, `TARGETARCH`) or build on native runners
  (`ubuntu-24.04-arm`) and join them with `docker buildx imagetools create`.
- Scan the built image in CI: `trivy image --severity HIGH,CRITICAL
  --ignore-unfixed --exit-code 1 <image>` or `grype <image> --fail-on high`;
  accepted findings in `.trivyignore` with a reason. Pin the scanner too:
  Trivy's own release and action tags were hijacked in March 2026.
- SBOM and provenance: `syft <image> -o cyclonedx-json` or `docker buildx
  build --sbom=true --provenance=mode=max`. Rebuild weekly for base patches.

## 9. Compose for local development

```yaml
services:
  app:
    build: .
    ports: ["127.0.0.1:3000:3000"]
    env_file: .env
    depends_on:
      db: { condition: service_healthy }
    develop:
      watch:
        - { action: sync, path: ./src, target: /app/src }
        - { action: rebuild, path: package.json }
  db:
    image: postgres:18.6
    environment: { POSTGRES_USER: app, POSTGRES_PASSWORD: app, POSTGRES_DB: app }
    ports: ["127.0.0.1:5432:5432"]
    volumes: ["pgdata:/var/lib/postgresql"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d app"]
      interval: 5s
      retries: 10
  mail:
    image: axllent/mailpit:v1.31
    profiles: ["mail"]
    ports: ["127.0.0.1:8025:8025"]
volumes:
  pgdata:
```

- Postgres 18 images keep data in `/var/lib/postgresql/18/docker` and refuse
  to start with a mount on the old `/var/lib/postgresql/data`: mount the parent.
- Ports bound to `127.0.0.1` (a published port bypasses host firewalls such
  as ufw); throwaway local credentials; `.env` ignored by git, `.env.example`
  committed; optional services behind `profiles`
  (`docker compose --profile mail up`); no obsolete top-level `version:`.

## Check it

- `hadolint Dockerfile` (or `docker run --rm -i hadolint/hadolint:v2.15.1 <
  Dockerfile`): no warnings you added; ignore a rule only with a reason.
- `docker build --progress=plain -t app:check .`; touch a source file and
  build again: the install steps show `CACHED`.
- `docker inspect -f '{{.Config.User}}' app:check` is a non-root numeric
  user; `docker image ls app:check` is within the targets.
- `docker run -d --name t app:check`, then `time docker stop t` returns well
  under 10 seconds and `docker inspect -f '{{.State.ExitCode}}' t` is not 137.
- `docker compose config -q`, then `docker compose up -d --wait` (waits for
  health). No Docker daemon: say so, and still run hadolint.

## Avoid

`latest` or unpinned base images; `COPY . .` before the dependency install;
no `.dockerignore`; secrets in `ARG`, `ENV` or a copied file; root, or a
user by name under `runAsNonRoot`; shell-form `CMD`, `npm start`, or no
`SIGTERM` handling; compilers, caches and dev dependencies in the runtime
stage; Debian releases mixed between stages; Alpine under a glibc stack; a
health check that queries the database; Compose ports on `0.0.0.0`;
Postgres 18 on the old data path; Bitnami base images.
