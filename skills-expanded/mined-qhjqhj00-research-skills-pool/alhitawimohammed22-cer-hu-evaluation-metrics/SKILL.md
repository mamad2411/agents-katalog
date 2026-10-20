---
name: alhitawimohammed22-cer-hu-evaluation-metrics
description: Compute AlhitawiMohammed22/CER_Hu-Evaluation-Metrics via the HuggingFace `evaluate` library. Use when the user has predictions + references and wants the canonical implementation of AlhitawiMohammed22/CER_Hu-Evaluation-Metrics.
metadata:
  skill_kind: metric
  source_lib: huggingface-evaluate
  hf_module: AlhitawiMohammed22/CER_Hu-Evaluation-Metrics
  source: library_introspection
---

# alhitawimohammed22-cer-hu-evaluation-metrics

> Metric `AlhitawiMohammed22/CER_Hu-Evaluation-Metrics` from the HuggingFace `evaluate` library.

## When to invoke

User asks to compute `AlhitawiMohammed22/CER_Hu-Evaluation-Metrics` or wants HF evaluate's canonical version.

## Recipe

```python
import evaluate
metric = evaluate.load("AlhitawiMohammed22/CER_Hu-Evaluation-Metrics")
result = metric.compute(predictions=preds, references=refs)
print(result)
```

## Don'ts

- Don't assume your in-house `AlhitawiMohammed22/CER_Hu-Evaluation-Metrics` matches HF — version conventions vary.
- Many evaluate metrics have task-specific arguments (`average=`, `lang=`, `model_type=`); read the metric card before reporting numbers.
