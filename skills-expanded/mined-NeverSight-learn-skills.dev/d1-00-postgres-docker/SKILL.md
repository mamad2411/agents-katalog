---
name: d1-00-postgres-docker
description: "Stands up Postgres 17 via Docker Compose as up-api/up-app's db. CRUD drill Day 1 step 0. Trigger: 'day1 step0', 'postgres docker compose', 'create db compose file'."
compatibility: "Requires Docker + Docker Compose."
---

# Day 1 · Step 0 — Postgres via Docker Compose

Copy `assets/docker-compose.db.yml` to project root as `docker-compose.yml` (root file later steps extend — don't recreate it).
Keep defaults unless user specifies otherwise.

Default: db `up_db`, user upadmin/password uppass, port `5432`.
