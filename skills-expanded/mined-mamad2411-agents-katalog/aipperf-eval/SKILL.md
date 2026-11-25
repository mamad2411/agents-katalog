---
name: aipperf-eval
description: Evaluates the end-to-end performance and weak scalability of heterogeneous AI-HPC systems using AutoML workloads. It measures how efficiently clusters execute dynamically scaling machine learning training and inference tasks across varying numbers of nodes. Use when the user wants to benchmark on CIFAR10, or asks about evaluating this task. Reports cumulative OPS.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2008.07141
  bibtex_key: ren2020aipperf
  confidence: high
---

# aipperf-eval

> AIPerf: Automated machine learning as an AI-HPC benchmark — Ren et al. (2020) (arXiv:2008.07141, 2020)

## What this evaluates

Evaluates the end-to-end performance and weak scalability of heterogeneous AI-HPC systems using AutoML workloads. It measures how efficiently clusters execute dynamically scaling machine learning training and inference tasks across varying numbers of nodes.

## Datasets

- **CIFAR10** — total ?; splits: train (-1)

## Metrics

- `cumulative OPS` **(primary)** — range: other
  - Total number of operations executed over a fixed evaluation period, measured in Peta OPS (POPS). Calculated after an initial warm-up phase until the value converges and increases steadily.

## Input / output format

**Input**: Heterogeneous AI-HPC cluster resources (CPU, memory, AI accelerators) configured via Kubernetes/Docker containers, running an AutoML workload that automatically adapts job size to the number of available nodes.

**Output**: Log files containing generated architectures, hyperparameter configurations, per-epoch accuracy, timestamps, and a final cumulative OPS score. GPU/NPU utilization and memory occupancy metrics are also recorded.

## Scoring recipe

```python
def calculate_score(logs, time_window_hours):
    # Filter logs to exclude warm-up phase until convergence
    valid_ops = [op for op in logs.ops_timeline if op.time > warmup_end]
    # Calculate cumulative operations over the pre-assigned time
    cumulative_ops = sum(valid_ops)
    # Convert to Peta OPS (10^15)
    score_pops = cumulative_ops / 1e15
    return score_pops
```

## Common pitfalls

- Failing to account for the warm-up phase, which causes initial OPS to be artificially low before convergence.
- Comparing absolute OPS across different cluster sizes without recognizing the benchmark uses weak scaling (job size increases with nodes), making per-node normalization necessary for fair comparison.
- Ignoring environment consistency requirements; the benchmark relies on Kubernetes/Docker containers with specific library versions, so hardware/software mismatches will break reproducibility.

## Evidence (verbatim from paper)

> As for stability characteristic, within the pre-assigned hours on various types and scales of AI accelerators, the cumulative OPS is calculated and shown in Fig.[4] as score. As we can see that in both two clusters, the cumulative OPS converges and increases steadily. The regulated score in Fig.[4] also converges since it is essentially just OPS multiplied with the model performance as a coefficient.

## Citation

```bibtex
@misc{ren2020aipperf,
  title={AIPerf: Automated machine learning as an AI-HPC benchmark},
  author={Ren et al. (2020)},
  year={2020},
  note={arXiv:2008.07141}
}
```

- arXiv: 2008.07141
