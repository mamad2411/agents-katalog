---
name: albertgong1-my-metric
description: Compute albertgong1/my_metric via the HuggingFace `evaluate` library. Use when the user has predictions + references and wants the canonical implementation of albertgong1/my_metric.
metadata:
  skill_kind: metric
  source_lib: huggingface-evaluate
  hf_module: albertgong1/my_metric
  source: library_introspection
---

# albertgong1-my-metric

> Metric `albertgong1/my_metric` from the HuggingFace `evaluate` library.

## When to invoke

User asks to compute `albertgong1/my_metric` or wants HF evaluate's canonical version.

## Recipe

```python
import evaluate
metric = evaluate.load("albertgong1/my_metric")
result = metric.compute(predictions=preds, references=refs)
print(result)
```

## Don'ts

- Don't assume your in-house `albertgong1/my_metric` matches HF — version conventions vary.
- Many evaluate metrics have task-specific arguments (`average=`, `lang=`, `model_type=`); read the metric card before reporting numbers.
