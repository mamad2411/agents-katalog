---
name: arm-cortex-ai-benchmark-eval
description: This benchmark evaluates how AI model size, pruning, and quantization affect deployment on bare-metal ARM Cortex-M0+/M4/M7 processors. It specifically probes the trade-offs between energy efficiency, inference latency, and model accuracy across different hardware architectures and application duty cycles. Use when the user wants to benchmark on Embedded AI Use Cases (e.g., Optical Digit Recognition, Visual Wake Words), or asks about evaluating this task. Reports inference cycle energy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2602.17508
  bibtex_key: jain2026pareto
  confidence: high
---

# arm-cortex-ai-benchmark-eval

> Pareto Optimal Benchmarking of AI Models on ARM Cortex Processors for Sustainable Embedded Systems — Jain et al. (2026) (arXiv:2602.17508, 2026)

## What this evaluates

This benchmark evaluates how AI model size, pruning, and quantization affect deployment on bare-metal ARM Cortex-M0+/M4/M7 processors. It specifically probes the trade-offs between energy efficiency, inference latency, and model accuracy across different hardware architectures and application duty cycles.

## Datasets

- **Embedded AI Use Cases (e.g., Optical Digit Recognition, Visual Wake Words)** — total ?; splits: (unstated)

## Metrics

- `inference cycle energy` **(primary)** — range: other
  - Total energy consumed per inference cycle, calculated as the integral of current over the active inference period plus the idle period, multiplied by the constant supply voltage (3.3V).
- `inference time` — range: other
  - Duration of the active model inference phase, measured in real-time on the target processor.
- `accuracy` — range: percent
  - Standard classification or prediction accuracy of the AI model on its target task dataset.

## Input / output format

**Input**: Pre-trained AI models (pruned and/or 8-bit quantized) deployed on bare-metal ARM Cortex-M0+/M4/M7 processors, along with task-specific input data for inference.

**Output**: Per inference cycle: measured current draw, inference time, total cycle energy, and model accuracy on the evaluation set.

## Scoring recipe

```python
def compute_accuracy(predictions, gold_labels):
    correct = sum(p == g for p, g in zip(predictions, gold_labels))
    return correct / len(gold_labels)
# Note: inference cycle energy and inference time are measured directly via hardware power analyzers/oscilloscopes, not computed from predictions.
```

## Common pitfalls

- Ignoring idle current when calculating total energy, which drastically underestimates power for infrequent inference tasks.
- Assuming RAM/ROM usage correlates with energy consumption; the paper explicitly states they are poor predictors and only serve as deployment constraints.
- Comparing processors without accounting for duty cycle (cycle time), as M4 and M7 dominate in different temporal regimes.

## Evidence (verbatim from paper)

> Figure[8] presents a Pareto front analysis comparing inference cycle energy and accuracy across varying cycle times (\qty0.5, \qty2.5, and \qty5.0) for the M4 and M7 processors.

## Citation

```bibtex
@misc{jain2026pareto,
  title={Pareto Optimal Benchmarking of AI Models on ARM Cortex Processors for Sustainable Embedded Systems},
  author={Jain et al. (2026)},
  year={2026},
  note={arXiv:2602.17508}
}
```

- arXiv: 2602.17508
