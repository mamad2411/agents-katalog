---
name: aye10032-loss-metric
description: Compute Aye10032/loss_metric via the HuggingFace `evaluate` library. Use when the user has predictions + references and wants the canonical implementation of Aye10032/loss_metric.
metadata:
  skill_kind: metric
  source_lib: huggingface-evaluate
  hf_module: Aye10032/loss_metric
  source: library_introspection
---

# aye10032-loss-metric

> Metric `Aye10032/loss_metric` from the HuggingFace `evaluate` library.

## When to invoke

User asks to compute `Aye10032/loss_metric` or wants HF evaluate's canonical version.

## Recipe

```python
import evaluate
metric = evaluate.load("Aye10032/loss_metric")
result = metric.compute(predictions=preds, references=refs)
print(result)
```

## Don'ts

- Don't assume your in-house `Aye10032/loss_metric` matches HF — version conventions vary.
- Many evaluate metrics have task-specific arguments (`average=`, `lang=`, `model_type=`); read the metric card before reporting numbers.
