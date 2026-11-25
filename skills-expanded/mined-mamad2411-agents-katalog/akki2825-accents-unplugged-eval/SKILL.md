---
name: akki2825-accents-unplugged-eval
description: Compute akki2825/accents_unplugged_eval via the HuggingFace `evaluate` library. Use when the user has predictions + references and wants the canonical implementation of akki2825/accents_unplugged_eval.
metadata:
  skill_kind: metric
  source_lib: huggingface-evaluate
  hf_module: akki2825/accents_unplugged_eval
  source: library_introspection
---

# akki2825-accents-unplugged-eval

> Metric `akki2825/accents_unplugged_eval` from the HuggingFace `evaluate` library.

## When to invoke

User asks to compute `akki2825/accents_unplugged_eval` or wants HF evaluate's canonical version.

## Recipe

```python
import evaluate
metric = evaluate.load("akki2825/accents_unplugged_eval")
result = metric.compute(predictions=preds, references=refs)
print(result)
```

## Don'ts

- Don't assume your in-house `akki2825/accents_unplugged_eval` matches HF — version conventions vary.
- Many evaluate metrics have task-specific arguments (`average=`, `lang=`, `model_type=`); read the metric card before reporting numbers.
