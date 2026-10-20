---
name: arxivcap-eval
description: Evaluates large vision-language models' ability to comprehend and generate text for scientific figures. It probes capabilities in single and multi-figure captioning, contextualized captioning using in-context examples, and inferring paper titles from figure-caption sequences. Use when the user wants to benchmark on ArXivCap, or asks about evaluating this task. Reports BLEU-2.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2403.00231
  bibtex_key: li2024multimodalarxiv
  confidence: high
---

# arxivcap-eval

> Multimodal ArXiv: A Dataset for Improving Scientific Comprehension of Large Vision-Language Models — Lei Li et al. (2024) (arXiv:2403.00231, 2024)

## What this evaluates

Evaluates large vision-language models' ability to comprehend and generate text for scientific figures. It probes capabilities in single and multi-figure captioning, contextualized captioning using in-context examples, and inferring paper titles from figure-caption sequences.

## Datasets

- **ArXivCap** — total ?; splits: test (-1)

## Metrics

- `BLEU-2` **(primary)** — range: [0, 1]
  - Computes the 2-gram precision between the generated caption/title and the ground-truth reference. Often scaled by 100 for reporting.
- `ROUGE-L` — range: [0, 1]
  - Measures the longest common subsequence (LCS) recall/precision between the generated and reference text, capturing sentence-level fluency and overlap.
- `BERT-Score` — range: [0, 1]
  - Calculates the cosine similarity between contextual embeddings of generated and reference tokens using a pre-trained BERT model, averaged across all tokens.

## Input / output format

**Input**: For captioning tasks: one or more scientific figures (images) optionally accompanied by a sequence of prior figure-caption pairs, plus a task-specific instruction prompt. For title generation: a sequence of figure-caption pairs from a paper plus a title generation prompt.

**Output**: A natural language caption describing the figure(s) or the inferred paper title.

## Scoring recipe

```python
def compute_metrics(predictions, references):
    bleu2 = compute_bleu(n_grams=2, preds=predictions, refs=references)
    rouge_l = compute_rouge_l(preds=predictions, refs=references)
    bert_s = compute_bert_score(preds=predictions, refs=references)
    return {'BLEU-2': bleu2, 'ROUGE-L': rouge_l, 'BERT-Score': bert_s}
```

## Common pitfalls

- Proprietary models (Bard, GPT-4V) are evaluated on a randomly sampled 200-instance subset due to API limits, while open-source models are evaluated on the full set, making direct comparison potentially biased.
- Contextualized captioning performance is highly sensitive to the order of in-context figure-caption pairs; shuffling the order significantly drops performance for baseline models.
- Figure QA tasks in external benchmarks like MathVista often use synthetic plots rather than real scientific figures, leading to misleading performance assessments for domain-specific comprehension.

## Evidence (verbatim from paper)

> We adopt BLEU-2(Papineni et al., 2002), ROUGE-L(Lin, 2004) and BERT-Score(Zhang et al., 2020) as the automatic evaluation metrics.

## Citation

```bibtex
@misc{li2024multimodalarxiv,
  title={Multimodal ArXiv: A Dataset for Improving Scientific Comprehension of Large Vision-Language Models},
  author={Lei Li et al. (2024)},
  year={2024},
  note={arXiv:2403.00231}
}
```

- arXiv: 2403.00231
