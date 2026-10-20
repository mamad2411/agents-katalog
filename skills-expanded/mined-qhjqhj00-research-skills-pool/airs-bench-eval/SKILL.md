---
name: airs-bench-eval
description: Evaluates AI research agents across the full scientific lifecycle, including idea generation, experiment design, and iterative refinement. Agents must generate and execute code to train models on specified datasets without baseline code, testing reasoning, generalization, and solution exploration capabilities. Use when the user wants to benchmark on AIRS-Bench, or asks about evaluating this task. Reports average normalized score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2602.06855
  bibtex_key: lupidi2026airsbench
  confidence: high
---

# airs-bench-eval

> AIRS-Bench: a Suite of Tasks for Frontier AI Research Science Agents — Lupidi et al. (2026) (arXiv:2602.06855, 2026)

## What this evaluates

Evaluates AI research agents across the full scientific lifecycle, including idea generation, experiment design, and iterative refinement. Agents must generate and execute code to train models on specified datasets without baseline code, testing reasoning, generalization, and solution exploration capabilities.

## Datasets

- **AIRS-Bench** — total 20; splits: test (20); repo https://github.com/facebookresearch/airs-bench

## Metrics

- `mean valid submission rate` — range: [0, 1]
  - Average fraction of valid (successful) runs across all tasks: VSR_a = (1/N_a) * sum(valid_{a,t} / total_{a,t}). Measures the agent's capability to produce a working solution and submit it confidently.
- `average normalized score` **(primary)** — range: [0, ∞)
  - NS_t^a = (phi_t(s_t^a) - phi_t(s_t^min)) / (phi_t(s_t^sota) - phi_t(s_t^min)), where phi_t(s) = -log10(|s - s_t^opt|). Normalizes raw scores against the worst observed score and literature SOTA using a logarithmic transform that weights closing gaps to the theoretical optimum equally across orders of magnitude. Failed/invalid submissions are treated as 0 normalized score.
- `Elo rating` — range: other
  - Derived from a Bradley-Terry model fitted to pairwise task outcomes. Skill parameters theta_a are converted to ratings via R_a = (400/ln(10)) * [theta_a - (1/N)sum(theta_k)] + 1000. Treats each task comparison as a game where better scores win, ties occur on equal/invalid submissions.

## Input / output format

**Input**: Task description specifying a scientific research goal, target dataset, and evaluation metric. Agents receive no baseline code, no SOTA methodology, and no SOTA score. They are granted access to a locally cached HuggingFace model repository (pre-2021) and one H-200 GPU for a 24-hour runtime.

**Output**: Executable code/scripts to train a model on the specified dataset, followed by a numerical score submission. Failed runs or invalid submissions that do not yield a numerical score are explicitly treated as 0 normalized score during aggregation.

## Scoring recipe

```python
def compute_airs_metrics(agent_runs, tasks, sota_scores, s_opt_scores):
    vsr_scores = []
    ns_scores = []
    for t in tasks:
        valid_runs = [r for r in agent_runs[t] if r.is_valid]
        total_runs = len(agent_runs[t])
        vsr_scores.append(len(valid_runs) / total_runs)
        
        s_agent = mean([r.score for r in valid_runs]) if valid_runs else 0.0
        s_min = min(all_agents_scores[t])
        s_sota = sota_scores[t]
        s_opt = s_opt_scores[t]
        
        phi = lambda s: -np.log10(abs(s - s_opt))
        ns = (phi(s_agent) - phi(s_min)) / (phi(s_sota) - phi(s_min))
        ns_scores.append(ns)
        
    return mean(vsr_scores), mean(ns_scores)
```

## Common pitfalls

- Agents are explicitly not provided with baseline code, SOTA methodology, or SOTA scores, requiring full solution exploration rather than incremental fine-tuning.
- Failed or invalid submissions are treated as 0 normalized score during averaging, heavily penalizing non-functional code or runtime crashes.
- The normalization transform uses the theoretical optimal score (s^opt, e.g., 1.0 for accuracy), not the best observed or SOTA score, which fundamentally changes how score improvements are weighted.

## Evidence (verbatim from paper)

> Our first evaluation metric is thus the mean valid submission rate (VSR) across tasks for an agent a, defined as ... where valid_{a,t} is the number of valid (successful) runs for agent a on task t, total_{a,t} is the number of total runs for agent a on task t ... Producing an aggregate score for AIRS-Bench is challenging due to the high diversity of tasks included: most tasks have unique metrics, and even for tasks sharing the same metric (e.g. accuracy), ranges reported in the literature for each of them may vary significantly. To aggregate heterogeneous metrics and ranges into a common scoring system, we define the normalized score (NS) of an agent a on a task t as: ... where s_t^{min} corresponds to the worst score observed across all seeds and all agents on task t, s_t^{sota} is the SOTA score on task t sourced from literature, s_t^{a} is the score achieved by agent a on task t and phi_t is a non-linear transformation.

## Citation

```bibtex
@misc{lupidi2026airsbench,
  title={AIRS-Bench: a Suite of Tasks for Frontier AI Research Science Agents},
  author={Lupidi et al. (2026)},
  year={2026},
  note={arXiv:2602.06855}
}
```

- arXiv: 2602.06855
