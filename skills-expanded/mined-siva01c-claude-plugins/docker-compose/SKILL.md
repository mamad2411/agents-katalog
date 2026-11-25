---
name: docker-compose
description: >
  Use this skill when authoring or editing Docker Compose files (compose.yaml /
  docker-compose.yml), running multi-container stacks, or containerizing a
  Drupal/PHP application — e.g. "set up a local Drupal stack with nginx and
  MariaDB", "add Redis to my compose file", "why won't my containers start",
  "split dev and prod compose configuration". Also trigger for compose
  commands (up, down, logs, exec, watch) and healthcheck/dependency issues
  between services.
---

# Docker Compose Skill

Docker Compose defines and runs multi-container applications from a single
`compose.yaml` file. This skill covers authoring the file, operating the
stack, and structuring configuration for development vs production, with a
typical Drupal stack (php-fpm, nginx, MariaDB, Redis) as the working example.

---

## compose.yaml essentials

- The canonical filename is `compose.yaml` (`docker-compose.yml` still works).
- **Do not add a top-level `version:` key** — it is obsolete and ignored by
  Compose v2; linters flag it.
- Services, networks, and volumes are declared at the top level.

### Drupal stack example

```yaml
services:
  php:
    build:
      context: .
      dockerfile: docker/php/Dockerfile
    volumes:
      - ./:/var/www/html
      - drupal-files:/var/www/html/web/sites/default/files
    environment:
      DRUPAL_DB_HOST: db
      DRUPAL_DB_NAME: drupal
      DRUPAL_DB_USER: drupal
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  web:
    image: nginx:1.27-alpine
    ports:
      - "8080:80"
    volumes:
      - ./:/var/www/html:ro
      - ./docker/nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      - php

  db:
    image: mariadb:11.4
    environment:
      MARIADB_DATABASE: drupal
      MARIADB_USER: drupal
      MARIADB_PASSWORD: ${DB_PASSWORD:?set DB_PASSWORD in .env}
      MARIADB_ROOT_PASSWORD: ${DB_ROOT_PASSWORD:?set DB_ROOT_PASSWORD in .env}
    volumes:
      - db-data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "healthcheck.sh", "--connect", "--innodb_initialized"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine

volumes:
  db-data:
  drupal-files:
```

Key points illustrated:

- **`depends_on` with `condition: service_healthy`** — Drupal installs and
  `drush` commands fail if the database container is *running* but not yet
  *accepting connections*. A healthcheck plus condition fixes the race.
- **Secrets via `${VAR:?error}`** — fail fast when required variables are
  missing instead of starting with empty passwords.
- **Named volume for `sites/default/files`** — keeps user uploads out of the
  bind-mounted codebase.

---

## Common commands

```bash
docker compose up -d              # start stack in background
docker compose up -d --build      # rebuild images first
docker compose down               # stop and remove containers (volumes kept)
docker compose down -v            # ALSO delete named volumes (destroys DB!)
docker compose ps                 # container status + health
docker compose logs -f php        # follow logs of one service
docker compose exec php bash      # shell into running container
docker compose exec php vendor/bin/drush cr   # run drush inside the stack
docker compose run --rm php composer install  # one-off command container
docker compose config             # render the final merged config (debug)
docker compose watch              # sync+rebuild on file changes (dev loop)
```

---

## Dev vs prod configuration

Compose merges multiple files; later files override earlier ones.
`compose.override.yaml` is loaded automatically for local development:

```
compose.yaml            # base — shared definition
compose.override.yaml   # dev only — bind mounts, xdebug, exposed ports
compose.prod.yaml       # prod — restart policies, no source bind mount
```

```bash
docker compose up -d                                   # base + override (dev)
docker compose -f compose.yaml -f compose.prod.yaml up -d   # prod set
```

Use **profiles** for optional services (e.g. Solr or Mailpit only when
needed):

```yaml
services:
  solr:
    image: solr:9
    profiles: ["search"]
```

```bash
docker compose --profile search up -d
```

---

## Best practices

- Pin image tags (`mariadb:11.4`, not `latest`) so the stack is reproducible.
- One process per container; php-fpm and nginx are separate services.
- Put everything secret in `.env` (gitignored) and reference with `${VAR}`.
- Add a `healthcheck` to every service another service depends on.
- For Drupal, mount the project root once and let nginx mount it read-only.
- Run `docker compose config` after edits — it validates and shows the merge
  result before anything starts.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Drupal install fails with "connection refused" to DB | Add DB `healthcheck` + `depends_on.condition: service_healthy` |
| Changes to compose.yaml have no effect | `docker compose up -d` again (recreates changed services); check `docker compose config` |
| Port already allocated | Another stack uses the host port — change `ports:` mapping or `docker compose down` the other project |
| Permission errors on `sites/default/files` | Align container user UID with host (`user:` key) or fix volume ownership in entrypoint |
| Stale vendor/ after switching branches | `docker compose run --rm php composer install` |
| `version` is obsolete warning | Delete the top-level `version:` key |
| Database empty after restart | You ran `down -v` — named volumes were deleted; restore from backup |
