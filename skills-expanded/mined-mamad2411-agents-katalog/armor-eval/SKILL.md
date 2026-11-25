---
name: armor-eval
description: This benchmark meta-evaluates objective music evaluation (OE) metrics by measuring how well their similarity scores and classification outputs align with human subjective judgments. It probes whether automated algorithms can reliably capture human perception of musical quality and distinguish human-composed from AI-generated music across diverse genres and generative models. Use when the user wants to benchmark on Armor, or asks about evaluating this task. Reports correlation coefficient.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2108.12973
  bibtex_key: wang2021armor
  confidence: high
---

# armor-eval

> Armor: A Benchmark for Meta-evaluation of Artificial Music — Wang et al. (2021) (arXiv:2108.12973, 2021)

## What this evaluates

This benchmark meta-evaluates objective music evaluation (OE) metrics by measuring how well their similarity scores and classification outputs align with human subjective judgments. It probes whether automated algorithms can reliably capture human perception of musical quality and distinguish human-composed from AI-generated music across diverse genres and generative models.

## Datasets

- **Armor** — total ?; splits: test (-1)

## Metrics

- `correlation coefficient` **(primary)** — range: [-1, 1]
  - Pearson or Spearman correlation between the similarity scores produced by an objective evaluation (OE) metric and the similarity scores provided by human evaluators across a set of music pairs. Values range from -1 to 1, with higher absolute values indicating stronger alignment with human judgment.

## Input / output format

**Input**: Pairs of original and continuation MIDI compositions (or human/AI music pieces) labeled with human similarity scores and ground-truth authorship (human vs. AI model).

**Output**: For the comparison task: a continuous similarity score from the OE metric. For the distinguishing task: a binary classification (human vs. AI) or feature vectors for clustering.

## Scoring recipe

```python
# Comparison task
corr = pearsonr(human_similarity_scores, oe_metric_scores)

# Distinguishing task
features = extract_features(midi_files, method="Mgeval")
clusters = kmeans(features, k=2)
acc = accuracy_score(clusters, human_labels)
```

## Common pitfalls

- Feature-based metrics require specific preprocessing (weighted averaging for Mir_eval, high-dimensional vector similarity for Mgeval) before correlation computation.
- Metric reliability is highly sensitive to track complexity; single-track compositions yield significantly higher correlation than multi-track ones, skewing results if not stratified.
- The 'Area' metric requires horizontal/vertical shifting of melody curves to minimize enclosed area, which is often omitted in naive implementations.

## Evidence (verbatim from paper)

> To explore how OE algorithms correspond with SE when comparing original and continuation compositions, we compute the correlation between the similarity scores provided by humans and algorithms. ... According to results displayed in Table 5, we observe that all four objective metrics have correlation coefficient less than 0.3 over all types of evaluators, which implies relatively weak correlation with human judgment.

## Citation

```bibtex
@misc{wang2021armor,
  title={Armor: A Benchmark for Meta-evaluation of Artificial Music},
  author={Wang et al. (2021)},
  year={2021},
  note={arXiv:2108.12973}
}
```

- arXiv: 2108.12973
