---
name: disk-full-runbook
description: >
  Emergency and planned response when disks fill: identify filesystem, safe cleanup order,
  log rotation, container/graph driver usage, inode exhaustion, expand volume, and prevent
  recurrence. Use when disk full, no space left on device, ENOSPC, inode exhausted,
  /var/lib/docker growth, journald disk, or owned host/VM/node storage incidents — not for
  attacking others’ storage or deleting customer data without policy.
---

# Disk Full Runbook

## Scope And Authorization

- **In scope:** Hosts, VMs, Kubernetes nodes, and volumes you operate.
- **Out of scope:** Deleting data on systems without ownership; wiping customer content without ticket/policy.
- Prefer read-only diagnosis first; destructive cleanup with change record on production.
- Redact customer paths and secrets found in logs during cleanup.
- Pair with `disk-io-saturation`, `observability-metrics-tracing`, and platform backup skills.

## When To Use

- Alerts: disk >90%, `ENOSPC`, failed writes, CrashLoop from volume full.
- CI runners, Docker hosts, DB volumes, or log partitions filling.
- Inode exhaustion (`No space left` but `df` shows free space).
- Post-incident hardening: retention, quotas, alerts at 70/85/95%.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| IO latency / util saturation | `disk-io-saturation` |
| App log sampling standards | `logging-message-style` / observability skills |
| Kubernetes PV design | k8s storage skills |
| Backup restore | backup/DR runbooks |
| Code quality baseline | `code-quality-standards` |

## Quick decision tree

```text
ENOSPC or services failing
  → df -hT  and  df -i
  → space full vs inodes full
  → which mount? (/, /var, /var/lib/docker, data vol)
  → safe cleanup for that mount
  → if critical DB: expand volume before aggressive delete
  → verify services + set retention
```

## Workflow

### 1. Confirm scope and page context

1. Host/node name, environment, blast radius (single node vs all writers).
2. Success: writable filesystem, critical services healthy, root cause and prevention ticketed.
3. Note backups before mass deletes on data volumes.

### 2. Diagnose (read-mostly)

```bash
# Linux host you own
df -hT
df -i
sudo du -xhd1 / 2>/dev/null | sort -h | tail
sudo du -xhd1 /var 2>/dev/null | sort -h | tail
sudo lsof +L1 2>/dev/null | head   # deleted but open files still holding space
mount | column -t
```

| Finding | Meaning |
| --- | --- |
| `df -h` 100%, `df -i` OK | Byte space exhaustion |
| `df -i` 100%, space free | Inode exhaustion (many tiny files) |
| Large `du` gap vs `df` | Open-deleted files or mount shadowing |
| `/var/lib/docker` huge | Images, containers, build cache, volumes |

### 3. Stabilize critical services

1. If DB or etcd on full disk: **stop nonessential writers**; prefer volume expand over deleting DB files.
2. Shed batch jobs / log verbosity if possible.
3. Maintain access: do not fill remaining space with huge debug captures.

### 4. Safe cleanup order (generic Linux)

Only delete what policy allows; prefer truncate/rotate over `rm -rf` unknown trees.

```bash
# 1) Package manager caches (usually safe)
sudo apt-get clean 2>/dev/null
sudo dnf clean all 2>/dev/null

# 2) Journal (keep limited)
sudo journalctl --disk-usage
sudo journalctl --vacuum-size=500M
# or: --vacuum-time=7d

# 3) Old rotated logs (verify paths)
sudo ls -lh /var/log
# truncate active huge log only if needed:
# sudo truncate -s 0 /var/log/huge.log

# 4) Crash dumps / core files
sudo find /var/crash /tmp -type f -name 'core*' 2>/dev/null | head

# 5) Container runtime (owned Docker/Podman hosts)
docker system df
docker builder prune -f
docker image prune -af   # careful: may break offline pins
# docker volume prune    # DANGER: unused volumes may be needed
```

**Do not:** delete PostgreSQL/MySQL data dirs, Kafka logs without runbook, or random `/var/lib` folders.

### 5. Application- and mount-specific actions

| Mount / product | Actions |
| --- | --- |
| Docker/K8s node | Prune images; fix log driver; check emptyDir; node-problem detector |
| DB data volume | Expand disk; VACUUM/archival per DBA—not OS `rm` |
| CI runner | Clean workspaces; tool caches with TTL |
| Nginx/app logs | logrotate config; ship to remote then local short retention |
| Inodes | Find high file-count dirs: `find /path -xdev -printf . | wc -c` patterns; clear temp upload spam |

```bash
# Top directories by size (owned host)
sudo du -xhd2 /var/lib 2>/dev/null | sort -h | tail -n 20
```

### 6. Expand capacity when cleanup is not enough

1. Cloud: increase EBS/Persistent Disk; grow partition/LVM; `resize2fs`/`xfs_growfs` per FS type.
2. Confirm `df -h` after grow.
3. For K8s PVs: storageclass allowVolumeExpansion if supported; follow platform docs.

### 7. Verify, prevent, hand off

```bash
df -hT
df -i
# service health
systemctl is-active docker nginx postgresql 2>/dev/null
curl -fsS http://127.0.0.1/healthz 2>/dev/null
```

1. Alerts at 70% warning / 85% critical; inode alerts separate.
2. logrotate + remote logging; container log size limits (`max-size`/`max-file`).
3. Image GC policies on clusters; disk pressure eviction understanding.
4. Postmortem: growth rate, owner, retention tickets.
5. Apply `code-quality-standards` if app logging code changed.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Order | Diagnose → safe prune → expand | `rm -rf /*` panic |
| DB | Expand + DBA | Delete table files as root |
| Logs | vacuum/rotate | Disable all logging forever |
| Docker | Targeted prune | `volume prune` blind on prod |
| Inodes | Find millions of temp files | Only look at `df -h` |
| Follow-up | Retention + alerts | Clear and ignore |

## Output Checklist

- [ ] Host, mount, and env recorded
- [ ] `df -hT` and `df -i` captured
- [ ] Top space consumers identified
- [ ] Safe cleanup performed with authorization
- [ ] Open-deleted files checked if mismatch
- [ ] Capacity expanded if required
- [ ] Services verified healthy
- [ ] Retention/logrotate/GC prevention set
- [ ] Alerts updated
- [ ] Incident notes and residual risk filed

## Rules

- Prefer expand + retention over destructive deletes of unknown data.
- Never delete database files as a “cleanup.”
- Authorize customer data deletion via policy.
- Capture evidence before and after.
- Focus on disk-full emergency ops; IO latency is a neighbor skill.
