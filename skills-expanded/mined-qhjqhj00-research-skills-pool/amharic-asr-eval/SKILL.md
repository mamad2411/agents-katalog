---
name: amharic-asr-eval
description: Evaluates fine-tuned Whisper models for Amharic speech-to-text recognition by measuring transcription accuracy at word and character levels, alongside n-gram overlap. It also probes the impact of homophone normalization and zero-shot generalization on low-resource language ASR performance. Use when the user wants to benchmark on FLEURS Amharic, BDU Speech Corpus, Mozilla Common Voice v17.0 Amharic, or asks about evaluating this task. Reports WER.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2503.18485
  bibtex_key: gete2025whisperingamharic
  confidence: high
---

# amharic-asr-eval

> Whispering in Amharic: Fine-tuning Whisper for Low-resource Language — Gete et al. (2025) (arXiv:2503.18485, 2025)

## What this evaluates

Evaluates fine-tuned Whisper models for Amharic speech-to-text recognition by measuring transcription accuracy at word and character levels, alongside n-gram overlap. It also probes the impact of homophone normalization and zero-shot generalization on low-resource language ASR performance.

## Datasets

- **FLEURS Amharic** — total ?; splits: test (516)
- **BDU Speech Corpus** — total ?; splits: test (389)
- **Mozilla Common Voice v17.0 Amharic** — total ?; splits: test (205)

## Metrics

- `WER` **(primary)** — range: percent
  - Word Error Rate measures the percentage of word-level errors (insertions, deletions, substitutions) in the transcribed text compared to the reference text. A lower WER indicates better performance.
- `CER` — range: percent
  - Character Error Rate measures the percentage of character-level errors in the transcribed text compared to the reference text. Lower values indicate better accuracy.
- `BLEU` — range: percent
  - Bilingual Evaluation Understudy measures the overlap between model-generated text and reference text using n-gram precision. Both corpus BLEU (overall dataset quality) and average BLEU (sentence-level consistency) are reported.

## Input / output format

**Input**: Audio files resampled to 16kHz, processed through Whisper's feature extractor and tokenizer.

**Output**: Amharic text transcription.

## Scoring recipe

```python
def compute_wer(predictions, references):
    total_errors = 0
    total_words = 0
    for pred, ref in zip(predictions, references):
        dist = levenshtein_distance(pred.split(), ref.split())
        total_errors += dist
        total_words += len(ref.split())
    return (total_errors / total_words) * 100 if total_words > 0 else 0.0
# CER and BLEU follow standard implementations (e.g., jiwer, sacrebleu)
```

## Common pitfalls

- Failing to apply homophone normalization to Amharic text before evaluation, which artificially inflates WER/CER due to orthographic variations of phonetically identical characters.
- Relying exclusively on automated metrics without human evaluation, as they cannot capture semantic correctness, fluency, or contextual usability of the transcriptions.
- Expecting zero-shot pre-trained Whisper models to perform well on Amharic without fine-tuning, as they typically generate gibberish, non-Amharic text, or repetitive characters.

## Evidence (verbatim from paper)

> In STT, the most widely used metrics, which are employed in this work, are Word Error Rate (WER), Character Error Rate (CER), and Bilingual Evaluation Understudy (BLEU). Additionally, we highlight the importance of Human Evaluation in addressing the litigation beyond these automated metrics. Word Error Rate measures the percentage of word-level errors in transcribed text compared to the reference text; a lower WER indicates better performance.

## Citation

```bibtex
@misc{gete2025whisperingamharic,
  title={Whispering in Amharic: Fine-tuning Whisper for Low-resource Language},
  author={Gete et al. (2025)},
  year={2025},
  note={arXiv:2503.18485}
}
```

- arXiv: 2503.18485
