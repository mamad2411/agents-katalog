---
name: follow-create-docker-setup-dockerfile
description: Create a production-ready Dockerfile — multi-stage, non-root, layer caching
argument-hint: "[app-type]"
related:
  - follow-create-docker
  - deep-review-codebase
  - follow-best-practice
  - ask-me
---

## Goal

Create a Dockerfile that is correct for the ecosystem — multi-stage build, non-root user, layer caching, and a small image

## Scope

- Covers Dockerfiles for apps by ecosystem (node/bun, rust, go, python)
- Does not cover compose orchestration (use `workflows/config-compose`) or deep image-size tuning (use `workflows/optimize-image`)

## Execute

### 1. Detect Ecosystem

> Goal: know the right base image and build steps

1. Check `package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml` to identify the runtime
2. Pick a slim/distroless base per the stack
3. If the runtime is unclear → `/ask-me`

### 2. Write Dockerfile

> Goal: a production-ready Dockerfile

1. multi-stage: separate the build stage from the runtime stage
2. copy dependency manifests before source → layer caching
3. non-root `USER`, `HEALTHCHECK` if it's a service
4. `.dockerignore` covering `node_modules`, `.git`, build artifacts

### 3. Verify

> Goal: the image builds and really runs

1. `docker build` passes with no significant warnings
2. The container starts and the health check passes

## Rules

- Never use the `latest` tag in a base image — pin the version
- Never run as root
- If multiple services are needed → delegate to `workflows/config-compose`

## Expected Outcome

- Dockerfile + `.dockerignore` that builds and runs in production
