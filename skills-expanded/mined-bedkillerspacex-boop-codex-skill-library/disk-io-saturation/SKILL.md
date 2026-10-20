---
name: disk-io-saturation
description: >
  Triage disk IO saturation on owned hosts: high util, await, queue depth, iowait, noisy
  neighbors, filesystem vs device, database checkpoints, container storage drivers, and
  remediation (throttle, move workload, faster disks, fix queries). Use when disk IO
  bottleneck, iowait high, %util 100, elevated latency, nvme saturation, or slow node from
  storage — not ENOSPC-only emergencies (use disk-full-runbook).
---

# Disk IO Saturation

## Scope And Authorization

- **In scope:** Servers, VMs, and nodes you operate; authorized performance tests.
- **Out of scope:** Stress-testing third-party infrastructure without permission.
- Prefer low-impact observation (`iostat`, `pidstat`) before synthetic fio in production.
- Redact tenant identifiers in performance captures shared widely.
- Pair with `disk-full-runbook`, `observability-metrics-tracing`, and DB performance skills.

## When To Use

- High `iowait`, API p99 spikes correlated with storage metrics.
- `%util` ~100 on `iostat`, long `await`, deep IO queues.
- Noisy neighbor on shared volumes or oversubscribed cloud disks.
- Post-deploy regression: new query or backup job saturates disks.
- Distinguishing CPU-bound vs IO-bound slowness.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Disk full / ENOSPC | `disk-full-runbook` |
| Network latency | network triage skills |
| App N+1 SQL | `django-orm-nplusone` / DB skills |
| Distributed lock issues | `distributed-lock-redis-safety` |
| Code quality baseline | `code-quality-standards` |

## Key metrics

| Metric | Saturation signal |
| --- | --- |
| Device `%util` | Near 100% sustained (context-dependent on NVMe) |
| `await` / latency | Elevated ms vs baseline |
| Queue depth / `avgqu-sz` | Growing under load |
| CPU `iowait` | High % waiting on IO |
| Throughput vs IOPS | Sequential fill vs small random |
| Cloud burst credits | Throttle after credit exhaust (gp2-style) |

## Workflow

### 1. Confirm scope and success criteria

1. Host list, time window, SLOs (p99 latency, IO wait).
2. Success: top consumers identified; mitigation applied; baseline restored or capacity ticketed.
3. Avoid production `fio` write storms unless approved.

### 2. Establish baselined symptoms

```bash
# Owned Linux host
uptime
vmstat 1 5
iostat -xz 1 5
# Per-process IO (if available)
sudo pidstat -d 1 5
sudo iotop -aoP 2>/dev/null | head
```

1. Correlate with app APM: which endpoints slow?
2. Check if disk full simultaneously (`df -h`)—different runbook path.

### 3. Map logical → physical

```bash
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE,ROTA
findmnt -t ext4,xfs,btrfs
# Cloud: note volume type (gp3/io2), IOPS/throughput caps
```

1. Container hosts: storage driver, volume mounts, log writes to disk.
2. Databases: data vs WAL vs temp on same spindle?

### 4. Identify consumers

| Class | Examples |
| --- | --- |
| Database | Seq scans, missing index, vacuum, checkpoint storms |
| Backups | pg_dump, snapshots, rsync |
| Containers | overlay pulls, build cache, chatty healthchecks writing logs |
| Logs | Debug logging to local disk |
| Antivirus/backup agents | Full scans |
| Misconfig | sync-heavy fsync loops, RAID rebuild |

```bash
# Which files get IO (needs tools; owned host)
sudo fatrace -c 2>/dev/null | head
# PostgreSQL example: check active queries (authorized)
# SELECT pid, query, wait_event_type FROM pg_stat_activity;
```

### 5. Classify bottleneck and remediate short-term

| Pattern | Short-term action |
| --- | --- |
| Backup vs traffic collision | Reschedule backup; throttle |
| Log storm | Reduce level; remote ship; rate limit |
| Bad query deploy | Rollback; kill query with DBA policy |
| Noisy container | cgroup IO throttle; reschedule pod |
| Cloud credit exhaust | Raise provisioned IOPS/throughput |
| Single disk for WAL+data | Separate volumes plan |

```bash
# Example cgroup v2 throttle sketch (know what you do)
# echo "8:0 $((100*1024*1024))" > /sys/fs/cgroup/.../io.max
```

1. Prefer application fix over forever over-provisioning when query is at fault.
2. For K8s: check node disk pressure, ephemeral storage, log rotation.

### 6. Longer-term capacity and design

1. Right-size volume IOPS/throughput; enable gp3 independent tuning.
2. Separate disks for WAL, data, and logs where justified.
3. Caching layers (when correctness allows); connection pool limits to reduce stampede.
4. Load tests in staging with production-like storage class.

### 7. Verify and hand off

```bash
iostat -xz 1 10
# App p99 back to SLO dashboards
```

1. Document root cause, graphs, and permanent fix ticket.
2. Alerts: disk latency, utilization, cloud throttle events—not only free space.
3. Apply `code-quality-standards` if app IO patterns changed.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Diagnosis | iostat + pid + app correlate | Reboot immediately as only step |
| fio in prod | Avoid / approved window | Unplanned write hammer |
| Fix | Throttle backup + fix query | Silent RAID rebuild during peak ignore |
| Metrics | Latency + util + queue | Only CPU graphs |
| Cloud | Provision IOPS consciously | Surprise gp2 credit starve |
| Full disk | Switch to disk-full runbook | Delete random files for latency |

## Output Checklist

- [ ] Symptom window and hosts recorded
- [ ] `iostat`/`vmstat`/`pidstat` evidence captured
- [ ] Device topology and cloud limits known
- [ ] Top IO consumers identified
- [ ] Short-term mitigation applied safely
- [ ] App SLO impact verified recovering
- [ ] Long-term capacity/design tickets filed
- [ ] Alerts for latency/throttle added
- [ ] Disk-full ruled out or linked
- [ ] Residual risk documented

## Rules

- Measure before large config changes.
- Do not run destructive benchmarks on production without approval.
- Separate full-disk emergencies from saturation latency.
- Prefer root-cause (query/backup) over blind hardware spend when appropriate.
- Owned systems only; evidence-driven triage.
