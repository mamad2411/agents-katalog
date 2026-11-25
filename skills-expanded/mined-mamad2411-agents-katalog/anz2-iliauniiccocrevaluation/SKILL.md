---
name: anz2-iliauniiccocrevaluation
description: Compute anz2/iliauniiccocrevaluation via the HuggingFace `evaluate` library. Use when the user has predictions + references and wants the canonical implementation of anz2/iliauniiccocrevaluation.
metadata:
  skill_kind: metric
  source_lib: huggingface-evaluate
  hf_module: anz2/iliauniiccocrevaluation
  source: library_introspection
---

# anz2-iliauniiccocrevaluation

> Metric `anz2/iliauniiccocrevaluation` from the HuggingFace `evaluate` library.

## When to invoke

User asks to compute `anz2/iliauniiccocrevaluation` or wants HF evaluate's canonical version.

## Recipe

```python
import evaluate
metric = evaluate.load("anz2/iliauniiccocrevaluation")
result = metric.compute(predictions=preds, references=refs)
print(result)
```

## Don'ts

- Don't assume your in-house `anz2/iliauniiccocrevaluation` matches HF — version conventions vary.
- Many evaluate metrics have task-specific arguments (`average=`, `lang=`, `model_type=`); read the metric card before reporting numbers.
