---
name: aiml-tuda-isomorphicperturbationtesting
description: Compute AIML-TUDA/IsomorphicPerturbationTesting via the HuggingFace `evaluate` library. Use when the user has predictions + references and wants the canonical implementation of AIML-TUDA/IsomorphicPerturbationTesting.
metadata:
  skill_kind: metric
  source_lib: huggingface-evaluate
  hf_module: AIML-TUDA/IsomorphicPerturbationTesting
  source: library_introspection
---

# aiml-tuda-isomorphicperturbationtesting

> Metric `AIML-TUDA/IsomorphicPerturbationTesting` from the HuggingFace `evaluate` library.

## When to invoke

User asks to compute `AIML-TUDA/IsomorphicPerturbationTesting` or wants HF evaluate's canonical version.

## Recipe

```python
import evaluate
metric = evaluate.load("AIML-TUDA/IsomorphicPerturbationTesting")
result = metric.compute(predictions=preds, references=refs)
print(result)
```

## Don'ts

- Don't assume your in-house `AIML-TUDA/IsomorphicPerturbationTesting` matches HF — version conventions vary.
- Many evaluate metrics have task-specific arguments (`average=`, `lang=`, `model_type=`); read the metric card before reporting numbers.
