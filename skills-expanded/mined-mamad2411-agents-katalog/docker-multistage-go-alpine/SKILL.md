---
name: docker-multistage-go-alpine
description: Two-stage Docker build for a Go service — golang:alpine builder stage produces static binaries, alpine runtime stage ships them minimally with ca-certificates and tzdata.
category: devops
version: 1.0.0
tags: [docker, go, alpine, multistage, production-image]
source_type: extracted-from-git
source_url: https://github.com/multica-ai/multica.git
source_ref: main
source_commit: 6cd49e132de7632b1f2aaa675c98e8eca9308bb7
source_project: multica
imported_at: 2026-04-18T00:00:00Z
version_origin: extracted
confidence: high
---

## When to use

- Deploying a Go backend service via Docker.
- You want a small, fast-to-pull image without shipping the Go toolchain in production.
- You have multiple binaries from the same module (server, CLI, migrator).

## Steps

1. **Builder stage** — full Go toolchain, layer-caches deps before source:
   ```dockerfile
   FROM golang:1.26-alpine AS builder
   RUN apk add --no-cache git
   WORKDIR /src
   COPY server/go.mod server/go.sum ./server/
   RUN cd server && go mod download
   COPY server/ ./server/
   ARG VERSION=dev
   ARG COMMIT=unknown
   RUN cd server && CGO_ENABLED=0 go build -ldflags "-s -w -X main.version=${VERSION} -X main.commit=${COMMIT}" -o bin/server ./cmd/server
   RUN cd server && CGO_ENABLED=0 go build -ldflags "-s -w" -o bin/migrate ./cmd/migrate
   ```
   - `CGO_ENABLED=0` → static binary, runs on plain alpine.
   - `-s -w` → strip symbol and DWARF tables (~30% smaller).
   - `-X main.version` → inject version/commit at link time.
2. **Runtime stage** — minimal alpine with only what the binary needs at runtime:
   ```dockerfile
   FROM alpine:3.21
   RUN apk add --no-cache ca-certificates tzdata
   WORKDIR /app
   COPY --from=builder /src/server/bin/server .
   COPY --from=builder /src/server/bin/migrate .
   COPY server/migrations/ ./migrations/
   COPY docker/entrypoint.sh .
   RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh
   EXPOSE 8080
   ENTRYPOINT ["./entrypoint.sh"]
   ```
   - `ca-certificates` for HTTPS, `tzdata` for time-zone-aware scheduling.
   - `sed -i 's/\r$//'` on entrypoint handles Windows checkouts with CRLF.
3. Pass version metadata at build time:
   ```bash
   docker build --build-arg VERSION=$(git describe --tags) --build-arg COMMIT=$(git rev-parse --short HEAD) -t app .
   ```

## Example

Final image size for a mid-size Go service: ~30-50 MB (vs ~800 MB for a naive single-stage with the toolchain).

## Caveats

- If your code uses cgo (e.g. sqlite), drop `CGO_ENABLED=0` and switch runtime to `alpine:3.21` → add `libc6-compat` or run on `gcr.io/distroless/cc`.
- Multiple binaries in the same image bloat it; if you deploy them as separate containers, split into separate Dockerfiles.
