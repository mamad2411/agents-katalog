---
name: ascend-eval
description: Evaluates automatic speech recognition (ASR) models on spontaneous Mandarin-English code-switching in multi-turn conversations. It probes the model's ability to accurately transcribe mixed-language speech under realistic, unscripted conditions with diverse speaker backgrounds. Use when the user wants to benchmark on ASCEND, or asks about evaluating this task. Reports MER.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2112.06223
  bibtex_key: lovenia2021ascend
  confidence: high
---

# ascend-eval

> ASCEND: A Spontaneous Chinese-English Dataset for Code-switching in Multi-turn Conversation — Holy Lovenia et al. (2021) (arXiv:2112.06223, 2021)

## What this evaluates

Evaluates automatic speech recognition (ASR) models on spontaneous Mandarin-English code-switching in multi-turn conversations. It probes the model's ability to accurately transcribe mixed-language speech under realistic, unscripted conditions with diverse speaker backgrounds.

## Datasets

- **ASCEND** — total ?; splits: validation (-1), test (-1); repo https://github.com/HLTCHKUST/ASCEND

## Metrics

- `CER` — range: percent
  - Computed as the total of substitutions, deletions, and insertions divided by the number of characters in the reference.
- `MER` **(primary)** — range: percent
  - Calculated by measuring the CER for Chinese characters and word error rate (WER) for other characters (English).

## Input / output format

**Input**: Normalized audio recordings of spontaneous multi-turn conversations, optionally augmented with SpecAugment (time/frequency masking) during training.

**Output**: CTC-decoded transcription string matching the reference text.

## Scoring recipe

```python
def compute_cer(pred, ref):
    return edit_distance(pred, ref) / len(ref)

def compute_mer(pred, ref):
    zh_pred, zh_ref = extract_chinese(pred, ref)
    en_pred, en_ref = extract_english(pred, ref)
    cer_zh = compute_cer(zh_pred, zh_ref)
    wer_en = compute_wer(en_pred, en_ref)
    return (cer_zh + wer_en) / 2.0
```

## Common pitfalls

- MER combines character-level and word-level errors differently for Chinese and English, so standard WER or CER alone does not capture code-switching performance accurately.
- The dataset uses spontaneous speech with diverse dialects and proficiency levels, meaning models trained on read-speech or clean corpora may significantly underperform compared to baseline expectations.
- Vocabulary extension with ASCEND-specific tokens is required before fine-tuning wav2vec 2.0; skipping this step leads to suboptimal tokenizer alignment and higher error rates.

## Evidence (verbatim from paper)

> As for evaluation metrics, considering the character-based nature of the Chinese transcriptions and the word-based nature of the English transcriptions in ASCEND, we measure the models' performance using character error rate (CER) and mixed error rate (MER) (Schultz et al., 2011; Hu et al., 2020; Qiu et al., 2020). The CER is computed as the total of substitutions, deletions, and insertions divided by the number of characters in the reference, while the MER is calculated by measuring the CER for Chinese characters and word error rate (WER) for other characters.

## Citation

```bibtex
@misc{lovenia2021ascend,
  title={ASCEND: A Spontaneous Chinese-English Dataset for Code-switching in Multi-turn Conversation},
  author={Holy Lovenia et al. (2021)},
  year={2021},
  note={arXiv:2112.06223}
}
```

- arXiv: 2112.06223
