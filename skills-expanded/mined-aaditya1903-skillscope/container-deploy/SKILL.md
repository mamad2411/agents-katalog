---
name: container-deploy
description: Build, tag and roll out container images to an environment with health checks and a documented rollback path. Use when shipping a service rather than running it locally.
license: MIT
compatibility: Requires a container runtime and registry credentials in the environment.
allowed-tools: Bash Read
metadata:
  category: infrastructure
---

# Container deployment

Ship a build you can identify and undo.

## Build

Tag every image with the exact source commit. A `latest` tag is not an
identifier and cannot be rolled back to.

## Roll out

1. Push the image and confirm the digest.
2. Start the new revision alongside the old one.
3. Wait for the readiness check, not the liveness check.
4. Shift traffic only after readiness passes.

## Rollback

Record the previous digest before shifting traffic. A rollback that requires a
rebuild is not a rollback.
