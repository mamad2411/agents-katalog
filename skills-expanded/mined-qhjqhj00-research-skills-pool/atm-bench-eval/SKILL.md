---
name: atm-bench-eval
description: Evaluates long-term personalized referential memory QA by testing a model's ability to retrieve and reason over multi-source, multimodal personal data spanning years. It probes conflict-aware aggregation, temporal-visual grounding, and accurate reference resolution across different question types. Use when the user wants to benchmark on ATM-Bench, or asks about evaluating this task. Reports QS.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2603.01990
  bibtex_key: mei2026accordingtome
  confidence: high
---

# atm-bench-eval

> According to Me: Long-Term Personalized Referential Memory QA — Mei et al. (2026) (arXiv:2603.01990, 2026)

## What this evaluates

Evaluates long-term personalized referential memory QA by testing a model's ability to retrieve and reason over multi-source, multimodal personal data spanning years. It probes conflict-aware aggregation, temporal-visual grounding, and accurate reference resolution across different question types.

## Datasets

- **ATM-Bench** — total ?; splits: test (-1), test-hard (-1); repo https://github.com/JingbiaoMei/ATM-Bench

## Metrics

- `QS` **(primary)** — range: [0, 100]
  - Overall question-answering score, computed as a composite or average across Number, Recall-list, and Open-ended question types. The No-Evidence baseline contributes ~0.2% to this score.
- `R@10` — range: [0, 100]
  - Retrieval recall at top-10, measuring the fraction of queries where the gold memory item appears in the top-10 retrieved evidence items.
- `Joint@10` — range: [0, 100]
  - Joint metric measuring the fraction of queries where both the correct memory item is retrieved in the top-10 and the final answer is correct.
- `N/R/O` — range: [0, 100]
  - Accuracy for Number, Recall-list, and Open-ended questions respectively. Open-ended answers are evaluated using an LLM-based judge (GPT-5-mini).

## Input / output format

**Input**: A natural language question, retrieved memory items (text), and corresponding raw visual inputs (images/videos, capped at 8 frames per video).

**Output**: A natural language answer string. Number/Recall-list questions expect exact matches or structured lists; Open-ended questions are free-text and scored by an LLM judge.

## Scoring recipe

```python
def compute_metrics(predictions, golds, retrieved_items):
    # Per-type accuracy
    n_acc = exact_match_or_llm_judge(predictions['N'], golds['N'])
    r_acc = exact_match_or_llm_judge(predictions['R'], golds['R'])
    o_acc = llm_judge_accuracy(predictions['O'], golds['O'])
    qs = (n_acc + r_acc + o_acc) / 3.0
    # Retrieval recall
    r_at_10 = sum(1 for g, ret in zip(golds, retrieved_items) if g in ret[:10]) / len(golds) * 100
    # Joint retrieval + answer accuracy
    joint_at_10 = sum(1 for p, g, ret in zip(predictions, golds, retrieved_items) if (g in ret[:10]) and is_correct(p, g)) / len(golds) * 100
    return {'QS': qs, 'R@10': r_at_10, 'Joint@10': joint_at_10, 'N': n_acc, 'R': r_acc, 'O': o_acc}
```

## Common pitfalls

- Assuming agentic answerers consistently outperform single-pass methods; the paper shows gains on the main set do not transfer to the hard set.
- Using multimodal embedding models for retrieval can degrade performance due to visual token dilution of critical metadata like timestamps and locations.
- Ignoring the No-Evidence baseline (~0.2% QS), which accounts for chance/abstention answers and must be contextualized when interpreting raw scores.

## Evidence (verbatim from paper)

> We report results by question type (Number / Recall-list / Open-ended questions, denoted as N/R/O), the overall QS score, retrieval recall (R@10), and the joint metric (Joint@10).

## Citation

```bibtex
@misc{mei2026accordingtome,
  title={According to Me: Long-Term Personalized Referential Memory QA},
  author={Mei et al. (2026)},
  year={2026},
  note={arXiv:2603.01990}
}
```

- arXiv: 2603.01990
