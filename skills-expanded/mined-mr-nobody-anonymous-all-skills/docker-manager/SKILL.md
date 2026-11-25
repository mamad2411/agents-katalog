---
name: docker-manager
description: Inspect and manage Docker resources with read-only defaults and confirmation for mutations.
category: development
aliases:
- docker
- container
- image
- compose
- podman
triggers:
- List docker containers
- Tail container logs
- Restart this container
- Prune docker
- Build this image
keywords:
- docker
- container
- image
- compose
- podman
- volume
- network
- prune
- build
dependencies:
- optional:docker
risk: high
version: 1.0.0
source: custom
enabled: true
capabilities:
- docker-manager
- development
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- compose
- container
- development
- docker
- image
- manager
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Docker Manager

## Purpose
Make common Docker operations safe and scriptable for an agent: list, inspect, run,
build, prune, and (with explicit confirmation) destroy. The skill defaults to **read
or report** mode; any state change is gated by an `--apply` flag.

## When to Use
- The user wants to inspect or control Docker resources
- A dev environment needs to be brought up or torn down
- A build is failing and the user needs the logs

## When NOT to Use
- The user has no Docker daemon access
- The user wants Kubernetes operations (use a different skill)
- The user wants production orchestration

## Capabilities
- `ps`, `images`, `networks`, `volumes` (all read-only)
- `logs <container>` (tail with timestamp)
- `exec <container> <cmd>` (interactive shell)
- `restart`, `start`, `stop` (gated)
- `compose up/down/ps/logs` (gated)
- `build` (gated, with `--no-cache` opt-in)
- `system prune` (gated, with size preview)
- `rm` / `rmi` (gated, never default)

## Inputs
- subcommand (`ps`, `logs`, `exec`, â€¦)
- target (container / image / volume / network id or name)
- `--apply` for any state-changing operation (default false)
- `--dry-run` to print the command without running it

## Workflow
1. **Detect** Docker (or Podman, via `DOCKER_HOST` or alias).
2. **Validate** the subcommand against the allowlist.
3. **For read-only ops**: run, parse, format (table or JSON).
4. **For state-changing ops**: print the exact command, ask for `--apply` confirmation.
5. **For destructive ops** (`rm`, `rmi`, `system prune`): require `--apply --force` and a
   5-second grace period with a clear "type YES to continue" prompt.
6. **Report** what changed, with IDs, before and after.

## Tools
- `docker` (or `podman`)
- `jq` for JSON shaping
- `less` / `tail` for log streaming

## Examples
**User:** "Show running containers."
**Response:** `docker ps --format '{{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Names}}'`.

**User:** "Tail the api logs."
**Response:** `docker logs -f --tail 200 --timestamps api`.

**User:** "Prune everything not in use."
**Response:** Will free ~3.2 GB across 14 images, 3 networks. Type `YES` to proceed.

## Safety
- All destructive ops require explicit `--apply` confirmation
- `system prune` requires `--apply --force` and a typed confirmation
- Never `rm` a container with status `Up` without a stop first
- Never `rmi` an image that has child images (warn first)
- Cap log tail at 10 MB per request

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical development category.
