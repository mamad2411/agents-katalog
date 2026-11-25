---
name: dockerfile-optimization
description: Rewrites Dockerfiles for small images, fast cached builds, a non-root user and reproducible builds, then proves the image still starts and runs.
---

# Dockerfile optimization

Measure first: `docker build` time, `docker image ls` size, `docker history` for the heavy layers.

## Steps

1. Read the Dockerfile and `.dockerignore`. Record the baseline size and the time of a clean build and of a rebuild after a one-line source change.
2. Order layers by how often they change: base image, system packages, dependency manifests (`package.json`, lockfile, `requirements.txt`), install dependencies, then copy source. A source edit must not trigger dependency installation.
3. Use multi-stage builds: build and test tooling in a builder stage, then copy only the artifacts into a slim final stage (`-slim`, `alpine` only if the app supports musl, or distroless).
4. Pin bases to a version tag, ideally with a digest (`FROM node:22.11-slim@sha256:...`). Install from the lockfile (`npm ci`, `pip install --require-hashes`). Never `latest`.
5. Combine package-manager steps and clean up in the same layer (`apt-get update && apt-get install -y --no-install-recommends ... && rm -rf /var/lib/apt/lists/*`).
6. Run as non-root: create a user and `USER app`; make files owned by it with `COPY --chown`. Use exec-form `CMD ["node","server.js"]` so signals reach the process.
7. Add a thorough `.dockerignore` (`.git`, `node_modules`, tests, local env files). Use BuildKit cache mounts for package caches.
8. Build the result, start it, hit its health endpoint, and compare size and times against the baseline.

## Rules

- Never put secrets in `ENV`, `ARG` or `COPY`; use build secrets.
- Do not push images.

## Report

A before and after table (size, clean build, cached rebuild) and each change with its reason.
