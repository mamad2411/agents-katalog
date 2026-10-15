---
name: d1-02-api-docker-deploy
description: "Dockerizes the up-api .NET project and deploys it via the existing Docker Compose file alongside the db service. Use when the user asks for Day 1 step 3 of the CRUD drill, or asks to dockerize/deploy up-api."
compatibility: "Requires Docker + Docker Compose, and an existing up-api project + root docker-compose.yml with a db service (from earlier drill steps)."
---

# Day 1 · Step 2 — Dockerize and deploy up-api

Copy `assets/api.Dockerfile` to `up-api/Dockerfile`. Merge the `up-api` service block from
`assets/docker-compose.api.yml` into the root `docker-compose.yml` under the existing `services:` key
(don't overwrite the `db` service already there).
