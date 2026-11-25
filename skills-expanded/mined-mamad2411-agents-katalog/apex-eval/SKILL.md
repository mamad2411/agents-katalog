---
name: apex-eval
description: Evaluates models on complex, real-world professional reasoning tasks across four domains (investment banking, management consulting, big law, primary care). It probes document analysis, multi-step reasoning, and domain-specific judgment under practical constraints. Use when the user wants to benchmark on APEX-v1.0, or asks about evaluating this task. Reports autograded scores.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2509.25721
  bibtex_key: vidgen2025apex
  confidence: high
---

# apex-eval

> The AI Productivity Index (APEX) — Vidgen et al. (2025) (arXiv:2509.25721, 2025)

## What this evaluates

Evaluates models on complex, real-world professional reasoning tasks across four domains (investment banking, management consulting, big law, primary care). It probes document analysis, multi-step reasoning, and domain-specific judgment under practical constraints.

## Datasets

- **APEX-v1.0** — total 200; splits: test (200); repo https://github.com/Mercor-Intelligence/apex-evals

## Metrics

- `autograded scores` **(primary)** — range: percent
  - Average of the median LM-judge rubric scores across all tasks, reported as a percentage. Each task response is scored by an LM judge (Gemini 2.5 Flash) using detailed rubrics.

## Input / output format

**Input**: Domain-specific professional reasoning prompts requiring document analysis and multi-step decision making.

**Output**: Free-form text responses, typically ranging from ~3,000 to ~30,000 characters.

## Scoring recipe

```python
scores = []
for task in tasks:
    responses = [model.generate(task.prompt) for _ in range(3)]
    task_scores = [lm_judge.score(response, rubric) for response in responses]
    scores.append(median(task_scores))
return mean(scores) * 100
```

## Common pitfalls

- Model non-determinism causes significant score variance across runs (mean range ~11.9 percentage points over 3 attempts).
- Reporting the maximum score across runs (pass@3) artificially inflates results for highly variable models.
- Response length varies drastically across models, which may confound LM judge evaluations if not normalized.

## Evidence (verbatim from paper)

> We collect responses from each model three times for each prompt and score them with an LM judge (see below). ... We use the median of the three scored responses for our leaderboard and analysis. ... Pairwise win rate is based on a head-to-head comparison of models’ autograded scores on each task.

## Citation

```bibtex
@misc{vidgen2025apex,
  title={The AI Productivity Index (APEX)},
  author={Vidgen et al. (2025)},
  year={2025},
  note={arXiv:2509.25721}
}
```

- arXiv: 2509.25721
