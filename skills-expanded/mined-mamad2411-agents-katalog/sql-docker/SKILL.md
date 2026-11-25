---
name: sql-docker
description: Set up a local PostgreSQL development service quickly with Docker Compose.
---

# sql-docker

Use this skill to bootstrap and run a local PostgreSQL service from the bundled local resources in `resources/skeleton`.

## When to use

- You need a fast local SQL environment for development/testing.
- You want a reproducible Docker-based database setup.
- You want a template-backed SQL starter using Zenviron.

## Instructions

1. Resolve this skill folder path (`$SKILL_DIR`):
   - Typical install path: `~/.agents/skills/sql-docker`
2. Copy bundled template resources to your project:
   - `cp -R "$SKILL_DIR/resources/skeleton" "<target-project-dir>"`
3. In the generated project, copy `.env.example` to `.env`.
4. Start the service: `docker compose -f docker-compose.sql.yml up -d`.
5. Verify status: `docker compose -f docker-compose.sql.yml ps`.
6. Stop when done: `docker compose -f docker-compose.sql.yml down`.
