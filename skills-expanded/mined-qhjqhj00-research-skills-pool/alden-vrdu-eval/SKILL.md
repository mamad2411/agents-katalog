---
name: alden-vrdu-eval
description: Evaluates vision-language models' ability to actively navigate long, visually rich documents to gather evidence and answer complex queries. It probes multi-turn reasoning, retrieval accuracy, and the effectiveness of direct page-index access versus semantic search. Use when the user wants to benchmark on MMLongBench, LongDocURL, PaperTab, PaperText, FetaTab, DUDE-sub, or asks about evaluating this task. Reports GPT-4o–judged answer accuracy (Acc).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2510.25668
  bibtex_key: yang2025alden
  confidence: high
---

# alden-vrdu-eval

> ALDEN: Reinforcement Learning for Active Navigation and Evidence Gathering in Long Documents — Yang et al. (2025) (arXiv:2510.25668, 2025)

## What this evaluates

Evaluates vision-language models' ability to actively navigate long, visually rich documents to gather evidence and answer complex queries. It probes multi-turn reasoning, retrieval accuracy, and the effectiveness of direct page-index access versus semantic search.

## Datasets

- **MMLongBench** — total ?; splits: test (-1)
- **LongDocURL** — total ?; splits: test (-1)
- **PaperTab** — total ?; splits: test (-1)
- **PaperText** — total ?; splits: test (-1)
- **FetaTab** — total ?; splits: test (-1)
- **DUDE-sub** — total 960; splits: val (960)

## Metrics

- `GPT-4o–judged answer accuracy (Acc)` **(primary)** — range: [0, 1]
  - GPT-4o evaluates the correctness of the model's final generated answer against the ground truth reference.
- `trajectory-level retrieval recall (Rec)` — range: [0, 1]
  - Ratio of correctly retrieved pages to the total number of ground-truth relevant pages in the document.
- `trajectory-level retrieval precision (Pre)` — range: [0, 1]
  - Ratio of correctly retrieved pages to the total number of pages retrieved by the agent during the trajectory.
- `F1-score (F1)` — range: [0, 1]
  - Harmonic mean of trajectory-level precision and recall.
- `number of unique collected pages (#UP)` — range: other
  - Count of distinct pages accessed or retrieved by the agent across all reasoning-action turns.

## Input / output format

**Input**: User query paired with a long, multi-page visually rich document. The model receives page images and can iteratively perform semantic search or direct page-index fetch actions.

**Output**: A multi-turn sequence of reasoning steps and actions (search/fetch), terminating in a final natural language answer string.

## Scoring recipe

```python
# Answer Accuracy
acc = gpt4o_judge(model.final_answer, ground_truth)

# Trajectory Metrics
retrieved = set(agent_trajectory.retrieved_pages)
relevant = set(ground_truth.relevant_pages)

rec = len(retrieved & relevant) / len(relevant) if relevant else 0
pre = len(retrieved & relevant) / len(retrieved) if retrieved else 0
f1 = 2 * (pre * rec) / (pre + rec) if (pre + rec) > 0 else 0
up = len(retrieved)
```

## Common pitfalls

- GPT-4o is used as the sole judge for answer accuracy, which may introduce subjective bias or inconsistency compared to deterministic exact-match metrics.
- Retrieval metrics (Rec, Pre, F1) are computed at the trajectory level, meaning they depend on the full multi-turn interaction history and the maximum turn limit (T=6).
- Baselines are evaluated with different retriever backbones (single-vector vs. multi-vector); comparing relative improvements requires matching retriever configurations to ensure fairness.

## Evidence (verbatim from paper)

> The primary evaluation metric is GPT-4o–judged answer accuracy (Acc) on each benchmark. For finer-grained analysis of ALDEN’s components, we further assess navigation quality using trajectory-level retrieval recall (Rec), precision (Pre), F1-score (F1), and the number of unique collected pages (#UP).

## Citation

```bibtex
@misc{yang2025alden,
  title={ALDEN: Reinforcement Learning for Active Navigation and Evidence Gathering in Long Documents},
  author={Yang et al. (2025)},
  year={2025},
  note={arXiv:2510.25668}
}
```

- arXiv: 2510.25668
