---
name: alpaca-eval-lc-winrate-eval
description: Evaluates the alignment quality of language models by measuring their win rate against a baseline on the AlpacaEval benchmark. It specifically uses length-controlled (LC) win rates to mitigate the known bias toward longer model outputs in standard auto-annotator evaluations. Use when the user wants to benchmark on alpaca_eval, or asks about evaluating this task. Reports AlpacaEval length-controlled (LC) win rate.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.04410
  bibtex_key: takahashi2026rdro
  confidence: high
---

# alpaca-eval-lc-winrate-eval

> Relative Density Ratio Optimization for Stable and Statistically Consistent Model Alignment — Takahashi et al. (2026) (arXiv:2604.04410, 2026)

## What this evaluates

Evaluates the alignment quality of language models by measuring their win rate against a baseline on the AlpacaEval benchmark. It specifically uses length-controlled (LC) win rates to mitigate the known bias toward longer model outputs in standard auto-annotator evaluations.

## Datasets

- **alpaca_eval** — total ?; splits: test (-1); HF `tatsu-lab/alpaca_eval`; repo https://github.com/tatsu-lab/alpaca_eval

## Metrics

- `AlpacaEval length-controlled (LC) win rate` **(primary)** — range: percent
  - Win rate against a baseline model computed by an LLM-based auto-annotator, with a regression step applied to remove bias toward longer outputs.

## Input / output format

**Input**: Text prompts from the AlpacaEval dataset.

**Output**: Model-generated text responses to each prompt.

## Scoring recipe

```python
def compute_lc_win_rate(prompts, model, baseline, annotator):
    preds = model.generate(prompts)
    base_preds = baseline.generate(prompts)
    scores = annotator.compare(preds, base_preds)
    raw_wr = mean(scores == 'win')
    lc_wr = regress_length_bias(raw_wr, preds, base_preds)
    return lc_wr
```

## Common pitfalls

- Reporting raw win rates instead of length-controlled (LC) win rates, which ignores AlpacaEval's known bias toward longer generations.
- Using mismatched auto-annotator or baseline models (e.g., not weighted_alpaca_eval_gpt4_turbo and gpt-4-turbo-2024-04-09), which breaks comparability with reported baselines.
- Failing to average results over multiple random seeds, as the protocol requires repeating each experiment three times.

## Evidence (verbatim from paper)

> As the metric, we used AlpacaEval length-controlled (LC) win rates (Dubois et al., 2024). We generated responses from the aligned models on the alpaca_eval prompts, computed win rates against a baseline using an LLM-based auto-annotator, and reported LC win rates that regress out AlpacaEval’s bias toward longer outputs. We used gpt-4-turbo-2024-04-09 for the baseline and weighted_alpaca_eval_gpt4_turbo for the auto-annotator.

## Citation

```bibtex
@misc{takahashi2026rdro,
  title={Relative Density Ratio Optimization for Stable and Statistically Consistent Model Alignment},
  author={Takahashi et al. (2026)},
  year={2026},
  note={arXiv:2604.04410}
}
```

- arXiv: 2604.04410
