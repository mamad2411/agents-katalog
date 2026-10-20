---
name: asr-wer-eval
description: Evaluates automatic speech recognition (ASR) performance across English and Croatian by measuring word error rate on multiple held-out test sets. It probes the model's ability to accurately transcribe spoken audio, including handling of punctuation and capitalization. Use when the user wants to benchmark on VoxPopuli, FLEURS, Mozilla Common Voice (MCV12), Hugging Face ASR Leaderboard datasets, or asks about evaluating this task. Reports WER.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2505.13404
  bibtex_key: koluguri2025granary
  confidence: high
---

# asr-wer-eval

> Granary: Speech Recognition and Translation Dataset in 25 European Languages — Koluguri et al. (2025) (arXiv:2505.13404, 2025)

## What this evaluates

Evaluates automatic speech recognition (ASR) performance across English and Croatian by measuring word error rate on multiple held-out test sets. It probes the model's ability to accurately transcribe spoken audio, including handling of punctuation and capitalization.

## Datasets

- **VoxPopuli** — total ?; splits: test (-1)
- **FLEURS** — total ?; splits: test (-1)
- **Mozilla Common Voice (MCV12)** — total ?; splits: test (-1)
- **Hugging Face ASR Leaderboard datasets** — total ?; splits: test (-1)

## Metrics

- `WER` **(primary)** — range: percent
  - Word Error Rate calculated as the percentage of edit operations (substitutions, deletions, insertions) relative to the number of words in the reference transcription. Reported with and without punctuation and capitalization (PnC vs. noPnC).

## Input / output format

**Input**: Raw audio recordings in English or Croatian.

**Output**: Transcribed text string corresponding to the audio input.

## Scoring recipe

```python
def compute_wer(predictions, references):
    # Align hypothesis and reference sequences
    # Count substitutions (S), deletions (D), insertions (I)
    # N = total words in reference
    wer = (S + D + I) / N
    return wer * 100  # Return as percentage
```

## Common pitfalls

- WER scores vary significantly depending on whether punctuation and capitalization (PnC) are included in the reference and hypothesis.
- Test set composition differs across benchmarks (e.g., FLEURS vs. VoxPopuli vs. MCV), making direct cross-dataset comparison difficult.
- Croatian evaluation is limited to a small subset due to lack of validated test data in Mozilla Common Voice.

## Evidence (verbatim from paper)

> We evaluate our models on three test sets, both with and without punctuation and capitalization where applicable: VoxPopuli [[7]] and FLEURS [[28]] for English and Croatian. Since no validated test set is available for Croatian in Mozilla Common Voice (MCV), we conduct evaluations on MCV only for English. Additionally, we assess our models on the Hugging Face ASR leaderboard[[29]] datasets for English. Table 2: WER of FastConformer-L on MOSEL and Granary English datasets [%] Table 3: WER of FastConformer-L model on MOSEL and Granary Croatian datasets [%]

## Citation

```bibtex
@misc{koluguri2025granary,
  title={Granary: Speech Recognition and Translation Dataset in 25 European Languages},
  author={Koluguri et al. (2025)},
  year={2025},
  note={arXiv:2505.13404}
}
```

- arXiv: 2505.13404
