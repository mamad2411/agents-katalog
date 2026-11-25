---
name: 3doc-bench-eval
description: This benchmark evaluates a model's ability to generate text-to-image outputs that strictly adhere to 3D layout constraints, handle complex inter-object occlusions, and maintain correct object orientations and visibility orders. It probes depth-consistent scene composition, attribute binding to specific objects, and overall image fidelity under varying camera viewpoints. Use when the user wants to benchmark on 3DOc-Bench, or asks about evaluating this task. Reports depth ordering.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2602.23359
  bibtex_key: agrawal2026seethrough3d
  confidence: high
---

# 3doc-bench-eval

> SeeThrough3D: Occlusion Aware 3D Control in Text-to-Image Generation — Agrawal et al. (2026) (arXiv:2602.23359, 2026)

## What this evaluates

This benchmark evaluates a model's ability to generate text-to-image outputs that strictly adhere to 3D layout constraints, handle complex inter-object occlusions, and maintain correct object orientations and visibility orders. It probes depth-consistent scene composition, attribute binding to specific objects, and overall image fidelity under varying camera viewpoints.

## Datasets

- **3DOc-Bench** — total 500; splits: test (500)

## Metrics

- `depth ordering` **(primary)** — range: [0, 1]
  - Accuracy of relative depth ordering for each object pair. Assigns 1 if the estimated depth order matches the ground truth, 0 otherwise. Aggregated over all valid object pairs.
- `CLIP objectness score` — range: [0, 100]
  - CLIP similarity score between extracted object masks (from 2D layouts + SAM) and their corresponding textual descriptions. Aggregated across all objects in the scene.
- `angular error` — range: degrees
  - Mean absolute error (in degrees) between estimated object orientations (via OrientAnything) and ground-truth orientations for each object.
- `CLIP image-text similarity` — range: [0, 1]
  - CLIP cosine similarity between the generated image embedding and the input text prompt embedding.
- `KID` — range: [0, inf)
  - Kernel Inception Distance measuring the distributional difference between generated images and real/reference images to assess image fidelity.

## Input / output format

**Input**: Text prompt, 3D bounding box layout (OSCR representation with transparency and color-coded faces), and camera viewpoint parameters.

**Output**: A single RGB image generated according to the prompt and 3D layout constraints.

## Scoring recipe

```python
def evaluate(pred_img, gold_layout, gold_prompt, gold_gt_imgs):
    masks = extract_masks(pred_img, gold_layout)
    valid_masks = [m for m in masks if clip_similarity(m, gold_prompt) > threshold]
    
    correct = sum(1 for p in pairs if depth_order(p) == gold.depth_order(p))
    depth_acc = correct / len(pairs)
    
    obj_scores = [clip_similarity(m, text) for m, text in zip(valid_masks, gold_texts)]
    ang_err = mean(abs(orient_est(valid_masks) - gold_orient))
    
    text_align = clip_similarity(pred_img, gold_prompt)
    kid = compute_kid(pred_img, gold_gt_imgs)
    return depth_acc, mean(obj_scores), ang_err, text_align, kid
```

## Common pitfalls

- Depth ordering metric only applies to objects actually present in the generated image; missing objects are filtered out using the CLIP objectness score, which can artificially inflate scores if the threshold is too high.
- Angular error is computed exclusively on filtered object segments using OrientAnything, not on the full image or background regions.
- KID values in the paper are scaled by 10^-3 for readability; raw KID scores are approximately 1000x larger.

## Evidence (verbatim from paper)

> We measure the models’ performance for layout adherence, text-to-image alignment, and image quality. For text-to-image alignment, we use CLIP image-text similarity, and for image quality, we use Kernel Inception Distance (KID). Evaluating 3D layout adherence using a single metric is challenging, as the generated scene may not conform to the metric depth specified by the 3D bounding-box layout. To this end, we compute three metrics that in unison effectively evaluate 3D layout adherence. Specifically, we compute 2D bounding box adherence, relative visibility order and 3D orientation consistency.

## Citation

```bibtex
@misc{agrawal2026seethrough3d,
  title={SeeThrough3D: Occlusion Aware 3D Control in Text-to-Image Generation},
  author={Agrawal et al. (2026)},
  year={2026},
  note={arXiv:2602.23359}
}
```

- arXiv: 2602.23359
