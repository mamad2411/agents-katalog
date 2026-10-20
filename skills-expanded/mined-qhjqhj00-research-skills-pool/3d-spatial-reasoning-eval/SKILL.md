---
name: 3d-spatial-reasoning-eval
description: Evaluates a model's ability to perform 3D visual grounding and situated question answering by reasoning over object coordinates and spatial relations in 3D scenes. It probes whether the model can accurately locate objects based on natural language instructions and answer spatial questions about scene layouts without linguistic interference. Use when the user wants to benchmark on ScanRefer, Multi3DRef, SQA3D, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2603.24721
  bibtex_key: zhou2026scalable
  confidence: medium
---

# 3d-spatial-reasoning-eval

> Scalable Object Relation Encoding for Better 3D Spatial Reasoning in Large Language Models — Zhou et al. (2026) (arXiv:2603.24721, 2026)

## What this evaluates

Evaluates a model's ability to perform 3D visual grounding and situated question answering by reasoning over object coordinates and spatial relations in 3D scenes. It probes whether the model can accurately locate objects based on natural language instructions and answer spatial questions about scene layouts without linguistic interference.

## Datasets

- **ScanRefer** — total ?; splits: test (-1)
- **Multi3DRef** — total ?; splits: test (-1)
- **SQA3D** — total ?; splits: test (-1)

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Standard exact-match accuracy: the percentage of instances where the model's predicted object identifier or answer exactly matches the ground truth reference. The paper collectively refers to this as 'metrics' across VG and VQA tasks.

## Input / output format

**Input**: 3D scene data (point clouds or RGB-D scans) with object coordinates, paired with natural language instructions (for visual grounding) or situated questions (for VQA).

**Output**: Grounded object identifiers or bounding boxes (for VG) and natural language text answers (for VQA).

## Scoring recipe

```python
def calculate_accuracy(predictions, gold):
    correct = 0
    for pred, gt in zip(predictions, gold):
        if pred == gt:  # Exact match for VG object ID or VQA answer
            correct += 1
    return correct / len(gold)
```

## Common pitfalls

- Axis-wise coordinate encoding causes 'false nearby' attention when coordinate differences are small on a single axis, disrupting spatial reasoning.
- Interference between spatial positional encoding and language RoPE can degrade linguistic capabilities if not properly isolated (e.g., via gated attention).
- Raw (x,y,z) coordinates added directly to features prevent the model from learning relative positions during attention.

## Evidence (verbatim from paper)

> The results in Table 1 demonstrate that our method outperforms baselines across all metrics, particularly on 3D VG tasks that require higher spatial reasoning abilities.

## Citation

```bibtex
@misc{zhou2026scalable,
  title={Scalable Object Relation Encoding for Better 3D Spatial Reasoning in Large Language Models},
  author={Zhou et al. (2026)},
  year={2026},
  note={arXiv:2603.24721}
}
```

- arXiv: 2603.24721
