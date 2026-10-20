---
name: agriculture-asr-eval
description: Evaluates Automatic Speech Recognition (ASR) models on real-world agricultural field recordings across three Indian languages (Hindi, Telugu, Odia). It probes the models' ability to transcribe domain-specific terminology under challenging acoustic conditions like wind noise and multi-speaker overlap. Use when the user wants to benchmark on Agricultural Field Recordings, or asks about evaluating this task. Reports AWWER.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2602.03868
  bibtex_key: chandrashekar2026agricultureasr
  confidence: high
---

# agriculture-asr-eval

> Benchmarking Automatic Speech Recognition for Indian Languages in Agricultural Contexts — Chandrashekar M S et al. (2026) (arXiv:2602.03868, 2026)

## What this evaluates

Evaluates Automatic Speech Recognition (ASR) models on real-world agricultural field recordings across three Indian languages (Hindi, Telugu, Odia). It probes the models' ability to transcribe domain-specific terminology under challenging acoustic conditions like wind noise and multi-speaker overlap.

## Datasets

- **Agricultural Field Recordings** — total 10934; splits: test (-1)

## Metrics

- `AWWER` **(primary)** — range: percent
  - Agriculture Weighted Word Error Rate. It computes the standard WER but applies domain-specific weights to errors: high-impact agricultural terms (weight 3–4), medium-weight terms (weight 2), and general vocabulary (weight 1). Errors on critical terms are penalized more heavily to reflect practical utility.
- `WER` — range: percent
  - Standard Word Error Rate, calculated as the minimum number of insertions, deletions, and substitutions required to transform the hypothesis transcript into the reference transcript, divided by the total number of words in the reference.

## Input / output format

**Input**: Real-world audio recordings of farmers asking agricultural queries, often containing background noise, wind, and multiple speakers. Reference transcripts are provided for evaluation.

**Output**: Transcribed text output from each ASR model. For models supporting diarization, the 'best-speaker' transcript is selected.

## Scoring recipe

```python
def compute_awwer(predictions, references, domain_weights):
    total_weighted_errors = 0
    total_weighted_words = 0
    for pred, ref in zip(predictions, references):
        ops = levenshtein_ops(pred, ref)
        for op in ops:
            word = op.word
            weight = domain_weights.get(word, 1)  # 1 for general, 2 for medium, 3-4 for high-impact ag terms
            total_weighted_errors += weight
            total_weighted_words += weight
    return (total_weighted_errors / total_weighted_words) * 100
```

## Common pitfalls

- Standard WER can severely underestimate practical impact in agricultural contexts because it treats all word errors equally, masking failures on critical terms like pesticides or crop names.
- Speaker diarization significantly impacts performance on multi-speaker recordings; failing to use best-speaker selection can inflate WER by up to 66%.
- LLM-based utility scoring may be less calibrated across different languages, potentially skewing cross-lingual comparisons.

## Evidence (verbatim from paper)

> Analysis of 10,934 real-world audio samples reveals significant performance disparities across languages—Hindi achieves the lowest WER (16.2%), while Odia suffers the highest (35.1%) due to noise and speaker overlap, with background talk and wind noise being dominant audio quality issues. It proposes the Agriculture Weighted Word Error Rate (AWWER) to penalize errors on high-impact agricultural terms (e.g., pesticides, crop diseases) more heavily than general vocabulary

## Citation

```bibtex
@misc{chandrashekar2026agricultureasr,
  title={Benchmarking Automatic Speech Recognition for Indian Languages in Agricultural Contexts},
  author={Chandrashekar M S et al. (2026)},
  year={2026},
  note={arXiv:2602.03868}
}
```

- arXiv: 2602.03868
