---
name: follow-release-deploy-docker
description: Release a Docker image — build, tag, push to the registry with verify
argument-hint: "[image-tag]"
related:
  - run-release
  - run-check
  - follow-secret-manager
  - resolve-errors
  - learn
---

## Goal

Build and publish a Docker image to a registry (Docker Hub or GHCR) — tags follow convention and the image really pulls and works

## Scope

- covers: `docker build`, `docker tag`, `docker push`, registry auth, post-push verify
- CI automation (workflow for auto-release) → follow the parent `/follow-release` Step 4

## Execute

### 1. Verify Image Readiness

> Goal: the Dockerfile is ready to build a production image

1. check the `Dockerfile`: multi-stage build, base image pinned, labels (`org.opencontainers.image.*` if used)
2. check `.dockerignore` covers secrets, `node_modules`, build artifacts
3. define the image name and tag per convention: `<registry>/<owner>/<name>:<version>` + `latest` if wanted

### 2. Authenticate Registry

> Goal: able to push to the target registry

1. Docker Hub: `docker login` with username + access token
2. GHCR: `docker login ghcr.io` with `GITHUB_TOKEN` (scope `write:packages`)
3. store credentials via `/follow-secret-manager` — never put them in scripts/config

### 3. Build And Tag

> Goal: the image builds successfully with complete tags

1. run `/run-check` first — the code in the image must pass tests
2. run `docker build -t <image>:<version> .`
3. add tags per convention: `docker tag <image>:<version> <image>:latest` (if used)
4. smoke test the image locally: `docker run` and check the entrypoint/health works

### 4. Push

> Goal: the image reaches the registry

1. `docker push <image>:<version>` and the other defined tags
2. record the image digest from the push output

### 5. Post-Push Verify

> Goal: the image pulls and works from the registry

1. pull back in a clean context: `docker pull <image>:<version>` and check the digest matches
2. verify on the registry UI (Docker Hub or the GHCR package page)
3. if the push was wrong → untag/delete on the registry per that registry's policy, then `/resolve-errors`
4. success → report tags + digest, then run `/run-release` if the parent needs a multi-platform release

## Rules

### 1. Immutable Tags

- once a version tag is pushed, never overwrite it — if a fix is needed, bump the version
- `latest` is the only mutable tag that may move

### 2. No Secrets In Image

- never COPY secrets into the image or bake them in layers — check `.dockerignore` every time
- credentials go through `/follow-secret-manager`

### 3. Docs First

- registry-specific features (provenance, attestations, multi-arch) → check official docs via `/learn-from-web` instead of guessing flags

## Expected Outcome

- the image is on the registry with its version tag + digest
- it pulls and runs for real from the registry
