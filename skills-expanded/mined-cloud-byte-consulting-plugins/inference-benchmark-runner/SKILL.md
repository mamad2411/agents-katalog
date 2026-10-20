---
name: inference-benchmark-runner
description: Benchmark model-inference latency, throughput, GPU efficiency, and cost on Kubernetes without conflating performance with answer quality. Use for TTFT, tokens per second, inter-token latency, p95/p99, concurrency sweeps, warm versus cold starts, DCGM utilization, VRAM, cost per 1,000 tokens, batching, k6/Locust load tests, or checkpoint performance comparisons.
---

# Inference Benchmark Runner

## Purpose
Produce defensible performance numbers for a model under realistic load on GPU Kubernetes, and compare candidates on speed, latency, throughput, efficiency, and cost — the axis `llm-eval-harness` deliberately ignores. A model can be the most accurate checkpoint in the registry and still fail its release gate because it blows the latency SLO or costs 3x per token. This skill measures that, correlates it with what the GPU is actually doing, and hands a comparison table to the release gate and the rollout strategist.

Scope boundary: quality lives in `llm-eval-harness`; this skill answers "how fast, how many, how much." Run both before promoting anything.

## Core model to hold in your head

### The metric catalog (know exactly what each means)
| Metric | Definition | Why it matters |
|---|---|---|
| **TTFT** (time to first token) | Latency from request to the first streamed token | The number users *feel*; interactive UIs notice ~250ms, abandon after seconds |
| **Inter-token latency** (ITL/TPOT) | Avg time between subsequent tokens | Governs perceived streaming smoothness once generation starts |
| **Tokens/sec (per request)** | Output tokens ÷ generation time for one request | Raw generation speed of the model on this hardware |
| **Throughput** (system tokens/sec) | Total tokens/sec across all concurrent requests | The capacity number for sizing and cost |
| **Throughput-at-concurrency** | Throughput measured across a sweep of concurrency levels | Reveals the saturation knee; the single most useful curve |
| **p50 / p95 / p99 latency** | Percentile end-to-end request latency | SLOs live at the tail; averages hide the pain |
| **Perf-per-billion-params** | (tokens/sec) ÷ (parameters in billions) | Size-normalized efficiency — compares models of different sizes fairly |
| **VRAM footprint** | Peak GPU memory at a given batch/context | Determines what fits, MIG sizing, and how much you can batch |
| **Cost-per-1k-tokens** | GPU $/hr ÷ (tokens/sec × 3.6) | The economics number the release gate and FinOps care about |

Two efficiency framings for cross-model comparison:
- **Raw tokens/sec** — speed on this hardware; always flatters the bigger model on bigger hardware.
- **Tokens/sec ÷ billions-of-params** — size-normalized efficiency; a higher number means the model does more with its size. This is the fair way to rank a 7B against a 70B under a fixed memory budget, and the one that matters when the question is "most throughput per GPU dollar under a VRAM ceiling."

Anchor the numbers to what users feel: interactive latency becomes noticeable around **250ms** and users abandon after a few seconds — so a p95 TTFT SLO in the hundreds-of-ms range, not the mean, is usually the binding constraint for a research UI. Batch/offline workloads invert this: they tolerate seconds-to-minutes latency and are scored on aggregate throughput and cost instead.

### Load-test design
- **Concurrency sweep** is the core experiment: hold input/output length fixed, step concurrency (1, 2, 4, 8, 16, 32, …), record throughput and p95/p99 at each level. Throughput rises then plateaus (the **saturation knee**); latency stays flat then hockey-sticks past the knee. Report the knee — it is the usable capacity, not the peak, and it is the concurrency `inference-rollout-strategist` sets the autoscaling target from.
- **Warm vs cold** must be separated — never average them together:
  - **Cold** = first request after pod/model load; includes weight load, CUDA init, and cache warm-up — can be minutes for large models, and model caching is what mitigates it. Cold numbers drive readiness-probe timeouts and autoscaling-headroom decisions.
  - **Warm** = steady state after warm-up. Warm numbers drive the user-facing SLOs.
- **Fix the workload shape.** Input length, output length, and sampling params dominate every metric — pin them and state them, or the numbers are meaningless across runs. Run a representative distribution of prompt/response lengths for the actual research workload, not one synthetic length.
- **Separate prefill from decode.** TTFT scales with *input* length (prefill compute); total latency scales with *output* length (decode). A single length hides which stage is slow — sweep short-in/long-out and long-in/short-out to locate the bottleneck.
- **Isolate the variable.** Same GPU type, same serving runtime, same batch config, same K8s node — change only the model (or only the one knob under test) between runs.

### The serving runtime is a variable, not a constant
The same weights on the same GPU produce wildly different numbers under different serving runtimes (vLLM, TGI, TensorRT-LLM, a plain framework server), because they differ in batching strategy, KV-cache management, quantization support, and kernel fusion. When the research question is "which model," pin one runtime. When it is "how fast can we serve this model," the runtime *is* part of the answer — benchmark the candidates. Record runtime name, version, quantization (fp16/int8/int4/awq), and tensor-parallel degree in the pinned-environment block; a benchmark that omits them cannot be reproduced or trusted across a team.

### GPU-utilization correlation (DCGM)
LLM serving performance — TTFT, tokens/sec, throughput, latency — **cannot be read from the node**; node CPU/memory tell you nothing about GPU serving health. Scrape GPU telemetry with the **NVIDIA DCGM exporter** into Prometheus and correlate each signal with the request-level metrics:
- **SM / compute utilization** — high occupancy with low tokens/sec means you are *not* compute-bound; look elsewhere.
- **Memory-bandwidth utilization** — the usual real bottleneck for decode; if this is pinned while SM is idle, you are memory-bound and bigger batches won't help linearly.
- **VRAM used** — sets the batch/context ceiling and MIG sizing; the number that decides what fits.
- **Power draw and temperature** — thermal throttling silently caps sustained throughput on long runs.

The point is the correlation, not the raw number — a run at 95% GPU utilization with low throughput means you are memory-bandwidth-bound or batching poorly, not "well utilized."

GPUs also can't be sliced like CPU, so how the model is packed onto the device changes the numbers: **MIG** (multi-instance GPU) partitions, **time-slicing**, and **CUDA MPS** each trade isolation for density and shift both VRAM footprint and achievable throughput. State the sharing mode alongside the GPU type — a benchmark on a full A100 is not comparable to one on a MIG slice of the same card. On the Lambda managed cluster these are node/scheduler choices that belong in the pinned-environment section of the report.

### Batching effects
Throughput and latency trade against each other through the serving runtime's batching policy — and this trade dominates most of the numbers:
- **Static/dynamic batching** — larger batches raise system throughput and GPU utilization but raise per-request latency and VRAM footprint.
- **Continuous / in-flight batching** (vLLM-class) — schedules at the token level, decoupling throughput from per-request latency somewhat, which is why it usually wins for interactive serving.
- **Reproducibility rule** — always report the batch configuration alongside every number. A throughput figure without its batch policy, max-concurrency, and KV-cache settings is not reproducible and not comparable.

### Cost modeling (the number FinOps and the gate read)
Speed is only half the decision; the research division pays for GPU-hours. Derive cost deliberately:
- **Cost-per-1k-tokens** = GPU $/hr ÷ (system tokens/sec × 3.6). Compute it at the *operating* concurrency (the knee), not at concurrency 1 — batching is what makes a GPU economical, so a single-request cost figure overstates real cost several-fold.
- **Cost-per-request** = cost-per-1k-tokens × avg output tokens ÷ 1000; the number to compare against a hosted-API alternative.
- **Idle cost** — a real-time endpoint runs 24/7; fold its floor (min replicas × GPU $/hr) into the comparison, because a slightly slower model that scales to zero between eval sweeps can be cheaper overall.
- **Batch economics** — for large offline eval sweeps, a batch job that spins up, saturates the GPU, and tears down beats a standing endpoint on cost and exploits the hardware better.

### Research-workload profiles
Benchmark the two shapes the research division actually runs, separately: **interactive** (low concurrency, latency-SLO-bound, warm) for human-in-the-loop evaluation, and **eval-sweep / batch** (high concurrency, throughput-bound, cost-sensitive) for running a suite over thousands of cases. A model can win one and lose the other; report both rather than a single blended number.

### Common pitfalls (call these out in every report)
- **GPU utilization ≠ application performance.** High SM occupancy can coincide with terrible tokens/sec (memory-bound, bad batching). Never report utilization as a success metric on its own.
- **Averages hide the tail.** Report p95/p99, not mean latency, for anything with an SLO.
- **Cold folded into warm** understates steady-state speed and hides real cold-start risk — separate them.
- **One prompt length** generalizes to nothing — sweep realistic shapes.
- **Un-pinned serving config** (batch size, max concurrency, KV-cache settings) makes cross-run comparison invalid.
- **Ignoring the saturation knee** — quoting peak throughput at a concurrency the SLO can never allow.
- **Comparing across runtimes or quantizations by accident** — an int4 model on vLLM vs an fp16 model on a framework server is two variables changed, not one.
- **Reporting concurrency-1 cost** — it ignores the batching that makes a GPU economical and overstates real cost several-fold.

## Workflow
1. **Define the workload profile.** Prompt/response length distribution, sampling params, target concurrency range, and the SLO (e.g. p95 TTFT < X, p95 end-to-end < Y) for the research use case.
2. **Pin the environment.** GPU type on the Lambda managed cluster, serving runtime + version, batch/KV-cache config, node class. Record all of it — it is part of the result.
3. **Wire telemetry.** DCGM exporter → Prometheus for GPU metrics; a load tool (k6 or locust) emitting per-request TTFT/ITL/latency; a `ServiceMonitor` scraping the serving endpoint `/metrics`.
4. **Run the cold pass.** First-request-after-load measurements; capture weight-load and warm-up time.
5. **Run the concurrency sweep (warm).** Step concurrency, record throughput and p50/p95/p99 at each level; find the saturation knee.
6. **Correlate with DCGM.** Overlay GPU utilization, memory bandwidth, VRAM, power against the throughput curve; diagnose the binding resource.
7. **Compute derived metrics.** Perf-per-billion-params, VRAM footprint at the chosen operating point, cost-per-1k-tokens and cost-per-request from the GPU hourly rate.
8. **Compare candidates.** Same profile, one variable changed; build the comparison table for both the interactive and the eval-sweep profile.
9. **Verify reproducibility.** Re-run one configuration; if the numbers move materially, an unpinned variable (batch, runtime, thermal state) is loose — find it before reporting.

## Output spec
Deliver a **Benchmark Comparison Report**: (1) workload profile + SLO + pinned environment (GPU, runtime, batch config); (2) per-model table — TTFT (p50/p95), ITL, warm tokens/sec, system throughput, p95/p99 end-to-end, throughput-at-concurrency knee, perf-per-billion-params, VRAM footprint, cost-per-1k-tokens; (3) cold-start section — model-load time and first-request latency, separate from warm; (4) the concurrency-sweep curve with the saturation knee marked; (5) DCGM correlation — binding resource per model and the utilization-vs-throughput reading; (6) pitfall audit — explicit note that utilization is reported as diagnostic not as success, and that batch config is pinned; (7) a pass/fail line against the SLO, handed to `model-release-gate`, and the recommended operating concurrency handed to `inference-rollout-strategist` for autoscaling-policy pairing. Note the Lambda managed-Kubernetes / OSS context throughout: DCGM + Prometheus for telemetry, k6/locust for load, KServe-class serving; asymmetric GPU autoscaling detail belongs to the rollout sibling.

## Suggested effort
Medium — the concurrency sweep plus DCGM correlation is a half-day per model once the load harness and telemetry are wired; the first wiring of k6/locust + DCGM exporter + ServiceMonitor is the up-front cost. Cold-start and cost modeling add an hour. When time is short, a warm concurrency sweep with p95 latency and cost-per-1k-tokens at the knee is the highest-signal subset.

## Siblings
`llm-eval-harness` (the quality axis — run alongside) · `model-release-gate` (consumes the SLO pass/fail) · `inference-rollout-strategist` (uses the saturation knee for autoscaling policy) · `drift-monitor-designer` (performance metrics can drift too — TTFT/throughput become monitored signals).
