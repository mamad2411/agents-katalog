---
name: alignment-research-classifier-eval
description: Evaluates a logistic regression model on SPECTER embeddings to distinguish AI alignment research articles from adjacent research on arXiv. Probes the model's ability to capture domain-specific semantic patterns and citation-driven textual features for automated literature filtering. Use when the user wants to benchmark on arXiv Alignment Research Corpus, or asks about evaluating this task. Reports AUC.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2206.02841
  bibtex_key: kirchner2022researching
  confidence: high
---

# alignment-research-classifier-eval

> Researching Alignment Research: Unsupervised Analysis — Kirchner et al. (2022) (arXiv:2206.02841, 2022)

## What this evaluates

Evaluates a logistic regression model on SPECTER embeddings to distinguish AI alignment research articles from adjacent research on arXiv. Probes the model's ability to capture domain-specific semantic patterns and citation-driven textual features for automated literature filtering.

## Datasets

- **arXiv Alignment Research Corpus** — total ?; splits: train (-1), test (-1); repo https://github.com/moirage/alignment-research-dataset.git

## Metrics

- `AUC` **(primary)** — range: [0, 1]
  - Area under the Receiver Operating Characteristic (ROC) curve, measuring the trade-off between true positive rate and false positive rate across all classification thresholds.

## Input / output format

**Input**: Concatenated title and abstract of arXiv articles, processed through the Allen SPECTER model to produce fixed-length sentence embeddings.

**Output**: Binary classification probability score indicating the likelihood that an article belongs to the AI alignment research domain (level-0).

## Scoring recipe

```python
embeddings = specter_model.encode(title + abstract)
log_reg = LogisticRegression()
log_reg.fit(train_embeddings, train_labels) # 1 for level-0, 0 for level-1
scores = log_reg.predict_proba(test_embeddings)[:, 1]
auc = roc_auc_score(test_labels, scores)
threshold = 0.75
relevant_articles = [score for score in scores if score >= threshold]
```

## Common pitfalls

- The negative class (level-1) is defined by citation network proximity rather than explicit content labeling, potentially including borderline or misclassified alignment papers.
- The 75% relevance threshold is chosen heuristically based on score distribution inspection rather than a formal validation or calibration step.
- SPECTER embeddings are trained on citation data, so the classifier may inadvertently learn citation patterns or journal/venue biases rather than pure semantic alignment concepts.

## Evidence (verbatim from paper)

> We trained the classifier on a training set (80%) to distinguish level-0 from level-1 articles and evaluated performance on a separate test set (20%). The classifier achieved good performance (AUC= 0.75; Fig. 4b inset), reliably rejecting level-1 articles and correctly identifying a large portion of level-0 articles (Fig. 4b).

## Citation

```bibtex
@misc{kirchner2022researching,
  title={Researching Alignment Research: Unsupervised Analysis},
  author={Kirchner et al. (2022)},
  year={2022},
  note={arXiv:2206.02841}
}
```

- arXiv: 2206.02841
