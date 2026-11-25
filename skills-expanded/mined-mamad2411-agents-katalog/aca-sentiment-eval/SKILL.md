---
name: aca-sentiment-eval
description: Evaluates the ability of sentiment analysis models to classify short social media posts and movie reviews into discrete sentiment categories. It probes how well supervised and unsupervised word representations capture task-specific sentiment orientation. Use when the user wants to benchmark on ACA, Stanford Sentiment Treebank (SST), or asks about evaluating this task. Reports Accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1908.07061
  bibtex_key: farhadloo2019twitter
  confidence: medium
---

# aca-sentiment-eval

> Twitter Sentiment on Affordable Care Act using Score Embedding — Farhadloo (2019) (arXiv:1908.07061, 2019)

## What this evaluates

Evaluates the ability of sentiment analysis models to classify short social media posts and movie reviews into discrete sentiment categories. It probes how well supervised and unsupervised word representations capture task-specific sentiment orientation.

## Datasets

- **ACA** — total 2458; splits: train (2212), test (246)
- **Stanford Sentiment Treebank (SST)** — total 11855; splits: train (8544), dev (1101), test (2210)

## Metrics

- `Accuracy` **(primary)** — range: [0, 1]
  - The proportion of correctly classified instances out of the total number of instances in the evaluation set. Calculated as count(correct predictions) / count(total instances).

## Input / output format

**Input**: Raw text of a tweet or movie review snippet.

**Output**: A single categorical sentiment label: for ACA, one of 'against TrumpCare', 'neutral', or 'pro TrumpCare'; for SST, one of 'very negative', 'negative', 'neutral', 'positive', or 'very positive'.

## Scoring recipe

```python
def calculate_accuracy(predictions, gold_labels):
    correct = sum(1 for p, g in zip(predictions, gold_labels) if p == g)
    return correct / len(gold_labels)
```

## Common pitfalls

- The Results section states performance was 'measured using 5-fold cross-validation', but Table 1 provides a fixed train/test split, creating ambiguity about the exact evaluation protocol for the ACA dataset.
- Lexicon baselines use a strict majority-vote rule on raw term counts rather than weighted scores, which may underestimate their performance compared to standard lexicon implementations.
- SST results compare against numerous baselines, but the exact preprocessing, tokenization, and hyperparameter tuning for the proposed Score Embedding method are not fully detailed, hindering direct reproduction.

## Evidence (verbatim from paper)

> We have used two data sets for evaluating our method. The first data set is the ACA data which we have collected to study the public opinions about the health-care on Twitter. The second data is the Stanford Sentiment Treebank (SST) which is used as a benchmark to be able to compare our results with other studies in the literature. ... To prepare a training/testing set, 3000 tweets were randomly selected and manually labeled by 2 annotators... There were 542 “do not know/not related" tweets which were discarded from the sets. ... In this section we report the performance of different methods that was measured using 5-fold cross-validation. ... To evaluate the performance of the lexicon based methods, we applied these lexicons to our test set and calculated the accuracy of them.

## Citation

```bibtex
@misc{farhadloo2019twitter,
  title={Twitter Sentiment on Affordable Care Act using Score Embedding},
  author={Farhadloo (2019)},
  year={2019},
  note={arXiv:1908.07061}
}
```

- arXiv: 1908.07061
