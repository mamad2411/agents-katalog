---
name: ai-writing-assistance-eval
description: Evaluates how source disclosure and perceived AI authorship influence human editing behavior and subsequent peer-review acceptance decisions for scientific abstracts. Use when the user wants to benchmark on CS-Conference-Abstracts, or asks about evaluating this task. Reports accept/reject decision.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2511.12529
  bibtex_key: hazra2025valueofaiassisted
  confidence: high
---

# ai-writing-assistance-eval

> Accepted with Minor Revisions: Value of AI-Assisted Scientific Writing — Hazra et al. (2025) (arXiv:2511.12529, 2025)

## What this evaluates

Evaluates how source disclosure and perceived AI authorship influence human editing behavior and subsequent peer-review acceptance decisions for scientific abstracts.

## Datasets

- **CS-Conference-Abstracts** — total 45; splits: test (45); repo https://github.com/skai-research/scientific-writing-assistance

## Metrics

- `accept/reject decision` **(primary)** — range: [0, 1]
  - Binary outcome determined by majority voting among three independent reviewers. An abstract is marked as accepted if it receives at least two Accept votes out of three.
- `edit_count` — range: count
  - Total number of character-level operations (insertions, deletions, substitutions) recorded by the custom FirePad editing interface during the author's revision process.

## Input / output format

**Input**: Research excerpt extracted from a published CS paper, paired with a provided abstract (either original human-written or AI-generated via GPT-4o), along with a source disclosure condition (with or without information about AI generation).

**Output**: Edited abstract text produced by the author, followed by a binary accept/reject decision from each of three independent reviewers.

## Scoring recipe

```python
def compute_decision(reviewer_votes):
    accepts = sum(reviewer_votes)
    return 1 if accepts >= 2 else 0

def compute_acceptance_rate(dataset):
    total = len(dataset)
    accepted = sum(compute_decision(ab['reviewer_votes']) for ab in dataset)
    return accepted / total if total > 0 else 0
```

## Common pitfalls

- Researchers may conflate the underlying scientific novelty of the paper with the quality of the abstract's writing, though the study attempts to isolate writing quality by using already published papers.
- Author editing effort is heavily influenced by performance-contingent financial incentives, which may not reflect natural, unpaid academic writing workflows.
- Copy-pasting abstracts to external AI tools or editors was a major protocol violation risk, requiring strict interface constraints to capture genuine keystroke-level edits.

## Evidence (verbatim from paper)

> We show each edited abstract to three independent reviewers to obtain the final accept/reject decision by majority voting.

## Citation

```bibtex
@misc{hazra2025valueofaiassisted,
  title={Accepted with Minor Revisions: Value of AI-Assisted Scientific Writing},
  author={Hazra et al. (2025)},
  year={2025},
  note={arXiv:2511.12529}
}
```

- arXiv: 2511.12529
