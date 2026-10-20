---
name: ai-accelerator-training-eval
description: Evaluates the computational performance and energy efficiency of various AI accelerators (CPUs, GPUs, TPUs) across standard deep learning workloads, including CNNs and NLP models. It measures how hardware architecture, numerical precision, and batch size impact training throughput and power consumption. Use when the user wants to benchmark on Standard DNN Workloads (ResNet50, Inception v3, Vgg16, LSTM, Deep Speech 2, Transformer), or asks about evaluating this task. Reports throughput.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1909.06842
  bibtex_key: wang2019benchmarking
  confidence: high
---

# ai-accelerator-training-eval

> Benchmarking the Performance and Energy Efficiency of AI Accelerators for AI Training — Wang et al. (2019) (arXiv:1909.06842, 2019)

## What this evaluates

Evaluates the computational performance and energy efficiency of various AI accelerators (CPUs, GPUs, TPUs) across standard deep learning workloads, including CNNs and NLP models. It measures how hardware architecture, numerical precision, and batch size impact training throughput and power consumption.

## Datasets

- **Standard DNN Workloads (ResNet50, Inception v3, Vgg16, LSTM, Deep Speech 2, Transformer)** — total ?; splits: test (-1)

## Metrics

- `throughput` **(primary)** — range: other
  - End-to-end training performance measured as throughput (samples/sec or images/sec), calculated by dividing the total processed samples by the wall-clock execution time. Also reports operator-level TFLOPS and hardware utilization (%).
- `TFLOPS` — range: other
  - Tera floating-point operations per second, computed by dividing the total FLOPs of the operator or model by the execution time.
- `energy_consumption` — range: other
  - Total energy used during end-to-end training, calculated as the integral of power draw over the training duration (typically measured in Joules).

## Input / output format

**Input**: DNN architecture configuration, hardware accelerator type, numerical precision (FP32/Mixed), and mini-batch size.

**Output**: Throughput/TFLOPS values, hardware utilization percentages, and total energy consumption (Joules) for end-to-end training runs.

## Scoring recipe

```python
def evaluate_accelerator(model, hw, batch_size, steps):
    start = time()
    run_training(model, hw, batch_size, steps)
    duration = time() - start
    energy = measure_power(hw) * duration
    throughput = (batch_size * steps) / duration
    tflops = compute_model_flops(model) / duration
    utilization = tflops / peak_tflops(hw)
    return throughput, tflops, energy, utilization
```

## Common pitfalls

- Hardware performance is highly sensitive to software stack optimizations (e.g., CUDA vs ROCm, Tensor Core utilization), which vary significantly across vendors and can skew cross-platform comparisons.
- Batch size selection critically impacts throughput and energy efficiency; suboptimal batch sizes can mask hardware capabilities, cause memory bottlenecks, or lead to misleading energy-per-sample metrics.
- Energy measurements must account for full system power draw, not just accelerator TDP, to reflect real-world efficiency and avoid underestimating cooling/power overhead.

## Evidence (verbatim from paper)

> We evaluate the AI Accelerators on the two major operators (i.e., matrix multiplication and 2D convolution) that are computation-intensive and widely used in DNN training. Computation-intensive operations call high-throughput kernels for calculating to achieve the highest FLOPS (throughput), as can be seen from Fig. 6.

## Citation

```bibtex
@misc{wang2019benchmarking,
  title={Benchmarking the Performance and Energy Efficiency of AI Accelerators for AI Training},
  author={Wang et al. (2019)},
  year={2019},
  note={arXiv:1909.06842}
}
```

- arXiv: 1909.06842
