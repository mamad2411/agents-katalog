---
name: docker-compose-engineering
description: Orchestrate local and simple multi-container stacks with Docker
  Compose. Use when running dev dependencies or small deployments.
metadata:
  tags: docker, compose, engineering
---

# Docker Compose Engineering

## Use this skill when
- Defining local dev environments (DB, services, queues)
- Running small multi-service stacks
- Reproducible environment setup for teams

## Do not use this skill when
- Production orchestration (use kubernetes-engineering)

## Instructions
1. Define services, named volumes, and networks explicitly.
2. Order startup with depends_on conditions and healthchecks.
3. Use env_file and profiles for environment differences.
4. Keep containers ephemeral; data in volumes.
5. Expose only needed ports.
6. Set resource limits and basic healthchecks.
7. Document usage commands in README/compose comments.

## Checklist
- Volumes for persistable data
- Reproducible across machines
- No hardcoded secrets

## Output Format
- Service map | volumes | networks | env strategy

## Common Mistakes
- Data in container filesystem
- Compose in prod without orchestration
- Committed secrets in compose files
