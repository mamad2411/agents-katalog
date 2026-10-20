---
name: axonn-scaling-eval
description: Evaluates the scaling efficiency and hardware utilization of asynchronous deep learning frameworks (AxoNN, Megatron-LM, DeepSpeed) on large-scale transformer models. It measures how well frameworks overlap communication and computation across varying GPU counts and model sizes while training on a fixed text corpus. Use when the user wants to benchmark on wikitext-103, or asks about evaluating this task. Reports expected_training_time.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2110.13005
  bibtex_key: singh2021axonn
  confidence: high
---

# axonn-scaling-eval

> AxoNN: An asynchronous, message-driven parallel framework for extreme-scale deep learning — Singh et al. (2021) (arXiv:2110.13005, 2021)

## What this evaluates

Evaluates the scaling efficiency and hardware utilization of asynchronous deep learning frameworks (AxoNN, Megatron-LM, DeepSpeed) on large-scale transformer models. It measures how well frameworks overlap communication and computation across varying GPU counts and model sizes while training on a fixed text corpus.

## Datasets

- **wikitext-103** — total ?; splits: train (-1)

## Metrics

- `expected_training_time` **(primary)** — range: other
  - Estimated time to train on 300 billion tokens, calculated as 3e11 * t / (b * s), where t is the average batch time (averaged over the last 10 of 11 batches), b is batch size, and s is sequence length.
- `percentage_of_peak_throughput` — range: percent
  - Percentage of theoretical peak half-precision throughput achieved. Computed as (96 * b * s * l * h^2 / t) * (1 + s/(6h) + V/(16lh)) / (125 Tflop/s * num_gpus), where l is layers, h is hidden size, and V is vocabulary size.

## Input / output format

**Input**: Transformer model architecture parameters (layers, hidden size, attention heads), dataset tokens (wikitext-103), and hyperparameters (batch size, sequence length, optimizer settings).

**Output**: Training metrics: average batch time over 10 batches, estimated training time for 300B tokens, and percentage of peak half-precision throughput.

## Scoring recipe

```python
# t = average of last 10 batch times from 11 total batches
# b, s, l, h, V, num_gpus = hyperparameters
estimated_training_time = 3e11 * t / (b * s)
flop_per_batch = (96 * b * s * l * h**2) * (1 + s/(6*h) + V/(16*l*h))
flop_per_sec = flop_per_batch / t
peak_throughput = 125e12 * num_gpus  # 125 Tflop/s per GPU
percentage_peak = (flop_per_sec / peak_throughput) * 100
return estimated_training_time, percentage_peak
```

## Common pitfalls

- Varying both batch size and model parameters simultaneously, which artificially inflates performance numbers.
- Using the average of all 11 batch times instead of the last 10 to calculate t, which would skew metrics due to initialization overhead.
- Forgetting to multiply the per-GPU peak throughput (125 Tflop/s) by the total number of GPUs when calculating percentage_of_peak_throughput.

## Evidence (verbatim from paper)

> We use two metrics in our experiments - namely expected training time and the percentage of peak half precision throughput. Both of these are metrics derived from the average batch time, which we calculate by training for eleven batches and averaging the timings of the last ten. In accordance with the training regime employed for GPT-3, we define the expected training time as the total time it would take to train a transformer on a total of 300 billion tokens.

## Citation

```bibtex
@misc{singh2021axonn,
  title={AxoNN: An asynchronous, message-driven parallel framework for extreme-scale deep learning},
  author={Singh et al. (2021)},
  year={2021},
  note={arXiv:2110.13005}
}
```

- arXiv: 2110.13005
