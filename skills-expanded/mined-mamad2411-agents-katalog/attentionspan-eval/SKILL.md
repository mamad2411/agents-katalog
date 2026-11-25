---
name: attentionspan-eval
description: Evaluates algorithmic reasoning and out-of-distribution generalization in Transformers by measuring prediction accuracy and attention pattern alignment against ground-truth reference masks on synthetic tasks. Use when the user wants to benchmark on AttentionSpan, or asks about evaluating this task. Reports Accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2503.01909
  bibtex_key: spiegel2025attend
  confidence: high
---

# attentionspan-eval

> Attend or Perish: Benchmarking Attention in Algorithmic Reasoning — Spiegel et al. (2025) (arXiv:2503.01909, 2025)

## What this evaluates

Evaluates algorithmic reasoning and out-of-distribution generalization in Transformers by measuring prediction accuracy and attention pattern alignment against ground-truth reference masks on synthetic tasks.

## Datasets

- **AttentionSpan** — total ?; splits: ID (-1), OOD (-1); repo https://github.com/michalspiegel/AttentionSpan

## Metrics

- `Accuracy` **(primary)** — range: [0, 1]
  - Exact-match sequence accuracy, calculated as 1 if the model's full output matches the gold output exactly, and 0 otherwise.
- `OOD Partial Accuracy` — range: [0, 1]
  - Token-level accuracy measuring the proportion of correctly predicted target tokens in out-of-distribution settings, even when the full sequence is incorrect.
- `Attention Score` — range: [0, 1]
  - Alignment metric quantifying how closely a model's learned attention weights match the provided discrete boolean reference attention masks for correct versus incorrect predictions.

## Input / output format

**Input**: Synthetic algorithmic reasoning problems (e.g., string reversal, long addition, long multiplication, flip-flop language modeling, value assignment) with configurable difficulty and input lengths.

**Output**: Corresponding correct output sequence (e.g., reversed string, sum, product, next token, assigned values).

## Scoring recipe

```python
def compute_metrics(pred, gold, pred_tokens, gold_tokens, model_attn, ref_mask):
    # Sequence Accuracy
    acc = 1.0 if pred == gold else 0.0
    # OOD Partial Accuracy
    partial_acc = sum(1 for p, g in zip(pred_tokens, gold_tokens) if p == g) / len(gold_tokens)
    # Attention Score (alignment with reference mask)
    attn_score = cosine_similarity(model_attn.flatten(), ref_mask.flatten())
    return acc, partial_acc, attn_score
```

## Common pitfalls

- Confusing high in-distribution (ID) accuracy with genuine algorithmic understanding, as models often memorize ID patterns while failing on OOD inputs.
- Interpreting zero OOD Accuracy as complete reasoning failure, when OOD Partial Accuracy reveals models still capture a large proportion of correct target tokens.
- Overlooking the reference attention masks, which are essential for diagnosing whether failures stem from attention misalignment rather than capacity limits.

## Evidence (verbatim from paper)

> Accuracy of finetuned models on AttentionSpan tasks with consistent in-distribution and out-of-distribution splits. Despite a sharp decline in OOD Accuracy in almost all cases, the OOD Partial Accuracy reveals that models correctly predict a large proportion of target tokens, indicating some extrapolation abilities are present.

## Citation

```bibtex
@misc{spiegel2025attend,
  title={Attend or Perish: Benchmarking Attention in Algorithmic Reasoning},
  author={Spiegel et al. (2025)},
  year={2025},
  note={arXiv:2503.01909}
}
```

- arXiv: 2503.01909
