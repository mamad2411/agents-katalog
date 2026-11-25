---
name: adiabatic-quantum-benchmark-eval
description: Evaluates the performance of adiabatic quantum optimization on complex network analysis tasks. It benchmarks quantum annealing against classical methods on Chimera Ising spin glass instances, independent set problems, planted-solution instances, and community detection. Use when the user wants to benchmark on Chimera Ising spin glass instances, Independent set problems, Planted-solution instances, Community detection, or asks about evaluating this task. Reports D-Wave run-time estimation.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1604.00319
  bibtex_key: parekh2016benchmarking
  confidence: low
---

# adiabatic-quantum-benchmark-eval

> Benchmarking Adiabatic Quantum Optimization for Complex Network Analysis — Parekh et al. (2016) (arXiv:1604.00319, 2016)

## What this evaluates

Evaluates the performance of adiabatic quantum optimization on complex network analysis tasks. It benchmarks quantum annealing against classical methods on Chimera Ising spin glass instances, independent set problems, planted-solution instances, and community detection.

## Datasets

- **Chimera Ising spin glass instances** — total ?; splits: test (-1)
- **Independent set problems** — total ?; splits: test (-1)
- **Planted-solution instances** — total ?; splits: test (-1)
- **Community detection** — total ?; splits: test (-1)

## Metrics

- `D-Wave run-time estimation` **(primary)** — range: other
  - Wall-clock execution time measured for the quantum annealer to solve the Ising spin glass instances.
- `Modularity results` — range: other
  - Graph modularity score quantifying the quality of detected community structures in network graphs.

## Input / output format

**Input**: Graph/network instances encoded as Chimera Ising spin glass formulations, independent set constraints, planted-solution graphs, and community detection networks.

**Output**: Spin configurations (solutions) from the quantum annealer, execution times, and modularity scores.

## Scoring recipe

```python
# Based on sections 5.2.2, 5.2.3, 5.5.2, 5.5.3
def evaluate(results):
    runtime = results["execution_time_seconds"]
    modularity = results["modularity_score"]
    # Compare quantum runtime and solution quality against classical baselines
    return {"runtime": runtime, "modularity": modularity}
```

## Common pitfalls

- Hardware connectivity constraints on the Chimera topology require minor embedding, which artificially inflates logical problem sizes and skews scaling analysis.
- Direct runtime comparisons between quantum annealers and classical solvers may not account for differences in parallelization, problem encoding overhead, or optimization paradigms.
- Modularity optimization is non-convex; reported results may reflect local optima rather than global community structures without rigorous verification.

## Evidence (verbatim from paper)

> 5.2.2 D-Wave run-time estimation 5.2.3 Results ... 5.5.3 Modularity results

## Citation

```bibtex
@misc{parekh2016benchmarking,
  title={Benchmarking Adiabatic Quantum Optimization for Complex Network Analysis},
  author={Parekh et al. (2016)},
  year={2016},
  note={arXiv:1604.00319}
}
```

- arXiv: 1604.00319
