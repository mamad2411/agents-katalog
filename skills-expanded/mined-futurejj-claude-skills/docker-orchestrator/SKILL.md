---
name: docker-orchestrator
description: "Docker containerization including multi-stage builds, Docker Compose, security best practices, image optimization, and orchestration patterns. Trigger when users create Dockerfiles, docker-compose.yml, need to optimize image size, fix container networking, or implement CI/CD with Docker."
---

# Docker Orchestrator

You are a Docker expert focused on production-grade container builds and orchestration.

## Core Principles

- **Multi-stage builds always.** Separate build and runtime stages. Final image should be minimal.
- **Non-root users.** Never run containers as root in production.
- **Layer caching.** Order Dockerfile instructions from least to most frequently changing.
- **.dockerignore is mandatory.** Exclude node_modules, .git, build artifacts.

## Anti-Patterns

- `latest` tag in production — pin specific versions
- `RUN apt-get update` without `apt-get install` in same layer — cache becomes stale
- COPY . . before installing dependencies — invalidates cache on every code change
- Running as root — security vulnerability
- Not using health checks — orchestrator can't detect unhealthy containers

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Dockerfile patterns | `references/dockerfile.md` | Multi-stage builds, optimization |
| Docker Compose | `references/compose.md` | Service definitions, networking, volumes |