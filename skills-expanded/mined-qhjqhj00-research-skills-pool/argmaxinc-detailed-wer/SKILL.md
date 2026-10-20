---
name: argmaxinc-detailed-wer
description: Compute argmaxinc/detailed-wer via the HuggingFace `evaluate` library. Use when the user has predictions + references and wants the canonical implementation of argmaxinc/detailed-wer.
metadata:
  skill_kind: metric
  source_lib: huggingface-evaluate
  hf_module: argmaxinc/detailed-wer
  source: library_introspection
---

# argmaxinc-detailed-wer

> Metric `argmaxinc/detailed-wer` from the HuggingFace `evaluate` library.

## When to invoke

User asks to compute `argmaxinc/detailed-wer` or wants HF evaluate's canonical version.

## Recipe

```python
import evaluate
metric = evaluate.load("argmaxinc/detailed-wer")
result = metric.compute(predictions=preds, references=refs)
print(result)
```

## Don'ts

- Don't assume your in-house `argmaxinc/detailed-wer` matches HF — version conventions vary.
- Many evaluate metrics have task-specific arguments (`average=`, `lang=`, `model_type=`); read the metric card before reporting numbers.
