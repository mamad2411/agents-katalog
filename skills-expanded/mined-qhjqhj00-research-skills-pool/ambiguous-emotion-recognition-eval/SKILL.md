---
name: ambiguous-emotion-recognition-eval
description: Evaluates audio-language models' ability to recognize ambiguous emotions in speech by predicting full emotion probability distributions and dominant class labels. It specifically probes how test-time scaling (TTS) strategies and model capacity interact with varying levels of emotional ambiguity to improve or degrade recognition performance. Use when the user wants to benchmark on IEMOCAP, MSP-Podcast, CREMA-D, or asks about evaluating this task. Reports JS divergence.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2602.03873
  bibtex_key: jia2026decoding
  confidence: high
---

# ambiguous-emotion-recognition-eval

> Decoding Ambiguous Emotions with Test-Time Scaling in Audio-Language Models — Hong Jia et al. (arXiv:2602.03873, 2026)

## What this evaluates

Evaluates audio-language models' ability to recognize ambiguous emotions in speech by predicting full emotion probability distributions and dominant class labels. It specifically probes how test-time scaling (TTS) strategies and model capacity interact with varying levels of emotional ambiguity to improve or degrade recognition performance.

## Datasets

- **IEMOCAP** — total ?; splits: test (-1)
- **MSP-Podcast** — total ?; splits: test (-1)
- **CREMA-D** — total ?; splits: test (-1)

## Metrics

- `JS divergence` **(primary)** — range: [0, 1]
  - Jensen-Shannon divergence between the predicted and ground-truth emotion probability distributions. Lower values indicate better distribution matching.
- `Bhattacharyya Coefficient (BC)` — range: [0, 1]
  - Bhattacharyya coefficient measuring the similarity between two probability distributions. Higher values indicate closer alignment.
- `R-squared ($R^2$)` — range: other
  - Coefficient of determination evaluating how well the predicted distribution captures the variance of the ground-truth distribution. Higher is better.
- `Accuracy` — range: [0, 1]
  - Proportion of correctly predicted dominant emotion classes in single-class classification.
- `F1-score` — range: [0, 1]
  - Macro-averaged F1 score for single-class emotion classification, balancing precision and recall across all emotion categories.

## Input / output format

**Input**: Raw speech audio clips corresponding to spoken utterances.

**Output**: A probability distribution over emotion categories, or a single predicted dominant emotion label.

## Scoring recipe

```python
import numpy as np
from scipy.spatial.distance import jensenshannon
from sklearn.metrics import accuracy_score, f1_score

def compute_metrics(pred_dist, gold_dist, pred_class=None, gold_class=None):
    js = jensenshannon(gold_dist, pred_dist) ** 2
    bc = np.sum(np.sqrt(np.array(gold_dist) * np.array(pred_dist)))
    r2 = 1 - np.sum((np.array(pred_dist) - np.array(gold_dist))**2) / np.sum((np.array(gold_dist) - np.mean(gold_dist))**2)
    acc = accuracy_score([gold_class], [pred_class]) if pred_class is not None else None
    f1 = f1_score([gold_class], [pred_class], average='macro') if pred_class is not None else None
    return js, bc, r2, acc, f1
```

## Common pitfalls

- TTS strategies like CoT and BoN optimized for distribution prediction can degrade performance on single-class classification tasks.
- Unweighted aggregation (e.g., BoN) fails on spontaneous datasets like MSP-Podcast where emotional expressions are subtle and multi-modal.
- High overall accuracy can mask severe failures on minority emotion classes, such as the consistent inability of most models to recognize 'disgust' in CREMA-D.

## Evidence (verbatim from paper)

> Table[1] presents the ambiguous emotion recognition performance of eight open-source and closed-source models. Closed-source models typically demonstrate superior performance compared to open-source models. Gemini 2.5 Pro consistently achieves the best or near-best results across almost all datasets and metrics. Notably, it achieves the best results across all datasets and metrics, with the exception of the BC and $R^{2}$ on IEMOCAP and the JS on CREMA-D, where it secures the second-best scores.

## Citation

```bibtex
@misc{jia2026decoding,
  title={Decoding Ambiguous Emotions with Test-Time Scaling in Audio-Language Models},
  author={Hong Jia et al.},
  year={2026},
  note={arXiv:2602.03873}
}
```

- arXiv: 2602.03873
