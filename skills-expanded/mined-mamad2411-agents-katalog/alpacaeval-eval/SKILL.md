---
name: alpacaeval-eval
description: Evaluates LLM response quality via pairwise win rates against a baseline, while specifically probing the metric's susceptibility to length bias, gameability via verbosity prompting, and robustness to adversarial truncation. Use when the user wants to benchmark on AlpacaEval, or asks about evaluating this task. Reports Win rate.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2404.04475
  bibtex_key: dubois2024lengthcontrolledalpacaeval
  confidence: high
---

# alpacaeval-eval

> Length-Controlled AlpacaEval: A Simple Way to Debias Automatic Evaluators — Dubois et al. (2024) (arXiv:2404.04475, 2024)

## What this evaluates

Evaluates LLM response quality via pairwise win rates against a baseline, while specifically probing the metric's susceptibility to length bias, gameability via verbosity prompting, and robustness to adversarial truncation.

## Datasets

- **AlpacaEval** — total 805; splits: test (805)

## Metrics

- `Win rate` **(primary)** — range: percent
  - Percentage of pairwise comparisons where the model's response is preferred over the baseline. Computed as 100% - winrate(baseline, model) ∈ [0%, 100%].
- `Length gameability` — range: percent
  - Normalized standard deviation of win rates across three verbosity prompts (concise, standard, verbose). Lower values indicate the metric is less sensitive to output length.
- `Spearman correlation` — range: [-1, 1]
  - Rank correlation between the benchmark's win rates and Chatbot Arena ELO ratings. Computed on benchmarks evaluating at least 25 models.

## Input / output format

**Input**: Instruction, baseline response, and model response provided to an LLM judge for pairwise preference comparison.

**Output**: Pairwise preference (model wins, baseline wins, or tie), aggregated into a win rate percentage.

## Scoring recipe

```python
def compute_metrics(pairs, arena_elo):
    # 1. Win rate
    wins = sum(1 for p in pairs if p.model_preferred)
    win_rate = (wins / len(pairs)) * 100
    
    # 2. Length gameability
    win_rates = [compute_win_rate(prompt=p) for p in ['concise', 'standard', 'verbose']]
    gameability = normalized_std(win_rates)
    
    # 3. Spearman correlation with Chatbot Arena
    spearman_corr = spearmanr(benchmark_win_rates, arena_elo)
    return win_rate, gameability, spearman_corr
```

## Common pitfalls

- Failing to control for output length can cause metrics to favor verbose but low-quality responses.
- Using Pearson correlation instead of Spearman for ELO ratings misrepresents the log-linear relationship.
- Stratification-based length control (length-balanced) can become unstable with few samples per stratum or vulnerable to truncation attacks.

## Evidence (verbatim from paper)

> We measure Spearman rather than Pearson correlation as probabilities are log-linearly correlated with ELO ratings, rather than linearly.

## Citation

```bibtex
@misc{dubois2024lengthcontrolledalpacaeval,
  title={Length-Controlled AlpacaEval: A Simple Way to Debias Automatic Evaluators},
  author={Dubois et al. (2024)},
  year={2024},
  note={arXiv:2404.04475}
}
```

- arXiv: 2404.04475
