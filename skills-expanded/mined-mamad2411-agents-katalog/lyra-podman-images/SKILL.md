---
name: lyra-podman-images
description: "Building minimal, fast, reproducible container images with Podman/Buildah: multi-stage Containerfiles, layer ordering, cache and secret mounts, base-image selection down to scratch/distroless, digest pinning, multi-arch manifests, and registry layer caching. Use when writing or optimizing a Containerfile/Dockerfile, shrinking an image, speeding up builds, or making builds reproducible."
compatibility: "Requires podman (5.x assumed; most rules apply to 4.x and to docker buildx). Optional: skopeo, dive. Composes with lyra-podman-deploy, lyra-ci-cd-automation, lyra-security-containers, lyra-security-supply-chain. Version policy: examples target the latest stable release of every tool; minimum supported is the newest LTS (or last maintained major), and features newer than the minimum are flagged inline."
---

# lyra-podman-images

## What it does

Produces images that are small (nothing ships that the process doesn't execute), fast to build (cache does the work), and reproducible (same inputs, same digest). Podman builds are rootless and daemonless via Buildah — same Containerfile/Dockerfile language, no privileged daemon. The mental model: an image is layers; each instruction is a layer; a layer written is a layer shipped, even if a later layer deletes the file. Every rule below follows from that.

## The rules

### 1. Multi-stage always: build fat, ship thin

Compilers, dev dependencies, and package managers live in build stages; the final stage receives only artifacts via `COPY --from=`. Name stages (`FROM node:22-slim AS build`) and use `--target` to stop at any stage for debugging or CI testing. See [containerfile-patterns.md](./references/containerfile-patterns.md) for canonical Node (pnpm), Go, and Python builds.

### 2. Pick the smallest base that still runs the workload — and pin it by digest

Descend until something breaks: `scratch` (static Go/Rust binaries) → distroless / Chainguard-Wolfi (runtime libs, no shell, no package manager) → `alpine` (musl — verify native deps) → `debian-slim` / `ubi-minimal` (glibc, apt/dnf when you truly need them). Never `FROM node:22` when `node:22-slim` runs it — the full tags carry compilers you already have in the build stage. Pin `FROM` by digest (`node:22-slim@sha256:…`) so builds don't silently change under you; update digests deliberately (Renovate or a scheduled job), not accidentally.

### 3. Order layers least- to most-volatile

Cache invalidation cascades: everything after a changed layer rebuilds. Copy dependency manifests first, install, then copy source — so editing a source file reuses the dependency layer:

```dockerfile
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile   # cached until the lockfile changes
COPY . .                             # only this invalidates per commit
RUN pnpm build
```

### 4. Cache mounts keep package caches out of layers entirely

`RUN --mount=type=cache` persists a directory across builds without it ever entering the image — faster rebuilds *and* smaller layers, replacing the old "clean up in the same RUN" gymnastics for caches:

```dockerfile
# pnpm: pair with ENV PNPM_HOME=/pnpm so the store path is deterministic —
# mount target and store location MUST match or the cache silently never hits
RUN --mount=type=cache,target=/pnpm/store pnpm install --frozen-lockfile
RUN --mount=type=cache,target=/root/.cache/go-build go build -o /out/app .
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked apt-get update && apt-get install -y --no-install-recommends curl
```

Debian-family caveat: stock images ship `/etc/apt/apt.conf.d/docker-clean`, which deletes downloaded packages after install — the mount "works" but caches nothing. Remove it first (`rm -f /etc/apt/apt.conf.d/docker-clean`) or the apt cache mount is theater.

### 5. What you must clean, clean in the same layer

Files deleted in a later instruction still ship in the earlier layer. `apt-get install --no-install-recommends … && rm -rf /var/lib/apt/lists/*` in one `RUN`; `pip install --no-cache-dir`; `dnf --setopt=install_weak_deps=False`. Use heredocs for legible multi-command layers:

```dockerfile
RUN <<EOF
set -eux
apt-get update
apt-get install -y --no-install-recommends ca-certificates
rm -rf /var/lib/apt/lists/*
EOF
```

### 6. Build secrets via `--mount=type=secret` — never ARG, never ENV

`ENV` persists in the image config; `ARG` persists in the image history — both are extractable by anyone who can pull the image. Secret mounts exist only during the instruction:

```dockerfile
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc pnpm install --frozen-lockfile
```
```bash
podman build --secret id=npmrc,src=$HOME/.npmrc -t app .
```

### 7. `.containerignore` before anything else

`.git`, `node_modules`, build outputs, `.env*`, test fixtures, docs — everything the build doesn't consume stays out of the context. A bloated context slows every build, busts `COPY . .` caching with irrelevant changes, and is the classic path for a secret to leak into a layer. Podman reads `.containerignore` first, `.dockerignore` as fallback.

### 8. Run as non-root with only the artifacts

Final stage: create a user (or use distroless `nonroot`), `COPY --from=build --chown=app:app`, set `USER app`, and prefer `--chmod` at COPY time over a separate `RUN chmod` (which duplicates the files into a new layer). No shell in the runtime image is a feature, not a limitation — exec-form `ENTRYPOINT ["/app/server"]` doesn't need one.

### 9. Reproducible builds: strip the timestamps

`podman build --timestamp 0` (or `SOURCE_DATE_EPOCH`) plus digest-pinned bases plus lockfile-pinned dependencies pins every *input*, which makes caches, signatures, and change comparisons trustworthy. Be honest about the output: package-manager install steps (apt, pip, pnpm) still inject nondeterminism — file ordering, generated bytecode, install metadata — so identical inputs give *near*-reproducible images, not guaranteed bit-identical digests. Treat digest equality as "provably unchanged", digest difference as "diff before trusting", and reserve bit-for-bit claims for stages you've verified (static binaries on scratch get there; an apt layer usually doesn't). `--squash` can help determinism of layer counts but discards layer-cache reuse — prefer good stage design; squash only final images that will never be base images.

### 10. Multi-arch through manifests, not tag juggling

```bash
podman build --platform linux/amd64,linux/arm64 --manifest ghcr.io/org/app:1.2.0 .
podman manifest push --all ghcr.io/org/app:1.2.0
```
Cross-arch emulation needs qemu-user-static; native per-arch builders are faster in CI — `podman farm build` drives a fleet of real per-arch machines and assembles the manifest in one command, the no-qemu answer when you have the hardware. Consumers pull one tag and get their arch.

### 11. Share build cache through the registry in CI

Ephemeral CI runners have no local cache. `podman build --layers --cache-to ghcr.io/org/app-cache --cache-from ghcr.io/org/app-cache` persists distributable layer cache in the registry. Know its limit: buildah's registry cache covers **RUN-produced layers only** — `COPY` layers always re-execute — so the win is proportional to how much work lives in RUN instructions (compiles, installs); pair with rule 3 and cache mounts, and don't promise ten-minutes-to-one-minute on a COPY-heavy build.

### 12. HEALTHCHECK is a format decision; metadata is not optional

`HEALTHCHECK` in a Containerfile requires building with `podman build --format docker` (it isn't in the OCI image spec) — when shipping OCI images, declare health checks at runtime instead (lyra-podman-deploy owns that). Always label with `org.opencontainers.image.source|revision|created|version` so registries, scanners, and future-you can trace any image back to its commit.

### 13. Measure before and after

`podman image tree` shows layer sizes; `podman history --no-trunc` shows which instruction produced them; `dive` scores wasted bytes; `podman system df` shows totals. Set a size budget per image and treat a regression like a failing test. The biggest wins, in order: wrong base image, dev dependencies in the final stage, caches baked into layers, build context leaking in.

---

_Part of the [skill collection](../README.md)._
