---
name: asr-coprocessor-eval
description: Evaluates the training efficiency and final accuracy of end-to-end acoustic models for Automatic Speech Recognition across different CPU-GPU co-processor hardware configurations. It measures how quickly models reach specific accuracy targets (Time-to-Accuracy) and compares final error rates against baseline architectures. Use when the user wants to benchmark on ASR_Dataset, or asks about evaluating this task. Reports TTA.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2003.12366
  bibtex_key: baunsgaard2020training
  confidence: high
---

# asr-coprocessor-eval

> Training for Speech Recognition on Coprocessors — Baunsgaard et al. (2020) (arXiv:2003.12366, 2020)

## What this evaluates

Evaluates the training efficiency and final accuracy of end-to-end acoustic models for Automatic Speech Recognition across different CPU-GPU co-processor hardware configurations. It measures how quickly models reach specific accuracy targets (Time-to-Accuracy) and compares final error rates against baseline architectures.

## Datasets

- **ASR_Dataset** — total ?; splits: train (-1), val (-1), test (-1)

## Metrics

- `TTA` **(primary)** — range: other
  - Time-to-Accuracy: the training duration in minutes required for the model to reach a predefined Character Error Rate (CER) or Word Error Rate (WER) threshold on the validation set.
- `CER` — range: percent
  - Character Error Rate: the standard character-level edit distance metric normalized by the reference length, reported as a percentage.
- `WER` — range: percent
  - Word Error Rate: the standard word-level edit distance metric normalized by the reference length, reported as a percentage.

## Input / output format

**Input**: Audio feature sequences and corresponding text transcripts for training; audio features for validation and testing.

**Output**: CTC probability distributions over time steps, decoded into character/word sequences for error rate calculation.

## Scoring recipe

```python
def calculate_tta(val_preds, val_labels, target_cer, target_wer):
    for t, (pred, label) in enumerate(zip(val_preds, val_labels)):
        cer = compute_cer(pred, label)
        wer = compute_wer(pred, label)
        if cer <= target_cer or wer <= target_wer:
            return t  # time in minutes
    return None  # NA if target not reached

def calculate_final_accuracy(test_preds, test_labels):
    return compute_cer(test_preds, test_labels), compute_wer(test_preds, test_labels)
```

## Common pitfalls

- Large batch sizes improve initial convergence speed but reduce final statistical efficiency, causing high-throughput systems to achieve lower final accuracy and potentially never reach lower TTA thresholds.
- Hardware utilization and throughput do not directly correlate with training efficiency or final model accuracy; a system can have high hardware utilization but low training efficiency.
- TTA is highly sensitive to the chosen accuracy thresholds, and models may never reach stricter thresholds (reported as NA), making cross-system comparisons dependent on the specific TTA levels selected.

## Evidence (verbatim from paper)

> The TTA levels chosen for CER are 10, 8, and 7. The TTA levels chosen for WER are 22, 20.2, and 19.2. All TTA levels have been plotted as horizontal lines to indicate when the different executions reach the TTA levels. Table 4 reports the specific TTA values, where NA represents the case, where the specified accuracy level is not reached.

## Citation

```bibtex
@misc{baunsgaard2020training,
  title={Training for Speech Recognition on Coprocessors},
  author={Baunsgaard et al. (2020)},
  year={2020},
  note={arXiv:2003.12366}
}
```

- arXiv: 2003.12366
