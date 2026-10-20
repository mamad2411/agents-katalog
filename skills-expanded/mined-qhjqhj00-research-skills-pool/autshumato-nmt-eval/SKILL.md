---
name: autshumato-nmt-eval
description: Evaluates neural machine translation performance across five Southern African languages (Afrikaans, isiZulu, Northern Sotho, Setswana, Xitsonga) from English. It probes how dataset size and morphological complexity (e.g., agglutinative vs. non-agglutinative) impact translation quality in low-resource settings. Use when the user wants to benchmark on Autshumato, or asks about evaluating this task. Reports BLEU.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1906.10511
  bibtex_key: martinus2019benchmarking
  confidence: high
---

# autshumato-nmt-eval

> Benchmarking Neural Machine Translation for Southern African Languages — Martinus & Abbott (2019) (arXiv:1906.10511, 2019)

## What this evaluates

Evaluates neural machine translation performance across five Southern African languages (Afrikaans, isiZulu, Northern Sotho, Setswana, Xitsonga) from English. It probes how dataset size and morphological complexity (e.g., agglutinative vs. non-agglutinative) impact translation quality in low-resource settings.

## Datasets

- **Autshumato** — total ?; splits: test (-1); repo https://github.com/LauraMartinus/ukuxhumana

## Metrics

- `BLEU` **(primary)** — range: percent
  - Standard n-gram overlap metric between machine-generated translations and human reference translations, computed with sentence-level averaging and a brevity penalty to penalize overly short outputs.

## Input / output format

**Input**: English source sentences.

**Output**: Target language translation (Afrikaans, isiZulu, Northern Sotho, Setswana, or Xitsonga).

## Scoring recipe

```python
def compute_bleu(predictions, references):
    # predictions and references are lists of strings
    bleu_scores = []
    for pred, ref in zip(predictions, references):
        # Standard sentence-level BLEU with 4-gram precision and smoothing
        score = sentence_bleu([ref], pred, smoothing_method=SmoothingFunction().method1)
        bleu_scores.append(score)
    return sum(bleu_scores) / len(bleu_scores) * 100
```

## Common pitfalls

- BLEU scores may not accurately reflect translation quality for highly agglutinative languages like isiZulu due to morphological richness and vocabulary mismatch.
- Dataset size and data quality are confounded; poor performance on isiZulu is attributed to both morphological complexity and low-quality parallel data, making it hard to isolate the cause.
- The paper reports baseline results on a newly released evaluation set without specifying exact train/val/test split sizes or tokenization details.

## Evidence (verbatim from paper)

> The BLEU scores for each model on English-to-Target language are presented in Table 2. The Transformer model outperformed the ConvS2S model for all languages. These results serve as initial baseline results for the given languages on the evaluation set.

## Citation

```bibtex
@misc{martinus2019benchmarking,
  title={Benchmarking Neural Machine Translation for Southern African Languages},
  author={Martinus & Abbott (2019)},
  year={2019},
  note={arXiv:1906.10511}
}
```

- arXiv: 1906.10511
