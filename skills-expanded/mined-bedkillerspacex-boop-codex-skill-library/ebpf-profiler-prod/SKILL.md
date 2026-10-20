---
name: ebpf-profiler-prod
description: >
  Production eBPF continuous profilers on owned Linux fleets: sampling safety,
  symbolization, multi-tenant isolation, CPU/memory budgets, rollout/rollback,
  and privacy of stack traces. Use when Parca, Pyroscope, Elastic Universal
  Profiling, async-profiler with eBPF, or in-house continuous profilers. Not for
  unauthorized host access or offensive tooling.
---

# eBPF Profiler Production Guardrails

## Scope And Authorization

- **In scope:** production/stage fleets you operate, with change windows for node agents.
- **Out of scope:** installing profilers on customer devices or third-party clusters without contract.
- Stack traces can reveal function names, paths, and business logic—treat as sensitive.
- Prefer sampling profilers over always-on tracing of every function entry.
- Pair agent packaging with `code-quality-standards` and `ebpf-observability-basics` for probe hygiene.

## When To Use

- Rolling out continuous CPU/heap/off-CPU profiling with eBPF to production.
- Setting sample rates, scrape intervals, and retention for profile storage.
- Ensuring symbolization (debuginfod, embedded symbols, build-ids) works for Go/C++/Java/native.
- Hardening DaemonSets: privileges, seccomp, AppArmor/SELinux, hostPID necessity.
- Incident workflow: pull profiles for a deploy window without drowning the cluster.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Ad-hoc bpftrace one-liners | `ebpf-observability-basics` |
| APM traces/metrics backends | `observability-metrics-tracing` |
| Falco detection rules | `falco-runtime-rules-basics` |
| Secrets program | `secrets-management-hygiene` |
| Generic load testing | performance skills |
| Unauthorized access | **do not** |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Sampling | Default low rate (e.g. 19–99 Hz class); raise temporarily during incidents |
| Isolation | Prefer cgroup/namespace targeting; avoid host-wide if multi-tenant |
| Privileges | Drop caps after load when architecture allows; no unnecessary host mounts |
| Symbolization | Build-id → symbols pipeline; strip only after symbols uploaded |
| Cost | Profile DB cardinality by service/version; TTL retention |
| Rollout | Canary nodes → wave; instant DaemonSet rollback |

## Workflow

### 1. Confirm scope and success criteria

1. Services/namespaces in scope; exclude multi-tenant noisy neighbors if needed.
2. Success metrics: p99 overhead bound (CPU %, RSS), successful symbolization rate, query latency for profiles.
3. Privacy review: are function names exportable to SaaS? DPA/region constraints?

### 2. Inventory current state

```bash
uname -r
ls /sys/kernel/btf/vmlinux
bpftool prog show | head
# Existing agents
kubectl -n observability get ds,deploy | grep -iE 'parca|pyroscope|profiler|elastic'
```

1. Kernel version skew across the fleet; BTF availability on oldest nodes.
2. Whether nodes allow unprivileged BPF (usually no in prod—document required caps).

### 3. Baseline performance

1. Node CPU/memory before agent install; app p99 latency for a canary service.
2. Disk/network egress if profiles ship off-cluster.
3. Record current incident tooling gaps (no profiles during last SEV).

### 4. Deploy with guardrails

1. Install agent as DaemonSet or node agent with:
   - `resources.requests/limits`
   - explicit securityContext (capabilities list, readOnlyRootFilesystem if possible)
   - tolerations only where required
2. Start with **canary** node group or labeled nodes.
3. Configure sample frequency and scrape interval conservatively.
4. Enable only needed profile types (CPU first; add heap/off-CPU later).

```yaml
# Illustrative securityContext fragment — tune to vendor docs
securityContext:
  privileged: false
  capabilities:
    add: ["BPF", "PERFMON", "SYS_RESOURCE"]
    drop: ["ALL"]
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
```

### 5. Symbolization and labels

1. Ensure production binaries keep build-id; upload debug symbols in CI after build.
2. Label profiles with `service`, `version`/`git_sha`, `region`—not `user_id` or raw pod IP as high-card labels if avoidable.
3. Verify a known hot function appears after generating load on canary.

### 6. Verify with evidence

```bash
# Agent healthy
kubectl -n observability logs ds/profiler-agent --tail=100

# BPF programs present and expected count
bpftool prog show | wc -l

# Node impact during load test window
# (use your metrics: node_cpu, container_cpu for agent)
```

1. Compare canary app SLOs before/after for at least one traffic cycle.
2. Confirm profiles for a deliberate CPU burn test show expected stacks.
3. Test **rollback**: scale agent to zero / previous chart version; programs unload.

### 7. Operate and hand off

1. Runbook: how to raise sample rate for 30 minutes during incident; who approves.
2. Alerts: agent crashloop, symbolization failure rate, unexpected BPF prog growth.
3. Retention/TTL and access control on the profile store (RBAC, SSO).
4. Schedule quarterly review of privileges and vendor CVE advisories.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Rollout | Canary nodes + SLO compare | Fleet-wide privileged DaemonSet day one |
| Sampling | Fixed low Hz + incident boost | Max-rate always-on everywhere |
| Data | service+version labels | pod UID + full cmdline as dimensions |
| Symbols | CI uploads build-id symbols | Stripped bins, empty stacks forever |
| Privileges | Minimal caps documented | `privileged: true` “because docs screenshot” |

## Output Checklist

- [ ] Scope, privacy, and success overhead bounds recorded
- [ ] Kernel/BTF inventory for oldest nodes
- [ ] Canary deploy with resource limits and capability list
- [ ] Symbolization verified for primary languages
- [ ] Before/after SLO and node impact evidence
- [ ] Rollback tested
- [ ] Incident sample-rate procedure documented
- [ ] Access control and retention on profile storage
- [ ] Residual risk noted (multi-tenant stacks, vendor egress)

## Rules

- Production only with ownership and change control.
- Sampling profilers first; avoid unbounded tracing as “profiling.”
- Treat stacks as sensitive telemetry.
- Prefer `ebpf-observability-basics` for exploratory one-liners.
- Never leave emergency high-frequency sampling enabled after the incident window.
