---
name: asr-clinical-continual-eval
description: This evaluation probes an ASR model's ability to continuously adapt to noisy, rural clinical telephony speech while retaining its baseline performance on standard general-domain speech. It specifically measures the trade-off between target-domain transcription accuracy and catastrophic forgetting of pre-trained linguistic knowledge. Use when the user wants to benchmark on Gram Vaani, Kathbath, or asks about evaluating this task. Reports WER.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2512.16401
  bibtex_key: chauhan2025navigating
  confidence: high
---

# asr-clinical-continual-eval

> Navigating the Reality Gap: Privacy-Preserving On-Device Continual Adaptation of ASR for Clinical Telephony — Chauhan et al. (2025) (arXiv:2512.16401, 2025)

## What this evaluates

This evaluation probes an ASR model's ability to continuously adapt to noisy, rural clinical telephony speech while retaining its baseline performance on standard general-domain speech. It specifically measures the trade-off between target-domain transcription accuracy and catastrophic forgetting of pre-trained linguistic knowledge.

## Datasets

- **Gram Vaani** — total ?; splits: test (-1)
- **Kathbath** — total ?; splits: val (3151), train_replay (25800)

## Metrics

- `WER` **(primary)** — range: percent
  - Word Error Rate calculated as (Substitutions + Deletions + Insertions) / Total Words in reference. Measures transcription accuracy at the word level.
- `CER` — range: percent
  - Character Error Rate calculated as (Substitutions + Deletions + Insertions) / Total Characters in reference. Provides finer-grained phonetic accuracy analysis.

## Input / output format

**Input**: Raw audio recordings (8kHz telephonic speech upsampled to 16kHz for clinical data; standard read speech for general domain).

**Output**: Text transcription corresponding to the input audio.

## Scoring recipe

```python
def compute_wer(predictions, references):
    S, D, I = edit_distance(predictions, references)
    N = sum(len(ref.split()) for ref in references)
    return (S + D + I) / N
```

## Common pitfalls

- Prior work reported results on a 5-hour Development set; this benchmark strictly uses the 3-hour Evaluation set (GV_Eval_3h) for fair comparison.
- The evaluation simulates a continual learning stream by processing 103 hours of training data sequentially, not as a single batch, which significantly impacts adaptation dynamics.
- CER is reported for phonetic/dialectal analysis but WER is the primary headline metric for overall transcription accuracy.

## Evidence (verbatim from paper)

> We evaluate performance using two standard metrics: Word Error Rate (WER) and Character Error Rate (CER). WER measures transcription accuracy at the word level, while CER provides a finer-grained analysis of phonetic accuracy, particularly useful for agglutinative languages and dialectal variations.

## Citation

```bibtex
@misc{chauhan2025navigating,
  title={Navigating the Reality Gap: Privacy-Preserving On-Device Continual Adaptation of ASR for Clinical Telephony},
  author={Chauhan et al. (2025)},
  year={2025},
  note={arXiv:2512.16401}
}
```

- arXiv: 2512.16401
