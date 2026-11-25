---
name: askbench-eval
description: Evaluates LLMs' ability to detect intent deficiencies or overconfidence in user queries and request targeted clarification during multi-turn interactive QA. It measures how well models balance asking clarifying questions versus providing final answers, using rubric-based checkpoints to score clarification quality and final answer accuracy. Use when the user wants to benchmark on AskBench, HealthBench, or asks about evaluating this task. Reports single-turn accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2602.11199
  bibtex_key: zhao2026askbench
  confidence: high
---

# askbench-eval

> When and What to Ask: AskBench and Rubric-Guided RLVR for LLM Clarification — Zhao et al. (2026) (arXiv:2602.11199, 2026)

## What this evaluates

Evaluates LLMs' ability to detect intent deficiencies or overconfidence in user queries and request targeted clarification during multi-turn interactive QA. It measures how well models balance asking clarifying questions versus providing final answers, using rubric-based checkpoints to score clarification quality and final answer accuracy.

## Datasets

- **AskBench** — total ?; splits: test (-1)
- **HealthBench** — total 5000; splits: test (500)

## Metrics

- `single-turn accuracy` **(primary)** — range: [0, 1]
  - Standard exact-match or judge-verified correctness on the original QA pairs, computed over the full test set.
- `normalized rubric score` — range: [0, 1]
  - Average score across itemized rubric criteria for clarification quality and final answer correctness, normalized by the maximum possible rubric points.

## Input / output format

**Input**: Initial user query (containing either missing key information or false premises) and, in multi-turn settings, the accumulated dialogue history up to the current turn.

**Output**: A single turn response: either a clarification question or a final answer. The protocol mandates a final answer on the last turn of the dialogue.

## Scoring recipe

```python
def compute_metrics(predictions, golds, healthbench_convs, rubric, judge):
    # Single-turn accuracy
    acc = sum(1 for pred, gold in zip(predictions, golds) if judge_verifies(pred, gold)) / len(predictions)
    
    # HealthBench normalized rubric score
    rubric_scores = [judge_score_rubric(conv, rubric) for conv in healthbench_convs]
    norm_rubric = sum(rubric_scores) / len(rubric_scores)
    
    return acc, norm_rubric
```

## Common pitfalls

- The HealthBench rubric score is computed on a 500-sample subset using a different judge (A3B) than the original benchmark, making it incomparable to published HealthBench numbers.
- The fixed turn budget (typically 3) and mandatory final answer on the last turn may artificially penalize models that naturally require more turns to clarify.
- The judge simulates user responses during evaluation, so performance metrics reflect the judge's simulation fidelity as much as the policy's actual clarification ability.

## Evidence (verbatim from paper)

> For multi-turn benchmarks we roll out dialogues with a fixed turn budget (3 turns unless noted) and require a final answer on the last turn; the judge classifies replies as clarification vs. final answer, simulates user responses when needed, and scores final answers. We additionally report single-turn accuracy on the original QA benchmarks and include HealthBench (Arora et al., [2025]), a rubric-scored benchmark of 5,000 multi-turn healthcare conversations, to test open-ended settings without a single gold answer. To keep judge-based rubric scoring tractable, we evaluate on a randomly sampled subset of 500 HealthBench conversations and score them with our A3B judge (instead of the proprietary GPT-based judge used in the original HealthBench protocol); we report the HealthBench score (normalized rubric score), which is not directly comparable to HealthBench’s published numbers.

## Citation

```bibtex
@misc{zhao2026askbench,
  title={When and What to Ask: AskBench and Rubric-Guided RLVR for LLM Clarification},
  author={Zhao et al. (2026)},
  year={2026},
  note={arXiv:2602.11199}
}
```

- arXiv: 2602.11199
