---
name: atc-asr-domain-shift-eval
description: This benchmark evaluates the robustness of self-supervised speech recognition models under domain shift in air traffic control communications. It probes few-shot fine-tuning capabilities, sensitivity to audio quality and accents, and potential gender bias in transcription performance. Use when the user wants to benchmark on NATS, ISAVIA, LiveATC-Test, ATCO2-Test, LDC-ATCC, UWB-ATCC, ATCOSIM, or asks about evaluating this task. Reports WER.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2203.16822
  bibtex_key: zuluagagomez2022atc
  confidence: high
---

# atc-asr-domain-shift-eval

> How Does Pre-trained Wav2Vec 2.0 Perform on Domain Shifted ASR? An Extensive Benchmark on Air Traffic Control Communications — Zuluaga-Gomez et al. (2022) (arXiv:2203.16822, 2022)

## What this evaluates

This benchmark evaluates the robustness of self-supervised speech recognition models under domain shift in air traffic control communications. It probes few-shot fine-tuning capabilities, sensitivity to audio quality and accents, and potential gender bias in transcription performance.

## Datasets

- **NATS** — total ?; splits: train (-1), test (-1); repo https://github.com/idiap/w2v2-air-traffic
- **ISAVIA** — total ?; splits: train (-1), test (-1); repo https://github.com/idiap/w2v2-air-traffic
- **LiveATC-Test** — total ?; splits: test (-1); repo https://github.com/idiap/w2v2-air-traffic
- **ATCO2-Test** — total ?; splits: test (-1); repo https://github.com/idiap/w2v2-air-traffic
- **LDC-ATCC** — total ?; splits: train (-1), test (-1); repo https://github.com/idiap/w2v2-air-traffic
- **UWB-ATCC** — total ?; splits: train (-1), test (-1); repo https://github.com/idiap/w2v2-air-traffic
- **ATCOSIM** — total ?; splits: train (-1), test (-1); repo https://github.com/idiap/w2v2-air-traffic

## Metrics

- `WER` **(primary)** — range: percent
  - Word Error Rate calculated as the percentage of word substitutions, deletions, and insertions relative to the total number of words in the reference transcript.

## Input / output format

**Input**: Mono-channel audio recordings up-sampled to 16 kHz (16-bit PCM).

**Output**: Character-level sequence using a 32-character vocabulary (English alphabet, symbols, and blank token), decoded via greedy Softmax.

## Scoring recipe

```python
def compute_wer(predictions, references):
    total_words = sum(len(ref.split()) for ref in references)
    if total_words == 0: return 0.0
    errors = sum(edit_distance(pred, ref) for pred, ref in zip(predictions, references))
    return (errors / total_words) * 100
```

## Common pitfalls

- Audio quality varies drastically (SNR 5–20 dB) and is not normalized, causing WER spikes that reflect channel conditions rather than model capability alone.
- Gender imbalance in fine-tuning data leads to significant performance gaps; models trained predominantly on one gender show degraded WER on the other.
- Few-shot scenarios (<1 hour) require careful data splitting to avoid speaker/utterance overlap between train and test sets, which otherwise inflates performance.

## Evidence (verbatim from paper)

> Initially, we assess WERs of several E2E models when fine-tuned with ATC audio. ... We report Word Error Rate (WER) in percentages (%) for models fine-tuned with different amounts of data (x-axis).

## Citation

```bibtex
@misc{zuluagagomez2022atc,
  title={How Does Pre-trained Wav2Vec 2.0 Perform on Domain Shifted ASR? An Extensive Benchmark on Air Traffic Control Communications},
  author={Zuluaga-Gomez et al. (2022)},
  year={2022},
  note={arXiv:2203.16822}
}
```

- arXiv: 2203.16822
