---
name: authenhallu-eval
description: Evaluates an LLM's capability to detect and categorize hallucinations in authentic, real-world human-LLM dialogues. It specifically probes whether models can identify input-conflicting, context-conflicting, and fact-conflicting errors in query-response pairs. Use when the user wants to benchmark on AuthenHallu, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2510.10539
  bibtex_key: ren2025authenhallu
  confidence: high
---

# authenhallu-eval

> Detecting Hallucinations in Authentic LLM-Human Interactions — Ren et al. (2025) (arXiv:2510.10539, 2025)

## What this evaluates

Evaluates an LLM's capability to detect and categorize hallucinations in authentic, real-world human-LLM dialogues. It specifically probes whether models can identify input-conflicting, context-conflicting, and fact-conflicting errors in query-response pairs.

## Datasets

- **AuthenHallu** — total 800; splits: test (800)

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Standard classification accuracy: the proportion of query-response pairs where the model's predicted hallucination occurrence and category labels exactly match the human-annotated ground truth.

## Input / output format

**Input**: A single query-response pair extracted from a real-world LLM-human dialogue.

**Output**: A binary label for hallucination occurrence ({Hallucination, No Hallucination}) and, if a hallucination is present, a category label ({Input-conflicting, Context-conflicting, Fact-conflicting}).

## Scoring recipe

```python
def compute_accuracy(predictions, gold):
    correct = sum(1 for p, g in zip(predictions, gold) if p == g)
    return correct / len(gold)
```

## Common pitfalls

- The dataset consists of query-response pairs, not full dialogues; each of the 400 dialogues contains exactly two pairs, yielding 800 total instances for evaluation.
- Strict filtering was applied to the source LMSYS-Chat-1M corpus (English only, no redacted/toxic content, 3-156 word queries, exactly two pairs), so results may not generalize to unfiltered or multilingual real-world logs.
- Hallucination categories are only assigned when a hallucination is detected; models must correctly predict the binary occurrence first before category accuracy is computed.

## Evidence (verbatim from paper)

> A binary label set {Hallucination, No Hallucination} is used. ... In cases where a hallucination occurs, annotators further classify the instance into one of three predefined categories, following Zhang et al. ([2025]): {Input-conflicting, Context-conflicting, Fact-conflicting} hallucination. Both hallucination occurrence and category are annotated at the query–response pair level.

## Citation

```bibtex
@misc{ren2025authenhallu,
  title={Detecting Hallucinations in Authentic LLM-Human Interactions},
  author={Ren et al. (2025)},
  year={2025},
  note={arXiv:2510.10539}
}
```

- arXiv: 2510.10539
