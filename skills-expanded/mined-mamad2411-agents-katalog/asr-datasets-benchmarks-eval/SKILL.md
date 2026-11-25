---
name: asr-datasets-benchmarks-eval
description: Evaluates Automatic Speech Recognition systems across diverse acoustic conditions, domains, and linguistic settings. It probes model robustness to read vs. spontaneous speech, clean vs. noisy environments, and demographic bias in multilingual crowdsourced data. Use when the user wants to benchmark on LibriSpeech, Switchboard, TED-LIUM 3, CHiME-6, Common Voice 17.0, or asks about evaluating this task. Reports Word Error Rate (WER).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2510.12827
  bibtex_key: nayeem2025asr
  confidence: medium
---

# asr-datasets-benchmarks-eval

> Automatic Speech Recognition in the Modern Era: Architectures, Training, and Evaluation — Nayeem et al. (2025) (arXiv:2510.12827, 2025)

## What this evaluates

Evaluates Automatic Speech Recognition systems across diverse acoustic conditions, domains, and linguistic settings. It probes model robustness to read vs. spontaneous speech, clean vs. noisy environments, and demographic bias in multilingual crowdsourced data.

## Datasets

- **LibriSpeech** — total 960; splits: train (-1), dev (-1), test-clean (-1), test-other (-1)
- **Switchboard** — total 300; splits: train (-1)
- **TED-LIUM 3** — total 452; splits: train (-1)
- **CHiME-6** — total 50; splits: train (-1)
- **Common Voice 17.0** — total 20000; splits: train (-1)

## Metrics

- `Word Error Rate (WER)` **(primary)** — range: percent
  - Not explicitly defined in this section; standard ASR evaluation computes the minimum number of insertions, deletions, and substitutions required to transform the predicted transcript into the reference transcript, normalized by reference length.

## Input / output format

**Input**: Audio recordings (8 kHz or 16 kHz sampled) with corresponding reference transcripts.

**Output**: Predicted text transcripts aligned with the input audio.

## Scoring recipe

```python
def compute_wer(predictions, references):
    total_errors = 0
    total_refs = 0
    for pred, ref in zip(predictions, references):
        edits = levenshtein_distance(pred, ref)
        total_errors += edits
        total_refs += len(ref.split())
    return (total_errors / total_refs) * 100
```

## Common pitfalls

- Evaluating LibriSpeech on test-clean vs test-other separately is critical, as they represent different speaker difficulty levels and acoustic conditions.
- Dataset licensing varies significantly (e.g., CC BY 4.0 vs. LDC license), which restricts data sharing and can hinder full reproducibility.
- Mismatched sampling rates (8 kHz telephone vs. 16 kHz studio) must be handled during preprocessing to avoid artificial performance degradation.

## Evidence (verbatim from paper)

> The development and evaluation of ASR systems are grounded in standardized datasets that serve as common benchmarks for the research community. These datasets vary widely in size, domain, recording conditions, and linguistic content, allowing for the assessment of different aspects of system performance.

## Citation

```bibtex
@misc{nayeem2025asr,
  title={Automatic Speech Recognition in the Modern Era: Architectures, Training, and Evaluation},
  author={Nayeem et al. (2025)},
  year={2025},
  note={arXiv:2510.12827}
}
```

- arXiv: 2510.12827
