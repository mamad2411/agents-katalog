---
name: auto-j-eval
description: Evaluates the alignment and preference alignment of LLMs through pairwise comparison, single-response critique generation, and overall rating. It probes the model's ability to consistently identify human-preferred responses, generate structured natural language critiques, and rank outputs according to a reference judge (GPT-4). Use when the user wants to benchmark on Eval-P, Eval-C, Eval-R, AlpacaEval, or asks about evaluating this task. Reports agreement rate.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2310.05470
  bibtex_key: li2023generativejudge
  confidence: high
---

# auto-j-eval

> Generative Judge for Evaluating Alignment — Li et al. (2023) (arXiv:2310.05470, 2023)

## What this evaluates

Evaluates the alignment and preference alignment of LLMs through pairwise comparison, single-response critique generation, and overall rating. It probes the model's ability to consistently identify human-preferred responses, generate structured natural language critiques, and rank outputs according to a reference judge (GPT-4).

## Datasets

- **Eval-P** — total ?; splits: test (-1)
- **Eval-C** — total ?; splits: test (-1)
- **Eval-R** — total 1993; splits: test (1993)
- **AlpacaEval** — total ?; splits: test (-1)

## Metrics

- `agreement rate` **(primary)** — range: [0, 1]
  - Percentage of test cases where the model's judgment matches the human judgment, requiring consistent results when the two response positions are swapped.
- `Spearman correlation` — range: [-1, 1]
  - Rank-based correlation coefficient measuring the monotonic relationship between the model's predicted ratings and the reference GPT-4 ratings.

## Input / output format

**Input**: Pairwise: Query string followed by two candidate responses (A and B). Single-response: Query string followed by one candidate response.

**Output**: Pairwise: Structured natural language critique followed by a final decision (e.g., 'Response 1' or 'Response 2'). Single-response: Structured natural language critique followed by a numerical rating in double brackets (e.g., '[[5]]').

## Scoring recipe

```python
def compute_agreement_rate(predictions, gold, swapped_predictions):
    consistent = [p == sp for p, sp in zip(predictions, swapped_predictions)]
    matches_human = [p == g for p, g in zip(predictions, gold)]
    agreements = [c and m for c, m in zip(consistent, matches_human)]
    return sum(agreements) / len(agreements)

def compute_spearman_corr(model_scores, gold_scores):
    return spearmanr(model_scores, gold_scores).correlation
```

## Common pitfalls

- Positional bias: Failing to swap response orders in the prompt leads to inconsistent judgments and inflated agreement rates.
- Tie handling: Reference judges like GPT-4 rarely output ties, while humans do frequently; this mismatch can skew critique comparison metrics.
- Consistency requirement: Agreement is only counted if the model's judgment matches the human label in BOTH the original and swapped response order prompts.

## Evidence (verbatim from paper)

> The agreement rates for AUTO-J and the baselines on Eval-P are in Tab. 1. AUTO-J achieves a significantly higher agreement rate than all baselines except GPT-4 on every scenario group. We also plot the prediction consistency for each model in Fig. 4. AUTO-J has a similar consistency rate to GPT-4 and is far more consistent than all other baselines, which makes it a more reliable and robust judge for pairwise comparison.

## Citation

```bibtex
@misc{li2023generativejudge,
  title={Generative Judge for Evaluating Alignment},
  author={Li et al. (2023)},
  year={2023},
  note={arXiv:2310.05470}
}
```

- arXiv: 2310.05470
