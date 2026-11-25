---
name: ayah-alignment-coverage-eval
description: Evaluates the ability of an audio segmentation pipeline to correctly identify and align individual Quranic verses (ayahs) from long-form recitations. It probes the robustness of alignment methods and ASR backbones against recitation style variations and phonological differences. Use when the user wants to benchmark on Tadabur Evaluation Set (5 Reciters), or asks about evaluating this task. Reports Alignment Coverage (%).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.18932
  bibtex_key: alherran2026tadabur
  confidence: high
---

# ayah-alignment-coverage-eval

> Tadabur: A Large-Scale Quran Audio Dataset — Alherran (2026) (arXiv:2604.18932, 2026)

## What this evaluates

Evaluates the ability of an audio segmentation pipeline to correctly identify and align individual Quranic verses (ayahs) from long-form recitations. It probes the robustness of alignment methods and ASR backbones against recitation style variations and phonological differences.

## Datasets

- **Tadabur Evaluation Set (5 Reciters)** — total ?; splits: test (-1); repo https://github.com/fherran/tadabur

## Metrics

- `Alignment Coverage (%)` **(primary)** — range: percent
  - Percentage of ayahs successfully identified and segmented by the pipeline: (Aligned Ayahs / Total Ayahs) × 100.

## Input / output format

**Input**: Long-form audio recordings of complete Quran recitations from five specific reciters, paired with the canonical Quranic text for alignment.

**Output**: A binary alignment decision (aligned/not aligned) for each ayah in the canonical text, resulting in segmented audio files for successfully aligned verses.

## Scoring recipe

```python
def compute_alignment_coverage(predictions, gold_ayahs):
    aligned_count = sum(1 for pred in predictions if pred.is_aligned)
    total_count = len(gold_ayahs)
    coverage_pct = (aligned_count / total_count) * 100
    return coverage_pct
```

## Common pitfalls

- Coverage scores can be artificially inflated if the evaluation audio contains repeated ayahs; the protocol requires strict deduplication.
- ASR transcription quality directly dictates alignment success, meaning low coverage may reflect poor speech recognition rather than a flawed alignment algorithm.

## Evidence (verbatim from paper)

> We define alignment coverage as the percentage of ayahs successfully identified and segmented by the pipeline: Coverage = (Aligned Ayahs / Total Ayahs) × 100. The evaluation set for each reciter was curated specifically for this purpose: recordings were gathered independently, deduplicated, and cleaned to ensure that each ayah appears exactly once.

## Citation

```bibtex
@misc{alherran2026tadabur,
  title={Tadabur: A Large-Scale Quran Audio Dataset},
  author={Alherran (2026)},
  year={2026},
  note={arXiv:2604.18932}
}
```

- arXiv: 2604.18932
