---
name: linux-perf-doctor
description: Diagnose Linux CPU saturation, memory leaks, OOM kills, disk I/O bottlenecks, syscall storms, thread contention, socket backlogs, and cgroup v1/v2 container throttling using real OS telemetry. Use when users report slow Linux servers, high load averages, container throttling, high iowait, OOM events, or process performance regressions.
license: MIT
compatibility: Linux hosts and containers with Python 3.8+ and standard /proc and /sys filesystems. Optional tools include perf, strace, ss, iostat, vmstat, pidstat, and bpftool.
metadata:
  version: "1.0.1"
  category: systems-performance
---

# linux-perf-doctor

Autonomous eBPF, syscall, process, I/O, and container bottleneck profiler that diagnoses Linux performance problems using operating-system telemetry rather than speculative source-code guesses.

## When to Use

- Diagnose high CPU usage, load average spikes, run-queue saturation, or involuntary context switching.
- Investigate high memory utilization, RSS growth, swap thrashing, or kernel Out-Of-Memory (OOM) kills.
- Identify disk I/O bottlenecks, elevated `iowait`, block device saturation, or high per-process read/write amplification.
- Inspect container resource constraints, cgroup v1 and cgroup v2 CPU throttling (`nr_throttled`), memory high/max events, and Pressure Stall Information (PSI).
- Analyze network socket backlogs (`Recv-Q`, `Send-Q`), TCP retransmissions, `TIME_WAIT` accumulation, or `SYN_RECV` pressure.
- Perform opt-in active process profiling (`perf`, `strace`, or eBPF tools) when passive `/proc` telemetry indicates syscall storms or user-space hot loops.

## Safety and Operating Principles

1. Default to read-only passive telemetry collection (`/proc`, `/sys`, cgroup filesystems, `ss`, `vmstat`, `iostat`).
2. Never invoke privilege-escalation wrappers automatically or escalate privileges without user execution.
3. Keep active profiling (`scripts/profile_process.sh` using `perf` or `strace`) strictly opt-in via `--enable-active-profiling` because attaching tracers can add latency or pause target threads.
4. Bound all sampling windows with `--interval` and `--duration` limits (default 1 second, max 60 seconds).
5. Separate measured facts (directly observed counters and ratios) from diagnostic hypotheses (inferred application-level root causes).

## Diagnostic Workflow

### Step 1: Verify Host and Profiler Capabilities

Run the capability detector first to see which tools (`perf`, `strace`, `ss`, `iostat`, `vmstat`, `pidstat`, `bpftool`), kernel interfaces (`/proc/pressure`, cgroup v2), and permission levels (`perf_event_paranoid`, `ptrace_scope`) are available:

```bash
bash scripts/check_perf_capabilities.sh --pretty
```

### Step 2: Collect System, Cgroup, I/O, and Network Baselines

Collect passive read-only telemetry across the host or container:

```bash
python3 scripts/collect_system_metrics.py --interval 0.2 --samples 2 --pretty
python3 scripts/inspect_cgroups.py --cgroup-root /sys/fs/cgroup --pretty
bash scripts/inspect_io.sh --pretty
python3 scripts/inspect_network.py --pretty
```

### Step 3: Inspect Target Process Metrics

When a specific process (`PID`) exhibits anomalous CPU, memory, file descriptor, or context-switch behavior, inspect its `/proc/<pid>` telemetry:

```bash
python3 scripts/collect_process_metrics.py --pid <PID> --interval 0.2 --pretty
```

### Step 4: Execute Unified Bottleneck Analysis and Report Generation

Synthesize all subsystem collectors into a unified diagnostic report with evidence-backed findings, confidence scores, and remediation steps:

```bash
python3 scripts/generate_report.py --pid <PID> --format markdown --output report.md
python3 scripts/generate_report.py --pid <PID> --format json --output report.json
```

### Step 5: Opt-In Active Process Profiling (Only When Necessary)

If passive telemetry shows high system CPU (`sy`) or high voluntary/involuntary context switches and the user explicitly consents to active profiling, run `scripts/profile_process.sh`:

```bash
bash scripts/profile_process.sh --pid <PID> --mode strace-summary --duration 3 --enable-active-profiling
bash scripts/profile_process.sh --pid <PID> --mode perf-stat --duration 3 --enable-active-profiling
```

## Interpreting Findings

- **CPU Throttling vs Host Saturation**: If cgroup `cpu.stat` shows rising `nr_throttled` and `throttled_usec` while host idle CPU is above 30%, the container CPU quota (`cpu.max`) is undersized rather than the underlying node being saturated.
- **System Time vs User Time**: System CPU (`sy`) above 25% accompanied by high `ctxt/s` points to syscall storms, lock contention, or small-buffer I/O. User CPU (`us`) above 80% with low `ctxt/s` points to compute-bound loops, serialization, or GC activity.
- **Memory Pressure vs Leak**: Steady RSS growth across intervals without anonymous page reclamation indicates an application retention issue or leak. High major page faults (`majflt`) and PSI `memory` full stall percentages indicate active thrashing.

## Gotchas

- Containerized environments often mount host `/proc/meminfo` while restricting memory via `/sys/fs/cgroup/memory.max`. Always run `scripts/inspect_cgroups.py` alongside `scripts/collect_system_metrics.py` to avoid misreading host RAM as container capacity.
- Non-root users cannot read `/proc/<pid>/io` or attach `strace` when `kernel.yama.ptrace_scope` is `1` or higher unless granted `CAP_SYS_PTRACE`. Handle permission denials gracefully and rely on `/proc/<pid>/stat` and `/proc/<pid>/status`.
- Refer to `references/technical-reference.md`, `references/diagnostic-workflows.md`, and `references/troubleshooting.md` for metric thresholds and kernel counter definitions.
