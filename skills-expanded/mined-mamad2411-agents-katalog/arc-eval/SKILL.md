---
name: arc-eval
description: Measures general fluid intelligence and developer-aware generalization by requiring systems to infer abstract transformation rules from few input-output grid demonstrations and apply them to novel test cases. It explicitly avoids measuring task-specific memorization or crystallized knowledge, focusing instead on abstraction, reasoning, and broad generalization under strict prior constraints. Use when the user wants to benchmark on Abstraction and Reasoning Corpus (ARC), or asks about evaluating this task. Reports fraction_of_tasks_solved.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1911.01547
  bibtex_key: chollet2019measure
  confidence: high
---

# arc-eval

> On the Measure of Intelligence — Chollet (2019) (arXiv:1911.01547, 2019)

## What this evaluates

Measures general fluid intelligence and developer-aware generalization by requiring systems to infer abstract transformation rules from few input-output grid demonstrations and apply them to novel test cases. It explicitly avoids measuring task-specific memorization or crystallized knowledge, focusing instead on abstraction, reasoning, and broad generalization under strict prior constraints.

## Datasets

- **Abstraction and Reasoning Corpus (ARC)** — total 1000; splits: train (400), public_eval (400), private_eval (200); repo github.com/fchollet/ARC

## Metrics

- `fraction_of_tasks_solved` **(primary)** — range: [0, 1]
  - Binary success per task: 1 if the system produces the exact correct output grid for all test examples in the task, 0 otherwise. The final score is the fraction of successfully solved tasks in the evaluation set.

## Input / output format

**Input**: A set of demonstration examples, each consisting of an input grid and an output grid (typically 3.3 on average), followed by the input grid of one or more test examples.

**Output**: An output grid constructed from scratch, specifying its dimensions, symbol placement, and layout that correctly transforms the test input grid according to the inferred rule.

## Scoring recipe

```python
score = 0
for task in evaluation_set:
    task_success = True
    for test_input in task.test_examples:
        predicted_output = model.generate_output(task.train_examples, test_input)
        if predicted_output != task.gold_output:
            task_success = False
            break
    if task_success:
        score += 1
final_score = score / len(evaluation_set)
```

## Common pitfalls

- Assuming the output grid dimensions are fixed or provided; the solver must determine height and width from scratch.
- Relying on memorization or pattern matching from the training set, as evaluation tasks are explicitly disjoint and designed to prevent developer-aware shortcuts.
- Ignoring the 3-trial limit per test example; systems must converge to the correct answer within this constraint and only receive binary feedback.

## Evidence (verbatim from paper)

> The task is successfully solved if the test-taker can produce the exact correct answer on all test examples for the task (binary measure of success). For each test example in a task, the test-taker (either human or machine) is allowed 3 trials. The score of an intelligent system on ARC is the fraction of tasks in the evaluation set that it can successfully solve.

## Citation

```bibtex
@misc{chollet2019measure,
  title={On the Measure of Intelligence},
  author={Chollet (2019)},
  year={2019},
  note={arXiv:1911.01547}
}
```

- arXiv: 1911.01547
