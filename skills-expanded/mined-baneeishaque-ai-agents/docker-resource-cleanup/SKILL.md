---
name: docker-resource-cleanup
description: Composer — clean up Docker resources (containers, images, volumes, build cache) with mandatory pre-flight inventory, a human scope gate, stop-before-remove discipline, volume-prune survivor sweep, and post-cleanup verification via the docker-resource-inventory base.
category: Docker-Management
layer: composer
---

# Docker Resource Cleanup Skill (v1) — Composer

Destructive workflow that removes Docker resources in a controlled, verified
order — delegating every enumeration to the read-only base primitive
[`docker-resource-inventory`](../docker-resource-inventory/SKILL.md).

## Composition Rationale

This skill is a **composer** — it owns ONLY the ordering, scope gates, and
verification; it performs NO inventory logic itself. It shells out to
`docker-resource-inventory/scripts/inventory-docker-resources.py --format json`
(resolved via a path anchored on its own `__file__`, never the caller's `cwd`)
at exactly two points:

1. **PRE-FLIGHT** — a deterministic report before any mutation (lesson L1).
2. **POST-CLEANUP** — a verification inventory compared against the per-scope
   expected end state (lesson L6).

It then issues each destructive `docker` command as its own `subprocess.run`
(L3), in an ordered plan that enforces stop-before-remove (L4) and a volume
survivor sweep after every prune (L5).

***

## Environment & Dependencies

| Requirement | Notes |
| --- | --- |
| Docker CLI (20.10+) | `docker --version`; the daemon must be reachable (`docker info`) |
| Python 3.10+ | Standard library only (`argparse`, `json`, `subprocess`, `pathlib`); no pip dependencies |
| Base inventory skill | Resolved relative to this script at runtime — exits 1 if missing |

***

## When to Apply

Use this skill when the user asks to **remove Docker resources** and has been
given the human scope gate:

- "get rid of my docker resources" (full disk reclamation)
- "remove stopped containers but keep the database running"
- "reclaim space from unused images / build cache only"

**Anti-trigger**: if the goal is to inspect or count resources without deleting,
use [`docker-resource-inventory`](../docker-resource-inventory/SKILL.md) —
this composer aborts cleanup if the base inventory cannot run.

***

## Workflow

1. **Scope gate (human decision — stays in prose, never asked by the script).**
2. **Pre-flight** — invoke the base inventory (`--format json`); record
   `summary` and `df[].reclaimable_bytes` before any mutation (L1).
3. **Stop-before-remove (L3, L4)** — for each running container in scope,
   `docker stop` then `docker rm`. Running containers are NEVER removed
   without an explicit prior `docker stop`.
4. **Prune by scope** — the single ordered plan below. Every `docker` command is
   one `subprocess.run`; destructive commands are NEVER chained in one shell call.
5. **Volume survivor sweep (L5)** — after `docker volume prune -f`, run `docker
   volume ls` and `docker volume rm <name>` for each listed volume (tolerating
   in-use refusals — in-use volumes refuse removal, so the sweep is safe).
6. **Verify** — re-invoke the base inventory; assert the per-scope expected end
   state; compute reclaimed bytes as `sum(reclaimable_bytes before) − sum(after)`.

***

## Scope Decision Table

| Scope | Stop running containers? | Remove containers? | Volumes pruned? | Survivors swept? | Images + build cache pruned? | Expected end state |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `full` | YES (all running) | YES (all) | YES | YES | YES | 0 containers / 0 images / 0 volumes / 0 build cache |
| `keep-running` | NO | stopped only | YES | YES | YES | running == total; 0 build cache |
| `unused` | NO | NO (stopped only via `prune -a`) | NO | NO | YES (`prune -a -f`) | running == total; 0 build cache |

***

## CLI Contract

Located at [`scripts/cleanup-docker-resources.py`](./scripts/cleanup-docker-resources.py).

```bash
python3 .agents/skills/docker/docker-resource-cleanup/scripts/cleanup-docker-resources.py \
  --scope {full|keep-running|unused} \
  [--dry-run]
```

| Flag | Required | Meaning |
| :--- | :---: | :--- |
| `--scope {full,keep-running,unused}` | YES | See Scope Decision Table. `full` = stop+remove everything |
| `--dry-run` | ❌ | Print the ordered execution plan + per-step rationale; mutate nothing |

### Exit Codes

| Code | Meaning |
| :---: | :--- |
| 0 | Success — cleanup complete, verification passed |
| 1 | Invalid scope / base inventory script missing |
| 2 | docker CLI binary not found in `PATH` |
| 3 | Docker daemon unreachable |
| 4 | Verification mismatch (post-cleanup inventory violates expected end state) |
| 5 | A docker command failed mid-cleanup (cleanup aborted) |

***

## Deep Command Explanation

- `docker stop <container>` (L3) — graceful SIGTERM; issued one-per-container as its own
  subprocess. NEVER chained with `docker rm` (the session's chained `rm -f … && prune` was
  rejected by the user).
- `docker rm <container>` — hard delete of a stopped container.
- `docker container prune -f` / `docker system prune -a -f` — stopped containers, unused
  images, build cache, dangling networks. Note (L4): `system prune` never removes running
  containers.
- `docker volume prune -f` — removes only DANGLING volumes (L5: can report `0B` while
  in-use volumes survive) → followed by the explicit survivor sweep.
- `docker volume ls` then `docker volume rm <name>` — the survivor sweep (L5); in-use
  volumes refuse removal, so only truly-dangling volumes are deleted.
- `docker system df` (run via the base) — final verification of the four categories reaching 0.

***

## Guardrails (the six lessons)

- **L1** Inspect before acting — inventory before ANY mutation.
- **L3** Stop-before-remove — run before any `docker rm`.
- **L4** Prune never touches running containers — explicit stop+rm required for full cleanup.
- **L5** Volume-prune survivor sweep — `volume prune -f` then `volume ls` + per-volume `rm`.
- **L6** Final verification via the base inventory + per-scope expected state.
- (L2 — the human scope gate — is the reason `--scope` is required and `--dry-run` exists.)

***

## Related Skills

| Skill | Relationship |
| :--- | :--- |
| [`docker-resource-inventory`](../docker-resource-inventory/SKILL.md) | Base primitive — supplies pre-flight + verification inventories (JSON contract) |
| [`is-this-command-safe`](../../is-this-command-safe/SKILL.md) | Scope classification reference for the docker commands used here |
| [`system-wide-tool-management`](../../system-wide-tool-management/SKILL.md) | docker binary install/verification when the CLI is absent |
| [`repo-scratch-output-capture`](../../repo-scratch-output-capture/SKILL.md) | Capture long dry-run / verification output to `scratch/` |

***

## Traceability

See [`TRACEABILITY.md`](./TRACEABILITY.md) for provenance, the source session, and the six
industrial lessons (L1–L6) extracted from the live cleanup replay.

## Changelog

See [`CHANGELOG.md`](./CHANGELOG.md) for the version history of this skill.
