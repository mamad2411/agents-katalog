---
name: asr-bambara-eval
description: Evaluates automatic speech recognition (ASR) models on spontaneous speech in Bambara, a low-resource West African language. It probes the models' ability to accurately transcribe audio segments in both a controlled test set and a more heterogeneous benchmark. Use when the user wants to benchmark on Afvoices Test, Nyana Eval, or asks about evaluating this task. Reports WER (%).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2511.18557
  bibtex_key: diarra2025dealing
  confidence: high
---

# asr-bambara-eval

> Dealing with the Hard Facts of Low-Resource African NLP — Diarra et al. (2025) (arXiv:2511.18557, 2025)

## What this evaluates

Evaluates automatic speech recognition (ASR) models on spontaneous speech in Bambara, a low-resource West African language. It probes the models' ability to accurately transcribe audio segments in both a controlled test set and a more heterogeneous benchmark.

## Datasets

- **Afvoices Test** — total ?; splits: test (-1)
- **Nyana Eval** — total ?; splits: test (-1)

## Metrics

- `WER (%)` **(primary)** — range: percent
  - Standard Word Error Rate: (Substitutions + Deletions + Insertions) / Reference Words * 100. Calculated after removing acoustic event tags from both reference and prediction.
- `CER (%)` — range: percent
  - Standard Character Error Rate: (Substitutions + Deletions + Insertions) / Reference Characters * 100. Calculated after removing acoustic event tags from both reference and prediction.

## Input / output format

**Input**: Audio segments containing spontaneous speech in Bambara.

**Output**: Text transcript corresponding to the input audio segment.

## Scoring recipe

```python
def compute_metrics(predictions, references):
    # Remove acoustic event tags from both reference and prediction
    ref_clean = remove_acoustic_tags(references)
    pred_clean = remove_acoustic_tags(predictions)
    
    # Calculate WER
    wer = 100 * edit_distance(ref_clean, pred_clean) / len(ref_clean.split())
    # Calculate CER
    cer = 100 * edit_distance(ref_clean, pred_clean) / len(ref_clean)
    return wer, cer
```

## Common pitfalls

- Failing to remove acoustic event tags from both the reference and prediction before calculating error rates, which artificially inflates WER/CER.
- Evaluating on the 98-hour training data instead of the designated test sets (Afvoices Test and Nyana Eval).
- Using unnormalized text or inconsistent tokenization when computing character-level metrics.

## Evidence (verbatim from paper)

> We apply the same normalization steps to our test sets and this time we remove the acoustic event tags from both the reference and the prediction before calculating the WER and CER.

## Citation

```bibtex
@misc{diarra2025dealing,
  title={Dealing with the Hard Facts of Low-Resource African NLP},
  author={Diarra et al. (2025)},
  year={2025},
  note={arXiv:2511.18557}
}
```

- arXiv: 2511.18557
