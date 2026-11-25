---
name: auto-split-eval
description: Evaluates the latency, accuracy, and model size of a collaborative edge-cloud DNN splitting framework (Auto-Split) compared to baselines like QDMP and Neurosurgeon across image classification and object detection tasks. Use when the user wants to benchmark on ImageNet, COCO 2017, or asks about evaluating this task. Reports End-to-end latency (normalized).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2108.13041
  bibtex_key: banitalebi2021autosplit
  confidence: high
---

# auto-split-eval

> Auto-Split: A General Framework of Collaborative Edge-Cloud AI — Amin Banitalebi-Dehkordi et al. (2021) (arXiv:2108.13041, 2021)

## What this evaluates

Evaluates the latency, accuracy, and model size of a collaborative edge-cloud DNN splitting framework (Auto-Split) compared to baselines like QDMP and Neurosurgeon across image classification and object detection tasks.

## Datasets

- **ImageNet** — total ?; splits: val (-1)
- **COCO 2017** — total ?; splits: val (-1)

## Metrics

- `End-to-end latency (normalized)` **(primary)** — range: percent
  - Measured via cycle-accurate SCALE-SIM simulator for Eyeriss (edge) and TPU (cloud). Normalized to the Cloud-Only baseline latency. Lower is better.
- `Top-1 ImageNet accuracy` — range: percent
  - Standard top-1 classification accuracy on ImageNet.
- `mAP (COCO 2017)` — range: percent
  - Mean Average Precision with IoU threshold 0.50:0.95 on COCO 2017 for YOLO-based detection models.
- `Edge DNN size (MB)` — range: other
  - Model footprint in megabytes stored on the edge device after partitioning and quantization.

## Input / output format

**Input**: DNN architecture (e.g., ResNet-50, YOLOv3), hardware constraints (on-chip/off-chip memory, bandwidth), and user-specified error threshold for allowable accuracy drop.

**Output**: Optimal split index, quantization bit-widths for weights/activations/transmission, and deployment configuration (Cloud-Only, Edge-Only, or SPLIT).

## Scoring recipe

```python
def evaluate(model, dataset, constraints, threshold):
    # Simulate latency using SCALE-SIM for edge (Eyeriss) and cloud (TPU)
    edge_lat = simulate(model.edge_part, constraints.edge)
    cloud_lat = simulate(model.cloud_part, constraints.cloud)
    total_lat = edge_lat + cloud_lat + transmission_latency
    latency_ratio = total_lat / simulate(model, constraints.cloud)
    
    # Compute accuracy on dataset
    acc = run_inference(model, dataset)
    acc_drop = (cloud_acc - acc) / cloud_acc
    
    # Calculate edge model size
    size_mb = calculate_size(model.edge_part, bit_widths)
    
    return latency_ratio, acc, size_mb
```

## Common pitfalls

- Tracking MACs or GFLOPs does not directly correspond to measured latency due to data movement bottlenecks in hardware.
- Uniform quantization (e.g., U8) can cause significant accuracy drops (10-50% mAP) in object detection tasks compared to classification.
- Baselines like QDMP may require saving the entire model on the edge device, which is often infeasible; the paper defines QDMPE to only save the edge part.

## Evidence (verbatim from paper)

> Previous studies have shown that tracking multiply accumulate operations (MACs) or GFLOPs does not directly correspond to measuring latency. We measure edge and cloud device latency on a cycle-accurate simulator based on SCALE-SIM... The right axis shows top-1 ImageNet accuracy for classification benchmarks and mAP (IoU=0.50:0.95) from COCO 2017 benchmark for YOLO-based detection models.

## Citation

```bibtex
@misc{banitalebi2021autosplit,
  title={Auto-Split: A General Framework of Collaborative Edge-Cloud AI},
  author={Amin Banitalebi-Dehkordi et al. (2021)},
  year={2021},
  note={arXiv:2108.13041}
}
```

- arXiv: 2108.13041
