---
name: agkphysics-ccc
description: Compute agkphysics/ccc via the HuggingFace `evaluate` library. Use when the user has predictions + references and wants the canonical implementation of agkphysics/ccc.
metadata:
  skill_kind: metric
  source_lib: huggingface-evaluate
  hf_module: agkphysics/ccc
  source: library_introspection
---

# agkphysics-ccc

> Metric `agkphysics/ccc` from the HuggingFace `evaluate` library.

## When to invoke

User asks to compute `agkphysics/ccc` or wants HF evaluate's canonical version.

## Recipe

```python
import evaluate
metric = evaluate.load("agkphysics/ccc")
result = metric.compute(predictions=preds, references=refs)
print(result)
```

## Don'ts

- Don't assume your in-house `agkphysics/ccc` matches HF — version conventions vary.
- Many evaluate metrics have task-specific arguments (`average=`, `lang=`, `model_type=`); read the metric card before reporting numbers.
