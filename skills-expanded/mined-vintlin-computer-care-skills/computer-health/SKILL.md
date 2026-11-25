---
name: computer-health
description: Use for a health check when a user reports a slow computer, high memory use, swap/pagefile pressure, CPU saturation, thermal throttling, disk I/O pressure, slow code execution, profiler needs, Rosetta/runtime architecture concerns, WSL/Docker/Linux container resource pressure, or asks for a reproducible health report on macOS, Windows, or Linux.
---

# Computer Health

## Overview

Check health before acting. Build a reproducible evidence pack from system pressure, top processes, runtime architecture, workload benchmarks, and profiler output; then choose the smallest reversible action.

"Free memory" or a task-manager memory percentage is not the goal. On macOS, memory pressure, swap growth, compressed memory, wired memory, CPU load, disk I/O, thermal limits, runtime architecture, and code profiler results matter more. On Windows, Available MBytes, commit pressure, Pages Output/sec, pagefile usage, process Private Bytes, Working Set, hard faults, disk I/O, WSL/Docker limits, and profiler results matter more. On Linux, MemAvailable, swap in/out, major faults, PSI, cgroup limits, process RSS/PSS/USS/VmSwap, disk latency, and profiler results matter more.

## When to Use

Use for:

- macOS, Windows, or Linux feels slow, hot, memory-full, swapping/pagefile-heavy, or laggy during development.
- Code runs slowly and the user wants CPU, memory, or I/O bottleneck evidence.
- Python, Node, Java, Go, Rust, Docker, IDE, browser, simulator, local model, or language server usage may affect performance.
- The user needs a shareable health report before changing settings or killing processes.

Do not use for pure disk cleanup; use `storage-clean`. Do not use for network-only slowness; use `network-optimize`.

If the user says the computer is slow, memory looks full, swap/pagefile use is high, CPU is hot, or code is slow, stay in this skill first. Only route to `storage-clean` after evidence shows disk space or disposable caches are the primary issue, or when the user explicitly asks to reclaim storage.

## Platform References

Read the matching reference before running commands:

| Platform | Reference | Status |
| --- | --- | --- |
| macOS | `references/macos.md` | supported |
| Windows | `references/windows.md` | supported |
| Linux | `references/linux.md` | supported |

## Workflow

1. Identify OS, chip, RAM, disk free space, power state, workload command, and what "slow" means.
2. Collect read-only evidence first into a timestamped report directory: system summary, memory pressure, VM/pagefile counters, top memory and CPU processes, disk I/O, runtime versions, Docker/WSL state when available, and optional thermal/power data.
   - Do not infer memory bottlenecks from low free memory alone. Use memory pressure/swap growth/commit pressure together.
   - On Windows, use `Pages Output/sec`, commit pressure, hard faults, and disk I/O together — never infer RAM shortage from `Memory\Pages/sec` alone.
3. Run a reproducible workload benchmark when the complaint involves code speed.
   - Require a repeatable command, input size, timing, and peak RSS before optimizing code.
4. Add a language or native profiler only after the benchmark reproduces the issue.
   - Check built-in tools first: `/usr/bin/time -l`, `sample`, Activity Monitor, Instruments, PowerShell `Measure-Command`, WPR/WPA, Visual Studio tooling.
5. Classify the bottleneck: memory/swap, CPU, thermal/power, disk I/O, runtime architecture, Docker/VM, or code hotspot.
6. Recommend only the smallest action supported by evidence, with validation and rollback.
   - Never recommend memory cleaners, `purge`, killing system processes, disabling security tools, or clearing caches as first-line fixes.
   - Do not disable the pagefile, globally turn off Defender, or move WSL Linux workloads to `/mnt/c` as a first-line optimization.
   - Warn that sharing raw reports externally may expose usernames, paths, ports, tokens, and project names.

## Quick Reference

| Evidence | Likely conclusion | Next step |
| --- | --- | --- |
| macOS Memory Pressure green and swap not growing, or Windows Pages Output/sec near zero and commit pressure normal | memory is not the bottleneck | benchmark and profile code |
| macOS Memory Pressure yellow/red with swap growth, or Windows Available MBytes low with high commit pressure and Pages Output/sec | memory bottleneck | reduce high RSS/Private Bytes processes or workload peak memory |
| Linux MemAvailable healthy, `vmstat si/so` zero, and PSI low | memory is not the bottleneck | benchmark and profile code |
| Linux MemAvailable low with sustained `so`/`pswpout`, major faults, or memory PSI | memory bottleneck | reduce high RSS/PSS/USS processes, batch size, workers, or container limits |
| CPU idle near zero and load above logical CPUs | CPU saturation | sample/profile the hot process |
| CPU high but throughput low, machine hot | thermal or power limit possible | inspect macOS `powermetrics` or Windows `powercfg` evidence |
| Disk writes high with swap growth | memory pressure causing I/O | fix memory pressure first |
| Disk writes high without swap | build/cache/index/sync I/O | identify writer before cleanup |
| Apple Silicon running x86_64 tools | Rosetta overhead possible | install arm64 or universal runtime |
| Windows `vmmem`/`VmmemWSL` or Docker dominates memory | VM/container pressure | inspect WSL/Docker limits before killing random processes |
| Linux cgroup `memory.events` shows `high`, `oom`, or `oom_kill` | container/service limit pressure | inspect cgroup and Docker/systemd limits before changing host settings |
| Profiler shows one hot function/allocation site | code bottleneck | optimize that site, then re-benchmark |

## Reporting

For each meaningful decision, include:

- Conclusion
- Reason
- Risk
- Next step
- Scope and validation method

Use this final shape:

```text
Baseline:
- Symptom:
- Workload:
- Key metrics:

Diagnosis:
- Main bottleneck:
- Evidence:
- Non-bottlenecks:
- Confidence:

Action:
- Smallest recommended change:
- Risk:
- Rollback or undo:
- Re-test command:
```
