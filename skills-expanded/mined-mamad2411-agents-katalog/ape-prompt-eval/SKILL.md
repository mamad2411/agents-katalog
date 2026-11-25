---
name: ape-prompt-eval
description: Evaluates the effectiveness of automatically generated prompts (instructions) from the APE framework compared to human-designed or baseline prompts across various natural language processing tasks. Use when the user wants to benchmark on Instruction Induction, BIG-Bench Instruction Induction (BBII), MultiArith, GSM8K, or asks about evaluating this task. Reports zero-shot execution accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2211.01910
  bibtex_key: zhou2022large
  confidence: high
---

# ape-prompt-eval

> Large Language Models Are Human-Level Prompt Engineers — Zhou et al. (2022) (arXiv:2211.01910, 2022)

## What this evaluates

Evaluates the effectiveness of automatically generated prompts (instructions) from the APE framework compared to human-designed or baseline prompts across various natural language processing tasks.

## Datasets

- **Instruction Induction** — total 24; splits: test (-1)
- **BIG-Bench Instruction Induction (BBII)** — total 21; splits: test (-1)
- **MultiArith** — total ?; splits: test (-1)
- **GSM8K** — total ?; splits: test (-1)

## Metrics

- `zero-shot execution accuracy` **(primary)** — range: percent
  - Percentage of correctly predicted answers when the model generates a response to a task using only the generated instruction, without in-context examples.
- `few-shot in-context test accuracy` — range: percent
  - Percentage of correctly predicted answers when the generated instruction is prepended to in-context demonstration examples.
- `normalized preferred metric` — range: percent
  - Score normalized to [0, 100] where 100 equals human expert performance and 0 equals random guessing. Scores can be negative if performance is worse than random guessing on multiple-choice tasks.

## Input / output format

**Input**: Task description or demonstration examples, optionally preceded by an automatically generated instruction/prompt.

**Output**: Model's predicted answer or label for the given input.

## Scoring recipe

```python
def compute_accuracy(predictions, golds):
    return sum(p == g for p, g in zip(predictions, golds)) / len(golds)

def compute_normalized_bbii(raw_score):
    # Map raw performance to 0-100 scale where 100=human baseline, 0=random
    return normalize_to_human_baseline(raw_score)
```

## Common pitfalls

- Generated instructions may overfit to zero-shot evaluation, causing performance drops when in-context examples are added.
- Prompts are highly model-specific; instructions generated for InstructGPT do not transfer well to GPT-3 or vice versa.
- Some instructions can 'hack' evaluation by inducing trivial solutions that match gold labels but fail on intended semantics (e.g., Rhymes task).

## Evidence (verbatim from paper)

> We evaluate APE-generated instructions in the few-shot in-context learning, where we insert the instruction before the in-context demonstrations. Those instructions are selected based on zero-shot execution accuracy... We report the normalized preferred metric defined in Srivastava et al. (2022). Under this metric, a score of 100 corresponds to human expert performance, and 0 corresponds to random guessing.

## Citation

```bibtex
@misc{zhou2022large,
  title={Large Language Models Are Human-Level Prompt Engineers},
  author={Zhou et al. (2022)},
  year={2022},
  note={arXiv:2211.01910}
}
```

- arXiv: 2211.01910
