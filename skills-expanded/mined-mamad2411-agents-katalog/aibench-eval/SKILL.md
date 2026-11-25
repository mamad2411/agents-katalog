---
name: aibench-eval
description: Probes the end-to-end latency and micro-architectural efficiency of AI-accelerated internet service workloads. It measures how AI components impact service latency and GPU execution stalls during both online inference and offline training. Use when the user wants to benchmark on AIBench E-commerce Search Workload, or asks about evaluating this task. Reports Latency (avg, p90, p99).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1908.08998
  bibtex_key: gao2019aibench
  confidence: high
---

# aibench-eval

> AIBench: An Industry Standard Internet Service AI Benchmark Suite — Gao et al. (2019) (arXiv:1908.08998, 2019)

## What this evaluates

Probes the end-to-end latency and micro-architectural efficiency of AI-accelerated internet service workloads. It measures how AI components impact service latency and GPU execution stalls during both online inference and offline training.

## Datasets

- **AIBench E-commerce Search Workload** — total 100000; splits: test (20000)

## Metrics

- `Latency (avg, p90, p99)` **(primary)** — range: milliseconds
  - Measures the time taken to process query requests. Reported as average, 90th percentile, and 99th percentile latencies in milliseconds across 20,000 completed queries.
- `SM Efficiency` — range: percent
  - Streaming Multiprocessor efficiency, defined as the percentage of time that the SM has one or more warps active during kernel execution.

## Input / output format

**Input**: Simulated user query requests (Poisson distribution, 30s warmup) sent to an online server backed by a 100k-product database; for offline evaluation, PyTorch implementations of 10 AI component benchmarks run on Titan XP GPU.

**Output**: Measured latency percentiles (ms), SM efficiency (%), running time breakdown by kernel category, and GPU execution stall percentages.

## Scoring recipe

```python
latencies = [measure_request_time(req) for req in requests]
avg_latency = sum(latencies) / len(latencies)
p90_latency = sorted(latencies)[int(len(latencies) * 0.9)]
p99_latency = sorted(latencies)[int(len(latencies) * 0.99)]
sm_efficiency = (time_active_warps / total_kernel_time) * 100
cache_misses_per_kilo = (total_cache_misses / total_instructions) * 1000
```

## Common pitfalls

- Confusing the latency contribution of AI components (e.g., recommender) with non-AI components (e.g., database access, communication), as both significantly impact total service latency.
- Assuming SM efficiency directly correlates with raw throughput; it specifically measures active warp occupancy, which can be low even if compute units are busy due to stalls.
- Overlooking that stall analysis is performed at the kernel and function level (e.g., using nvprof), not just at the application level.

## Evidence (verbatim from paper)

> Latency is an important metric to evaluate the service quality. We find that the overall latencies of the entire execution paths of the current baseline implementation are 161.13, 392, and 956 milliseconds for the average, 90th percentile and 99th percentile latencies respectively.

## Citation

```bibtex
@misc{gao2019aibench,
  title={AIBench: An Industry Standard Internet Service AI Benchmark Suite},
  author={Gao et al. (2019)},
  year={2019},
  note={arXiv:1908.08998}
}
```

- arXiv: 1908.08998
