---
name: docker-engineering
description: Containerize applications with Docker best practices. Use when
  writing Dockerfiles or managing images.
metadata:
  tags: docker, engineering
---

# Docker Engineering

## Use this skill when
- Writing optimized, minimal images
- Multi-stage builds and caching
- Local dev containers and debugging

## Do not use this skill when
- Cluster orchestration (use kubernetes-engineering)
- Runtime security (use container-security)

## Instructions
1. Use multi-stage builds: builder stage then minimal runtime.
2. Order layers by change frequency to leverage build cache.
3. Run as non-root with minimal image base.
4. Copy only what is needed; respect .dockerignore.
5. Pin base image digests in production builds.
6. Keep services single-process and stateless where possible.
7. Use healthchecks; define resource limits.

## Checklist
- Non-root user
- No secrets in layers
- Reproducible builds

## Output Format
- Dockerfile strategy | layers | base images | cache plan

## Common Mistakes
- Fat images with build tools in prod
- Copying node_modules and secrets in
- Unpinned mutable tags
