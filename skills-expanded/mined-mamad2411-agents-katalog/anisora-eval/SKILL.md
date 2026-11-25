---
name: anisora-eval
description: Evaluates the quality and controllability of AI-generated animation videos, specifically probing character consistency, style consistency, and distortion detection. It addresses the unique challenges of non-photorealistic content, exaggerated motion, and artistic coherence that standard video benchmarks often miss. Use when the user wants to benchmark on AniSora Benchmark, or asks about evaluating this task. Reports character consistency.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2412.10255
  bibtex_key: jiang2024anisora
  confidence: medium
---

# anisora-eval

> AniSora: Exploring the Frontiers of Animation Video Generation in the Sora Era — Jiang et al. (2024) (arXiv:2412.10255, 2024)

## What this evaluates

Evaluates the quality and controllability of AI-generated animation videos, specifically probing character consistency, style consistency, and distortion detection. It addresses the unique challenges of non-photorealistic content, exaggerated motion, and artistic coherence that standard video benchmarks often miss.

## Datasets

- **AniSora Benchmark** — total 948; splits: test (948); repo https://github.com/bilibili/Index-anisora

## Metrics

- `character consistency` **(primary)** — range: [0, 1]
  - Measures how well the generated video maintains the visual identity and features of the target character across all frames. Specific mathematical formula not provided in the excerpt.
- `style consistency` — range: [0, 1]
  - Evaluates the preservation of the target artistic style and non-photorealistic rendering quality throughout the video sequence. Specific mathematical formula not provided in the excerpt.
- `distortion detection` — range: [0, 1]
  - Assesses the presence of visual artifacts, unnatural deformations, or temporal flickering in the generated animation. Specific mathematical formula not provided in the excerpt.

## Input / output format

**Input**: Guide frames, text prompts, and motion masks for video generation tasks.

**Output**: Generated video clips.

## Scoring recipe

```python
# Not fully detailed in the provided text.
# Typically involves computing the six tailored metrics on the 948-video test set.
# score = evaluate_consistency(generated_video, gold_video)
# Returns average metric values across the benchmark for character consistency, style consistency, and distortion detection.
```

## Common pitfalls

- Standard video generation metrics often fail to capture the specific requirements of non-photorealistic animation, such as exaggerated motion and artistic style preservation.
- Character consistency evaluation requires frame-level tracking that automated metrics may not accurately perform without specialized design tailored to animation.

## Evidence (verbatim from paper)

> a novel benchmark of 948 animation videos with six tailored evaluation metrics (character consistency, style consistency, distortion detection, etc.)—the first dedicated evaluation framework for animation video generation

## Citation

```bibtex
@misc{jiang2024anisora,
  title={AniSora: Exploring the Frontiers of Animation Video Generation in the Sora Era},
  author={Jiang et al. (2024)},
  year={2024},
  note={arXiv:2412.10255}
}
```

- arXiv: 2412.10255
