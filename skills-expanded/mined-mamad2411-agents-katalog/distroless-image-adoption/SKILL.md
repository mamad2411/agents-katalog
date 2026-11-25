---
name: distroless-image-adoption
description: >
  Adopt and migrate application runtimes to distroless (or equivalent minimal non-shell)
  container images: multi-stage copy-in, language base choice (static/base/cc/java/nodejs/python),
  nonroot UIDs, CA/tzdata, and debug without a package manager. Use when distroless migration,
  gcr.io/distroless, Chainguard/wolfi minimal runtime, no-shell final image, static binary into
  distroless, or shrinking production attack surface by dropping apt/apk/shell from the runtime stage.
---

# Distroless Image Adoption

## Scope And Authorization

- **In scope:** Container images and registries you own; authorized hardening of deployables.
- **Out of scope:** Scanning/pushing to others’ registries without permission.
- Prefer staging rollouts; keep a debug variant for break-glass, not for prod default.
- Redact registry credentials and private base image paths in tickets.
- Pair with `dockerfile-best-practices`, `docker-multi-stage-builds`, `docker-rootless-mode`, and `code-quality-standards`.

## When To Use

- Production images still contain apt, shells, package managers, and build tools.
- Migrating Go/static binaries, Java, Node, or Python apps to distroless/Chainguard-style minimal runtimes.
- Reducing CVE surface from unused OS packages.
- Meeting policy: nonroot, no shell, read-only root FS where possible.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General Dockerfile practices | `dockerfile-best-practices` |
| Multi-stage patterns deep dive | `docker-multi-stage-builds` |
| Rootless daemon | `docker-rootless-mode` |
| Compose secrets/network | `docker-compose-security` |
| K8s Pod security | pod security skills |
| Code quality baseline | `code-quality-standards` |

## Distroless idea

**Distroless** images ship runtime libraries needed by the app—not a full distro userland. Typically:

- No package manager, no shell, no `apt-get` in the final stage
- Often nonroot user (e.g. uid 65532)
- Debug via ephemeral debug containers or special `:debug` tags—not by SSHing a shell into prod

| Base family (examples) | Fits |
| --- | --- |
| `static` / static-debian | Fully static binaries (many Go builds) |
| `base` / `cc` | glibc/openssl needs, CGO |
| `java*` | JRE apps |
| `nodejs*` | Node apps (match major version) |
| `python*` | Python apps (watch site-packages layout) |
| Chainguard/wolfi minimal | Similar goals; verify license/support |

Pin digests, not only floating tags.

## Workflow

### 1. Confirm scope and success criteria

1. Apps, languages, current base images, compliance requirements.
2. Success: final image has no shell/package manager; runs as nonroot; healthchecks pass; CVEs for OS packages drop; digests pinned.
3. Rollback tag strategy ready.

### 2. Inventory current images

```bash
# Owned build context
rg -n "^FROM|USER |apt-get|apk add" -g 'Dockerfile*'
docker history IMAGE:TAG | head
# Optional: dive / syft for contents
```

1. List runtime needs: CA certs, tzdata, libc, glibc vs musl, ffmpeg, etc.
2. Note entrypoint/cmd and config paths.

### 3. Multi-stage build pattern

```dockerfile
# Go static example
FROM golang:1.22 AS build
WORKDIR /src
COPY . .
RUN CGO_ENABLED=0 go build -o /out/app -ldflags="-s -w" ./cmd/app

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=build /out/app /app
USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["/app"]
```

```dockerfile
# Node sketch — use official distroless node matching version
FROM node:20 AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
# RUN npm run build if needed

FROM gcr.io/distroless/nodejs20-debian12:nonroot
WORKDIR /app
COPY --from=build /app /app
USER nonroot:nonroot
CMD ["server.js"]
```

1. Build stage may use full distro; **runtime stage** stays minimal.
2. Copy only artifacts and required shared libs—not whole build toolchains.
3. For Python, copy venv carefully and set `PYTHONPATH`; prefer tested Chainguard/distroless python images.

### 4. Nonroot, filesystem, networking

1. `USER nonroot` (or numeric uid); ensure app can write only to mounted volumes.
2. Kubernetes: `readOnlyRootFilesystem: true` + emptyDir for temp; `runAsNonRoot`.
3. Listen on non-privileged ports (>1024) or use platform capabilities carefully.
4. Include CA certs if making TLS egress—distroless variants often include them; verify.

### 5. Debugging without a shell

| Approach | Use |
| --- | --- |
| `:debug` distroless variant | Temporary, not prod default |
| `kubectl debug` ephemeral container | Prod break-glass |
| Local reproduce with same digest | Preferred |
| Sidecar with tools | When policy allows |

1. Do not reintroduce `apt` into prod images to debug.
2. Emit structured logs to stdout; metrics endpoints for ops.

### 6. CI, scanning, signing

```bash
docker build -t ghcr.io/org/app:sha-$GIT_SHA .
# scan
# cosign sign ...
# push digest
```

1. Pin `FROM ...@sha256:...`.
2. SBOM + CVE scan gate; expect fewer OS packages, still scan language deps.
3. Confirm healthcheck: distroless may lack `curl`—use container runtime probe against TCP/HTTP from kubelet, or a tiny in-process health.

### 7. Verify and hand off

```bash
# Should fail: no shell
docker run --rm --entrypoint /bin/sh IMAGE 2>&1 | head
# Should run app
docker run --rm -p 8080:8080 IMAGE
# Check user
docker run --rm --entrypoint /app IMAGE --version  # if supported
```

1. Load test and integration tests on staging.
2. Document base image upgrade cadence.
3. Apply `code-quality-standards` to Dockerfiles and app config paths.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Final stage | Distroless nonroot | Ubuntu + app + build-essential |
| Pin | Digest pins | `:latest` forever |
| Debug | Ephemeral debug pod | Shell in every prod image |
| Copy | Binary + needs only | Copy entire build stage |
| Health | K8s HTTP probe | Depends on `curl` in image |
| Secrets | Runtime mount | Secrets in image layers |

## Output Checklist

- [ ] Runtime deps inventory complete
- [ ] Multi-stage Dockerfile with distroless/minimal final
- [ ] Nonroot user and port policy
- [ ] Base digests pinned
- [ ] No shell/package manager in final image verified
- [ ] TLS CA/tzdata needs verified
- [ ] Probes work without in-image curl if required
- [ ] Scans and tests green on staging
- [ ] Debug break-glass documented
- [ ] Upgrade/ownership of base images assigned

## Rules

- Minimal final images; keep compilers out of prod.
- Nonroot by default; no secrets in layers.
- Debug strategy must not undo hardening for everyday deploys.
- Pin and scan continuously—distroless is not “CVE-free forever.”
- Owned images only; topic is distroless adoption, not general K8s.
