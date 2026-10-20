---
name: adaptmmbench-eval
description: Evaluates Vision-Language Models' ability to dynamically select between text-only and tool-augmented reasoning modes, and assesses the quality, efficiency, and final accuracy of their reasoning processes across multimodal domains. Use when the user wants to benchmark on AdaptMMBench, or asks about evaluating this task. Reports Accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2602.02676
  bibtex_key: zhang2026adaptmmbench
  confidence: high
---

# adaptmmbench-eval

> AdaptMMBench: Benchmarking Adaptive Multimodal Reasoning for Mode Selection and Reasoning Process — Zhang et al. (2026) (arXiv:2602.02676, 2026)

## What this evaluates

Evaluates Vision-Language Models' ability to dynamically select between text-only and tool-augmented reasoning modes, and assesses the quality, efficiency, and final accuracy of their reasoning processes across multimodal domains.

## Datasets

- **AdaptMMBench** — total 1300; splits: test (1300)

## Metrics

- `Accuracy` **(primary)** — range: [0, 1]
  - Percentage of correctly answered questions across all domains and reasoning modes. Calculated as the number of correct predictions divided by the total number of samples.
- `MCC` — range: [-1, 1]
  - Matthews Correlation Coefficient measuring the correlation between a model's adaptive mode selection (text vs. tool) and task difficulty/correctness. Computed as (TP*TN - FP*FN) / sqrt((TP+FP)(TP+FN)(TN+FP)(TN+FN)).

## Input / output format

**Input**: Multimodal prompts containing images and text questions, formatted with mode-specific instructions (text-only, adaptive, or oracle tool-augmented).

**Output**: Final answer prediction, plus optional intermediate reasoning steps and tool calls (for adaptive mode).

## Scoring recipe

```python
def compute_accuracy(predictions, golds):
    correct = sum(1 for p, g in zip(predictions, golds) if p == g)
    return correct / len(golds)

def compute_mcc(pred_mode, gold_mode, pred_acc, gold_acc):
    tp = sum(1 for p, g, pa, ga in zip(pred_mode, gold_mode, pred_acc, gold_acc) if p==g and pa==ga)
    tn = sum(1 for p, g, pa, ga in zip(pred_mode, gold_mode, pred_acc, gold_acc) if p!=g and pa!=ga)
    fp = sum(1 for p, g, pa, ga in zip(pred_mode, gold_mode, pred_acc, gold_acc) if p!=g and pa==ga)
    fn = sum(1 for p, g, pa, ga in zip(pred_mode, gold_mode, pred_acc, gold_acc) if p==g and pa!=ga)
    denom = math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))
    return (tp*tn - fp*fn) / denom if denom > 0 else 0.0
```

## Common pitfalls

- Confusing adaptive reasoning accuracy with oracle accuracy, as oracle represents an upper-bound with perfect tool invocation rather than actual model behavior.
- Assuming fewer reasoning steps or tool calls automatically imply better efficiency, since token consumption does not linearly correlate with step count.
- Applying process-level metrics (key step coverage, tool effectiveness) to closed-source models, whose intermediate reasoning traces are inaccessible.

## Evidence (verbatim from paper)

> As shown in Table[1] and Table[3], mode selection capability does not exhibit a strong correlation with final task accuracy. For example, AdaptVision achieves a relatively modest accuracy, yet demonstrates strong mode selection behavior with an MCC of 0.17, outperforming all other models trained on Qwen2.5-VL-7B backbones. In contrast, GPT-5 attains the highest MCC of 0.41, demonstrating good mode selection capability.

## Citation

```bibtex
@misc{zhang2026adaptmmbench,
  title={AdaptMMBench: Benchmarking Adaptive Multimodal Reasoning for Mode Selection and Reasoning Process},
  author={Zhang et al. (2026)},
  year={2026},
  note={arXiv:2602.02676}
}
```

- arXiv: 2602.02676
