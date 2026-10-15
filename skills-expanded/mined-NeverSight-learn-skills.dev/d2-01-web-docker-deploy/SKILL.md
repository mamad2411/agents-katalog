---
name: d2-01-web-docker-deploy
description: "Dockerizes the up-app Angular project (multi-stage build served by nginx with SPA fallback) and deploys it via Docker Compose alongside up-api and the db. Use when the user asks for Day 2 step 1 of the CRUD drill, or asks to dockerize/deploy up-app."
compatibility: "Requires Docker + Docker Compose, and an existing up-app project + root docker-compose.yml with db and up-api services (from earlier drill steps)."
---

# Day 2 · Step 1 — Dockerize and deploy up-app

Copy `assets/web.Dockerfile` to `up-app/Dockerfile` and `assets/nginx.conf` to `up-app/nginx.conf`.
Merge the `up-app` service block from `assets/docker-compose.web.yml` into the root `docker-compose.yml`
under the existing `services:` key (don't overwrite `db` or `up-api`).
