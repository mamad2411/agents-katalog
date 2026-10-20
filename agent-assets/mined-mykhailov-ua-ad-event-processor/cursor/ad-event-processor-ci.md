---
description: GitHub Actions merge gates, local CI commands, BPF thresholds
globs:
  - scripts/ci/**
  - .github/workflows/**
  - Makefile
  - .ci-baselines/**
alwaysApply: false
---

# CI and Merge Gates

## Purpose

GitHub Actions merge gates, local CI commands, BPF thresholds, and test tiers. Run before PR: `bash scripts/ci/lint.sh` and `bash scripts/ci/pr_fast.sh` (`SKIP_LINT=1` in pr_fast; lint in merge-lint).

Toolchain: Go **1.25.12**, Node **22**. Job prefix: `Gate merge-*` (GitHub Actions). Overlapping runs cancel in-progress except nightly/release.

## Required merge checks

| Check | Script | Blocks merge |
| :--- | :--- | :---: |
| Gate merge-lint | `lint/go.sh all` + `go vet` + `lint/go_modernize.sh` + `lint/gopls.sh` + `lint/lua.sh` + `lint/shell.sh` + `lint/python.sh` + `lint/proto.sh` + `lint/workflows.sh` + `lint/ts.sh` + `lint/configs.sh` | Yes |
| Gate merge-pr-fast | `bash scripts/ci/pr_fast.sh` (includes `static/doc_go_verify.sh`) | Yes |
| Gate merge-race-short | `bash scripts/ci/race_short.sh` | Yes |
| Gate merge-integration | `bash scripts/ci/integration_test.sh` | Yes |

### merge-pr-fast includes

Config validation, tier A docs, compliance, ClickHouse direct, integration slop, anti-slop, SQL safety, hot/cold static gates, escape heap, `static/package_size.sh`, `make test-alloc-gate`, `make test-fast`, state shard nil gate, `static/budget_rollback_gate.sh`, cold-path JSON, CAPI staging, legacy naming, `naming/antifraud_doc.sh`, `admin/web.sh`. Gate layering rules: `anti-slop.mdc` (CI and script slop).

### Main-only (push `main`)

| Check | Script |
| :--- | :--- |
| Gate main-full-test | `bash scripts/ci/full_test.sh` |
| Gate main-resilience | `bash scripts/fault/run.sh` (`RESILIENCE_MIN_PROOFS=52`, MR proofs >=12) |
| Gate main-license-red-team | `make license-red-team` |

## Path filters (ci.yaml)

| Output | Paths |
| :--- | :--- |
| `openrtb` | `internal/openrtb/**`, `internal/ingestion/openrtb*.go` |
| `model` | `model/**` |
| `go` | `**/*.go`, `go.mod`, `api/**`, `internal/**/queries/**` |
| `integration` | go deps + `scripts/**`, `tests/**`, `deploy/**`, compose, Dockerfiles |

Optional: govulncheck, openrtb-fuzz, fraudtrain, perf-smoke.

## Test tiers

| Target | Command |
| :--- | :--- |
| Fast | `make test-fast` (`-short`) |
| Race | `bash scripts/ci/race_short.sh` |
| Integration | `make test-integration` |
| Fault | `make test-fault` |
| Alloc | `make test-alloc-gate` |
| Budget rollback holdouts | `make budget-rollback-gate` (`-short`; `-race` via `race_short.sh`) |

Integration skips under `-short` need `integration:` in reason (`static/anti_slop.sh`, `static/integration_test_slop.sh`).

## BPF gate layers

| Layer | Scope | Blocks merge |
| :--- | :--- | :---: |
| A static | alloc-gate, race, anti-slop | PR |
| B microbench | `gate_bench.sh`, perf-gate +12% | PR smoke / main strict |
| C eBPF load | `bpf/resource.sh`, `load-report bpf-gate` | When `PERF_RUNNER_LABEL` set |
| D cold soak | admin, goleak | Nightly |
| E security | parser fuzz, SQL safety | Parallel |

### Hot-path BPF FAIL thresholds

| Metric | FAIL |
| :--- | ---: |
| tracker handler p99 | **>= 80 ms** |
| Redis Lua p99/shard | **>= 10 ms** |
| `tracker_outbound_connect` | **> 0** |
| `tracker_rss_delta_kb` | **> 5120** |

Static: `static/hot_path_static.sh` - no `fmt.Sprintf`, `context.With*`, hot `defer` in ingestion/rtb/tracker.

### Cold-path BPF FAIL

`fd_delta > 0`, `max_rss_delta_kb > 51200`, `ch_spool_segments > 0`, `broker_disk_writable < 1`, `stream_producer_queue_depth_p99 >= 1000`, admin handler p99 > 500 ms.

Self-hosted perf runner: Linux amd64, BTF, `PERF_RUNNER_LABEL`, Go 1.25.12, Docker, clang/llvm/libbpf.

## Nightly (UTC)

| Job | Schedule |
| :--- | :--- |
| perf-nightly | Mon 03:00 |
| admin-stack-e2e | Mon 03:00 |
| license-fuzz | Mon 04:00 |
| compose-fault | Mon 04:00 |
| bpf-nightly | Tue 04:00 |
| parser-fuzz | Sun 05:00 |

Baselines: `.ci-baselines/`.

Gate reports and workflow tee logs: `var/ci/` (`CI_ARTIFACT_DIR`, override with env). Scripts source `scripts/lib/ci_artifacts.sh` via `paths.sh`; workflows use `bash scripts/lib/tee_ci_log.sh <name> <command...>`.

| Path | Contents |
| :--- | :--- |
| `var/ci/escape_heap_gate.txt` | `static/escape_heap.sh` compiler `-m` report |
| `var/ci/perf-gate/` | `pr_bench.txt`, `baseline_bench.txt`, `gate_report.txt` from `gate_run.sh` |
| `var/ci/*.log` | CI job transcripts (`race_short.log`, `integration_test.log`, …) |

## Local commands

```bash
bash scripts/ci/pr_fast.sh
bash scripts/ci/race_short.sh
bash scripts/ci/integration_test.sh
bash scripts/fault/run.sh
PERF_GATE_STRICT=true bash scripts/test/load/gate_run.sh
export BPF_GATE_STRICT=true AD_EVENT_PROCESSOR_BPF_PROBE=1
bash scripts/ci/bpf/resource.sh
```

## Related rules

`anti-slop.mdc`, `load-test-bpf.mdc`, `quality.mdc`, `testing.mdc`.
