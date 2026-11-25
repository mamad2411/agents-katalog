---
name: container-image-pinning
description: Pin container image versions to prevent unexpected breaking changes.
---

# Container image pinning

Floating tags like `:latest` mean a redeploy can silently pull a different image than the one you tested, breaking production with no code change and no audit trail. Pinning is a non-negotiable invariant — back this rule with a CI grep/lint check (e.g. `grep -rn ':latest'` failing the build) so it cannot regress.

## Rules

- Never use `:latest` or `:main` tags in image references anywhere in the codebase.
- Pin to a specific semantic version: `:1.2.3`, `:v1.2.3-alpine`, or a content digest `:@sha256:abc123...`.
- When updating an image version, review the changelog or release notes for breaking API changes.
- Document the reason for any image version bump in the commit message.
- For base images in Dockerfile, pin to a release tag; avoid `FROM node:latest` or `FROM python:main`.

## Scope

This rule applies everywhere images are referenced:

- `docker-compose.yml` and `docker-compose.override.yml`
- Ansible `docker-compose*.yml.j2` templates
- `group_vars/`, `host_vars/` environment variable definitions
- `.env` files and templated `.env.j2`

## Verification

- Before committing, verify the pinned version exists in the registry.
- Use `docker pull image:tag` or check Docker Hub / Quay / ECR to confirm the digest exists.
- If using digest pins, verify the image is signed and matches your expected content.

## Examples

```yaml
# BAD — floating tags; breaks on upstream update
services:
  db:
    image: postgres:latest
  cache:
    image: redis:main

# GOOD — pinned to specific versions
services:
  db:
    image: postgres:16.3-alpine
  cache:
    image: redis:7.2.5-alpine
```

```dockerfile
# BAD
FROM node:latest

# GOOD
FROM node:20.15.0-alpine3.20
```
