---
name: ast-eval
description: Evaluates automatic speech translation (AST) and automatic speech recognition (ASR) performance on English-French and English-Romanian datasets. It probes the model's ability to convert spoken source audio directly into written target-language translations, and to recognize speech transcripts. Use when the user wants to benchmark on AST LibriSpeech, MuST-C, or asks about evaluating this task. Reports BLEU.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2002.12231
  bibtex_key: mccarthy2020skinaugment
  confidence: high
---

# ast-eval

> SkinAugment: Auto-Encoding Speaker Conversions for Automatic Speech Translation — McCarthy et al. (2020) (arXiv:2002.12231, 2020)

## What this evaluates

Evaluates automatic speech translation (AST) and automatic speech recognition (ASR) performance on English-French and English-Romanian datasets. It probes the model's ability to convert spoken source audio directly into written target-language translations, and to recognize speech transcripts.

## Datasets

- **AST LibriSpeech** — total ?; splits: test (-1)
- **MuST-C** — total ?; splits: test (-1)

## Metrics

- `BLEU` **(primary)** — range: [0, 100]
  - Standard BLEU score computed on tokenized target-language translations.
- `WER` — range: percent
  - Word Error Rate computed on tokenized transcripts.

## Input / output format

**Input**: Source-language audio waveform (and optionally source transcripts for ASR/AST training).

**Output**: Target-language text translation (for AST) or source-language transcript (for ASR), tokenized using Moses for translations or standard tokenization for transcripts.

## Scoring recipe

```python
def score_ast(predictions, gold):
    pred_tok = moses_tokenize(predictions)
    gold_tok = moses_tokenize(gold)
    return bleu_score(pred_tok, gold_tok) * 100

def score_asr(predictions, gold):
    return wer_score(predictions, gold) * 100
```

## Common pitfalls

- AST LibriSpeech test sets do not correspond to the original LibriSpeech test sets; they are a subset of LibriSpeech's training set.
- Voices present in the AST LibriSpeech test set must be removed from the LibriSpeech training set before training the speaker conversion model to prevent data leakage.
- BLEU and WER are computed on tokenized output, not raw text.

## Evidence (verbatim from paper)

> We experiment on two standard AST datasets: AST LibriSpeech [12] (English-French; we use the same setup as [13]) and MuST-C (English-Romanian; 432 hours) [14]. For AST, we report BLEU [15] on tokenized output. (On the ASR task, the transcript is already tokenized; on the AST tasks, we tokenize translations with Moses [16].) For ASR, we use word error rate (WER), also on tokenized output.

## Citation

```bibtex
@misc{mccarthy2020skinaugment,
  title={SkinAugment: Auto-Encoding Speaker Conversions for Automatic Speech Translation},
  author={McCarthy et al. (2020)},
  year={2020},
  note={arXiv:2002.12231}
}
```

- arXiv: 2002.12231
