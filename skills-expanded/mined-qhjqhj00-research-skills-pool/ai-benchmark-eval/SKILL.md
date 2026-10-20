---
name: ai-benchmark-eval
description: Evaluates the inference performance of mobile AI accelerators across major SoC vendors by running a standardized suite of deep learning models via TensorFlow Lite and NNAPI. It measures latency and accuracy to compare on-device AI capabilities against desktop hardware and track hardware evolution. Use when the user wants to benchmark on AI Benchmark 3.0, or asks about evaluating this task. Reports AI-Score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1910.06663
  bibtex_key: ignatov2019aibenchmark
  confidence: high
---

# ai-benchmark-eval

> AI Benchmark: All About Deep Learning on Smartphones in 2019 — Ignatov et al. (2019) (arXiv:1910.06663, 2019)

## What this evaluates

Evaluates the inference performance of mobile AI accelerators across major SoC vendors by running a standardized suite of deep learning models via TensorFlow Lite and NNAPI. It measures latency and accuracy to compare on-device AI capabilities against desktop hardware and track hardware evolution.

## Datasets

- **AI Benchmark 3.0** — total 20000; splits: test (-1)

## Metrics

- `AI-Score` **(primary)** — range: points
  - A composite score aggregating normalized inference latency and accuracy across multiple deep learning tasks (classification, detection, segmentation, etc.) for both floating-point and quantized models. Higher values indicate better overall performance.

## Input / output format

**Input**: Deep learning models (e.g., image classification, object detection, segmentation) executed on mobile devices via TensorFlow Lite or NNAPI.

**Output**: Per model/task: inference latency in milliseconds and accuracy/error rate. Aggregated into a composite AI-Score.

## Scoring recipe

```python
# Pseudo-code for AI-Score calculation
score = 0
for task in tasks:
    latency = get_latency_ms(task)
    accuracy = get_accuracy(task)
    # Normalize latency (lower is better) and accuracy (higher is better)
    norm_lat = 1 / (1 + latency)
    norm_acc = accuracy
    score += weight_lat * norm_lat + weight_acc * norm_acc
return score
```

## Common pitfalls

- Latency measurements are highly sensitive to thermal throttling, background processes, and Android OS version, requiring controlled testing environments.
- Accuracy metrics differ significantly between floating-point and quantized models, so results must be reported separately to avoid misleading comparisons.
- The benchmark covers a wide range of SoCs and device generations; direct comparisons should account for hardware architecture differences (CPU/GPU/NPU).

## Evidence (verbatim from paper)

> As the performance of mobile AI accelerators has grown significantly in the past year, we decided to add desktop CPUs and GPUs used for training / running deep learning models to the comparison as well. This will help us to understand how far mobile AI silicon has progressed thus far. It also will help developers to estimate the relation between the runtime of their models on smartphones and desktops. In this section, we present quantitative benchmark results obtained from over 20,000 mobile devices tested in the wild (including a number of prototypes) and discuss in detail the performance of all available mobile chipsets providing hardware acceleration for floating-point or quantized models. The results for floating-point and quantized inference obtained on mobile SoCs are presented in tables[2](#S4.T2 "Table 2 ‣ 4.4 AI Benchmark for Desktops ‣ 4 AI Benchmark 3.0 ‣ AI Benchmark: All About Deep Learning on Smartphones in 2019") and[3](#S4.T3 "Table 3 ‣ 4.4 AI Benchmark for Desktops ‣ 4 AI Benchmark 3.0 ‣ AI Benchmark: All About Deep Learning on Smartphones in 2019"), respectively. The detailed performance results for smartphones are shown in table[4](#S5.T4 "Table 4 ‣ 5 Benchmark R

## Citation

```bibtex
@misc{ignatov2019aibenchmark,
  title={AI Benchmark: All About Deep Learning on Smartphones in 2019},
  author={Ignatov et al. (2019)},
  year={2019},
  note={arXiv:1910.06663}
}
```

- arXiv: 1910.06663
