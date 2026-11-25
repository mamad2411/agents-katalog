---
name: docker-multi-stage-builds
description: >
  Write secure efficient multi-stage Dockerfiles: compile in builder stages, copy artifacts
  only, minimal final images, non-root, BuildKit secret mounts, and cache-friendly layer
  order. Use when multi-stage Dockerfile, AS build, COPY --from, reducing image size, or
  keeping compilers out of runtime images on owned apps.
---

# Docker Multi-Stage Builds

## Scope And Authorization

- **In scope:** Application images you build and ship.
- **Out of scope:** Publishing secrets into public build logs; malicious images.
- Prefer BuildKit for secrets and cache mounts.
- Redact build args that accidentally contain tokens.
- Pair with `dockerfile-best-practices`, `distroless-image-adoption`, and `code-quality-standards`.

## When To Use

- Final image contains gcc, maven, npm, source maps, or `.git`.
- Need smaller/faster deploys and smaller CVE surface.
- Cross-compile or multi-arch builds with clean runtime stage.
- Separating test stage from runtime stage in one Dockerfile.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Broader Dockerfile hygiene | `dockerfile-best-practices` |
| Distroless bases specifically | `distroless-image-adoption` |
| Compose security | `docker-compose-security` |
| Hub rate limits | `docker-hub-rate-limit-ci` |
| Code quality baseline | `code-quality-standards` |

## Pattern

```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.22 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /out/app ./cmd/app

FROM gcr.io/distroless/static-debian12:nonroot AS runtime
COPY --from=build /out/app /app
USER nonroot:nonroot
ENTRYPOINT ["/app"]
```

| Stage | Contains |
| --- | --- |
| deps/build | Compilers, sources, tests optional |
| runtime | Binary/assets + minimal libs only |
| optional test | May never be pushed |

## Workflow

### 1. Confirm scope and success criteria

1. Languages, artifacts (binary, static site, jar), runtime needs (glibc, certs).
2. Success: runtime image without build toolchain; size target; nonroot; secrets not in layers.
3. CI builds with BuildKit enabled.

### 2. Split stages by concern

1. **deps**: package manifests first for cache.
2. **build**: compile/bundle.
3. **test** (optional): `RUN pytest`—discard stage.
4. **runtime**: copy outputs only.

```dockerfile
FROM node:20 AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM deps AS build
COPY . .
RUN npm run build

FROM gcr.io/distroless/nodejs20-debian12:nonroot AS runtime
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=deps /app/node_modules ./node_modules
COPY package.json ./
USER nonroot:nonroot
CMD ["dist/server.js"]
```

### 3. COPY --from discipline

1. Copy explicit paths—not entire build filesystem.
2. Use `--chown=nonroot:nonroot` when needed.
3. Multiple `COPY --from=build` fine; avoid bringing `.git` or secrets.

### 4. Secrets and build-args

```dockerfile
# BuildKit secret (not stored in layer)
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci
```

```bash
DOCKER_BUILDKIT=1 docker build --secret id=npmrc,src=$HOME/.npmrc -t app:dev .
```

1. Never `ARG SECRET` + `ENV SECRET` for long-lived credentials.
2. Multi-stage does **not** remove secrets if you copy a file that contains them into runtime.

### 5. Cache and performance

1. Order: least → most frequently changing.
2. `RUN --mount=type=cache,target=/go/pkg/mod` for module caches (BuildKit).
3. Pin base digests for reproducibility.
4. Target stage: `docker build --target runtime`.

### 6. Security checks

```bash
docker history app:runtime
# ensure no compiler layers in final
# scan runtime image
```

1. Final USER nonroot; read-only root where possible.
2. Drop shell if using distroless.
3. SBOM on final image.

### 7. Hand off

1. Document stages and `--target` for CI.
2. Size budget in CI (fail if image grows unexpectedly).
3. Apply `code-quality-standards` to app and Dockerfile comments via neighbor comment skills if needed.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Final | Binary only | Builder = final |
| COPY | `/out/app` | `COPY --from=build / /` |
| Secrets | BuildKit secret mount | `echo token > file` in layer |
| Cache | Manifests first | COPY . first always |
| User | nonroot | root runtime |
| Targets | push runtime only | push intermediate with secrets |

## Output Checklist

- [ ] Builder and runtime stages separated
- [ ] Only required artifacts copied
- [ ] Build toolchain absent from final
- [ ] Secrets via BuildKit not layers
- [ ] Layer order cache-friendly
- [ ] Nonroot final USER
- [ ] Digests pinned as policy requires
- [ ] Image size/history reviewed
- [ ] CI builds `--target` runtime
- [ ] Scans green on final image

## Rules

- Multi-stage is for exclusion of tools and secrets—not magic.
- Explicit COPY paths; verify with `docker history`.
- BuildKit secrets over ARG credentials.
- Owned images only.
- Broader Dockerfile rules in neighbor skill.
