---
name: alvinasvk-accents-unplugged-eval
description: Compute alvinasvk/accents_unplugged_eval via the HuggingFace `evaluate` library. Use when the user has predictions + references and wants the canonical implementation of alvinasvk/accents_unplugged_eval.
metadata:
  skill_kind: metric
  source_lib: huggingface-evaluate
  hf_module: alvinasvk/accents_unplugged_eval
  source: library_introspection
---

# alvinasvk-accents-unplugged-eval

> Metric `alvinasvk/accents_unplugged_eval` from the HuggingFace `evaluate` library.

## When to invoke

User asks to compute `alvinasvk/accents_unplugged_eval` or wants HF evaluate's canonical version.

## Recipe

```python
import evaluate
metric = evaluate.load("alvinasvk/accents_unplugged_eval")
result = metric.compute(predictions=preds, references=refs)
print(result)
```

## Don'ts

- Don't assume your in-house `alvinasvk/accents_unplugged_eval` matches HF — version conventions vary.
- Many evaluate metrics have task-specific arguments (`average=`, `lang=`, `model_type=`); read the metric card before reporting numbers.
