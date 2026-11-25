---
name: atc-asr-csd-eval
description: Evaluates automatic speech recognition (ASR) and call sign detection (CSD) capabilities on real-world air traffic control audio. It probes the model's ability to transcribe accented, noisy pilot and controller speech and accurately identify aircraft call signs in domain-specific phraseology. Use when the user wants to benchmark on Airbus ATC Speech Recognition 2018 Challenge Corpus, or asks about evaluating this task. Reports WER.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1810.12614
  bibtex_key: pellegrini2018airbus
  confidence: high
---

# atc-asr-csd-eval

> The Airbus Air Traffic Control speech recognition 2018 challenge: towards ATC automatic transcription and call sign detection — Pellegrini et al. (2018) (arXiv:1810.12614, 2018)

## What this evaluates

Evaluates automatic speech recognition (ASR) and call sign detection (CSD) capabilities on real-world air traffic control audio. It probes the model's ability to transcribe accented, noisy pilot and controller speech and accurately identify aircraft call signs in domain-specific phraseology.

## Datasets

- **Airbus ATC Speech Recognition 2018 Challenge Corpus** — total ?; splits: eval (-1)

## Metrics

- `WER` **(primary)** — range: percent
  - Word Error Rate: (S + D + I) / N, where S=substitutions, D=deletions, I=insertions, N=number of reference words.
- `CSD F1-score` — range: percent
  - F1-score for Call Sign Detection: harmonic mean of precision and recall computed over detected call sign spans.

## Input / output format

**Input**: Audio recordings of air traffic control communications (pilot and controller speech) with varying noise levels and accents.

**Output**: For ASR: word-level transcription. For CSD: detected call sign spans or labels.

## Scoring recipe

```python
# ASR WER
wer = (substitutions + deletions + insertions) / len(reference_words)

# CSD F1
precision = true_positives / (true_positives + false_positives)
recall = true_positives / (true_positives + false_negatives)
f1 = 2 * (precision * recall) / (precision + recall)
```

## Common pitfalls

- Call signs are often shortened or used in partial forms, making detection harder than strict rule-based matching.
- Pilots' speech has significantly higher WER than controllers' due to greater accent diversity and faster speech rates.
- Some teams submitted only ASR results without CSD predictions, resulting in zero CSD scores that skew overall rankings.

## Evidence (verbatim from paper)

> Figures [1]a and [1]b show the Word Error Rates (WER) for the ASR task and the F1-scores for CSD, obtained by the 22 teams ordered by their final ranking. VOCAPIA-LIMSI achieved the best results in both tasks with a 7.62% WER and a 82.41% CSD F1-score.

## Citation

```bibtex
@misc{pellegrini2018airbus,
  title={The Airbus Air Traffic Control speech recognition 2018 challenge: towards ATC automatic transcription and call sign detection},
  author={Pellegrini et al. (2018)},
  year={2018},
  note={arXiv:1810.12614}
}
```

- arXiv: 1810.12614
