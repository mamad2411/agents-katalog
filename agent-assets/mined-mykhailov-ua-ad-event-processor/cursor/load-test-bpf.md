---
description: BPF + Prometheus load-test validation before perf claims
globs:
  - scripts/test/**
  - scripts/dev/bpf*
  - cmd/bpf-collector/**
  - cmd/loadgen/**
  - deploy/dev/bpf/**
alwaysApply: false
---

# Load Test and BPF Probes

## Purpose

Before claiming hot-path perf wins, run Prometheus bottleneck report and optional BPF session report. Does not replace production `edge-xdp` compliance maps. Requires root/CAP_BPF on dev host.

## Quick path

```bash
make bpf-dev
AD_EVENT_PROCESSOR_BPF_PROBE=1 bash scripts/test/load/malformed.sh business
go run ./cmd/load-report all
```

Loadgen + reports under `var/load-test/<timestamp>/`. Outputs: `bottleneck-report.md` + `bpf-report.md`.

Standalone session (no loadgen):

```bash
make bpf-session-start
make bpf-session-stop
```

## Environment

| Variable | Role |
| :--- | :--- |
| `AD_EVENT_PROCESSOR_BPF_PROBE=1` | Enable BPF probe collection |
| `AD_EVENT_PROCESSOR_BPF_SAMPLE_RATE` | Use 10 on laptops |
| `AD_EVENT_PROCESSOR_BPF_SLOW_US` | Slow-path threshold |
| `AD_EVENT_PROCESSOR_BPF_TARGETS` | `tracker,nginx,redis,processor` |

## Artifacts

Under `var/load-test/<utc>/`:

| File | Content |
| :--- | :--- |
| `bottleneck-report.md` | Prometheus SLO summary |
| `bpf-report.md` | BPF scheduling and syscall view |
| `bpf/maps/summary.json` | Map statistics |
| `events.ndjson` | Raw probe events |

## Interpretation

| Source | Trust for |
| :--- | :--- |
| BPF reports | Host scheduling, syscall latency, worker pinning |
| Prometheus | App SLOs (`ad_http_request_duration_seconds`, Lua p99, queue depth) |

High loadgen CPU on laptop often caps RPS before tracker Lua - do not cite laptop RPS as production capacity.

## Abort rules

Abort if handler p99 > 80 ms for 30 s (`malformed.sh`, `core.mdc`). Also abort on budget invariant violation.

## BPF gate thresholds (CI)

When `PERF_RUNNER_LABEL` set, `bash scripts/ci/bpf/resource.sh` enforces:

| Metric | FAIL |
| :--- | ---: |
| tracker handler p99 | >= 80 ms |
| Redis Lua p99/shard | >= 10 ms |
| `tracker_outbound_connect` | > 0 |
| `tracker_rss_delta_kb` | > 5120 |

See `ci.mdc` for full BPF gate layers.

## Related rules

`ci.mdc`, `core.mdc`, `development.mdc`, `fault-tests.mdc`, `hot-path.mdc`.
