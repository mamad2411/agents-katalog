---
name: performance-profiling
description: Investigate latency, throughput, memory, and contention issues by baselining, profiling hot paths, and validating improvements with repo-local tools. Use when performance, capacity, or resource usage needs evidence-based diagnosis.
version: 2.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Performance Profiling

Use this skill when investigating slow paths, memory growth, concurrency bottlenecks, or capacity limits.

## When to Use

- latency is rising or unstable
- throughput is lower than expected
- memory usage keeps growing
- CPU spikes under load
- a change needs before/after performance comparison
- a service is approaching scaling or capacity limits

## Core Rules

- baseline before optimizing — no optimization may be merged without before/after flame graphs or benchmark evidence
- profile the real hot path, not an assumed one; use eBPF zero-instrumentation profiling (OTel Profiles — public Alpha since 2026-03 — with Pyroscope or Parca backends) for always-on continuous profiling alongside traces
- prefer repo-local and language-native tooling first; escalate to eBPF agents when system-wide profiling across runtimes is needed
- do not profile production without explicit approval and a safety plan — continuous profilers must stay under 1.5% CPU overhead with bounded memory limits
- validate improvements with repeatable measurements, not intuition — report p50/p95/p99 before and after, not mean alone
- correlate profiling data with distributed traces via `trace_id` using OTel Profiles OTLP format to avoid vendor lock-in
- for AI inference paths: measure and baseline model latency p50/p95/p99 separately from service latency — LLM calls are often the dominant latency source
- for GPU services (vLLM, Ollama, ONNX Runtime): profile GPU utilization, VRAM usage, KV cache hit rate, and time-to-first-token (TTFT) — use `nvitop` or PyTorch Profiler
- when speculative decoding is enabled (EAGLE-3 / MTP drafters): profile draft acceptance rate — acceptance below ~70% makes speculative decoding a net throughput loss; report acceptance alongside TTFT/ITL
- for batch inference services: profile queue depth and batch fill efficiency — under-batching wastes GPU; over-batching increases tail latency
- for RAG / semantic search: measure embedding cache hit rate — redundant embedding calls are the most common preventable AI cost spike
- report AI inference cost per request (\$ per call) alongside latency so optimization decisions weigh both UX and cost impact

## First Questions To Answer

1. What symptom matters most: latency, throughput, CPU, memory, or contention?
2. Under what workload does it happen?
3. Is the issue local to one code path, one dependency, or one environment?
4. What is the current baseline?
5. What metric will prove the change helped?

## Suggested Process

The full 7-step workflow (baseline, reproduce, identify hot path, form
hypothesis, apply smallest optimization, measure again, check secondary
effects) and the tool guidance live in
[`references/suggested-process.md`](references/suggested-process.md). Key
constraints the main file keeps in scope:

- Always record a baseline before optimizing; no optimization is merged without before/after evidence.
- Profile the real hot path with always-on continuous profiling (eBPF / Pyroscope); correlate with distributed traces via `trace_id`.
- Validate improvements with p50/p95/p99 before/after, not mean alone.
- For AI inference paths, measure model latency separately from service latency; for GPU services, profile VRAM/KV cache/TTFT.

## Production Safety

If profiling a shared or production environment, get explicit approval first,
use the least invasive method that answers the question, keep the duration
short, and ensure the profiling endpoints are access-controlled. For the
full production-safety checklist, see
[`references/patterns-and-safety.md`](references/patterns-and-safety.md).

## Common Performance Patterns

For the full pattern library (request path, data, memory, concurrency), the
AI inference-specific profiling checklist, and the production-safety rules,
see [`references/patterns-and-safety.md`](references/patterns-and-safety.md).

## What To Capture In Your Output

When reporting performance work, include:

- workload used
- baseline metrics
- hotspot identified
- optimization applied
- measured result after the change
- remaining risks or next bottlenecks

## Checklist

- [ ] baseline recorded
- [ ] issue reproduced
- [ ] hot path identified with measurement
- [ ] narrow hypothesis tested
- [ ] optimization applied
- [ ] before/after comparison recorded (p50/p95/p99, not just mean)
- [ ] correctness and secondary effects checked
- [ ] for AI inference paths, model latency profiled separately from service latency
- [ ] for GPU services, VRAM/KV cache/TTFT captured
- [ ] production profiling approved with safety plan if applicable

## Output Contracts

When benchmarking, profiling hot paths, or diagnosing system performance bottlenecks, emit:

- **`contracts/schemas/performance-audit.json`** — Emitted to provide empirical latency, throughput, and resource profiling evidence before and after optimization. Set `produced_by_role` to the profiling engineer role.

Skip emission for casual development-mode micro-benchmarks with no gate dependency.

## Related Skills

- **troubleshoot-service**: Debug runtime and dependency issues
- **review-code**: Review risky optimizations and trade-offs
- **write-tests**: Add regression or benchmark coverage
- **navigate-service**: Map the hot path before optimizing
- **meeting-review**: Review performance trade-offs across roles
- **develop-mobile-app**: Profile React Native frame rates, Hermes bytecode, and JS thread starvation

## Failure Modes

- **Optimization without baseline**: a "fix" is merged without before/after evidence. Mitigation: enforce baseline-first; the validator rejects performance reports without a documented baseline.
- **Mean-only reporting**: only the mean latency improves while p95/p99 worsens. Mitigation: report tail latency; treat tail regressions as a release-blocking issue.
- **Wrong hot path**: the optimization targets an assumed hot path that the profile does not actually show. Mitigation: profile the real hot path; cross-check with traces via `trace_id`.
- **Production profile without approval**: a continuous profiler runs in production without a safety plan. Mitigation: enforce the 1.5% CPU / bounded memory limit and explicit user approval.
- **Inference cost hidden**: a latency win is achieved by routing through a more expensive model, raising per-request cost. Mitigation: report cost per request alongside latency; treat unexplained cost increases as a regression.
- **Downstream bottleneck shifted**: an optimization moves the bottleneck to a downstream system. Mitigation: re-profile the full request path after each change; check secondary effects.
- **Tail regression ignored**: the change improves the median but worsens p99. Mitigation: every before/after report must include p50/p95/p99; reject reports that hide the tail.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a profile report may try to reframe a regression as an improvement by cherry-picking metrics. Cross-check the report against the full metric set; reject selective reporting.
- **ASI03 Identity & Privilege Abuse**: production profiling endpoints must be access-controlled; reject profiles that require standing privileged access.
- **ASI04 Supply Chain**: continuous profiler agents must be schema-validated against the expected manifest; treat unknown or schema-drifted profilers as untrusted.
- **ASI05 RCE Guard**: never run a profiler that evaluates dynamic code from external content; validate every profiler configuration before deployment.
- **ASI07 Inter-Agent Communication**: profile reports are consumed by SRE and development roles; emit a structured `performance-audit.json` so each role can validate the same evidence.

