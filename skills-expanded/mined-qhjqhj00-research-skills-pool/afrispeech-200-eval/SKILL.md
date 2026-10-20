---
name: afrispeech-200-eval
description: Evaluates automatic speech recognition (ASR) models on pan-African accented English speech across clinical and general domains. It probes out-of-distribution generalization, zero-shot performance on unseen accents, and domain-specific robustness. Use when the user wants to benchmark on AfriSpeech-200, or asks about evaluating this task. Reports WER.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2310.00274
  bibtex_key: olatunj2023afrispeech200
  confidence: high
---

# afrispeech-200-eval

> AfriSpeech-200: Pan-African Accented Speech Dataset for Clinical and General Domain ASR — Olatunj et al. (2023) (arXiv:2310.00274, 2023)

## What this evaluates

Evaluates automatic speech recognition (ASR) models on pan-African accented English speech across clinical and general domains. It probes out-of-distribution generalization, zero-shot performance on unseen accents, and domain-specific robustness.

## Datasets

- **AfriSpeech-200** — total 67577; splits: train (57999), dev (3231), test (6346)

## Metrics

- `WER` **(primary)** — range: percent
  - Word Error Rate: (Substitutions + Deletions + Insertions) / Total Reference Words. Standard ASR metric reported as a percentage or raw ratio.

## Input / output format

**Input**: Raw audio clips paired with ground-truth transcriptions (clinical or general domain). Models may also receive a custom alphanumeric vocabulary definition containing medical symbols and punctuation.

**Output**: Predicted text transcription for each input audio clip.

## Scoring recipe

```python
def compute_wer(predictions, references):
    total_errors = 0
    total_words = 0
    for pred, ref in zip(predictions, references):
        dist = levenshtein_distance(ref.split(), pred.split())
        total_errors += dist
        total_words += len(ref.split())
    return (total_errors / total_words) * 100 if total_words > 0 else 0.0
```

## Common pitfalls

- Speakers are strictly partitioned across train/dev/test to prevent data leakage; mixing them will invalidate results.
- Evaluation uses single-run results rather than averaging over multiple random seeds, which may introduce variance.
- Commercial ASR systems are only benchmarked, not fine-tuned, due to proprietary architecture constraints.

## Evidence (verbatim from paper)

> We report our results as WER on AfriSpeech dev and test sets in addition to domain and accent-specific performance. Results are compared with Librispeech (Panayotov et al., 2015a) test set performance. We also report the zero-shot performance of fine-tuned models on unseen accents in the test set.

## Citation

```bibtex
@misc{olatunj2023afrispeech200,
  title={AfriSpeech-200: Pan-African Accented Speech Dataset for Clinical and General Domain ASR},
  author={Olatunj et al. (2023)},
  year={2023},
  note={arXiv:2310.00274}
}
```

- arXiv: 2310.00274
