---
name: docker-build-optimized
description: "Trigger: Dockerfile, docker build, imagen pesada, build lento, multi-stage, .dockerignore, buildx cache. Build small, fast, well-cached images on Kiri with the multiarch builder."
metadata:
  author: "alvaroofernaandez"
  version: "2.0"
---

## Activation Contract

Load when writing or reviewing a `Dockerfile`, `.dockerignore`, `compose.yaml`/`docker-compose.yml`, or when a build is slow, an image is large, or caching misbehaves.

## Hard Rules

- Read `Dockerfile`, `.dockerignore` and the compose file BEFORE building or editing.
- Build against the `kiri` context with `BUILDX_BUILDER=multiarch` (see `kiri-docker`). Never build deploy images on Kiri's own `kiri` builder: it can silently return ARM64 for `--platform linux/amd64`.
- Pin base images to a version tag (e.g. `node:22.11-alpine`, `python:3.12-slim`); never `latest`.
- Show proposed Dockerfile changes as a diff and explain each; do not rewrite build files the user did not ask to change.
- Tag images consistently: `<app>:<git-short-sha>` or `<app>:local` for dev; never rely on implicit `latest`.

## Decision Gates

| Finding | Recommendation |
|---|---|
| Build toolchain ends up in final image | Multi-stage: `build` stage → minimal runtime stage |
| No `.dockerignore` or it misses `.git`, `node_modules`, `.venv`, `dist`, `.env*` | Add/extend it |
| `COPY . .` before dependency install | Copy lockfiles first, install, then copy source |
| Dependencies re-download every build | `RUN --mount=type=cache,target=<pkg cache>` |
| Full distro base for a static/interpreted app | `-slim`, `-alpine` or distroless — only if native deps allow |
| Many `RUN` lines cleaning caches separately | Merge install + cleanup in one layer |
| amd64-only target | `--platform linux/amd64` on the `multiarch` builder, then verify the architecture |
| `InvalidBaseImagePlatform` warning | Wrong builder: `echo $BUILDX_BUILDER` must be `multiarch` |

## Execution Steps

1. Inspect the build files and the current image size (`docker image ls <app>`).
2. Apply the approved recommendations from the table.
3. Build: `docker buildx build --tag <app>:local --load .` or `docker compose up -d --build` (builder `multiarch`, `default-load=true`).
4. For any image to push or deploy, verify: `docker image inspect -f '{{.Architecture}}' <image>` must print `amd64` (or the intended arch). Do not push otherwise.
5. Report: `docker image ls`, `docker system df`.
6. If build cache exceeds ~10 GB or `/` has < 20 GiB free, suggest `docker-space-optimizer`.

## Output Contract

Return: changes applied (diff), build command, image size before/after, build time if measured, and `docker system df` summary.

## References

- `../kiri-docker/SKILL.md` — runtime rules.
- `../docker-space-optimizer/SKILL.md` — cache cleanup.
