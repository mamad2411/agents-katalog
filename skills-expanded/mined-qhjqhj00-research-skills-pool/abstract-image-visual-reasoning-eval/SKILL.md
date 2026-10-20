---
name: abstract-image-visual-reasoning-eval
description: Evaluates multimodal models' ability to comprehend and reason over synthetic abstract images, including charts, tables, road maps, dashboards, relation graphs, flowcharts, visual puzzles, and planar layouts. Use when the user wants to benchmark on Synthetic Abstract Image Benchmark, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2407.07053
  bibtex_key: zhang2024multimodalselinstruct
  confidence: high
---

# abstract-image-visual-reasoning-eval

> Multimodal Self-Instruct: Synthetic Abstract Image and Visual Reasoning Instruction Using Language Model — Wenqi Zhang et al. (arXiv:2407.07053, 2024)

## What this evaluates

Evaluates multimodal models' ability to comprehend and reason over synthetic abstract images, including charts, tables, road maps, dashboards, relation graphs, flowcharts, visual puzzles, and planar layouts.

## Datasets

- **Synthetic Abstract Image Benchmark** — total ?; splits: test (-1); repo https://github.com/zwq2018/Multi-modal-Self-instruct

## Metrics

- `accuracy` **(primary)** — range: percent
  - Standard classification accuracy: the proportion of correctly predicted answers out of the total number of instances. Calculated per task and averaged across tasks.

## Input / output format

**Input**: An abstract image (e.g., chart, map, flowchart) paired with a natural language instruction or question.

**Output**: A natural language text response answering the instruction or question.

## Scoring recipe

```python
def compute_accuracy(predictions, gold_labels):
    correct = sum(1 for p, g in zip(predictions, gold_labels) if p.strip().lower() == g.strip().lower())
    return correct / len(gold_labels)
```

## Common pitfalls

- Models typically resize abstract images to 336x336, discarding fine geometric features critical for tasks like planar layout or dashboard reading.
- Tasks require distinct reasoning skills (e.g., dynamic path planning for maps, pattern induction for puzzles); models strong on natural photos often fail on abstract spatial relationships.
- Performance gaps are highly task-dependent; e.g., dashboard accuracy drops to ~54% while other tasks may be higher, so averaging without task-level reporting masks weaknesses.

## Evidence (verbatim from paper)

> We observe that for these abstract images, even advanced LMMs like GPT-4o and Claude-3.5-Sonnet achieved only 64.7% and 59.9% accuracy on average for all tasks, leaving a significant gap to human-level performance (82.1%).

## Citation

```bibtex
@misc{zhang2024multimodalselinstruct,
  title={Multimodal Self-Instruct: Synthetic Abstract Image and Visual Reasoning Instruction Using Language Model},
  author={Wenqi Zhang et al.},
  year={2024},
  note={arXiv:2407.07053}
}
```

- arXiv: 2407.07053
