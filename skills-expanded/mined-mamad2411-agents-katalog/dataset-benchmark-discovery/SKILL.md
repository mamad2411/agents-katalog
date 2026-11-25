---
name: dataset-benchmark-discovery
description: Use when the user asks for latest datasets, benchmark suites, leaderboards, baseline or SOTA comparisons, dataset selection for experiments, or evidence that a paper needs complete experimental validation. This skill routes to the dataset_benchmark_discovery tool and keeps access/license limits explicit.
---

# Dataset Benchmark Discovery

Use this skill before experiment planning or manuscript drafting when the user
needs datasets, benchmarks, metrics, baselines, or leaderboard context.

## Core Rules

- Prefer the `dataset_benchmark_discovery` tool over generic browsing for dataset and benchmark mapping.
- Do not download restricted, login-gated, license-gated, or private data unless the user has provided access and the environment is configured for it.
- Treat `dataset_benchmark_map.json` as a candidate map. It can support dataset selection and experiment planning, but it is not executed experimental evidence.
- Verify version/date, license, standard split, metric definition, and official leaderboard status before writing strong manuscript claims.
- Route actual evaluation to `experiment_lab`, then use `claim_support_matrix.json` for manuscript claim support.

## Workflow

1. Call `dataset_benchmark_discovery(topic=..., scope=...)`.
2. Review candidates by task fit, recency/version, license/access, metric alignment, and reproducibility risk.
3. If the user wants experiments, choose feasible datasets and pass local paths or uploaded files into `experiment_lab`.
4. If writing a paper before experiments are complete, describe benchmark choices as planned validation, not completed results.

## Output Discipline

When summarizing results, report:

- strongest candidate datasets/benchmarks
- access and license risks
- standard metrics and splits when detected
- baseline/SOTA hints when available
- what still needs manual verification
