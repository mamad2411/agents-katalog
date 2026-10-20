---
name: ahnyeonchan-alignment-and-uniformity
description: Compute ahnyeonchan/Alignment-and-Uniformity via the HuggingFace `evaluate` library. Use when the user has predictions + references and wants the canonical implementation of ahnyeonchan/Alignment-and-Uniformity.
metadata:
  skill_kind: metric
  source_lib: huggingface-evaluate
  hf_module: ahnyeonchan/Alignment-and-Uniformity
  source: library_introspection
---

# ahnyeonchan-alignment-and-uniformity

> Metric `ahnyeonchan/Alignment-and-Uniformity` from the HuggingFace `evaluate` library.

## When to invoke

User asks to compute `ahnyeonchan/Alignment-and-Uniformity` or wants HF evaluate's canonical version.

## Recipe

```python
import evaluate
metric = evaluate.load("ahnyeonchan/Alignment-and-Uniformity")
result = metric.compute(predictions=preds, references=refs)
print(result)
```

## Don'ts

- Don't assume your in-house `ahnyeonchan/Alignment-and-Uniformity` matches HF — version conventions vary.
- Many evaluate metrics have task-specific arguments (`average=`, `lang=`, `model_type=`); read the metric card before reporting numbers.
