---
tags: [devops, docker, compose, auto, detect]
name: docker-compose-v1-v2-auto-detect
description: Shell helper that prefers `docker compose` (v2) over `docker-compose` (v1) with graceful fallback
category: devops
version: 1.0.0
source_project: lucida-for-docker
trigger: Shell scripts that must run on hosts mid-migration from compose v1 to v2 where v2-only flags (--env-file, config --images) otherwise cause false-negative prechecks
---

See `content.md`.
