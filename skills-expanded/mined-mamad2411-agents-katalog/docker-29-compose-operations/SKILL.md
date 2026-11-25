---
name: docker-29-compose-operations
description: Designs, validates, and troubleshoots Docker Engine 29 Compose applications. Use when working with compose.yaml, docker compose, service startup order, profiles, healthchecks, volumes, networks, logs, or local development containers.
license: MIT
compatibility: Requires modern Docker Compose plugin for runtime validation. Static review works without Docker.
---

# Docker 29 Compose Operations

This skill helps the agent work safely and effectively with Docker Compose applications under Docker Engine 29-era tooling.

## When to Use

Use this skill for:

- Creating or changing `compose.yaml` files.
- Validating service configuration.
- Debugging startup order, healthchecks, networking, volumes, or logs.
- Designing local development workflows with Compose profiles.
- Reviewing Compose safety and portability.

## Principles

1. Prefer `docker compose` over legacy `docker-compose`.
2. Use the Compose Specification and omit legacy `version:` unless required by the project.
3. Keep Compose files portable and project-scoped.
4. Use profiles for optional dependencies.
5. Use healthchecks for dependencies that need readiness, not just startup ordering.
6. Protect data volumes from accidental deletion.
7. Avoid privileged host access.
8. Validate with `docker compose config` before mutating services.

## Workflow Selection

- Use `workflows/compose-local-dev-workflow.md` for adding or improving local Compose development.
- Use `workflows/compose-troubleshooting-workflow.md` for diagnosing Compose failures.

## Resources and Examples

- `resources/compose-review-checklist.md`
- `examples/compose-development-pattern.md`

## Safe Command Sequence

Start with inspection:

```bash
docker compose config
docker compose ps
docker compose logs --tail=100
```

Then apply scoped actions:

```bash
docker compose up --build <service>
docker compose exec <service> sh
docker compose restart <service>
```

Ask for explicit approval before:

```bash
docker compose down -v
docker volume rm <volume>
docker system prune
```
