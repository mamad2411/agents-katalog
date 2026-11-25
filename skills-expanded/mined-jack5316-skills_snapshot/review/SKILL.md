---
name: review
description: Run monthly or quarterly system review. Use when user asks for monthly review, quarterly review, system audit, or /review.
---

# System Review Skill

Orchestrates L5 Review layer at monthly (30-day) or quarterly (90-day) cadence. Optimizes system, upgrades skills, and performs Goodhart resistance audit.

## Usage

```bash
python3 _scripts/review_system.py [--monthly|--quarterly] [--save]
```

- `--monthly` (default): 30-day lookback — reflect, evolve, insights, skill-grab
- `--quarterly`: 90-day lookback — same + deeper synthesis
- `--save`: Write review note to vault

## What It Runs

| Step | Monthly | Quarterly |
|------|---------|-----------|
| Self-reflection | 30 days | 90 days |
| Self-evolution | 1 cycle | 1 cycle |
| Insight enhancement | ✓ | ✓ |
| Skill upgrade (skills.sh) | ✓ | ✓ |
| Meta synthesis | Brief | Extended |

## Output

- `Sources/Review - YYYY-MM-DD.md` — dated review note (when `--save`)
- `_logs/review_YYYYMMDD.log` — execution log

## Review Checklist (Manual)

The script automates data gathering. Consider manually:

- [ ] Prune stale sources (arxiv_topics.txt, subreddits.txt, twitter_accounts.txt)
- [ ] Archive completed projects
- [ ] Update PARA structure
- [ ] Goodhart check: Are metrics still serving curiosity?
