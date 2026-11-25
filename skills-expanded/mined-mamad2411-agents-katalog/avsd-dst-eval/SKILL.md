---
name: avsd-dst-eval
description: Evaluates a model's ability to perform dialogue state tracking in an open-domain, multimodal setting by framing it as a question-answering task. It measures how well the system tracks conversation state and generates accurate answers based on video/audio context and dialogue history. Use when the user wants to benchmark on AVSD, or asks about evaluating this task. Reports F1 score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2007.09903
  bibtex_key: mou2020multimodal
  confidence: medium
---

# avsd-dst-eval

> Multimodal Dialogue State Tracking By QA Approach with Data Augmentation — Mou et al. (2020) (arXiv:2007.09903, 2020)

## What this evaluates

Evaluates a model's ability to perform dialogue state tracking in an open-domain, multimodal setting by framing it as a question-answering task. It measures how well the system tracks conversation state and generates accurate answers based on video/audio context and dialogue history.

## Datasets

- **AVSD** — total ?; splits: train (-1), val (-1)

## Metrics

- `F1 score` **(primary)** — range: [0, 1]
  - Standard token-level F1 score computed between the predicted answer sequence and the ground truth answer. It balances precision and recall of overlapping words.

## Input / output format

**Input**: A sequence of question-answer pairs representing the dialogue history, followed by a target question to be answered.

**Output**: A sequence of predicted words forming the answer to the target question.

## Scoring recipe

```python
def compute_f1(pred_tokens, gold_tokens):
    pred_set = set(pred_tokens)
    gold_set = set(gold_tokens)
    intersection = pred_set & gold_set
    precision = len(intersection) / len(pred_set) if pred_set else 0
    recall = len(intersection) / len(gold_set) if gold_set else 0
    if precision + recall == 0:
        return 0
    return 2 * (precision * recall) / (precision + recall)
```

## Common pitfalls

- The paper explicitly states that temporal order of dialogue history is not strictly necessary for answering, so models should be robust to shuffled QA pairs rather than relying on strict sequence modeling.
- F1 score is only explicitly mentioned for validation-based early stopping; test evaluation metrics are not detailed in the provided text.
- Theoretical data augmentation suggests tens of thousands of samples per instance via shuffling, but the authors only double the training set in practice due to time constraints.

## Evidence (verbatim from paper)

> The F1 score on the validation set is used to terminate the training procedure. To increase the training efficiency and accuracy, we use teacher forcing (Williams and Zipser 1989); it uses the ground truth word to predict the next word during training.

## Citation

```bibtex
@misc{mou2020multimodal,
  title={Multimodal Dialogue State Tracking By QA Approach with Data Augmentation},
  author={Mou et al. (2020)},
  year={2020},
  note={arXiv:2007.09903}
}
```

- arXiv: 2007.09903
