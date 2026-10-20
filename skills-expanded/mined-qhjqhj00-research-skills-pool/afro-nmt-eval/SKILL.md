---
name: afro-nmt-eval
description: Evaluates neural machine translation performance across five low-resource African languages (Swahili, Amharic, Tigrigna, Oromo, Somali) paired with English. It probes model robustness to domain shifts and compares single-language, semi-supervised, transfer-learning, and multilingual training strategies. Use when the user wants to benchmark on AfroNMT, or asks about evaluating this task. Reports BLEU.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2003.14402
  bibtex_key: lakew2020lowresource
  confidence: high
---

# afro-nmt-eval

> Low Resource Neural Machine Translation: A Benchmark for Five African Languages — Lakew et al. (2020) (arXiv:2003.14402, 2020)

## What this evaluates

Evaluates neural machine translation performance across five low-resource African languages (Swahili, Amharic, Tigrigna, Oromo, Somali) paired with English. It probes model robustness to domain shifts and compares single-language, semi-supervised, transfer-learning, and multilingual training strategies.

## Datasets

- **AfroNMT** — total ?; splits: test (-1), test_ted (-1); repo https://github.com/surafelml/Afro-NMT

## Metrics

- `BLEU` **(primary)** — range: percent
  - Standard sentence-level BLEU score computing n-gram precision with a brevity penalty. The paper reports averaged (AVG) BLEU scores across multiple test domains for final comparison.

## Input / output format

**Input**: Source sentence in an African language or English.

**Output**: Translated target sentence in English or the corresponding African language.

## Scoring recipe

```python
def compute_bleu(predictions, references):
    # predictions and references are lists of tokenized strings
    bleu_scores = []
    for pred, ref in zip(predictions, references):
        # Standard sentence-level BLEU (Papineni et al., 2002)
        # Computes geometric mean of 1-4 gram precisions with brevity penalty
        score = sentence_bleu([ref], pred, smoothing_function=smoothing)
        bleu_scores.append(score * 100)  # Scale to 0-100
    return sum(bleu_scores) / len(bleu_scores)
```

## Common pitfalls

- BLEU scores are averaged across multiple domains (in-domain and Ted), which can mask significant per-domain performance drops.
- Out-of-domain (Ted) test sets show larger performance degradation for single-language models compared to in-domain sets.
- Multilingual models perform best when translating into English due to data distribution, but degrade when translating into low-resource languages.

## Evidence (verbatim from paper)

> Table 1 shows the performance of the different LRL modeling criteria with multi-domain test sets. Looking at the single pair NMT models (S-NMT), we observe that in all the test domains they underperform with respect to the SS-NMT, TL, or M-NMT models in terms of averaged (AVG) BLEU scores.

## Citation

```bibtex
@misc{lakew2020lowresource,
  title={Low Resource Neural Machine Translation: A Benchmark for Five African Languages},
  author={Lakew et al. (2020)},
  year={2020},
  note={arXiv:2003.14402}
}
```

- arXiv: 2003.14402
