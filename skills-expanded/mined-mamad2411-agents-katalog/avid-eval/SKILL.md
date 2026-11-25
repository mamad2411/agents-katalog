---
name: avid-eval
description: Evaluates a model's ability to detect, classify, and temporally ground audio-visual inconsistencies in long-form videos, as well as generate causal explanations for cross-modal mismatches across eight fine-grained categories. Use when the user wants to benchmark on AVID, or asks about evaluating this task. Reports mIoU.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.13593
  bibtex_key: chen2026avid
  confidence: high
---

# avid-eval

> AVID: A Benchmark for Omni-Modal Audio-Visual Inconsistency Understanding via Agent-Driven Construction — Chen et al. (2026) (arXiv:2604.13593, 2026)

## What this evaluates

Evaluates a model's ability to detect, classify, and temporally ground audio-visual inconsistencies in long-form videos, as well as generate causal explanations for cross-modal mismatches across eight fine-grained categories.

## Datasets

- **AVID** — total 11200; splits: train (9639), test (1561)

## Metrics

- `mIoU` **(primary)** — range: [0, 1]
  - Mean Intersection over Union for temporal grounding, calculated as the average IoU across all predicted inconsistency segments compared to ground-truth timestamps.
- `BLEU-4` — range: [0, 1]
  - 4-gram BLEU score measuring the n-gram overlap between generated causal explanations or reasoning text and reference annotations.

## Input / output format

**Input**: Full-length videos or temporally segmented clips containing synchronized audio and visual streams.

**Output**: Predicted inconsistency labels (consistent/inconsistent), classification into one of 8 fine-grained categories, temporal boundaries (start/end timestamps) for each event, and a textual causal explanation.

## Scoring recipe

```python
def compute_mIoU(pred_segments, gold_segments):
    ious = []
    for pred, gold in zip(pred_segments, gold_segments):
        intersection = max(0, min(pred.end, gold.end) - max(pred.start, gold.start))
        union = max(pred.end, gold.end) - min(pred.start, gold.start)
        ious.append(intersection / union if union > 0 else 0.0)
    return sum(ious) / len(ious) if ious else 0.0

def compute_bleu4(predictions, references):
    return nltk.bleu_score.corpus_bleu([[ref] for ref in references], predictions, weights=(0.25, 0.25, 0.25, 0.25))
```

## Common pitfalls

- Inconsistency patterns are class-dependent (e.g., lip-sync vs. semantic vs. environmental), so models must adapt reasoning per segment type rather than using a single heuristic.
- Evaluation operates at both video and segment levels; confusing segment-level temporal grounding with video-level classification leads to inflated or deflated scores.
- Agent-driven construction may introduce synthesis artifacts that models could reverse-engineer instead of performing true cross-modal reasoning.

## Evidence (verbatim from paper)

> enables evaluation of detection, classification, and reasoning tasks with precise temporal annotations and causal explanations, revealing significant limitations in state-of-the-art omni-modal models—particularly in temporal grounding (mIoU: 36.1% vs. 26.2%) and segment-level reasoning (2.8× BLEU-4 improvement over base models)

## Citation

```bibtex
@misc{chen2026avid,
  title={AVID: A Benchmark for Omni-Modal Audio-Visual Inconsistency Understanding via Agent-Driven Construction},
  author={Chen et al. (2026)},
  year={2026},
  note={arXiv:2604.13593}
}
```

- arXiv: 2604.13593
