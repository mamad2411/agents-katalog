---
name: ahat-planning-eval
description: Evaluates an agent's ability to decompose abstract, long-horizon household instructions into feasible, constraint-satisfying action plans. It probes intent inference, subgoal grounding, and robustness to environmental clutter and instruction ambiguity. Use when the user wants to benchmark on AHAT, Human Tasks, PARTNR, Behavior-1K, or asks about evaluating this task. Reports Success Rate (SR).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2602.12244
  bibtex_key: liu2026anyhouseanytask
  confidence: high
---

# ahat-planning-eval

> Any House Any Task: Scalable Long-Horizon Planning for Abstract Human Tasks — Zhihong Liu et al. (2026) (arXiv:2602.12244, 2026)

## What this evaluates

Evaluates an agent's ability to decompose abstract, long-horizon household instructions into feasible, constraint-satisfying action plans. It probes intent inference, subgoal grounding, and robustness to environmental clutter and instruction ambiguity.

## Datasets

- **AHAT** — total 346; splits: Easy (146), Complex (94), Abstract (108)
- **Human Tasks** — total 50; splits: (unstated)
- **PARTNR** — total 368; splits: (unstated)
- **Behavior-1K** — total 30; splits: (unstated)

## Metrics

- `Success Rate (SR)` **(primary)** — range: [0, 1]
  - SR = (1/N) * Σ I_feas(o_i) * R_comp(o_i), where I_feas indicates plan feasibility and R_comp indicates task completion across N samples.
- `Planning Time (T)` — range: other
  - Average wall-clock or inference time to generate and solve the full plan across N tasks.

## Input / output format

**Input**: Natural language instruction describing a household task, paired with a structured scene graph representing the environment (objects, furniture, rooms, and their spatial relationships).

**Output**: A sequence of grounded actions or PDDL-formulated subgoals that constitute a complete plan to execute the instruction.

## Scoring recipe

```python
def compute_sr(predictions, N):
    total_sr = 0
    for i in range(N):
        feas = 1 if predictions[i] is feasible else 0
        comp = 1 if predictions[i] completes the gold task else 0
        total_sr += feas * comp
    return total_sr / N
```

## Common pitfalls

- The AHAT benchmark subsets (Easy, Complex, Abstract) are stratified by instruction type and constraint density, not independent datasets; scene counts overlap across subsets.
- Behavior-1K scenes were artificially augmented with distractor objects to increase clutter, meaning results are not directly comparable to the original Behavior-1K release.
- LLM baselines (Gemini-3-Pro, GPT-5) had their inference budgets explicitly controlled to match AHAT's planning latency, which may artificially equalize planning time metrics.

## Evidence (verbatim from paper)

> We evaluate each method in terms of average planning time (T) and success rate (SR). The success rate accounts for both plan feasibility and task completion, as defined below: $SR=\frac{1}{N}\sum_{i=1}^{N}\mathbb{I}_{\text{feas}}(o_{i})\cdot R_{\text{comp}}(o_{i}).$ N refers to the number of samples in the corresponding test dataset.

## Citation

```bibtex
@misc{liu2026anyhouseanytask,
  title={Any House Any Task: Scalable Long-Horizon Planning for Abstract Human Tasks},
  author={Zhihong Liu et al. (2026)},
  year={2026},
  note={arXiv:2602.12244}
}
```

- arXiv: 2602.12244
