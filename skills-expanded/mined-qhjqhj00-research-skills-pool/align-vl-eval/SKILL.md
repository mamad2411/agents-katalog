---
name: align-vl-eval
description: Evaluates a vision-language model's cross-modal retrieval capabilities (matching images to text and vice versa) and zero-shot image classification performance without task-specific fine-tuning. It also measures transfer learning effectiveness on downstream visual benchmarks via linear probing and full fine-tuning. Use when the user wants to benchmark on Flickr30K, MSCOCO, or asks about evaluating this task. Reports R@10.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2102.05918
  bibtex_key: jia2021align
  confidence: high
---

# align-vl-eval

> Scaling Up Visual and Vision-Language Representation Learning With Noisy Text Supervision — Jia et al. (2021) (arXiv:2102.05918, 2021)

## What this evaluates

Evaluates a vision-language model's cross-modal retrieval capabilities (matching images to text and vice versa) and zero-shot image classification performance without task-specific fine-tuning. It also measures transfer learning effectiveness on downstream visual benchmarks via linear probing and full fine-tuning.

## Datasets

- **Flickr30K** — total 31000; splits: train (30000), test (1000)
- **MSCOCO** — total 115000; splits: train (82000), val (30000), test (5000)

## Metrics

- `R@10` **(primary)** — range: percent
  - Recall at K: the percentage of queries where the ground-truth match appears in the top K ranked results based on cosine similarity scores between image and text embeddings.
- `Top-1 Accuracy` — range: percent
  - The percentage of images correctly classified into the target class among all candidate classes.

## Input / output format

**Input**: An image and a set of candidate text captions (for retrieval) or class name prompts (for zero-shot classification).

**Output**: A ranked list of candidate texts or images sorted by similarity score, or a predicted class label.

## Scoring recipe

```python
def compute_recall_at_k(sim_scores, k, gt_indices):
    # sim_scores: (N, M) similarity matrix, gt_indices: (N,) ground truth indices
    ranks = np.argsort(-sim_scores, axis=1)
    hits = np.any(ranks[:, :k] == gt_indices[:, None], axis=1)
    return np.mean(hits) * 100
```

## Common pitfalls

- Using non-standard train/test splits for Flickr30K or MSCOCO breaks comparability with reported SOTA results.
- Failing to apply prompt ensembling (averaging embeddings of multiple templates like 'A photo of a {classname}') and L2 normalization for zero-shot classification drops accuracy by ~2.9%.
- Confusing intra-modal (image-image, text-text) and inter-modal (image-text) retrieval tasks on the CxC dataset, as the model is optimized for cross-modal matching.

## Evidence (verbatim from paper)

> We evaluate ALIGN on Flickr30K and MSCOCO cross-modal retrieval benchmarks, in both zero-shot and fully fine-tuned settings. ... Table 1 shows that, compared to previous works, ALIGN achieves SOTA results in all metrics of Flickr30K and MSCOCO benchmarks. R@1 R@5 R@10

## Citation

```bibtex
@misc{jia2021align,
  title={Scaling Up Visual and Vision-Language Representation Learning With Noisy Text Supervision},
  author={Jia et al. (2021)},
  year={2021},
  note={arXiv:2102.05918}
}
```

- arXiv: 2102.05918
