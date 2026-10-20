---
name: attention-pruning-eval
description: Evaluates the effectiveness of attention head pruning methods in reducing gender bias in large language models while preserving language model utility. It probes the trade-off between fairness mitigation and general language modeling performance across models of varying sizes. Use when the user wants to benchmark on HolisticBias, WikiText-2, or asks about evaluating this task. Reports HolisticBias.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2503.15815
  bibtex_key: dasu2025attentionpruning
  confidence: high
---

# attention-pruning-eval

> Attention Pruning: Automated Fairness Repair of Language Models via Surrogate Simulated Annealing — Dasu et al. (2025) (arXiv:2503.15815, 2025)

## What this evaluates

Evaluates the effectiveness of attention head pruning methods in reducing gender bias in large language models while preserving language model utility. It probes the trade-off between fairness mitigation and general language modeling performance across models of varying sizes.

## Datasets

- **HolisticBias** — total 10268; splits: val (10268)
- **WikiText-2** — total 2461; splits: val (2461)

## Metrics

- `HolisticBias` **(primary)** — range: [0, 1]
  - Standard HolisticBias metric measuring gender bias in model outputs. Values typically range between 0 and 1, where higher indicates more bias. The paper reports mean and standard deviation over 3 generation seeds.
- `perplexity` — range: other
  - Standard language model perplexity computed over the WikiText-2 validation split. Lower values indicate better language modeling utility and are used as a proxy for model quality preservation.

## Input / output format

**Input**: For bias evaluation: gender bias prompts from the HolisticBias validation dataset. For perplexity evaluation: text sequences from the WikiText-2 validation split.

**Output**: Model-generated text responses to prompts (for bias) and token probabilities/losses over WikiText-2 sequences (for perplexity). Bias and perplexity scores are aggregated as mean ± standard deviation over 3 generation seeds.

## Scoring recipe

```python
bias_scores = []
for seed in [seed1, seed2, seed3]:
    outputs = model.generate(prompts, seed=seed)
    bias_scores.append(holisticbias_metric(outputs))
bias_mean = sum(bias_scores) / len(bias_scores)
bias_std = (sum((x - bias_mean)**2 for x in bias_scores) / len(bias_scores))**0.5

ppl_scores = [model_perplexity(text) for text in wikitext2_val]
ppl_mean = sum(ppl_scores) / len(ppl_scores)
```

## Common pitfalls

- The paper reports bias scores as mean ± standard deviation over 3 generation seeds, but does not specify the exact random seed values used.
- Baseline hyperparameters (e.g., pruning ratio α) are tuned via exhaustive search per model, which may not reflect a fair zero-shot comparison.
- Perplexity is evaluated on the validation split, which may lead to optimistic utility estimates compared to a held-out test set.

## Evidence (verbatim from paper)

> We primarily focus on reducing gender bias from the HolisticBias metric in LLMs. We use the entire WikiText-2 validation split as it only contains 2,461 text sequences. Once we have identified a good set of hyperparameters for FASP and AP, we generate text with pruned LLMs using three different seeds to sample tokens and report the mean and standard deviation of the bias.

## Citation

```bibtex
@misc{dasu2025attentionpruning,
  title={Attention Pruning: Automated Fairness Repair of Language Models via Surrogate Simulated Annealing},
  author={Dasu et al. (2025)},
  year={2025},
  note={arXiv:2503.15815}
}
```

- arXiv: 2503.15815
