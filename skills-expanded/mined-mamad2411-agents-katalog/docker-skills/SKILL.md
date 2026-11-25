---
name: docker-skills
description: Docker containerization patterns, best practices, and multi-stage builds
category: stacks/infrastructure/docker
applies_to: docker
allowed-tools: Read, Write, Glob, Grep, Bash
user-invocable: true
context: inject
---

# Docker Skills

Container platform for building, shipping, and running applications.

## Sub-Skills

### Dockerfile
- [multi-stage.md](dockerfile/multi-stage.md) - Multi-stage builds
- [best-practices.md](dockerfile/best-practices.md) - Dockerfile best practices
- [security.md](dockerfile/security.md) - Security hardening
- [optimization.md](dockerfile/optimization.md) - Image optimization

### Compose
- [services.md](compose/services.md) - Service definitions
- [networks.md](compose/networks.md) - Network configuration
- [volumes.md](compose/volumes.md) - Volume management
- [profiles.md](compose/profiles.md) - Compose profiles

### Networking
- [bridge.md](networking/bridge.md) - Bridge networks
- [overlay.md](networking/overlay.md) - Overlay networks
- [host.md](networking/host.md) - Host networking

### Storage
- [volumes.md](storage/volumes.md) - Volume patterns
- [bind-mounts.md](storage/bind-mounts.md) - Bind mounts
- [tmpfs.md](storage/tmpfs.md) - tmpfs mounts

### Security
- [rootless.md](security/rootless.md) - Rootless containers
- [secrets.md](security/secrets.md) - Secret management
- [scanning.md](security/scanning.md) - Image scanning

### CI/CD
- [github-actions.md](cicd/github-actions.md) - GitHub Actions
- [buildx.md](cicd/buildx.md) - Docker Buildx
- [registry.md](cicd/registry.md) - Registry patterns

### Debugging
- [logs.md](debugging/logs.md) - Log management
- [exec.md](debugging/exec.md) - Container debugging
- [healthchecks.md](debugging/healthchecks.md) - Health checks

## Detection
Auto-detected when project contains:
- `Dockerfile`
- `docker-compose.yml` or `docker-compose.yaml`
- `FROM ` or `EXPOSE ` patterns
