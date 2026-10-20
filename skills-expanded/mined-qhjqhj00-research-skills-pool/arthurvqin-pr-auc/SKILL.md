---
name: arthurvqin-pr-auc
description: Compute arthurvqin/pr_auc via the HuggingFace `evaluate` library. Use when the user has predictions + references and wants the canonical implementation of arthurvqin/pr_auc.
metadata:
  skill_kind: metric
  source_lib: huggingface-evaluate
  hf_module: arthurvqin/pr_auc
  source: library_introspection
---

# arthurvqin-pr-auc

> Metric `arthurvqin/pr_auc` from the HuggingFace `evaluate` library.

## When to invoke

User asks to compute `arthurvqin/pr_auc` or wants HF evaluate's canonical version.

## Recipe

```python
import evaluate
metric = evaluate.load("arthurvqin/pr_auc")
result = metric.compute(predictions=preds, references=refs)
print(result)
```

## Don'ts

- Don't assume your in-house `arthurvqin/pr_auc` matches HF — version conventions vary.
- Many evaluate metrics have task-specific arguments (`average=`, `lang=`, `model_type=`); read the metric card before reporting numbers.
