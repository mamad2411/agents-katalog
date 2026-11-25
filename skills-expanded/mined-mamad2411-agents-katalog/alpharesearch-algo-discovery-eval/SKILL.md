---
name: alpharesearch-algo-discovery-eval
description: Evaluates an LLM-based autonomous agent's ability to discover novel algorithms through iterative idea generation, code modification, and execution-based verification. It probes the model's capacity for scientific reasoning, program synthesis, and optimization under simulated peer-review feedback. Use when the user wants to benchmark on AlphaResearch Algorithm Discovery Problems, or asks about evaluating this task. Reports win_rate (excel@best > 0).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2511.08522
  bibtex_key: yu2025alpharesearch
  confidence: high
---

# alpharesearch-algo-discovery-eval

> AlphaResearch: Accelerating New Algorithm Discovery with Language Models — Yu et al. (2025) (arXiv:2511.08522, 2025)

## What this evaluates

Evaluates an LLM-based autonomous agent's ability to discover novel algorithms through iterative idea generation, code modification, and execution-based verification. It probes the model's capacity for scientific reasoning, program synthesis, and optimization under simulated peer-review feedback.

## Datasets

- **AlphaResearch Algorithm Discovery Problems** — total 8; splits: test (8); repo https://github.com/answers111/alpha-research

## Metrics

- `win_rate (excel@best > 0)` **(primary)** — range: [0, 1]
  - Number of problems where the discovered algorithm's performance exceeds the best-known human baseline divided by the total number of problems (8). Range: [0, 1].
- `execution_reward` — range: other
  - Problem-specific objective function evaluated by a verification program (e.g., sum of radii for Packing Circles). Maximized during the discovery process via iterative patching.

## Input / output format

**Input**: Problem description, initial research proposal, baseline program, and metadata from previous iterations (ideas, code, execution results).

**Output**: New research ideas, code patches to modify the baseline program, and execution results. The best program and idea are selected as the final solution.

## Scoring recipe

```python
def compute_win_rate(discovered_perf, human_best_perf, total_problems=8):
    wins = sum(1 for d, h in zip(discovered_perf, human_best_perf) if d > h)
    return wins / total_problems

def compute_execution_reward(program, verification_fn):
    # verification_fn checks constraints and returns objective value
    return verification_fn(program)
```

## Common pitfalls

- Novelty validation is difficult; the agent often fails to improve upon human baselines in 6/8 problems despite reward growth.
- Execution success rates vary drastically across problems (e.g., 28.9% vs 51.7%), heavily influencing reward trends.
- The peer-review reward model filters ~30-40% of ideas but has a ~28% false rejection rate (43/151), which can prematurely halt promising searches.

## Evidence (verbatim from paper)

> AlphaResearch achieved a 2/8 win rate (excel@best > 0) against human researchers, with one notable success: the algorithm discovered by AlphaResearch for “Packing Circles” problem reaches the best-of-known performance (2.636 for n=26, 2.939 for n=32), outperforming human researchers (2.634 for n=26, 2.936 for n=32) and AlphaEvolve (2.635 for n=26, 2.937 for n=32).

## Citation

```bibtex
@misc{yu2025alpharesearch,
  title={AlphaResearch: Accelerating New Algorithm Discovery with Language Models},
  author={Yu et al. (2025)},
  year={2025},
  note={arXiv:2511.08522}
}
```

- arXiv: 2511.08522
