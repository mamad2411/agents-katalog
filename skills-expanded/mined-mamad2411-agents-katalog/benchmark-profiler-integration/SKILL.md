---
name: benchmark-profiler-integration
description: Use when BenchmarkDotNet diagnosers beyond MemoryDiagnoser are needed — covering hardware counters, ETW/perf_events setup, profiler correlation, and diagnoser co-existence rules.
---

# BenchmarkDotNet Profiler Integration

## Specialization

Use this skill to configure and interpret advanced BenchmarkDotNet diagnosers — hardware performance counters, ETW (Windows) and perf_events (Linux) integration, and correlation with external profiler output.

This skill is specialized for advanced diagnostic configuration. It does not cover basic `MemoryDiagnoser` usage (handled by `benchmark-experiment-design`) or statistical result interpretation (handled by `benchmark-statistical-analysis`).

## Objective

Produce a deterministic profiler integration plan with explicit diagnoser selection, platform requirements, counter selection rationale, co-existence rules, and an interpretation guide for advanced diagnostic output.

## Trigger Conditions

- A benchmark shows acceptable time and allocation metrics but CPU or cache behavior is suspect.
- A profiler trace suggested a bottleneck and the hypothesis must be confirmed with reproducible counter evidence.
- A benchmark suite requires hardware counter columns for branch misprediction, cache miss, or instruction throughput analysis.
- A diagnoser combination is needed and co-existence constraints must be validated.
- Results from BenchmarkDotNet must be correlated with an external profiler (PerfView, dotTrace, VTune).

## Scope Boundaries

In scope:

- `HardwareCounters` enum selection and platform availability matrix.
- ETW diagnoser setup on Windows and perf_events diagnoser setup on Linux.
- `DisassemblyDiagnoser` for instruction-level inspection.
- `EtwProfiler` and `PerfCollectProfiler` integration.
- Diagnoser co-existence rules and conflict table.
- Correlation workflow between BenchmarkDotNet output and external profiler traces.

Out of scope:

- Basic `MemoryDiagnoser` usage (covered by `benchmark-experiment-design`).
- Statistical interpretation of time and allocation results (covered by `benchmark-statistical-analysis`).
- CI artifact storage and threshold enforcement (covered by `benchmark-ci-integration`).

## Inputs

- Benchmark class and target methods.
- Performance hypothesis: which CPU-level behavior is under investigation.
- Host OS (Windows / Linux / cross-platform requirement).
- Available profiler tooling (PerfView, dotTrace, VTune, perf CLI).
- Elevated privilege availability (ETW requires admin; perf_events may require `perf_event_paranoid` tuning).
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

- Diagnoser selection decision with rationale and platform check.
- `HardwareCounters` selection table with counter meaning and expected signal.
- Platform setup checklist (ETW or perf_events).
- Diagnoser co-existence assessment for the selected combination.
- Annotated benchmark configuration showing diagnoser wiring.
- Profiler correlation workflow if external profiler is in scope.
- Interpretation guide for the resulting diagnostic columns.

## Hardware Counter Selection

### Counter Catalog

| Counter (`HardwareCounters` enum value) | Signal | When to use |
|---|---|---|
| `InstructionRetired` | Total instructions executed | Baseline for IPC (instructions per cycle) |
| `TotalCycles` | Total CPU cycles | Paired with `InstructionRetired` for IPC calculation |
| `CacheMisses` | L1/L2/LLC cache misses | Suspect data-access locality or large working sets |
| `CacheReferences` | Total cache accesses | Paired with `CacheMisses` for miss rate |
| `BranchMispredictions` | Branch predictor failures | Suspect conditional branches in hot paths |
| `BranchInstructions` | Total branch instructions | Paired with `BranchMispredictions` for miss rate |
| `UnhaltedCoreCycles` | Active (non-halted) cycles | More accurate than `TotalCycles` when DVFS is active |

### Counter Selection Rules

- Select the smallest set that tests the hypothesis. Do not enable all counters speculatively.
- Always pair rate-numerator counters with their denominator (e.g., `CacheMisses` + `CacheReferences`).
- On Windows, limit to 4 counters per run due to PMU multiplexing constraints.
- On Linux, PMU multiplexing applies above 4 counters; counter values become sampled approximations — document this.

## Platform Setup

### Windows — ETW Diagnoser

**Prerequisites:**
- Run benchmark process as Administrator or with elevated UAC.
- Windows Performance Recorder (WPR) available (ships with Windows ADK).
- No other ETW sessions consuming the same counters simultaneously.

**Configuration:**

```csharp
using BenchmarkDotNet.Configs;
using BenchmarkDotNet.Diagnosers;

var config = DefaultConfig.Instance
    .AddDiagnoser(new EtwProfiler())
    .AddHardwareCounters(
        HardwareCounters.CacheMisses,
        HardwareCounters.CacheReferences);
```

**Validation check:** If ETW session registration fails silently, the counter columns will be empty. Always confirm counter columns appear in the output before interpreting results.

### Linux — perf_events Diagnoser

**Prerequisites:**
- `perf` CLI installed (`linux-tools-$(uname -r)` or equivalent).
- `perf_event_paranoid` set to `0` or `-1` (requires root or sysctl change): `sudo sysctl kernel.perf_event_paranoid=-1`
- Kernel version ≥ 4.1 recommended for stable PMU access.

**Configuration:**

```csharp
using BenchmarkDotNet.Configs;
using BenchmarkDotNet.Diagnosers;

var config = DefaultConfig.Instance
    .AddDiagnoser(new PerfCollectProfiler())
    .AddHardwareCounters(
        HardwareCounters.CacheMisses,
        HardwareCounters.CacheReferences);
```

**Validation check:** Run `perf stat ls` before benchmarking to confirm perf_events access is available.

### Cross-Platform Notes

- `EtwProfiler` is Windows-only. `PerfCollectProfiler` is Linux-only. Do not mix.
- Hardware counter availability varies by CPU microarchitecture. Verify counter support with `cpuid` or `perf list`.
- CI runners (especially GitHub-hosted) frequently lack PMU access. Advanced diagnosers are local-development and self-hosted-runner only.

## DisassemblyDiagnoser

Use when JIT-generated code must be inspected to verify inlining, vectorization, or dead-code elimination:

```csharp
var config = DefaultConfig.Instance
    .AddDiagnoser(new DisassemblyDiagnoser(new DisassemblyDiagnoserConfig(
        maxDepth: 2,
        printSource: true,
        printInstructionAddresses: true,
        syntax: DisassemblySyntax.Intel)));
```

- `maxDepth` controls call-graph depth. Use `1` for leaf-method inspection; `2` for inlining verification.
- Combine with `[DisassemblyDiagnoser]` attribute on the class for class-level defaults.
- Output is saved as HTML and diff-friendly text artifacts in BenchmarkDotNet.Artifacts.

## Diagnoser Co-existence Rules

| Combination | Compatible | Notes |
|---|---|---|
| `MemoryDiagnoser` + `HardwareCounters` | Yes | Safe; runs in separate passes |
| `EtwProfiler` + `HardwareCounters` | Yes (Windows) | Use together for time + counter data |
| `PerfCollectProfiler` + `HardwareCounters` | Yes (Linux) | Use together; same perf session |
| `DisassemblyDiagnoser` + `MemoryDiagnoser` | Yes | Safe; independent collection |
| `DisassemblyDiagnoser` + `EtwProfiler` | Avoid | ETW tracing interferes with timing precision for disassembly inspection |
| Multiple `EtwProfiler` instances | No | Only one ETW profiler session per process |
| `ThreadingDiagnoser` + `EtwProfiler` | Caution | Thread-related ETW events may conflict; validate output |

## External Profiler Correlation Workflow

Use when BenchmarkDotNet counter data requires deeper trace-level investigation:

1. **Reproduce the suspect run** with the hypothesis-relevant hardware counters enabled.
2. **Record the ETW or perf trace** during a benchmark run using `EtwProfiler` or `PerfCollectProfiler`.
3. **Open the trace** in PerfView (`.etl`), dotTrace (`.dtt`), or `perf report` (Linux).
4. **Filter to the benchmark method** by class name and method name.
5. **Correlate counter columns** from BenchmarkDotNet output with the hot-path samples in the profiler trace.
6. **Record findings** in the change artifact with: hypothesis, counter values, profiler frame evidence, and conclusion.

### Tooling Quick Reference

| Tool | Platform | Trace Format | Best for |
|---|---|---|---|
| PerfView | Windows | `.etl` | GC, JIT, threading, cache |
| dotTrace | Windows | `.dtt` | Call stack sampling and timeline |
| Intel VTune | Windows/Linux | VTune project | Microarchitecture analysis |
| `perf report` / `perf annotate` | Linux | `perf.data` | CPU sampling and cache analysis |

## Interpretation Guide

### IPC (Instructions Per Cycle)

`IPC = InstructionRetired / TotalCycles`

- IPC > 2: well-vectorized or pipelined code.
- IPC 1–2: typical scalar code.
- IPC < 1: memory-bound; suspect cache misses or stalls.

### Cache Miss Rate

`Miss Rate = CacheMisses / CacheReferences`

- < 1%: excellent locality.
- 1–5%: acceptable for most workloads.
- > 5%: investigate data structure layout, access pattern, or working set size.

### Branch Misprediction Rate

`Misprediction Rate = BranchMispredictions / BranchInstructions`

- < 1%: well-predicted; low overhead.
- > 5%: consider branch-free alternatives or sorted input to improve predictability.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Diagnoser selection rationale | Hardware Counter Selection |
| Platform setup and prerequisites | Platform Setup |
| Co-existence rules | Diagnoser Co-existence Rules |
| Disassembly inspection | DisassemblyDiagnoser |
| Profiler trace correlation | External Profiler Correlation Workflow |
| Counter output interpretation | Interpretation Guide |

## Sources

- [Adam Sitnik's Blog](https://adamsitnik.com/) — hardware counters, ETW diagnoser, pitfall avoidance (primary authority)
- [BenchmarkDotNet Docs – Diagnosers](https://benchmarkdotnet.org/articles/configs/diagnosers.html)
- [BenchmarkDotNet GitHub – HardwareCounters](https://github.com/dotnet/BenchmarkDotNet)
- [PerfView Docs](https://github.com/microsoft/perfview)
- [dotnet/performance repo](https://github.com/dotnet/performance) — real-world diagnoser usage patterns
