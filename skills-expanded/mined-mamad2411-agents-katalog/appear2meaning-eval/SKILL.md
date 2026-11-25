---
name: appear2meaning-eval
description: This benchmark probes vision-language models' ability to infer non-observable, culturally grounded structured metadata (culture, period, origin, creator) from images of heritage artifacts. It evaluates whether models can go beyond visual perception to perform semantic alignment with museum annotations, revealing culture-dependent reasoning capabilities and potential biases. Use when the user wants to benchmark on Appear2Meaning, or asks about evaluating this task. Reports exact match accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.07338
  bibtex_key: jiang2026appear2meaning
  confidence: high
---

# appear2meaning-eval

> Appear2Meaning: A Cross-Cultural Benchmark for Structured Cultural Metadata Inference from Images — Jiang et al. (2026) (arXiv:2604.07338, 2026)

## What this evaluates

This benchmark probes vision-language models' ability to infer non-observable, culturally grounded structured metadata (culture, period, origin, creator) from images of heritage artifacts. It evaluates whether models can go beyond visual perception to perform semantic alignment with museum annotations, revealing culture-dependent reasoning capabilities and potential biases.

## Datasets

- **Appear2Meaning** — total 750; splits: test (750)

## Metrics

- `exact match accuracy` **(primary)** — range: [0, 1]
  - Computed by dividing the number of samples where the LLM-as-Judge assigns a 'correct' label for all metadata fields by the total number of samples. Requires semantic alignment across culture, period, origin, and creator.
- `partial match rate` — range: [0, 1]
  - Proportion of samples where the judge assigns a 'partially correct' label, indicating some attributes match semantically while others do not.
- `attribute-level accuracy` — range: [0, 1]
  - For each metadata field (culture, period, origin, creator), the fraction of samples where the predicted value semantically aligns with the reference annotation.

## Input / output format

**Input**: A single image $x$ of a cultural heritage artifact.

**Output**: Structured metadata fields: culture, period, origin, creator (and optionally title).

## Scoring recipe

```python
judge = GPT-4.1-mini
exact_correct = 0
partial_correct = 0
attr_correct = {attr: 0 for attr in ['culture', 'period', 'origin', 'creator']}
for pred, gold in zip(predictions, ground_truth):
    prompt = f'Compare predicted metadata {pred} with reference {gold}. Assign: correct, partially correct, or incorrect.'
    label = judge.evaluate(prompt)
    if label == 'correct': exact_correct += 1
    if label in ['correct', 'partially correct']: partial_correct += 1
    for attr in attr_correct:
        if pred[attr] semantically matches gold[attr]: attr_correct[attr] += 1
N = len(predictions)
return exact_correct/N, partial_correct/N, {k: v/N for k, v in attr_correct.items()}
```

## Common pitfalls

- Models may rely solely on visual cues, but the task explicitly requires inferring non-observable attributes, leading to hallucination or culture-dependent guessing.
- The evaluation explicitly prioritizes semantic alignment over lexical similarity, so exact string matching will underestimate model performance.
- The LLM-as-Judge uses GPT-4.1-mini, which may introduce judge bias or inconsistency compared to human verification or strict schema matching.

## Evidence (verbatim from paper)

> Metrics include exact match accuracy, partial match rate, and outcome distributions. We also compute attribute-level accuracy and analyze performance across cultural regions, enabling fine-grained assessment of structured cultural metadata inferenceand bias.

## Citation

```bibtex
@misc{jiang2026appear2meaning,
  title={Appear2Meaning: A Cross-Cultural Benchmark for Structured Cultural Metadata Inference from Images},
  author={Jiang et al. (2026)},
  year={2026},
  note={arXiv:2604.07338}
}
```

- arXiv: 2604.07338
