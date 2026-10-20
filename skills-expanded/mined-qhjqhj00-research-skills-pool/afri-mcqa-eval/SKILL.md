---
name: afri-mcqa-eval
description: Evaluates multimodal large language models' ability to answer visual questions about African cultural contexts in both native African languages and English, across text and audio input modalities. Use when the user wants to benchmark on Afri-MCQA, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2601.05699
  bibtex_key: tonja2026afimcqa
  confidence: medium
---

# afri-mcqa-eval

> Afri-MCQA: Multimodal Cultural Question Answering for African Languages — Tonja et al. (2026) (arXiv:2601.05699, 2026)

## What this evaluates

Evaluates multimodal large language models' ability to answer visual questions about African cultural contexts in both native African languages and English, across text and audio input modalities.

## Datasets

- **Afri-MCQA** — total ?; splits: test (-1)

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - For MC-VQA, accuracy is the proportion of correctly selected options out of total questions. Open-ended VQA metrics are not explicitly defined in the experimental setup.

## Input / output format

**Input**: An image paired with a question in either text or audio format, optionally accompanied by multiple-choice options. A location/country context is appended via a prompt template.

**Output**: For MC-VQA: the selected answer option. For Open-ended VQA: a generated text response.

## Scoring recipe

```python
def compute_accuracy(predictions, gold_labels):
    correct = sum(1 for p, g in zip(predictions, gold_labels) if p == g)
    return correct / len(gold_labels)
# Open-ended metrics not specified in text
```

## Common pitfalls

- Performance heavily depends on input modality (text vs. audio) and language, with significant drops for native African languages and speech inputs.
- Multiple-choice performance may overestimate true cultural understanding compared to open-ended generation.
- Prompt design (location-aware vs. image-only) significantly impacts results and must be controlled.

## Evidence (verbatim from paper)

> To understand how task format affects model performance (RQ4), we evaluate models on both Multiple-Choice VQA (MC-VQA) and Open-ended VQA. MC-VQA provides answer options, while Open-ended VQA requires answer generation. Comparing these formats shows whether strong MC-VQA performance reflects actual cultural understanding or simply selecting from provided options. We provide results for Image-only prompts and language-wise results in Appendix[C] affect accuracy?

## Citation

```bibtex
@misc{tonja2026afimcqa,
  title={Afri-MCQA: Multimodal Cultural Question Answering for African Languages},
  author={Tonja et al. (2026)},
  year={2026},
  note={arXiv:2601.05699}
}
```

- arXiv: 2601.05699
