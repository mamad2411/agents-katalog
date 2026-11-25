---
name: atbench-eval
description: Evaluates vision-language models on five assistive technology tasks for people with visual impairments: panoptic segmentation, depth estimation, optical character recognition, image captioning, and visual question answering. It probes the model's ability to unify multiple visual understanding and generation tasks within a single parameter set using task-specific prompts. Use when the user wants to benchmark on ADE-150, NYU-V2, OCR (IC13, IC15, SVT, IIIT5K, SVTP, CUTE), VizWiz_Cap, VizWiz_VQA, or asks about evaluating this task. Reports PQ, RMSE, Accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2409.14215
  bibtex_key: jiang2024atbench
  confidence: high
---

# atbench-eval

> @Bench: Benchmarking Vision-Language Models for Human-centered Assistive Technology — Xin Jiang et al. (2024) (arXiv:2409.14215, 2024)

## What this evaluates

Evaluates vision-language models on five assistive technology tasks for people with visual impairments: panoptic segmentation, depth estimation, optical character recognition, image captioning, and visual question answering. It probes the model's ability to unify multiple visual understanding and generation tasks within a single parameter set using task-specific prompts.

## Datasets

- **ADE-150** — total ?; splits: test (-1)
- **NYU-V2** — total ?; splits: test (-1)
- **OCR (IC13, IC15, SVT, IIIT5K, SVTP, CUTE)** — total ?; splits: test (-1)
- **VizWiz_Cap** — total ?; splits: test (-1)
- **VizWiz_VQA** — total ?; splits: test (-1)

## Metrics

- `PQ` **(primary)** — range: [0, 1]
  - Panoptic Quality, combining segmentation quality and recognition quality for panoptic segmentation tasks.
- `RMSE` **(primary)** — range: [0, inf]
  - Root Mean Square Error between predicted and ground-truth depth maps; lower is better.
- `Accuracy` **(primary)** — range: [0, 1]
  - Percentage of correctly predicted labels or answers for OCR and VQA tasks.
- `BLEU-1` — range: [0, 1]
  - Unigram precision between generated captions and ground-truth references; higher is better.
- `CIDEr` — range: [0, inf]
  - Consensus-based Image Description Evaluation metric based on TF-IDF weighted n-gram similarity.

## Input / output format

**Input**: An input image concatenated with a task-specific text prompt (e.g., 'panoptic segmentation', 'depth estimation', 'OCR', 'caption', or a VQA question).

**Output**: Task-specific prediction: a segmentation mask, a depth map, recognized text, an image caption, or a short answer string.

## Scoring recipe

```python
def evaluate(predictions, golds, task):
    if task == 'panoptic_segmentation':
        return pq_score(predictions.masks, golds.masks)
    elif task == 'depth_estimation':
        return np.sqrt(np.mean((predictions.depth - golds.depth) ** 2))
    elif task == 'ocr':
        return np.mean([1.0 if p == g else 0.0 for p, g in zip(predictions.texts, golds.texts)])
    elif task == 'captioning':
        return bleu1_score(predictions.captions, golds.captions), cider_score(predictions.captions, golds.captions)
    elif task == 'vqa':
        return np.mean([1.0 if p == g else 0.0 for p, g in zip(predictions.answers, golds.answers)])
```

## Common pitfalls

- Comparing multi-task training results directly with baselines that use task-specific fine-tuning or pre-trained weights, which unfairly inflates baseline performance.
- Averaging OCR accuracy across six diverse datasets without weighting for dataset size or difficulty, potentially masking performance on harder benchmarks.
- Ignoring significant parameter count differences when claiming efficiency gains, as some baselines use models 5-50x larger.

## Evidence (verbatim from paper)

> Table 3: Comparison of multi-task training @Model and other generalist models. We report the multi-task training results without any pre-training and task-specific fine-tuning. Note: GIT and PaLI are LVLMs. “*” denotes the model has the capability for the task but does not have number reported. “–” means the model does not have the ability for the specific task. “†” means the model uses pre-trained weights for training. (B@1 = BLEU-1)

## Citation

```bibtex
@misc{jiang2024atbench,
  title={@Bench: Benchmarking Vision-Language Models for Human-centered Assistive Technology},
  author={Xin Jiang et al. (2024)},
  year={2024},
  note={arXiv:2409.14215}
}
```

- arXiv: 2409.14215
