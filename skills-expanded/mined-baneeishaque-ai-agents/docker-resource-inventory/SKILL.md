---
name: docker-resource-inventory
description: Base primitive — deterministic inventory of Docker resources (running/stopped containers, images, volumes, build cache with byte-precise sizes) as JSON (stable machine contract) or human text; the pre-flight and verification primitive for the docker-resource-cleanup composer.
category: Docker-Management
---

# Docker Resource Inventory Skill (v1) — Base Primitive

Atomic base primitive that enumerates every Docker resource category through
the docker CLI and emits a deterministic, machine-readable JSON document
(the stable composer contract) or a human-readable text summary:

- Containers — running AND stopped, with name, image, state, status, size
- Images — repository:tag and size
- Volumes — name and driver
- `docker system df` totals — every category (Images, Containers, Local
  Volumes, Build Cache) with raw human sizes PLUS byte-precise `size_bytes`
  and `reclaimable_bytes` fields

The composer layer
([`docker-resource-cleanup`](../docker-resource-cleanup/SKILL.md))
owns the destructive workflow (scope gates, stop-before-remove ordering,
volume survivor sweep) and invokes this primitive for its mandatory pre-flight
report and post-cleanup verification.

***

## Composition Rationale

This skill is a **base primitive** — it owns ONLY the deterministic
inventory logic. It accepts `--format json|text` and produces a
deterministic document; it NEVER mutates Docker state (no stop/rm/prune).

Composers that invoke this skill:

| Composer | Role |
| :--- | :--- |
| [`docker-resource-cleanup`](../docker-resource-cleanup/SKILL.md) | Runs this inventory via `scripts/inventory-docker-resources.py --format json` (self-anchored relative path) at TWO mandatory points: pre-flight (before any mutation) and post-cleanup verification (compared against the per-scope expected state). Consumes the `summary` and `df[].reclaimable_bytes` fields. |

The primitive was extracted because every future Docker workflow (log-cleanup,
image GC, CI cache pruning, disk-usage audits) needs the same enumeration with
the same JSON contract — inlining it into the cleanup composer would split the
SSOT and silently diverge.

**Anti-Duplication**: any skill that needs to enumerate Docker resources MUST
invoke this primitive rather than re-implementing `docker ps -a` /
`docker images` / `docker system df` parsing.

***

## Environment & Dependencies

| Requirement | Notes |
| --- | --- |
| Docker CLI (20.10+) | `docker --version`; the daemon must be reachable (`docker info`). On macOS, Docker Desktop or OrbStack both expose a standard socket |
| Docker daemon running | Verified by the script itself (`docker version --format '{{.Server.Version}}'`); exit 2 with a clear message when unreachable |
| Python 3.10+ | Standard library only (`argparse`, `json`, `subprocess`, `shutil`) — no pip dependencies; `python3 --version` |
| docker binary absent | Delegate installation to [`system-wide-tool-management`](../../system-wide-tool-management/SKILL.md) (macOS: `brew install --cask docker` or `brew install --cask orbstack`; Linux: `apt install docker.io`) |

***

## When to Apply

Use this skill whenever the agent must **enumerate Docker resources** before
deciding or acting:

- Pre-flight of any destructive Docker operation ("what exists before I
  delete anything?")
- Post-action verification ("is the daemon actually empty?")
- Disk-usage triage (`docker system df` breakdown, reclaimable bytes)
- Any workflow that must detect running vs stopped containers or dangling
  volumes

**Anti-trigger**: if the goal is to DELETE resources, use
[`docker-resource-cleanup`](../docker-resource-cleanup/SKILL.md) — this
inventory skill is read-only and never mutates Docker state.

***

## CLI Contract (Stable)

Located at [`scripts/inventory-docker-resources.py`](./scripts/inventory-docker-resources.py).

```bash
python3 .agents/skills/docker/docker-resource-inventory/scripts/inventory-docker-resources.py \
  [--format {json,text}] \
  [--docker PATH]
```

| Flag | Required | Meaning |
| :--- | :---: | :--- |
| `--format json` | ❌ (default) | Machine contract — deterministic JSON document on stdout; NO diagnostic noise on stdout (stderr only) |
| `--format text` | ❌ | Human-readable summary — one section per category plus a `SUMMARY` line |
| `--docker PATH` | ❌ | Explicit path to the docker binary (default: resolved via `PATH`) |

### Exit Codes

| Code | Meaning |
| :---: | :--- |
| 0 | Success (including an empty inventory) |
| 1 | docker CLI binary not found in `PATH` |
| 2 | Docker daemon unreachable (socket/context problem) |
| 3 | Unexpected failure while invoking a docker subcommand (or non-JSON parse) |

### JSON Contract

The `--format json` document (this exact shape is the stable composer
contract — new fields may be added, existing fields never renamed or dropped):

```json
{
  "generated_at": "2026-08-10T23:18:26+0530",
  "docker_cli_version": "29.4.0",
  "daemon_reachable": true,
  "daemon_version": "29.4.0",
  "containers": [
    {"id": "", "name": "", "image": "", "state": "running|exited|...", "status": "", "size": ""}
  ],
  "images": [
    {"id": "", "repo_tag": "repo:tag", "size": ""}
  ],
  "volumes": [
    {"name": "", "driver": ""}
  ],
  "df": [
    {"type": "Images", "total": 0, "active": 0, "size": "0B", "size_bytes": 0,
     "reclaimable": "0B", "reclaimable_bytes": 0}
  ],
  "summary": {
    "containers_total": 0,
    "containers_running": 0,
    "images": 0,
    "volumes": 0,
    "build_cache_entries": 0
  }
}
```

Notes on the contract:

- `containers[].state == "running"` is the discriminator used by composers to
  plan `docker stop` targets.
- `df[].reclaimable_bytes` is parsed from docker's human `Reclaimable` column
  (e.g. `244.9MB (3%)` → `256868024`); composers compute reclaimed space as
  the delta of the sum of `reclaimable_bytes` before vs after a cleanup.
- `df[].build_cache_entries` is surfaced as `summary.build_cache_entries`.

***

## Output Anatomy

### `--format json` (machine contract)

One `json.dump(indent=2)` document, no trailing diagnostic text. All docker
invocations use `--format` TSV templates parsed cell-by-cell; malformed rows
are skipped, never fatal.

### `--format text` (human)

Sections in order: header (CLI + daemon versions), `CONTAINERS (N total / M
running)`, `IMAGES (N)`, `VOLUMES (N)`, `DOCKER SYSTEM DF` (aligned columns),
`SUMMARY` (one line with all five counters). Empty categories print their
section header with `(0)` and no rows.

***

## Manual Usage Examples

Human summary (pre-flight display):

```bash
python3 .agents/skills/docker/docker-resource-inventory/scripts/inventory-docker-resources.py --format text
```

Machine contract piped to a composer or `jq`:

```bash
python3 .agents/skills/docker/docker-resource-inventory/scripts/inventory-docker-resources.py --format json \
  | python3 -m json.tool > /tmp/docker-inventory.json
```

Count only running containers:

```bash
python3 .agents/skills/docker/docker-resource-inventory/scripts/inventory-docker-resources.py --format json \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['summary']['containers_running'])"
```

***

## Related Skills

| Skill | Relationship |
| :--- | :--- |
| [`system-wide-tool-management`](../../system-wide-tool-management/SKILL.md) | Reference — docker binary install/verify when the CLI is absent |
| [`repo-scratch-output-capture`](../../repo-scratch-output-capture/SKILL.md) | Companion — capture long inventory output to `scratch/` when probing |

***

## Traceability

See [`TRACEABILITY.md`](./TRACEABILITY.md) for provenance, the source
session, and the layer decision.

## Changelog

See [`CHANGELOG.md`](./CHANGELOG.md) for the version history of this skill.
