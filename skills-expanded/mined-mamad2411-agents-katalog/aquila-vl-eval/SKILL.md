---
name: aquila-vl-eval
description: Evaluates a 2B-parameter vision-language model's visual understanding, knowledge reasoning, and text reading capabilities across a comprehensive suite of standard multimodal benchmarks. It measures how well the model handles general VQA, mathematical reasoning, and document comprehension tasks. Use when the user wants to benchmark on MMBench, MMStar, MMMU, MathVista, HallusionBench, AI2D, OCRBench, MMVet, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2410.18558
  bibtex_key: gu2024infinitymm
  confidence: high
---

# aquila-vl-eval

> Infinity-MM: Scaling Multimodal Performance with Large-Scale and High-Quality Instruction Data — Gu et al. (2024) (arXiv:2410.18558, 2024)

## What this evaluates

Evaluates a 2B-parameter vision-language model's visual understanding, knowledge reasoning, and text reading capabilities across a comprehensive suite of standard multimodal benchmarks. It measures how well the model handles general VQA, mathematical reasoning, and document comprehension tasks.

## Datasets

- **MMBench** — total ?; splits: test (-1)
- **MMStar** — total ?; splits: test (-1)
- **MMMU** — total ?; splits: val (-1)
- **MathVista** — total ?; splits: testmini (-1)
- **HallusionBench** — total ?; splits: test (-1)
- **AI2D** — total ?; splits: test (-1)
- **OCRBench** — total ?; splits: test (-1)
- **MMVet** — total ?; splits: test (-1)

## Metrics

- `accuracy` **(primary)** — range: percent
  - Standard exact-match or multiple-choice accuracy computed per benchmark. Scores are reported as percentages averaged across the listed benchmarks.

## Input / output format

**Input**: Paired image and text instruction/question.

**Output**: Text response (multiple-choice selection or open-ended answer).

## Scoring recipe

```python
def compute_accuracy(predictions, gold):
    correct = sum(1 for p, g in zip(predictions, gold) if p.strip().lower() == g.strip().lower())
    return (correct / len(gold)) * 100
```

## Common pitfalls

- Benchmarks use heterogeneous evaluation protocols (e.g., multiple-choice vs. open-ended), making direct score comparison difficult.
- The reported 'Average' is a simple arithmetic mean across disparate benchmarks, which can mask performance on specific capabilities.
- Some benchmarks (e.g., MMVet, MME) have strict and lenient evaluation modes; the paper does not specify which mode was used.

## Evidence (verbatim from paper)

> We assessed the visual capabilities of Aquila-VL-2B using a range of visual benchmarks provided by the VLMEvalKit*[[21]]*. Experimental results are shown in Table [4]. Aquila-VL-2B demonstrates highly competitive performance at the same scale, achieving new state-of-the-art results.

## Citation

```bibtex
@misc{gu2024infinitymm,
  title={Infinity-MM: Scaling Multimodal Performance with Large-Scale and High-Quality Instruction Data},
  author={Gu et al. (2024)},
  year={2024},
  note={arXiv:2410.18558}
}
```

- arXiv: 2410.18558
