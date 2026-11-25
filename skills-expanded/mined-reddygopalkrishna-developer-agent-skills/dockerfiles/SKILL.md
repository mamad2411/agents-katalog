---
name: dockerfiles
description: Writes and reviews production-grade Dockerfiles and container images, covering multi-stage builds, pinned minimal base images, non-root users, cache-friendly layers, secret-free builds, signal handling and health checks. Use when creating or editing a Dockerfile, .dockerignore or compose file, shrinking or hardening an image, fixing slow container builds, or containerizing an app. Not for Kubernetes manifests.
license: MIT
---

# Dockerfiles

A production image contains only what is needed to run the app: no compilers, no secrets, no root user. It builds reproducibly from pinned inputs, and it shuts down cleanly when asked.

## When to use

- Containerizing an application, or writing a new Dockerfile.
- Reviewing or hardening an existing Dockerfile.
- Builds are slow, images are large, or scanners report many vulnerabilities.
- Writing `.dockerignore` or a `compose.yaml` for local development.

Not for: Kubernetes manifests, Helm charts, or cluster configuration.

## Workflow

1. **Learn the app:** language and version (from `.nvmrc`, `go.mod`, `pom.xml`, `pyproject.toml`, `*.csproj`), build command, the artifact that runs (binary, jar, `dist/`), port, config via environment variables, and writable paths.
2. **Choose the base images** for the build stage and the runtime stage (table below).
3. **Write a multi-stage Dockerfile:** dependencies → build → minimal runtime. Start from [references/examples.md](references/examples.md) for Node, Python, Go, Java and .NET.
4. **Order layers for caching:** copy only the lockfiles, install dependencies, then copy the source.
5. **Add `.dockerignore`** before the first build.
6. **Harden:** non-root numeric user, no secrets in any layer, pinned base images, no build tools in the final stage.
7. **Make it stop cleanly:** exec-form `CMD`/`ENTRYPOINT`, and an init process or proper SIGTERM handling.
8. **Build, run and inspect:**

   ```bash
   docker build -t app:dev .
   docker run --rm -p 8080:8080 app:dev
   docker image ls app:dev           # size
   docker history app:dev            # what each layer added
   ```

9. **Lint and scan:** `hadolint Dockerfile` (or `docker run --rm -i hadolint/hadolint < Dockerfile`), then `trivy image app:dev` or `docker scout cves app:dev`. Fix findings by updating the base image or dependencies, not by suppressing them.
10. **Do not push images to a registry, or change tags others deploy from, without explicit confirmation from the user.**

## Base images

| App | Build stage | Runtime stage |
|---|---|---|
| Go, Rust (static binary) | `golang:<ver>`, `rust:<ver>` | `gcr.io/distroless/static-debian12:nonroot`, or `scratch` (then add CA certificates and time zone data yourself) |
| Node.js | `node:<ver>-slim` | `node:<ver>-slim`, or `gcr.io/distroless/nodejs<major>-debian12` |
| Python | `python:<ver>-slim` | `python:<ver>-slim` |
| Java | `maven:<ver>-eclipse-temurin-<jdk>` or `gradle:<ver>-jdk<jdk>` | `eclipse-temurin:<jdk>-jre`, or `gcr.io/distroless/java<jdk>-debian12` |
| .NET | `mcr.microsoft.com/dotnet/sdk:<ver>` | `mcr.microsoft.com/dotnet/aspnet:<ver>` (or `runtime:<ver>`); chiseled variants are smaller |

- Match the version to the project's runtime version. Check that the tag exists before using it (`docker buildx imagetools inspect <image:tag>`).
- **Alpine** uses musl libc. Python wheels and Node native modules often need compiling or behave differently on it. Prefer Debian `-slim` unless you have tested Alpine.
- **Distroless and chiseled** images have no shell or package manager. They are smaller and safer, but you cannot `docker exec` into them with a shell, and `HEALTHCHECK` commands that call `curl` will not work.

### Pin base images

- Never use `latest`. Use a specific version tag, and for production pin the digest too:

  ```dockerfile
  FROM node:22-slim@sha256:<digest>
  ```

- Get the digest with `docker buildx imagetools inspect node:22-slim` (the `Digest:` line). Never invent a digest.
- Let Renovate or Dependabot update tags and digests, so pinning does not mean never patching.

## Layer caching

```dockerfile
COPY package.json package-lock.json ./
RUN npm ci                      # re-runs only when the lockfile changes
COPY . .                        # source changes invalidate only from here on
RUN npm run build
```

- Copy only what each step needs. A `COPY . .` before installing dependencies reinstalls everything on every code change.
- Use BuildKit cache mounts for package manager caches (add `# syntax=docker/dockerfile:1` as the first line):

  | Ecosystem | Cache mount |
  |---|---|
  | npm | `RUN --mount=type=cache,target=/root/.npm npm ci` |
  | pip | `RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt` |
  | Go | `RUN --mount=type=cache,target=/go/pkg/mod --mount=type=cache,target=/root/.cache/go-build go build ...` |
  | Maven | `RUN --mount=type=cache,target=/root/.m2 mvn -B package` |
  | NuGet | `RUN --mount=type=cache,target=/root/.nuget/packages dotnet restore` |

- Combine `apt-get update` and `install` in one `RUN`, and clean up in the same layer:

  ```dockerfile
  RUN apt-get update \
   && apt-get install -y --no-install-recommends ca-certificates \
   && rm -rf /var/lib/apt/lists/*
  ```

## .dockerignore

Keep the build context small, and keep secrets out of it:

```
.git
**/node_modules
**/dist
**/build
**/target
**/bin
**/obj
**/.venv
**/__pycache__
coverage
*.log
.env
.env.*
**/*.pem
**/*.key
Dockerfile*
compose*.yaml
docker-compose*.yml
```

Adjust it to the project: never exclude files the build needs.

## Secrets

- Never pass secrets with `ARG`, `ENV` or `COPY`. They end up in the image metadata or layers, and `docker history` shows build arguments.
- Use BuildKit secret mounts, which exist only for that one `RUN`:

  ```dockerfile
  RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci
  ```

  ```bash
  docker build --secret id=npmrc,src=$HOME/.npmrc -t app:dev .
  ```

- Runtime secrets come from the platform (environment variables or mounted files from a secret manager), never baked into the image.

## Non-root user

```dockerfile
# Debian/Ubuntu-based images
RUN useradd --system --uid 10001 --no-create-home app
USER 10001
```

- Use a **numeric** UID in `USER`, so Kubernetes `runAsNonRoot` can verify it.
- Many images already ship a user: `node` in official Node images, `nonroot` (UID 65532) in distroless `:nonroot` tags, and `$APP_UID` in .NET 8+ images.
- Leave application files owned by root and readable. The app should not be able to modify its own code. Give write access only to the directories that need it.
- Listen on a port above 1024 (8080, 3000), because non-root users cannot bind to low ports by default.

## Signals and PID 1

When the platform stops a container it sends SIGTERM, waits for a grace period (10 seconds by default in Docker), then sends SIGKILL.

- Use **exec form**: `CMD ["node", "server.js"]`. Shell form (`CMD node server.js`) runs under `/bin/sh -c`, which does not forward signals to your app.
- Do not use `npm start` or other wrapper scripts as PID 1. If you need an entrypoint script, end it with `exec "$@"` so the app replaces the shell.
- A process running as PID 1 gets no default signal handlers, so the app must handle SIGTERM itself, or run under an init process:
  - `docker run --init`, or `init: true` in compose.
  - For Kubernetes and other platforms without `--init`, install tini in the image (Debian: `apt-get install -y --no-install-recommends tini`) and use `ENTRYPOINT ["/usr/bin/tini", "--"]`.
- On SIGTERM the app should stop accepting new work, finish in-flight requests, close connections, and exit.
- Test it: `docker stop <container>` should return well before the grace period ends.

## Health checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=20s --retries=3 \
  CMD ["curl", "-fsS", "http://localhost:8080/healthz"]
```

- Docker and compose use `HEALTHCHECK`. Kubernetes ignores it and uses liveness and readiness probes instead.
- The command must exist in the image. Distroless images have no `curl`; use a tiny health-check binary or rely on the orchestrator's probes.

## Other rules

- One main process per container. Use separate containers (or compose services) for the web server, worker and database, not supervisord.
- Use `COPY`, not `ADD`, unless you specifically need `ADD`'s archive extraction.
- Use `WORKDIR`, not `RUN cd ...`.
- Configure via environment variables. Do not bake environment-specific config into the image: build once, run in every environment.
- Add OCI labels for traceability: `LABEL org.opencontainers.image.source="https://github.com/org/repo"`.
- Multi-architecture builds: `docker buildx build --platform linux/amd64,linux/arm64 -t <image> .`.
- Do not `curl | sh` installers in the Dockerfile. Download a pinned version and verify its checksum.

## Compose for local development

```yaml
# compose.yaml (the top-level "version:" key is obsolete; omit it)
services:
  app:
    build: .
    ports: ["8080:8080"]
    env_file: .env
    init: true
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:17
    environment:
      POSTGRES_PASSWORD: dev-only-password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      retries: 10
    volumes:
      - db-data:/var/lib/postgresql/data
volumes:
  db-data:
```

Credentials in a compose file are for local development only. Never reuse them anywhere else.

## Anti-patterns

- `FROM something:latest`: builds change under you, and rollbacks are not reproducible.
- Running as root.
- Secrets in `ARG`, `ENV`, copied files, or `.npmrc`/`pip.conf` left in a layer.
- `COPY . .` before dependency installation.
- No `.dockerignore`, so `.git`, `node_modules` and `.env` end up in the context or the image.
- Compilers and build tools in the runtime image (use multi-stage).
- Shell-form `CMD`, or `npm start` as PID 1, so the container ignores SIGTERM and is killed after the grace period.
- `apt-get update` in its own layer (stale cache), or no cleanup of `/var/lib/apt/lists`.
- Writing application data into the container filesystem instead of a volume or external storage.

## Done when

- The image builds from pinned base images, and rebuilds without source changes are fully cached.
- The final stage contains no compilers, package caches, `.git`, tests or secrets (`docker history` and a scan confirm it).
- The container runs as a non-root numeric UID.
- `docker stop` stops it promptly, and the app handles SIGTERM gracefully.
- `hadolint` passes, or has only justified ignores, and the scan shows no fixable critical or high vulnerabilities.
- `.dockerignore` exists, and image size is recorded before and after the change.

## References

- [references/examples.md](references/examples.md) — read when writing a Dockerfile for Node.js, Python, Go, Java or .NET; contains complete multi-stage examples.
