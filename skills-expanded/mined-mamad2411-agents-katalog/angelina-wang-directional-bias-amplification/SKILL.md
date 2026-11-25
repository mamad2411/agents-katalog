---
name: angelina-wang-directional-bias-amplification
description: Compute angelina-wang/directional_bias_amplification via the HuggingFace `evaluate` library. Use when the user has predictions + references and wants the canonical implementation of angelina-wang/directional_bias_amplification.
metadata:
  skill_kind: metric
  source_lib: huggingface-evaluate
  hf_module: angelina-wang/directional_bias_amplification
  source: library_introspection
---

# angelina-wang-directional-bias-amplification

> Metric `angelina-wang/directional_bias_amplification` from the HuggingFace `evaluate` library.

## When to invoke

User asks to compute `angelina-wang/directional_bias_amplification` or wants HF evaluate's canonical version.

## Recipe

```python
import evaluate
metric = evaluate.load("angelina-wang/directional_bias_amplification")
result = metric.compute(predictions=preds, references=refs)
print(result)
```

## Don'ts

- Don't assume your in-house `angelina-wang/directional_bias_amplification` matches HF — version conventions vary.
- Many evaluate metrics have task-specific arguments (`average=`, `lang=`, `model_type=`); read the metric card before reporting numbers.
