---
name: containerization-fundamentals
description: >-
  Containerization fundamentals — Dockerfile layer ordering for cache
  efficiency and multi-stage builds to keep production images small, with
  Docker as the current worked example of the underlying containerization
  principles. Use whenever writing or reviewing a Dockerfile, debugging slow
  or bloated image builds, or asking how to structure a container build for
  a project — including "why is my docker build so slow", "make this image
  smaller", "write a Dockerfile for X", or "review this Dockerfile".
---

# Containerization fundamentals

Two ideas do most of the work in any container build: order instructions so
the cache actually helps you, and don't ship your build toolchain into
production. Everything below is framed generally; Docker is the concrete
syntax because it's the current default runtime, not because these ideas are
Docker-specific (the same logic applies to Podman, Buildah, or any other
OCI-image builder).

## 1. Layer ordering for cache efficiency

- Every build instruction creates a layer. Changing a layer invalidates
  every layer after it — the cache can only reuse a prefix of the build.
- Order instructions from **least-frequently-changing to
  most-frequently-changing**. Dependency manifests change rarely; source
  code changes constantly.
- Checklist for a new or suspect Dockerfile:
  - [ ] Copy dependency manifests first (`package.json`/`package-lock.json`,
    `requirements.txt`, `go.mod`/`go.sum`, `Cargo.toml`/`Cargo.lock`, ...).
  - [ ] Install dependencies in their own instruction, immediately after.
  - [ ] Copy the rest of the source **after** the install step, not before.
  - [ ] Verify: touch only a source file, rebuild, confirm the dependency
    install layer shows as cached, not re-run.
  - [ ] If the dependency-install layer re-runs on a source-only change,
    something upstream of it is copying more than the manifest — fix the
    `COPY` scope (see `.dockerignore` note below) before anything else.
- This is a default habit, not a later optimization — it costs nothing to
  do correctly from the first draft and is expensive to retrofit once a
  team's muscle memory has set around the wrong order.

## 2. Multi-stage builds for small production images

- Separate **build-time tooling** from **runtime**. A build stage installs
  the full compiler/toolchain and produces artifacts; a final stage starts
  from a lean runtime base and copies in only what's needed to run.
- Checklist:
  - [ ] Name the build stage (`FROM node:20 AS build`) and do all
    compiling/bundling/toolchain work there.
  - [ ] Start the final stage from a minimal runtime base appropriate to the
    artifact (a slim/distroless base, `nginx`, a language-specific slim
    image, etc.) — not the same image the build stage used.
  - [ ] Copy only the compiled output across (`COPY --from=build
    /app/dist ./dist`), never the source tree, dev dependencies, or
    compiler.
  - [ ] Verify: compare image size before/after, and confirm the compiler
    and dev dependencies are actually absent from the final image
    (`docker history`, or shell into the final image and check).
- Payoff: smaller images, faster pulls/deploys, and reduced attack surface
  because the toolchain and source never ship to production.

## Scope and companion practices

This skill's core is deliberately narrow: layer ordering and multi-stage
builds are the two highest-leverage practices and the entry point into image
efficiency, not the whole picture. Base image choice (e.g. Alpine/distroless
variants), non-root `USER` directives, and a correct `.dockerignore` (so
`COPY . .` doesn't drag `node_modules`, `.git`, or build artifacts into the
cache-busting layer) are standard companions worth applying alongside this,
but are treated as a follow-on rather than covered in depth here.

## When the runtime isn't Docker

The layer-cache-ordering and build/runtime-separation principles hold for
any OCI-compatible builder (Podman, Buildah, Kaniko) and conceptually for
non-container build pipelines too (e.g. ordering a CI cache key by
manifest-hash before source-hash). Don't assume Docker-specific syntax
(`FROM ... AS`, `--from=`) carries over verbatim — check the target tool's
docs for its equivalent multi-stage/cache-scoping mechanism.

## Source

Grounded in the Docker "Get Started" workshop's image-building-best-practices
module — see `literature/devops/image-building-best-practices-docker.md` in
the vault for the full note and its noted gaps (base-image selection,
`.dockerignore`, non-root users aren't covered by that source).
