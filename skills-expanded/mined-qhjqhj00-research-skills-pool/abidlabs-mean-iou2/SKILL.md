---
name: abidlabs-mean-iou2
description: Compute abidlabs/mean_iou2 via the HuggingFace `evaluate` library. Use when the user has predictions + references and wants the canonical implementation of abidlabs/mean_iou2.
metadata:
  skill_kind: metric
  source_lib: huggingface-evaluate
  hf_module: abidlabs/mean_iou2
  source: library_introspection
---

# abidlabs-mean-iou2

> Metric `abidlabs/mean_iou2` from the HuggingFace `evaluate` library.

## When to invoke

User asks to compute `abidlabs/mean_iou2` or wants HF evaluate's canonical version.

## Recipe

```python
import evaluate
metric = evaluate.load("abidlabs/mean_iou2")
result = metric.compute(predictions=preds, references=refs)
print(result)
```

## Don'ts

- Don't assume your in-house `abidlabs/mean_iou2` matches HF — version conventions vary.
- Many evaluate metrics have task-specific arguments (`average=`, `lang=`, `model_type=`); read the metric card before reporting numbers.
