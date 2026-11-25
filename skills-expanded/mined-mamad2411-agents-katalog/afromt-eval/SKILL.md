---
name: afromt-eval
description: This benchmark evaluates machine translation capabilities across eight morphologically rich African languages translated from English. It specifically probes how well models handle complex morphosyntactic features like noun classification and verb extensions in low-resource settings. Use when the user wants to benchmark on AFROMT, or asks about evaluating this task. Reports BLEU.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2109.04715
  bibtex_key: reid2021afromt
  confidence: high
---

# afromt-eval

> AfroMT: Pretraining Strategies and Reproducible Benchmarks for Translation of 8 African Languages — Reid et al. (2021) (arXiv:2109.04715, 2021)

## What this evaluates

This benchmark evaluates machine translation capabilities across eight morphologically rich African languages translated from English. It specifically probes how well models handle complex morphosyntactic features like noun classification and verb extensions in low-resource settings.

## Datasets

- **AFROMT** — total ?; splits: test (-1); repo https://github.com/machelreid/afromt

## Metrics

- `BLEU` **(primary)** — range: percent
  - Detokenized BLEU score measuring n-gram overlap between predicted and reference translations. Computed using the SacreBLEU library for reproducibility.
- `chrF` — range: percent
  - Character n-gram F-score that evaluates overlap at the character level to better capture morphological richness in low-resource African languages.

## Input / output format

**Input**: Source English sentence (En-XX direction).

**Output**: Target sentence in one of the eight African languages (Runyankole, Zulu, Afrikaans, Xhosa, Lingala, Bemba, Sesotho, or Swahili).

## Scoring recipe

```python
import sacrebleu
# predictions and references are lists of strings
bleu_score = sacrebleu.corpus_bleu(predictions, [references]).score
chrf_score = sacrebleu.corpus_chrf(predictions, [references]).score
return {'BLEU': bleu_score, 'chrF': chrf_score}
```

## Common pitfalls

- Using tokenized BLEU instead of detokenized BLEU, which can skew scores for morphologically rich languages.
- Relying solely on word-level BLEU without character-level metrics like chrF, which fails to capture complex morphology (noun classes, verb extensions) common in the target languages.
- Not using the SacreBLEU library for standardized, reproducible metric computation as specified by the authors.

## Evidence (verbatim from paper)

> We evaluate our system outputs using two automatic evaluation metrics: detokenized BLEU (Papineni et al., 2002; Post, 2018) and chrF (Popović, 2015). Although BLEU is a standard metric for machine translation, being cognizant of the morphological richness of the languages in the AFROMT benchmark, we use chrF to measure performance at a character level. Both metrics are measured using the SacreBLEU library<sup>13</sup> (Post, 2018).

## Citation

```bibtex
@misc{reid2021afromt,
  title={AfroMT: Pretraining Strategies and Reproducible Benchmarks for Translation of 8 African Languages},
  author={Reid et al. (2021)},
  year={2021},
  note={arXiv:2109.04715}
}
```

- arXiv: 2109.04715
