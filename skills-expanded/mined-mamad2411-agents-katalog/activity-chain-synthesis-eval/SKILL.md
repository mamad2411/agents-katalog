---
name: activity-chain-synthesis-eval
description: Evaluates a generative model's ability to synthesize realistic human mobility patterns by producing activity chains and location trajectories conditioned on socio-demographic and household attributes. It probes the model's capacity to capture temporal dynamics, activity type distributions, transition probabilities, and household interdependencies at both the sequence and system levels. Use when the user wants to benchmark on Household Travel Survey (HTS) / NHTS, or asks about evaluating this task. Reports JSD.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2405.17468
  bibtex_key: liao2024deepactivitymodel
  confidence: high
---

# activity-chain-synthesis-eval

> Deep Activity Model: A Generative Approach for Human Mobility Pattern Synthesis — Liao et al. (2024) (arXiv:2405.17468, 2024)

## What this evaluates

Evaluates a generative model's ability to synthesize realistic human mobility patterns by producing activity chains and location trajectories conditioned on socio-demographic and household attributes. It probes the model's capacity to capture temporal dynamics, activity type distributions, transition probabilities, and household interdependencies at both the sequence and system levels.

## Datasets

- **Household Travel Survey (HTS) / NHTS** — total 197043; splits: train (160831), val (18106), test (18106)

## Metrics

- `JSD` **(primary)** — range: other
  - Jensen-Shannon Divergence between the histogram of generated activity statistics (P) and ground truth (Q): JSD(P||Q) = 0.5 * Σ P(x)log(P(x)/M(x)) + 0.5 * Σ Q(x)log(Q(x)/M(x)), where M=(P+Q)/2. Computed over activity frequencies, start times, end times, chain length, and duration. Lower values indicate better distribution alignment.
- `Edge Completeness (EC)` — range: percent
  - Percentage of valid activity transitions in the generated chains that also appear in the ground truth transition graph. EC = |E_gen ∩ E_gt| / |E_gt| * 100.
- `Frobenius Norm (F-Norm)` — range: other
  - L2 distance between the activity transition probability matrices of generated (A) and ground truth (B) chains: |A - B|_F = sqrt(ΣΣ|a_ij - b_ij|^2). Lower values indicate better transition probability alignment.

## Input / output format

**Input**: Household socio-demographic attributes, day-of-week, age group, and contextual conditioning tokens to generate a sequence of activities.

**Output**: A synthesized activity chain specifying activity type, start time, end time, duration, and assigned location/trajectory for each step.

## Scoring recipe

```python
def compute_jsd(gen_hist, gt_hist):
    P, Q = np.array(gen_hist), np.array(gt_hist)
    M = (P + Q) / 2
    return 0.5 * np.sum(P * np.log(P / M)) + 0.5 * np.sum(Q * np.log(Q / M))

def compute_ec(gen_chains, gt_chains):
    gen_edges = set(tuple(chain[i:i+2]) for chain in gen_chains for i in range(len(chain)-1))
    gt_edges = set(tuple(chain[i:i+2]) for chain in gt_chains for i in range(len(chain)-1))
    return len(gen_edges & gt_edges) / len(gt_edges) * 100

def compute_fnorm(gen_chains, gt_chains):
    A = build_transition_matrix(gen_chains)
    B = build_transition_matrix(gt_chains)
    return np.sqrt(np.sum((A - B) ** 2))
```

## Common pitfalls

- JSD measures distribution-level similarity, not instance-level accuracy; evaluating single-agent prediction is explicitly discouraged by the authors.
- Location assignment is evaluated via system-level traffic metrics (MAPE on VMT/flow), not standard top-k location prediction accuracy.
- Edge Completeness only measures transition coverage; node (activity type) coverage is 100% for all models and not reported as a differentiator.

## Evidence (verbatim from paper)

> In this paper, the Jensen-Shannon Divergence (JSD) is used as the similarity metric [29], as shown in Equation 4. The goal is to minimize the difference between the distributions of generated and real activity patterns from activity chains. The metrics include: 1) activity frequencies, 2) start times, 3) end times, 4) number of daily activities (activity chain length), and 5) duration of each activity.

## Citation

```bibtex
@misc{liao2024deepactivitymodel,
  title={Deep Activity Model: A Generative Approach for Human Mobility Pattern Synthesis},
  author={Liao et al. (2024)},
  year={2024},
  note={arXiv:2405.17468}
}
```

- arXiv: 2405.17468
