---
name: reviewsearch
description: Search 200k+ ML/NLP/CV peer reviews (ICLR/ICML/NeurIPS/COLM) with their author rebuttals. Use when the user wants real examples of reviewer concerns, how a kind of paper gets critiqued, or how authors rebutted — e.g. "find reviews asking for significance tests", "how did papers rebut novelty concerns", "what weaknesses do reviewers raise about diffusion models".
---

# ReviewSearch

Search a corpus of **205,988 peer reviews** (with author rebuttals) from ICLR / ICML / NeurIPS / COLM,
served by the ReviewSearch hybrid-search API.

## When to use

Reach for this when the user wants **real peer-review evidence**: what reviewers criticize about a kind
of paper, examples of a specific concern, or how authors rebutted a critique. Not for searching paper
*content* — this searches *reviews*.

## How to search

Run the bundled script (Python 3, no dependencies). **Paths here are relative to this skill's own
directory**, the one this SKILL.md was loaded from, so they resolve in any host that discovers skills:

```bash
python "<this skill dir>/scripts/search_reviews.py" "<query>" [options]
```

Options: `--top-k N` (default 10), `--accepted-only`, `--year-min YYYY`, `--year-max YYYY` (corpus spans 2023–2026).

Example:

```bash
python "<this skill dir>/scripts/search_reviews.py" \
  "reviews asking for a statistical significance test" --top-k 5 --accepted-only
```

## Writing good queries

- Queries are **English** and work best as **concern-style natural language**, e.g.
  "missing ablation on learning rate", "reviewers doubting reproducibility",
  "papers criticized for weak baselines".
- The primary search target is each review's **concern** text (weaknesses + questions).

## Reading results

The script prints JSON: `{ count, results: [...] }`. Each result has:
- `venue`, `year`, `title`, `decision` (Accept/Reject variants)
- `summary` — the reviewer's summary of the paper
- `concern` — the reviewer's weaknesses + questions (what to focus on)
- `rebuttal` — the author's response (every result has one)
- `score` — relevance

When you present results to the user, cite the venue/year and note the source (see attribution below).

## Notes

- The API is a free demo and may **cold-start** (take a minute) after being idle — if a call times out,
  wait ~1 minute and retry once.
- Point at a different backend with the `RS_API_URL` env var if needed.

## Attribution

Data: peer reviews from **OpenReview** (ICLR / ICML / NeurIPS / COLM), licensed **CC-BY-4.0**.
