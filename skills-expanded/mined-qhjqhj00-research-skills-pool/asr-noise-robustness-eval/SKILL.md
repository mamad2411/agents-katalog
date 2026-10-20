---
name: asr-noise-robustness-eval
description: Evaluates the robustness of end-to-end automatic speech recognition models to real-world acoustic distortions, including far-field reverberation, mixed sampling rates, low-bitrate codecs, and background noise at varying signal-to-noise ratios. Use when the user wants to benchmark on LibriSpeech, BUT ReverbDB, Hub5 Switchboard & CallHome, AISHELL-2, or asks about evaluating this task. Reports greedy WER (%).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2010.12715
  bibtex_key: balam2020improving
  confidence: high
---

# asr-noise-robustness-eval

> Improving Noise Robustness of an End-to-End Neural Model for Automatic Speech Recognition — Balam et al. (2020) (arXiv:2010.12715, 2020)

## What this evaluates

Evaluates the robustness of end-to-end automatic speech recognition models to real-world acoustic distortions, including far-field reverberation, mixed sampling rates, low-bitrate codecs, and background noise at varying signal-to-noise ratios.

## Datasets

- **LibriSpeech** — total ?; splits: test-clean (-1), test-other (-1)
- **BUT ReverbDB** — total ?; splits: D105 (-1), L207 (-1), L212 (-1), Q301 (-1)
- **Hub5 Switchboard & CallHome** — total ?; splits: SWB (-1), CHM (-1)
- **AISHELL-2** — total ?; splits: dev_ios (-1), test_ios (-1)

## Metrics

- `greedy WER (%)` **(primary)** — range: percent
  - Word Error Rate calculated as (Substitutions + Deletions + Insertions) / Total Reference Words × 100. The protocol explicitly requires greedy decoding without an external language model to isolate acoustic model improvements.

## Input / output format

**Input**: Raw audio utterances (speech), optionally augmented with simulated background noise, reverberation, or low-rate codec distortion.

**Output**: Text transcription of the audio utterance.

## Scoring recipe

```python
def compute_greedy_wer(predictions, references):
    total_errors = 0
    total_words = 0
    for pred, ref in zip(predictions, references):
        # Calculate edit distance operations (substitutions, deletions, insertions)
        errors = calculate_wer_errors(ref, pred)
        total_errors += errors
        total_words += len(ref.split())
    return (total_errors / total_words) * 100
```

## Common pitfalls

- Using an external language model during decoding, which masks the true acoustic robustness of the model and violates the paper's protocol.
- Failing to average WER over multiple noise realizations (the protocol specifies 20 iterations per SNR for simulated noise tests).
- Evaluating on clean test sets to claim noise robustness, which contradicts the focus on augmented/far-field/noisy splits.

## Evidence (verbatim from paper)

> We use greedy WERs without the usage of an external language model throughout this paper to elucidate improvements solely due to data augmentation used in acoustic modeling. At each SNR, random noise segments are added to each utterance for 5 iterations for each of the four types of noises in VOiCES, resulting in 20 simulated noise sets at each SNR.

## Citation

```bibtex
@misc{balam2020improving,
  title={Improving Noise Robustness of an End-to-End Neural Model for Automatic Speech Recognition},
  author={Balam et al. (2020)},
  year={2020},
  note={arXiv:2010.12715}
}
```

- arXiv: 2010.12715
