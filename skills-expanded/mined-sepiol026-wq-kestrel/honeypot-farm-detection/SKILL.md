---
name: honeypot-farm-detection
description: "Separate real hosts from honeypot farms before touching."
version: 1.0.0
author: Kestrel Agent
license: AGPL-3.0
platforms: [linux, macos]
tags: [honeypot, verification, recon, authenticity]
metadata:
  hermes:
    tags: [honeypot, verification, recon, authenticity]
    related_skills: [node-hunting-at-scale, anonymous-service-to-root]
---

# Honeypot farm detection

Large pools of imitation hosts sit in cheap hosting ranges and answer popular ports
plausibly. They cost a night if you mistake them for wins. The whole method is one
idea: **a real service holds state, an imitation only answers**.

## When to Use

Load before trusting any product-query hit list, and whenever a candidate's behaviour
looks too convenient.

## 1. The tell before any probe

A single-product query that returns an implausible hit rate — most of a few thousand
candidates answering — is a farm. Real Redis on random hosting IPs is a few percent;
real Docker API is under one percent. When it is 30 %, you are looking at a facade.

## 2. Per-service state tests

| service | imitation | test that separates |
| --- | --- | --- |
| Docker 2375 | `/version` answers | create a container, `start` returns 204, then `/containers/json` still empty |
| Nomad 4646 | node list answers | submit a job, the allocation stays `pending` forever |
| Ollama 11434 | `/api/tags` answers | any prompt returns the same canned sentence ("Got it! How can I assist you today?") |
| Jupyter 8888 | `/api/contents` and `/api/status` answer | `/static/...` assets 404, WebSocket `/api/kernels/<id>/channels` 404, created kernel vanishes from `/api/kernels` |
| Portainer 9000 | `/api/system/status` answers | `/api/users/admin/init` returns 409 but no login ever succeeds |
| Redis 6379 | `PING` → `PONG` | `CONFIG SET` accepted but `CONFIG GET` does not return what you set |
| SSH 22 | accepts any password | `df` fails with `Exec format error`, `curl -m` unknown option, no `/proc/sys/kernel/random/boot_id` |
| any | banner is consistent | `hostname` differs between two logins |

## 3. The shell-level tells

Inside an "owned" shell, the imitations show themselves quickly:

- `hostname` flips between logins (`router-30` → `gw-39-wk`), or a literal `$(hostname)`
  comes back as the string.
- `/proc` is incomplete: no `/proc/sys/kernel/random/boot_id`, no `/proc/self/environ`.
- Core binaries are fake: `df` → `cannot execute binary file: Exec format error`,
  `curl -m` → `option -m not recognized`, `ss` missing on a modern distro.
- `/tmp` already contains someone else's artifacts (`c2t`, `agent.log`, `findings.json`)
  whose timestamps are identical to the microsecond across every host.
- A fixed door port (e.g. `22222`) with an ancient `libssh-0.6.0` banner.

## 4. The gate

Two samples, minutes apart, plus one state write. Concretely:

```bash
# sample 1
hostname; cat /proc/sys/kernel/random/boot_id; uptime -s
# sample 2 (separate connection, later)
hostname; cat /proc/sys/kernel/random/boot_id; echo $((6*7))
# state
mkdir -p /tmp/.probe && date +%s%N > /tmp/.probe/a && cat /tmp/.probe/a
```

Same `boot_id`, same hostname, `42` from the arithmetic, and the written value read back
later — that is a real machine. Anything less is a candidate, not a host.

**A farm can accept credentials you planted.** A no-auth service that writes
`authorized_keys` (Redis being the usual one) makes the pool look conquered: the key
lives in a shared image, so every instance logs you in. The sessions are still
ephemeral — a second connection lands in a fresh container with a new `boot_id`, a new
hostname and an empty `/tmp`. That is why the gate is two connections plus a state
write, not one successful `ssh`.

Symptom of a whole pool being a farm: every hit sits in a handful of /16 blocks of one
cheap provider, and the hostnames read like labels (`cam-37`, `prod-db-83`, `router-14`,
`mail-14.example`).

## 5. Reading the result

Three buckets, not two:

- **real** — passes the gate; goes in the ledger.
- **facade** — answers everything, holds nothing; blacklist the whole subnet once you
  see two of them in it.
- **broken real** — real kernel and real files, but crippled (read-only root, no exec on
  `/tmp`, no network egress). Worth keeping for local compute, useless as a foothold.

## 6. Cost control

The farm answers cheaply but verification is not free: a two-sample gate over thousands
of candidates multiplies your probe count by three. Bucket first with one cheap call per
host, then gate only the survivors, and never gate more than a few hundred in parallel —
the farms throttle, and a throttled probe reads exactly like a dead host.
