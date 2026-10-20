---
name: docker-container-list
description: List running Docker containers via Docker socket API
---

# Docker Container List

List running Docker containers via Docker socket API

## When to Use

- User wants to docker list
- User wants to list containers
- Keywords: docker, container, devops, list

## Required Parameters

- **filter_status** (string): Filter by status: running, exited, all

## Output

- **containers** (array): List of containers
- **count** (number): Number of containers

## Security

- Sandbox level: standard
- Max execution time: 30000ms
- Network whitelist: *
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `fetch` -> 5 steps -> Exit: `ret_ok`, `ret_fail`
