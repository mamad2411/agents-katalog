---
name: semantic-scholar-paper-triage-starter
description: Rank a small set of candidate papers for triage using deterministic citation, recency, and query-overlap heuristics inspired by Semantic Scholar recommendation workflows.
---

# Semantic Scholar Paper Triage Starter

Use this starter to rank a small local paper set for quick screening.

## Run

```bash
python3 skills/scientific-knowledge/semantic-scholar-paper-triage-starter/scripts/run_semantic_scholar_paper_triage.py \
  --input skills/scientific-knowledge/semantic-scholar-paper-triage-starter/examples/candidate_papers.json \
  --query "single-cell RNA-seq atlas integration"
```

## Notes

- The starter is deterministic and local-first.
- It operates on already collected paper metadata rather than downloading full corpora.
- The output is a machine-readable JSON summary suitable for downstream routing or human review.
