---
name: abidlabs-mean-iou
description: Compute abidlabs/mean_iou via the HuggingFace `evaluate` library. Use when the user has predictions + references and wants the canonical implementation of abidlabs/mean_iou.
metadata:
  skill_kind: metric
  source_lib: huggingface-evaluate
  hf_module: abidlabs/mean_iou
  source: library_introspection
---

# abidlabs-mean-iou

> Metric `abidlabs/mean_iou` from the HuggingFace `evaluate` library.

## When to invoke

User asks to compute `abidlabs/mean_iou` or wants HF evaluate's canonical version.

## Recipe

```python
import evaluate
metric = evaluate.load("abidlabs/mean_iou")
result = metric.compute(predictions=preds, references=refs)
print(result)
```

## Don'ts

- Don't assume your in-house `abidlabs/mean_iou` matches HF — version conventions vary.
- Many evaluate metrics have task-specific arguments (`average=`, `lang=`, `model_type=`); read the metric card before reporting numbers.
