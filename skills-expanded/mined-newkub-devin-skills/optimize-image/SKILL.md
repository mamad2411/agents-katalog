---
name: follow-create-docker-optimize-image
description: Shrink and harden docker images — layer analysis, distroless, security scan
argument-hint: "[image]"
related:
  - follow-create-docker
  - deep-review-codebase
  - ask-me
---

## Goal

Reduce image size and improve security posture — analyze layers, switch bases, scan vulnerabilities

## Scope

- Use once a Dockerfile already exists — optimization-focused
- Creating a new Dockerfile → `workflows/setup-dockerfile`

## Execute

### 1. Analyze Image

> Goal: know where the size comes from

1. Use `docker history <image>` or `dive` to view layer sizes
2. Identify dev deps, build tools, and caches left over in the final stage

### 2. Optimize

> Goal: a significantly smaller image

1. multi-stage: move only build artifacts into the runtime stage
2. Consider distroless/alpine/slim bases per compatibility
3. Merge RUN layers, remove caches in the same layer (`--no-cache-dir`, `apt clean`)
4. Complete `.dockerignore` — small context

### 3. Harden And Verify

> Goal: a secure image that behaves the same

1. Scan vulnerabilities with `docker scout` or `trivy image`
2. Non-root user, read-only filesystem where possible
3. Build + run + health check still pass as before

## Rules

- Never break the runtime while shrinking the image — verify every time
- Don't pin the base as `latest` — pin digest/tag version

## Expected Outcome

- Noticeably smaller image, scan passes, runtime unchanged
