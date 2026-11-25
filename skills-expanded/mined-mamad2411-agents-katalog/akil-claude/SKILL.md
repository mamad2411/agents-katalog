# AKIL — AI Assistant Context

> This file provides structured context for AI coding assistants working in this repository.
> It is not part of the project's deliverables.

---

## Project Identity

- **Full Name**: Adaptive Kernel Intelligence Layer for Runtime-Aware Container Scheduling
- **Acronym**: AKIL
- **One-line Purpose**: A Kubernetes scheduler plugin that uses eBPF-collected kernel telemetry to make placement decisions informed by actual OS-level workload behavior.
- **Context**: Operating Systems course project (August 2026)
- **Phase**: Review 1 complete; implementation pending

---

## Domain Context

This project sits at the intersection of three domains:

1. **Kubernetes Scheduling** — Extending `kube-scheduler` via the Scheduling Framework's `Score` plugin extension point to influence pod-to-node placement.
2. **eBPF Kernel Instrumentation** — Attaching eBPF programs to kernel tracepoints and perf events to observe per-container (per-cgroup) runtime behavior with low overhead.
3. **OS-Level Telemetry** — Collecting and aggregating fine-grained kernel signals that are invisible to Kubernetes' default scheduling inputs.

The project does **NOT** involve machine learning, reinforcement learning, or "AI" in any traditional sense — the name "Intelligence Layer" refers to the system's ability to make *informed* (not *learned*) scheduling decisions.

---

## Architecture — Four Layers

```
┌─────────────────────────────────────────────────────────────────────┐
│                       Kubernetes Cluster                            │
│                                                                     │
│  ┌───────────────────────────┐    ┌──────────────────────────────┐  │
│  │  Per-Node DaemonSet        │    │    Control Plane              │  │
│  │                           │    │                              │  │
│  │  ┌─────────────────────┐  │    │  ┌────────────────────────┐  │  │
│  │  │ Layer 1: eBPF Probes│  │    │  │ Layer 3: Aggregation   │  │  │
│  │  │ (kernel space)      │  │    │  │ Service (gRPC server)  │  │  │
│  │  │  • Page Fault       │  │    │  │  • Sliding window      │  │  │
│  │  │  • Cache Miss       │  │    │  │  • Profile Store       │  │  │
│  │  │  • Lock Contention  │  │    │  │  • Query API           │  │  │
│  │  │  • Context Switch   │  │    │  └──────────┬─────────────┘  │  │
│  │  └─────────┬───────────┘  │    │             │ gRPC unary     │  │
│  │            │ ring buffer   │    │  ┌──────────▼─────────────┐  │  │
│  │  ┌─────────▼───────────┐  │    │  │ Layer 4: Scheduler     │  │  │
│  │  │ Layer 2: Collector  │  │    │  │ Plugin (Score)         │  │  │
│  │  │ (user space, Go)    │──┼────┼─▶│  • Penalty scoring     │  │  │
│  │  │  • Cgroup resolver  │ gRPC  │  │  • Confidence adjust   │  │  │
│  │  │  • Batch assembler  │stream │  │  • Graceful degradation│  │  │
│  │  └─────────────────────┘  │    │  └────────────────────────┘  │  │
│  └───────────────────────────┘    └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### Layer 1: eBPF Probes (Kernel Space)

- **Location**: `pkg/ebpf/` (C source + bpf2go generated Go)
- **Shared BPF ring buffer** (16 MB, `BPF_MAP_TYPE_RINGBUF`) — all 4 probes write to one buffer
- **Event struct**: `{ u8 event_type, u64 cgroup_id, u64 timestamp_ns, union { per-type fields } }`
- **Internal map**: `BPF_MAP_TYPE_HASH` "lock_starts" for tracking lock contention begin/end pairs
- **Probes**:
  - `tracepoint/exceptions/page_fault_user` + `page_fault_kernel` — page fault rate
  - `perf_event` HW counter `PERF_COUNT_HW_CACHE_MISSES` — cache miss rate (sampled, 1 event per 10K misses)
  - `tracepoint/lock/contention_begin` + `contention_end` — lock/mutex contention duration
  - `tracepoint/sched/sched_switch` — context-switch frequency (captures both prev/next cgroup IDs)
- **CO-RE**: All programs use BTF for kernel portability. Minimum kernel: 5.8.

### Layer 2: Telemetry Collector (DaemonSet)

- **Location**: `cmd/collector/`, `pkg/telemetry/`
- **Pipeline**: Ring Buffer Reader → Cgroup Resolver → Batch Assembler → gRPC Stream Sender
- **Cgroup resolution**: cgroupfs walk → path parsing (containerd/CRI-O) → kubelet `/pods` API → LRU cache (TTL: 30s)
- **Key type**: `PodIdentity { namespace, pod_name, container, workload_key, node_name }`
- **`workload_key`**: Owner reference string `"namespace/Kind/name"` (e.g., `"default/Deployment/web-frontend"`) — identifies workload type, not individual pod
- **Batching**: Flush on 1000 events OR 1 second, whichever first
- **Backpressure**: Drop events if gRPC stream is down (not lossless — continuous observation, not audit logging)

### Layer 3: Aggregation Service (Deployment)

- **Location**: `cmd/aggregator/`, `pkg/profile/`, `pkg/proto/`
- **Dual API**: `StreamTelemetry` (bidirectional streaming for ingest) + `QueryProfile` / `QueryNodeProfiles` (unary for scheduler)
- **Storage**: `sync.Map` of `workload_key → *WorkloadProfile`
- **Sliding window**: 12 buckets × 5 seconds = 60s window. Circular buffer, oldest bucket evicted every 5s.
- **Rate computation**: `rate = total_events_in_window / window_duration_seconds`
- **Confidence**: `LOW` (<100 samples), `MEDIUM` (100–1000), `HIGH` (>1000)

### Layer 4: Scheduler Plugin (Score)

- **Location**: `cmd/scheduler-plugin/`, `pkg/scoring/`
- **Framework**: Kubernetes Scheduling Framework `ScorePlugin` interface
- **Algorithm**: Start at 100, subtract pairwise co-location penalties against every existing workload on the candidate node
- **Penalty formula per co-located workload**:
  - `cachePenalty = min(candidate.cache_miss_rate, p.cache_miss_rate) / max_rate × 35`
  - `lockPenalty = (candidate.lock_ratio + p.lock_ratio) × 30`
  - `pageFaultPenalty = (candidate.pf_rate + p.pf_rate) / max_rate × 20`
  - `ctxSwitchPenalty = (candidate.cs_rate + p.cs_rate) / max_rate × 15`
- **Confidence dampening**: LOW=0.25×, MEDIUM=0.75×, HIGH=1.0×
- **Graceful degradation**: Return neutral score (50) on any failure — aggregator unreachable, timeout (>5ms), no profile, unknown confidence

---

## Performance Budget

| Component | Metric | Target |
|---|---|---|
| eBPF probes | Per-event overhead | < 1μs |
| eBPF probes | Node CPU overhead | < 0.5% of one core |
| Collector | Event-to-gRPC latency (p99) | < 10ms |
| Collector | Memory (RSS) | < 64 MB |
| Aggregator | Ingestion throughput | ≥ 100K events/sec |
| Aggregator | Query latency (p99) | < 500μs |
| Plugin | Score() time (p99) | < 5ms |
| Plugin | Scheduling throughput impact | < 5% increase |

---

## gRPC Proto Schema Reference

The proto file at `pkg/proto/akil.proto` defines:

- **`AkilTelemetry` service**: `StreamTelemetry`, `QueryProfile`, `QueryNodeProfiles`
- **`TelemetryBatch`**: `{ node_name, batch_timestamp_ns, repeated TelemetryEvent }`
- **`TelemetryEvent`**: `{ event_type, workload_key, timestamp_ns, oneof payload }`
- **`RuntimeProfile`**: `{ workload_key, page_fault_rate, cache_miss_rate, lock_contention_ratio, context_switch_rate, sample_count, window_start_ns, window_end_ns, confidence }`
- **`ProfileConfidence` enum**: `UNKNOWN=0, LOW=1, MEDIUM=2, HIGH=3`

When generating proto code, use `protoc-gen-go` and `protoc-gen-go-grpc`. Generated files are committed.

---

## Security & Privileges

**Collector** (elevated):
- `CAP_BPF`, `CAP_PERFMON`, `CAP_SYS_ADMIN` (fallback for kernel <5.19)
- `hostPID: true`, read-only mounts: `/sys/fs/cgroup`, `/sys/kernel/btf`

**Aggregator & Plugin**: No elevated privileges.

---

## Kernel Signal Types

These are the four signal classes AKIL collects. When writing eBPF programs or aggregation logic, all four must be handled:

| Signal | Source | What It Indicates |
|---|---|---|
| **Page Fault Rate** | `tracepoint/exceptions/page_fault_*` | Memory pressure, working-set size relative to available memory, swap activity |
| **Cache Miss Rate** | `perf_event` (HW counter: `PERF_COUNT_HW_CACHE_MISSES`) | Cache locality / thrashing potential; high rates indicate workloads that compete for LLC |
| **Lock/Mutex Contention** | `tracepoint/lock/contention_begin/end` | Synchronization overhead; co-locating two contention-heavy workloads amplifies latency |
| **Context-Switch Frequency** | `tracepoint/sched/sched_switch` | CPU-boundedness vs I/O-boundedness; scheduling overhead |

---

## Tech Stack

| Layer | Choice |
|---|---|
| Language | Go 1.22+ |
| eBPF library | cilium/ebpf (pure Go, CO-RE) |
| eBPF programs | C (restricted kernel C, compiled via clang/llvm) |
| Code generation | bpf2go (cilium/ebpf) |
| Inter-component RPC | gRPC + Protocol Buffers |
| Hot-path storage | In-memory sliding-window ring buffer |
| Observability | Prometheus client_golang (dashboards only, not on scheduler critical path) |
| Build | Go modules + Makefile + Docker multi-stage |
| K8s integration | Kubernetes Scheduling Framework (v1.29+), Score extension point |
| Deployment | Helm 3 charts |
| Local dev cluster | kind (Kubernetes in Docker) |
| Testing | Go testing + testify (unit), kind + e2e (integration) |
| CI | GitHub Actions |

---

## Codebase Conventions

- **Directory layout**: Standard Go project layout — `cmd/` for binaries, `pkg/` for importable packages, `internal/` for non-exported packages, `deploy/` for Helm charts, `hack/` for scripts.
- **Error handling**: Wrap errors with `fmt.Errorf("context: %w", err)`. Never silently swallow errors.
- **Logging**: Use `klog` (Kubernetes standard) in scheduler plugin code. Use `slog` (Go stdlib structured logging) in collector and aggregator.
- **Naming**: Follow Go naming conventions. eBPF C programs use `snake_case`. Proto messages use `CamelCase`.
- **eBPF programs**: All `.c` files in `pkg/ebpf/` are compiled at build time via `bpf2go`. Never load eBPF programs from external files at runtime.
- **gRPC**: Proto files live in `pkg/proto/`. Generated Go code is committed to the repo (no protoc at deploy time).
- **Tests**: Unit tests co-located with source (`_test.go`). Integration tests in `test/e2e/`.

---

## Scope Boundaries — What IS and IS NOT Part of This Phase

### ✅ In Scope

- eBPF-based collection of the four signal types listed above
- Aggregation into per-workload runtime profiles
- A Kubernetes `Score` plugin that uses profiles to adjust node scores
- Synthetic benchmark workloads to demonstrate measurable improvement
- Quantitative evaluation: latency, cache-miss rate, migration/eviction counts
- Documentation of architecture, results, and scoped novelty claim

### ❌ Explicitly Out of Scope

- **Predictive migration** based on trend forecasting (future extension)
- **Reinforcement-learning** policy refinement across deployments (future extension)
- **Energy/thermal-aware** scheduling (future extension)
- **Behavioral-fingerprint-based** security quarantine (future extension)
- **Production hardening** — this is a research/course project, not production-grade software
- **Multi-cluster** scheduling — single cluster only

When generating code or documentation, do **not** include features from the out-of-scope list. They may be mentioned as "future work" but must not be implemented or designed in detail.

---

## Literature Anchors

When describing this project's novelty, use these anchors:

- **Borg/Autopilot** handle resource-usage prediction, not kernel-level behavioral signals → AKIL adds the signal types they don't cover.
- **Firmament** optimizes scheduling formulation, not signal acquisition → AKIL's telemetry could feed a Firmament-style optimizer, but currently uses the simpler Score-plugin approach.
- **Kubernetes Topology Manager** provides NUMA hints for CPU pinning → AKIL adds *dynamic, continuously observed* runtime signals alongside static topology.
- **Cilium/Pixie/Parca** collect eBPF telemetry for observability → AKIL closes the loop by feeding telemetry into a *live scheduling decision*.

The novelty claim is the **combination**: continuous kernel telemetry → aggregation → live scheduler input. Each piece exists independently; the closed loop does not.

---

## Common Pitfalls to Avoid

1. **Do not call this project "AI-powered"** — there is no machine learning. The name "Intelligence Layer" refers to informed decision-making, not artificial intelligence.
2. **Do not overclaim novelty** — the claim is narrow and specific (closed-loop architecture). Individual components are well-established.
3. **Do not put Prometheus on the scheduler's critical path** — Prometheus is for dashboards. The scheduler queries the in-memory aggregation service directly.
4. **Do not use CGo** — the entire userspace is pure Go. eBPF programs are C compiled to `.o` files and loaded via cilium/ebpf.
5. **Do not block scheduling on telemetry** — if the aggregation service is unreachable, the plugin must return a neutral score and let default scheduling proceed.
6. **Do not target specific kernel versions** — use CO-RE (BTF) to ensure portability across kernel 5.8+.
