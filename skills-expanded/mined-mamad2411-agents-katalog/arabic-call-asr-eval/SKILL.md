---
name: arabic-call-asr-eval
description: Evaluates the ability of Automatic Speech Recognition (ASR) models to accurately transcribe spoken Arabic from real-world telephonic calls. It probes robustness to dialectal diversity, variable audio quality, and background noise typical of call-domain environments. Use when the user wants to benchmark on Arabic Call Domain Benchmark, or asks about evaluating this task. Reports WER.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2403.04280
  bibtex_key: aboobaidah2024arabiccall
  confidence: high
---

# arabic-call-asr-eval

> A New Benchmark for Evaluating Automatic Speech Recognition in the Arabic Call Domain — Abo Obaidah et al. (2024) (arXiv:2403.04280, 2024)

## What this evaluates

Evaluates the ability of Automatic Speech Recognition (ASR) models to accurately transcribe spoken Arabic from real-world telephonic calls. It probes robustness to dialectal diversity, variable audio quality, and background noise typical of call-domain environments.

## Datasets

- **Arabic Call Domain Benchmark** — total ?; splits: test (-1)

## Metrics

- `WER` **(primary)** — range: percent
  - Word Error Rate: 100 * (S + D + I) / N, where S=substitutions, D=deletions, I=insertions, and N=total words in the reference transcription. Lower is better.
- `CER` — range: percent
  - Character Error Rate: 100 * (S + D + I) / N, where S=substitutions, D=deletions, I=insertions, and N=total characters in the reference transcription. Lower is better.

## Input / output format

**Input**: Audio recordings of telephonic calls in Arabic, featuring six dialects and variable audio quality (clean to noisy environments).

**Output**: Transcribed text corresponding to the input audio.

## Scoring recipe

```python
def compute_metrics(predictions, references):
    wer_scores, cer_scores = [], []
    for pred, ref in zip(predictions, references):
        pred_words = pred.split()
        ref_words = ref.split()
        n_ref = len(ref_words)
        if n_ref == 0: continue
        # Standard Levenshtein-based edit distance
        wer_scores.append(100 * edit_distance(pred_words, ref_words) / n_ref)
        cer_scores.append(100 * edit_distance(list(pred), list(ref)) / len(ref))
    return {
        'WER': sum(wer_scores) / len(wer_scores),
        'CER': sum(cer_scores) / len(cer_scores)
    }
```

## Common pitfalls

- Audio quality varies significantly from clean to noisy, which heavily impacts WER/CER and requires careful preprocessing or robust model selection.
- Dialectal diversity across six Arabic dialects means models trained primarily on Modern Standard Arabic (MSA) will likely underperform without dialect-specific fine-tuning.
- Telephonic bandwidth limitations (narrowband audio) can artificially inflate error rates compared to high-fidelity speech datasets, making direct comparison with lab-recorded benchmarks misleading.

## Evidence (verbatim from paper)

> The evaluation of Automatic Speech Recognition (ASR) systems reveals a wide range of performance across different models, as evidenced by their Word Error Rate (WER) and Character Error Rate (CER). These metrics serve as critical benchmarks for assessing the ability of ASR systems to accurately transcribe spoken language into text.

## Citation

```bibtex
@misc{aboobaidah2024arabiccall,
  title={A New Benchmark for Evaluating Automatic Speech Recognition in the Arabic Call Domain},
  author={Abo Obaidah et al. (2024)},
  year={2024},
  note={arXiv:2403.04280}
}
```

- arXiv: 2403.04280
