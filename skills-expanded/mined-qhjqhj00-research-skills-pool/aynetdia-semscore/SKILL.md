---
name: aynetdia-semscore
description: Compute aynetdia/semscore via the HuggingFace `evaluate` library. Use when the user has predictions + references and wants the canonical implementation of aynetdia/semscore.
metadata:
  skill_kind: metric
  source_lib: huggingface-evaluate
  hf_module: aynetdia/semscore
  source: library_introspection
---

# aynetdia-semscore

> Metric `aynetdia/semscore` from the HuggingFace `evaluate` library.

## When to invoke

User asks to compute `aynetdia/semscore` or wants HF evaluate's canonical version.

## Recipe

```python
import evaluate
metric = evaluate.load("aynetdia/semscore")
result = metric.compute(predictions=preds, references=refs)
print(result)
```

## Don'ts

- Don't assume your in-house `aynetdia/semscore` matches HF — version conventions vary.
- Many evaluate metrics have task-specific arguments (`average=`, `lang=`, `model_type=`); read the metric card before reporting numbers.
