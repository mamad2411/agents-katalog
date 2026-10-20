---
name: amos-downstream-eval
description: Evaluates the downstream performance of pretrained text encoders on a suite of natural language understanding and reading comprehension benchmarks via standard single-task fine-tuning. Use when the user wants to benchmark on GLUE, SQuAD 2.0, or asks about evaluating this task. Reports AVG.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2204.03243
  bibtex_key: meng2022amos
  confidence: high
---

# amos-downstream-eval

> Pretraining Text Encoders with Adversarial Mixture of Training Signal Generators — Meng et al. (2022) (arXiv:2204.03243, 2022)

## What this evaluates

Evaluates the downstream performance of pretrained text encoders on a suite of natural language understanding and reading comprehension benchmarks via standard single-task fine-tuning.

## Datasets

- **GLUE** — total ?; splits: dev (-1); HF `glue`
- **SQuAD 2.0** — total ?; splits: dev (-1); HF `squad_v2`

## Metrics

- `AVG` **(primary)** — range: percent
  - Average of the eight individual task scores on GLUE.
- `Accuracy` — range: percent
  - Proportion of correctly predicted labels for classification tasks.
- `Spearman correlation` — range: [-1, 1]
  - Rank-based correlation coefficient used for STS-B.
- `Matthews correlation` — range: [-1, 1]
  - Correlation coefficient for binary classification used for CoLA.
- `Exact Match (EM)` — range: [0, 1]
  - Fraction of predictions where the generated answer exactly matches the gold answer.
- `F1` — range: [0, 1]
  - Token-level F1 score for span prediction in SQuAD 2.0.

## Input / output format

**Input**: Task-specific fine-tuning inputs: sentence pairs or single sentences for GLUE tasks, and question-context pairs for SQuAD 2.0.

**Output**: Task-specific predictions: class labels or regression scores for GLUE, and predicted answer spans for SQuAD 2.0.

## Scoring recipe

```python
def compute_metric(preds, golds, task):
    if task == 'STS-B': return spearmanr(preds, golds).correlation
    elif task == 'CoLA': return matthews_corrcoef(golds, preds)
    elif task == 'SQuAD 2.0': return exact_match(preds, golds), token_f1(preds, golds)
    else: return accuracy(golds, preds)

glue_scores = [compute_metric(p, g, t) for t, p, g in glues]
avg_glue = sum(glue_scores) / len(glue_scores)
return avg_glue
```

## Common pitfalls

- Reporting test set scores instead of the development set scores as specified in the evaluation table.
- Failing to report the median across five random seeds, which is required for fair comparison.
- Using multi-task or joint fine-tuning instead of the specified single-task vanilla fine-tuning protocol.

## Evidence (verbatim from paper)

> We use the tasks included in GLUE (Wang et al., 2018) and SQuAD 2.0 reading comprehension (Rajpurkar et al., 2016). All models are evaluated with the same standard fine-tuning protocols: Single task learning with vanilla fine-tuning and reporting the median of five random seeds in GLUE and SQuAD. We use Spearman correlation for STS, Matthews correlation for CoLA, and accuracy for the rest on GLUE. AVG is the average of the eight tasks on GLUE.

## Citation

```bibtex
@misc{meng2022amos,
  title={Pretraining Text Encoders with Adversarial Mixture of Training Signal Generators},
  author={Meng et al. (2022)},
  year={2022},
  note={arXiv:2204.03243}
}
```

- arXiv: 2204.03243
