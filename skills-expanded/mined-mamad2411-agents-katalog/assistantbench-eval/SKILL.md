---
name: assistantbench-eval
description: Evaluates web agents' ability to perform realistic, time-consuming multi-hop navigation and information retrieval tasks across the open web. It probes planning, memory, dynamic interaction, and robustness against hallucinations and navigation failures. Use when the user wants to benchmark on AssistantBench, or asks about evaluating this task. Reports Acc..
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2407.15711
  bibtex_key: yoran2024assistantbench
  confidence: high
---

# assistantbench-eval

> AssistantBench: Can Web Agents Solve Realistic and Time-Consuming Tasks? — Yoran et al. (2024) (arXiv:2407.15711, 2024)

## What this evaluates

Evaluates web agents' ability to perform realistic, time-consuming multi-hop navigation and information retrieval tasks across the open web. It probes planning, memory, dynamic interaction, and robustness against hallucinations and navigation failures.

## Datasets

- **AssistantBench** — total 214; splits: test (-1)

## Metrics

- `Acc.` **(primary)** — range: [0, 1]
  - Fraction of total tasks where the model's final answer is deemed correct by the evaluation script.
- `Ans. %` — range: percent
  - Percentage of tasks for which the model produces any answer, as opposed to abstaining due to navigation failure or inability to solve.
- `Prec.` — range: [0, 1]
  - Fraction of the model's provided answers that are factually correct or contain the required information.
- `EM` — range: percent
  - Percentage of tasks where the model's output string exactly matches the reference answer string.

## Input / output format

**Input**: A natural language task description requiring multi-step web navigation, information gathering from multiple websites, and dynamic interaction to produce a final answer.

**Output**: The model must execute web actions (clicks, searches, navigation) and ultimately output a final answer string. The evaluation script checks for the presence of an answer, its correctness, and exact string match.

## Scoring recipe

```python
def score(predictions, golds):
    correct = 0
    answered = 0
    correct_answers = 0
    exact_matches = 0
    for pred, gold in zip(predictions, golds):
        if pred is not None:
            answered += 1
            if is_correct(pred, gold):
                correct += 1
                correct_answers += 1
            if pred.strip() == gold.strip():
                exact_matches += 1
    acc = correct / len(golds)
    ans_rate = answered / len(golds)
    prec = correct_answers / answered if answered > 0 else 0
    em = exact_matches / len(golds)
    return {'accuracy': acc, 'answer_rate': ans_rate, 'precision': prec, 'exact_match': em}
```

## Common pitfalls

- Agents frequently abstain from answering when navigation fails, which drastically lowers accuracy but leaves answer rate high; evaluators must distinguish between failure to answer and incorrect answers.
- Precision is calculated only over answered tasks, not the full dataset, so a model that answers everything with low correctness will have high answer rate but low precision.
- Exact match scores are near zero for most models due to strict string matching requirements, making accuracy and precision more informative for real-world performance.

## Evidence (verbatim from paper)

> All systems perform poorly, with no system reaching more than 25% accuracy. Our agent, SPA, outperforms SeeAct by 20% in answer rate and 5 precision points, and has the best precision. When using the more strict exact match, we observe similar trends, and no model obtains more than 9.9% points.

## Citation

```bibtex
@misc{yoran2024assistantbench,
  title={AssistantBench: Can Web Agents Solve Realistic and Time-Consuming Tasks?},
  author={Yoran et al. (2024)},
  year={2024},
  note={arXiv:2407.15711}
}
```

- arXiv: 2407.15711
