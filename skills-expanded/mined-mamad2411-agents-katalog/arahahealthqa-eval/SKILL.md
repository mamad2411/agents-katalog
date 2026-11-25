---
name: arahahealthqa-eval
description: This benchmark evaluates Arabic language models on healthcare-related question answering, specifically probing their ability to classify mental health conditions and generate culturally appropriate medical advice. It tests both discriminative capabilities (multi-label classification and multiple-choice selection) and generative capabilities (open-ended response generation) in clinical and mental health contexts. Use when the user wants to benchmark on AraHealthQA, or asks about evaluating this task. Reports Weighted-F1.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2508.20047
  bibtex_key: alhuzali2025arahahealthqa
  confidence: high
---

# arahahealthqa-eval

> AraHealthQA 2025: The First Shared Task on Arabic Health Question Answering — Alhuzali et al. (2025) (arXiv:2508.20047, 2025)

## What this evaluates

This benchmark evaluates Arabic language models on healthcare-related question answering, specifically probing their ability to classify mental health conditions and generate culturally appropriate medical advice. It tests both discriminative capabilities (multi-label classification and multiple-choice selection) and generative capabilities (open-ended response generation) in clinical and mental health contexts.

## Datasets

- **AraHealthQA** — total ?; splits: test (-1)

## Metrics

- `Weighted-F1` **(primary)** — range: [0, 1]
  - F1 score calculated per class and averaged, weighted by the number of true instances for each class. Used as the primary ranking metric for classification subtasks.
- `Jaccard Score` — range: [0, 1]
  - The size of the intersection divided by the size of the union of the predicted and gold label sets: |A ∩ B| / |A ∪ B|.
- `BERTScore` — range: [0, 1]
  - Computes cosine similarity between contextualized BERT embeddings of the generated response and the reference text, then averages the maximum similarities across tokens.
- `Accuracy` — range: [0, 1]
  - Proportion of correctly predicted multiple-choice options out of the total number of instances.

## Input / output format

**Input**: Arabic text containing a health-related question, optionally accompanied by multiple-choice options. For generative subtasks, the input is the question alone; for classification, it may include candidate labels or categories.

**Output**: For classification subtasks: a set of predicted label(s) or a single selected option. For generative subtasks: a free-form Arabic text response. Predictions must be parseable as label sets or strings for automated scoring.

## Scoring recipe

```python
def compute_metrics(preds, golds):
    f1s, jaccs, berts, accs = [], [], [], []
    for p, g in zip(preds, golds):
        p_set, g_set = set(p), set(g)
        jaccs.append(len(p_set & g_set) / len(p_set | g_set) if (p_set | g_set) else 0)
        tp, fp, fn = len(p_set & g_set), len(p_set - g_set), len(g_set - p_set)
        prec = tp / (tp + fp) if (tp + fp) else 0
        rec = tp / (tp + fn) if (tp + fn) else 0
        f1s.append(2 * prec * rec / (prec + rec) if (prec + rec) else 0)
        berts.append(bertscore.compute(p, g))
        accs.append(1 if p == g else 0)
    return {'Weighted-F1': np.mean(f1s), 'Jaccard Score': np.mean(jaccs), 'BERTScore': np.mean(berts), 'Accuracy': np.mean(accs)}
```

## Common pitfalls

- Automatic metrics like BERTScore may overestimate model quality by capturing lexical overlap without verifying clinical accuracy or cultural sensitivity.
- Frequency-based baselines can achieve deceptively high Jaccard scores while performing poorly on Weighted-F1, masking poor precision and recall.
- Small test set sizes in certain subtasks lead to low variance between systems, making statistical significance of rankings difficult to assess.

## Evidence (verbatim from paper)

> The results of Subtask 1 shown in Table[2] reveal a range of performances among participating teams, with Weighted-F1 scores spanning from 0.61 to 0.24 as presented in Table [2]. The top-performing system, mucAI, achieved a Weighted-F1 of 0.61 and a Jaccard score of 0.53, closely followed by Binary_Bunch with nearly identical results.

## Citation

```bibtex
@misc{alhuzali2025arahahealthqa,
  title={AraHealthQA 2025: The First Shared Task on Arabic Health Question Answering},
  author={Alhuzali et al. (2025)},
  year={2025},
  note={arXiv:2508.20047}
}
```

- arXiv: 2508.20047
