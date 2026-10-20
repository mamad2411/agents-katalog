---
name: alpsbench-eval
description: AlpsBench evaluates the full lifecycle of LLM personalization, including extracting structured memories from dialogue, dynamically updating them, retrieving relevant memories under distractors, and utilizing them to generate aligned responses across dimensions like persona awareness, preference following, and emotional intelligence. Use when the user wants to benchmark on AlpsBench, or asks about evaluating this task. Reports F1 score (exact match).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2603.26680
  bibtex_key: xiao2026alpsbench
  confidence: high
---

# alpsbench-eval

> AlpsBench: An LLM Personalization Benchmark for Real-Dialogue Memorization and Preference Alignment — Xiao et al. (2026) (arXiv:2603.26680, 2026)

## What this evaluates

AlpsBench evaluates the full lifecycle of LLM personalization, including extracting structured memories from dialogue, dynamically updating them, retrieving relevant memories under distractors, and utilizing them to generate aligned responses across dimensions like persona awareness, preference following, and emotional intelligence.

## Datasets

- **AlpsBench** — total 2500; splits: test (-1); repo https://github.com/ThisIsCosine/AlpsBench

## Metrics

- `F1 score (exact match)` **(primary)** — range: [0, 1]
  - Harmonic mean of precision and recall for exact matches between extracted structured memories and human-annotated ground truth. Measures coverage and quality of extracted attributes (ID, Type, Label, Value, Confidence).
- `Action accuracy` — range: [0, 1]
  - Percentage of correctly predicted update actions (Retention, Addition, Modification) compared to human-annotated ground truth.
- `Recall` — range: [0, 1]
  - Standard recall measuring whether the model correctly retrieves the human-labeled positive memory from a candidate set containing one positive and several randomly sampled negative memories.
- `LLM-as-a-Judge score` — range: [1, 5]
  - Binary (0/1) scores for Persona Awareness, Preference Following, Virtual-Reality Awareness, and Constraint Following based on LLM judge criteria. Emotional Intelligence uses a 1–5 scale from an LLM reward model.

## Input / output format

**Input**: Task 1: Dialogue history H. Task 2: Existing memories M + new dialogue H_new. Task 3: Positive memory M_pos, negative memories M_neg, query Q. Task 4: Dialogue history H + query Q.

**Output**: Task 1: List of structured memories (ID, Type, Label, Value, Confidence). Task 2: Updated memories M_new + action type Act in [Retention, Addition, Modification]. Task 3: Retrieved memory M_pos. Task 4: Generated response R.

## Scoring recipe

```python
def score_alpsbench(predictions, gold):
    # Task 1: F1
    f1 = exact_match_f1(predictions['extracted'], gold['extracted'])
    # Task 2: Action Accuracy
    acc = accuracy(predictions['actions'], gold['actions'])
    # Task 3: Recall
    recall = 1.0 if predictions['retrieved'] == gold['positive'] else 0.0
    # Task 4: LLM Judge
    scores = llm_judge.evaluate(predictions['response'], dimensions=['PA','PF','VRA','CF','EI'])
    # PA/PF/VRA/CF: binary 0/1; EI: 1-5 scale
    return {'f1': f1, 'action_acc': acc, 'recall': recall, 'judge_scores': scores}
```

## Common pitfalls

- Emotional Intelligence is scored on a 1–5 scale via an LLM reward model, while other utilization dimensions use binary 0/1 judgments, requiring careful aggregation and normalization.
- Task 3 retrieval uses randomly sampled negative samples, meaning recall scores can fluctuate based on distractor difficulty and sampling strategy.
- Semantic similarity for Task 1 relies on an external LLM, introducing potential judge bias and variability across runs.

## Evidence (verbatim from paper)

> Specifically, we calculate the F1 score for exact matches, measuring both the coverage and quality of the memories relative to the ground truth. Furthermore, we leverage an LLM to assess semantic similarity, ensuring a more nuanced evaluation beyond lexical matching. ... We use the widely recognized metric of recall to report the evaluation results of this task.

## Citation

```bibtex
@misc{xiao2026alpsbench,
  title={AlpsBench: An LLM Personalization Benchmark for Real-Dialogue Memorization and Preference Alignment},
  author={Xiao et al. (2026)},
  year={2026},
  note={arXiv:2603.26680}
}
```

- arXiv: 2603.26680
