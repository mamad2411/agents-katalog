---
name: argscichat-eval
description: Evaluates the ability of dialogue agents to select supportive facts from scientific papers and generate contextually appropriate responses in argumentative scientific dialogues. Probes document-grounded response generation and fact selection under expert-level, opinion-driven interactions. Use when the user wants to benchmark on ArgSciChat, or asks about evaluating this task. Reports Fact-F1.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2202.06690
  bibtex_key: ruggeri2022argscichat
  confidence: high
---

# argscichat-eval

> ArgSciChat: A Dataset for Argumentative Dialogues on Scientific Papers — Ruggeri et al. (2022) (arXiv:2202.06690, 2022)

## What this evaluates

Evaluates the ability of dialogue agents to select supportive facts from scientific papers and generate contextually appropriate responses in argumentative scientific dialogues. Probes document-grounded response generation and fact selection under expert-level, opinion-driven interactions.

## Datasets

- **ArgSciChat** — total ?; splits: train (-1), val (-1), test (-1)

## Metrics

- `Fact-F1` **(primary)** — range: [0, 1]
  - F1 score computed over candidate sentences selected by the agent against the human-selected reference supportive facts (up to two sentences per query).
- `Message-F1` — range: [0, 1]
  - Token-level F1 score (SQuAD convention) computed over individual words between the generated response and the reference expert message.
- `BERTScore` — range: [0, 1]
  - Contextualized embedding-based similarity score between generated and reference responses.
- `MoverScore` — range: [0, 1]
  - Wasserstein distance-based metric measuring semantic similarity between generated and reference texts.

## Input / output format

**Input**: Query (Q), scientific paper (P), dialogue history (H), and optionally human-selected supportive facts (F).

**Output**: For fact selection: up to two sentences from the paper. For response generation: a free-form text response to the prompt's message.

## Scoring recipe

```python
def compute_fact_f1(pred_sentences, gold_sentences):
    pred_set = set(pred_sentences)
    gold_set = set(gold_sentences)
    tp = len(pred_set & gold_set)
    prec = tp / len(pred_set) if pred_set else 0
    rec = tp / len(gold_set) if gold_set else 0
    return 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0

def compute_message_f1(pred_text, gold_text):
    pred_tokens = pred_text.split()
    gold_tokens = gold_text.split()
    common = Counter(pred_tokens) & Counter(gold_tokens)
    num_same = sum(common.values())
    prec = num_same / len(pred_tokens) if pred_tokens else 0
    rec = num_same / len(gold_tokens) if gold_tokens else 0
    return 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
```

## Common pitfalls

- Splits are stratified by scientific paper, not by dialogue turn, to prevent data leakage of the same paper across train/val/test folds.
- Fact selection is strictly limited to two sentences per query, matching the human annotation protocol, rather than a variable number.
- Message-F1 uses word-level tokenization (SQuAD convention), not subword or character-level, which significantly affects scores compared to modern generation metrics.

## Evidence (verbatim from paper)

> For evaluation metrics, similar to Dasigi et al. (2021), for fact selection, we compute the F1 score over candidate sentences in a scientific paper against the reference supportive facts. We denote this metric as Fact-F1. For response generation, we use the token-level F1 score introduced in SQUAD (Rajpurkar et al., 2016). This metric is computed over individual words between the generated response and the reference E's message. We denote this metric as Message-F1. Following recent suggestions for evaluating text generation systems, we also report BERTScore (BScore) (Zhang et al., 2020) and MoverScore (Mover) (Zhao et al., 2019) for the response generation task.

## Citation

```bibtex
@misc{ruggeri2022argscichat,
  title={ArgSciChat: A Dataset for Argumentative Dialogues on Scientific Papers},
  author={Ruggeri et al. (2022)},
  year={2022},
  note={arXiv:2202.06690}
}
```

- arXiv: 2202.06690
