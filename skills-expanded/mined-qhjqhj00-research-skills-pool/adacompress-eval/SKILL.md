---
name: adacompress-eval
description: Evaluates a reinforcement learning-based adaptive JPEG compression framework for cloud computer vision services. It measures how effectively the system balances image file size reduction against the accuracy degradation of downstream black-box vision models, while accounting for end-to-end latency overhead compared to standard JPEG baselines. Use when the user wants to benchmark on ImageNet, DNIM, or asks about evaluating this task. Reports relative top-5 accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1909.08148
  bibtex_key: li2019adacompress
  confidence: high
---

# adacompress-eval

> AdaCompress: Adaptive Compression for Online Computer Vision Services — Li et al. (2019) (arXiv:1909.08148, 2019)

## What this evaluates

Evaluates a reinforcement learning-based adaptive JPEG compression framework for cloud computer vision services. It measures how effectively the system balances image file size reduction against the accuracy degradation of downstream black-box vision models, while accounting for end-to-end latency overhead compared to standard JPEG baselines.

## Datasets

- **ImageNet** — total ?; splits: test (-1)
- **DNIM** — total ?; splits: test (-1)

## Metrics

- `relative top-5 accuracy` **(primary)** — range: [0, 1]
  - Calculated by comparing the cloud service's top-5 prediction on the compressed image against the prediction on a reference uncompressed image. True labels are unavailable, so the reference model's output serves as the ground truth proxy.
- `compression rate` — range: ratio
  - Ratio of the compressed image file size to the original uncompressed image size, or compared against a standard JPEG quality 75 baseline.
- `end-to-end latency` — range: milliseconds
  - Sum of the DRL agent's inference time and the network transmission time, simulated using a fixed broadband upload speed of 27.64 Mbps.

## Input / output format

**Input**: Raw images (daytime scenes from ImageNet, nighttime scenes from DNIM) passed to a Deep Q-Network agent to determine JPEG compression quality, then transmitted to cloud CV APIs (Amazon Rekognition, Face++, Baidu Vision).

**Output**: Compressed JPEG image sent to the cloud service; the cloud service returns object detection/classification predictions. The agent outputs a discrete compression quality level.

## Scoring recipe

```python
def compute_metrics(original_img, compressed_img, ref_img, cloud_service, bandwidth):
    ref_pred = cloud_service.predict(ref_img)
    comp_pred = cloud_service.predict(compressed_img)
    relative_accuracy = 1.0 if ref_pred in comp_pred.top5 else 0.0
    size_ratio = len(compressed_img_bytes) / len(original_img_bytes)
    overhead_ratio = len(compressed_img_bytes) / len(baseline_q75_bytes)
    transmission_latency = len(compressed_img_bytes) / bandwidth
    total_latency = drl_inference_time + transmission_latency
    return relative_accuracy, size_ratio, overhead_ratio, total_latency
```

## Common pitfalls

- Assuming ground-truth labels are used for accuracy evaluation; the paper explicitly uses the reference model's output as a proxy for ground truth.
- Ignoring the DRL agent's inference latency when calculating end-to-end latency; the paper adds ~2.09 ms to the transmission time.
- Comparing against adaptive baselines; the benchmark is strictly standard JPEG at quality 75.

## Evidence (verbatim from paper)

> In our experiments, we measure the compressed and original image's file size to obtain the compression rate Δs. Since we don't have the real ground truth label of an image, we use the output from a reference image y_ref as the ground truth label, and calculate the relative top-5 accuracy A as the accuracy metric, the formula of A is presented in Sec. 2.1.

## Citation

```bibtex
@misc{li2019adacompress,
  title={AdaCompress: Adaptive Compression for Online Computer Vision Services},
  author={Li et al. (2019)},
  year={2019},
  note={arXiv:1909.08148}
}
```

- arXiv: 1909.08148
