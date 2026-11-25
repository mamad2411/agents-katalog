---
name: babyslm-eval
description: Evaluates the lexical and syntactic competence of self-supervised spoken language models using child-centered, developmentally plausible speech data. It probes whether models can acquire language-like representations from ecologically valid, in-the-wild audio recordings compared to clean audiobooks or text-based inputs. Use when the user wants to benchmark on BabySLM, or asks about evaluating this task. Reports lexical accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2306.01506
  bibtex_key: lavechin2023babyslm
  confidence: high
---

# babyslm-eval

> BabySLM: language-acquisition-friendly benchmark of self-supervised spoken language models — Lavechin et al. (2023) (arXiv:2306.01506, 2023)

## What this evaluates

Evaluates the lexical and syntactic competence of self-supervised spoken language models using child-centered, developmentally plausible speech data. It probes whether models can acquire language-like representations from ecologically valid, in-the-wild audio recordings compared to clean audiobooks or text-based inputs.

## Datasets

- **BabySLM** — total ?; splits: test (-1); repo https://github.com/MarvinLvn/BabySLM

## Metrics

- `lexical accuracy` **(primary)** — range: percent
  - Percentage of correct predictions on lexical probing tasks. Calculated as the number of correct predictions divided by the total number of predictions, multiplied by 100.
- `syntactic accuracy` — range: percent
  - Percentage of correct predictions on syntactic probing tasks. Calculated as the number of correct predictions divided by the total number of predictions, multiplied by 100.

## Input / output format

**Input**: Raw audio recordings, phoneme sequences, or orthographic words (BPE) from child-centered or clean speech corpora.

**Output**: Predicted lexical items or syntactic categories/tokens for probing tasks.

## Scoring recipe

```python
def compute_accuracy(predictions, gold):
    correct = sum(1 for p, g in zip(predictions, gold) if p == g)
    return (correct / len(gold)) * 100
```

## Common pitfalls

- Domain mismatch between training data (in-the-wild, long-form recordings) and test data (synthesized, well-articulated stimuli) causes chance-level performance for speech models.
- Speech-based models require significantly more data than text-based models to emerge above chance, following a logarithmic scaling trend rather than linear.

## Evidence (verbatim from paper)

> Results indicate no evidence of lexical and syntactic knowledge for STELA trained on 1,024 hours of speech from SEEDLingS. This contrasts, in appearance, with what has been found in the ZeroSpeech challenge [2], but this is due to the large variability of speech found in long-forms as we will see in Section 3.3. Results are no different for STELA trained on 128 hours of speech extracted from Providence whose lexical and syntactic accuracies remain close to chance level.

## Citation

```bibtex
@misc{lavechin2023babyslm,
  title={BabySLM: language-acquisition-friendly benchmark of self-supervised spoken language models},
  author={Lavechin et al. (2023)},
  year={2023},
  note={arXiv:2306.01506}
}
```

- arXiv: 2306.01506
