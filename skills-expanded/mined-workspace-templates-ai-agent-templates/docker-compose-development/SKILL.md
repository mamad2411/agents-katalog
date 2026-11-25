---
name: docker-compose-development
description: Sets up a Docker Compose dev environment with health checks, ordered startup, sane volumes and seed data so a new teammate runs one command.
---

# Docker Compose development

Aim for `docker compose up` to give a working, seeded app with live reload.

## Steps

1. Read the app's start commands, ports and environment variables. List the services it needs: database, cache, queue, mail catcher.
2. Write `compose.yaml` (no `version:` key). Give each service a pinned image tag, not `latest`.
3. Add a `healthcheck` to every dependency, such as `pg_isready -U app` or `redis-cli ping`. Use `depends_on` with `condition: service_healthy` for the app.
4. Mount source code as a bind mount for reload; keep `node_modules` or the virtualenv in a named volume so the host does not overwrite it. Use named volumes for database data.
5. Put variables in `.env` and commit `.env.example`. Never commit real secrets.
6. Seed data with a one-shot service or an idempotent script (`docker compose run --rm seed`) that can run twice without duplicating rows.
7. Publish only the ports the developer needs, bound to `127.0.0.1`.
8. Add a `.dockerignore` and a multi-stage Dockerfile with a `dev` target.
9. Test it: `docker compose down -v`, then `docker compose up --build`, and confirm the app responds and the seed ran.

## Rules

- Never run containers as privileged or mount the Docker socket without saying why.
- Never use `docker compose down -v` on a developer's real data without warning; it deletes volumes.

## Report

Services, ports, the one-line start command, and how to reset the data.
