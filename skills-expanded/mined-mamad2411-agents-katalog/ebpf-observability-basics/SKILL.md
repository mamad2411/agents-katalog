---
name: ebpf-observability-basics
description: >
  Authorized eBPF observability on owned Linux hosts/clusters: bpftrace/BCC
  safety, capabilities, CO-RE/BTF, sampling, map cardinality, and production
  guardrails. Use when bpftrace, BCC, bpftool, kprobes/tracepoints, or eBPF
  metrics/tracing agents. Not for offensive rootkits or unauthorized host access.
---

# eBPF Observability Basics

## Scope And Authorization

- **In scope:** Linux hosts, VMs, or cluster nodes you own/operate, with change approval for production.
- **Out of scope:** Loading programs on machines without authorization; capturing secrets from other tenants’ memory/traffic without mandate.
- Prefer read-mostly probes (tracepoints, stable kfuncs) over invasive kprobes on hot paths until impact is measured.
- Redact hostnames, pod names, user identifiers, and packet payloads from shared notes.
- Production agents need an owner, rollback plan, and resource limits.

## When To Use

- Explaining latency, syscalls, networking, or scheduler behavior with eBPF tools.
- Evaluating bpftrace one-liners vs BCC tools vs production agents (Pixie, Parca, Cilium Hubble, vendor agents).
- Hardening who may load BPF (`CAP_BPF` / `CAP_PERFMON` / `CAP_SYS_ADMIN`) and which programs are approved.
- CO-RE/BTF portability across kernel versions.
- Bounding CPU, memory, and data volume from continuous probes.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Continuous production CPU profiling productization | `ebpf-profiler-prod` |
| Generic metrics/logs/traces backend design | `observability-metrics-tracing` |
| Falco runtime policy rules | `falco-runtime-rules-basics` |
| Network packet capture forensics | `traffic-analysis-pcap` / NetworkProtocolAnalysisSkill |
| Implementation quality baseline | `code-quality-standards` |
| Unauthorized host compromise | **do not** |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Privileges | Prefer `CAP_BPF`+`CAP_PERFMON` over full root where kernel allows |
| Program types | Tracepoints/USDT first; kprobes only with version awareness |
| Safety | Bounded maps, sampling, rate limits; avoid unbounded `printk` |
| Portability | BTF/CO-RE; check `/sys/kernel/btf/vmlinux` |
| Data | Aggregate in-kernel; export low-cardinality labels |
| Ops | Inventory loaded progs with `bpftool`; document unload |

## Workflow

### 1. Confirm scope and success criteria

1. Host list, kernel versions, and whether multi-tenant (shared CI runners vs single-tenant prod).
2. Question to answer (e.g. “which syscalls dominate p99 latency for service X”).
3. Success: answer with evidence without exceeding agreed CPU/memory budget.

### 2. Inventory kernel and privileges

```bash
uname -r
cat /boot/config-$(uname -r) 2>/dev/null | grep -E 'BTF|BPF' | head
ls -l /sys/kernel/btf/vmlinux
# capabilities for the tool user
capsh --print | head
bpftool feature probe | head -n 40
```

1. Confirm bpftrace/BCC versions and whether packages match kernel headers/BTF.
2. List already-loaded programs: `bpftool prog show`; maps: `bpftool map show`.

### 3. Baseline without eBPF

1. Capture ordinary metrics (CPU steal, run queue, app RED) before attaching probes.
2. Note cgroup/namespace layout if targeting containers only.
3. Agree max attach duration for exploratory sessions.

### 4. Start with safe, high-value probes

```bash
# Who is reading a hot path file? (example; adjust path)
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_openat /str(args->filename) == "/etc/passwd"/ { @[comm] = count(); }'

# Syscall error histogram for one process
sudo bpftrace -e 't:syscalls:sys_exit_* /pid == $1/ { if (args->ret < 0) { @[probe, -args->ret] = count(); } }' $(pgrep -n myapp)

# BCC-style tool if installed
sudo opensnoop-bpfcc -p $(pgrep -n myapp)
```

1. Prefer **tracepoints** over kprobes for stability.
2. Filter by pid/cgroup early to avoid whole-node floods.
3. Aggregate with `@map = count()` / histograms rather than printing every event.

### 5. Production guardrails

1. Run tools under an audited account; revoke broad sudo when done.
2. Set map sizes and sampling (e.g. 1-in-N packets, time windows).
3. Export metrics with low cardinality (service, endpoint class—not raw URL or user id).
4. For cluster agents: DaemonSet resource requests/limits, priorityClass, and allowlist of program types.
5. Document how to unload: `bpftool prog show` → `bpftool prog detach` / restart agent.

### 6. Verify with evidence

```bash
bpftool prog show
bpftool prog show id <ID> --pretty
# CPU impact rough check while probe runs
pidstat -p $(pgrep bpftrace) 1 5
```

1. Confirm probe answers the original question with multi-sample evidence.
2. Confirm no unexpected high-volume logs or disk growth.
3. Unload exploratory programs after the session.

### 7. Hand off

1. If a probe is valuable long-term, promote to a maintained agent config—not a root shell history one-liner.
2. Link dashboards/alerts; set retention and PII policy.
3. Apply `code-quality-standards` if shipping custom BPF C/libbpf.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Attach surface | Filtered tracepoint on one service | Global kprobe printing every syscall |
| Privileges | Scoped caps + audit | World-writable bpf loader scripts |
| Cardinality | `comm`, status class | Full path + user id + pod uid as labels |
| Duration | Time-boxed exploration | Forgotten bpftrace for weeks |
| Portability | CO-RE + BTF checks | Kernel-header-only tools that break on upgrade |

## Output Checklist

- [ ] Authorization and host list recorded
- [ ] Kernel BTF/BPF feature baseline captured
- [ ] Existing bpf programs inventoried
- [ ] Probes use filters, aggregation, and resource limits
- [ ] Evidence answers the observability question
- [ ] Exploratory programs unloaded or promoted with owner
- [ ] PII/payload redaction reviewed
- [ ] Residual risk (overhead, multi-tenant leakage) noted

## Rules

- Authorized hosts only; eBPF is privileged observability, not a toy on shared laptops without consent.
- Prefer stable tracepoints and vendor agents for long-running production use.
- Do not ship “debug forever” printk flooders.
- Focus on observability basics; continuous profilers → `ebpf-profiler-prod`.
- Never paste captured secrets or full packet payloads into tickets.
