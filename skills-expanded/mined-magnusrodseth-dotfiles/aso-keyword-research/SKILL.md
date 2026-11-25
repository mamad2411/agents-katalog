---
name: aso-keyword-research
description: App Store Optimization keyword research using the public iTunes Search API. Computes keyword popularity (5-100) and difficulty (1-100) scores based on RespectASO algorithms. Use when the user asks to research ASO keywords, find keyword opportunities, check keyword difficulty, analyze App Store competition, optimize App Store keywords, or find sweet spot keywords. Triggers on "ASO", "keyword research", "keyword difficulty", "keyword popularity", "App Store keywords", "App Store optimization keywords".
---

# ASO Keyword Research

Compute App Store keyword popularity and difficulty scores using the public iTunes Search API (no API key needed).

## Quick Start

```bash
# Single keyword
python3 scripts/aso_research.py "seed oil" --country us

# Batch analysis
python3 scripts/aso_research.py --batch "seed oil,allergen,food dye,preservative" --country us
```

## Output

Each keyword returns:
- **popularity** (5-100): Estimated search volume based on competitor landscape
- **difficulty** (1-100): How hard it is to rank for this keyword
- **verdict**: SWEET SPOT / HIGH COMPETITION / HIDDEN GEM / AVOID
- **top_5_apps**: Top competing apps with review counts and ratings

## Arthur's Golden Ratio

From the ASO Playbook: target keywords with **popularity > 20** and **difficulty < 50**.

| Verdict | Popularity | Difficulty | Action |
|---------|-----------|------------|--------|
| SWEET SPOT | >= 20 | < 50 | Target these |
| HIDDEN GEM | < 20 | < 50 | Use if relevant, low volume |
| HIGH COMPETITION | >= 20 | >= 50 | Avoid unless you have traction |
| AVOID | < 20 | >= 50 | Skip entirely |

## ASO Rules (from Arthur's Playbook)

- Never repeat keywords across title, subtitle, and keyword field
- Use singular forms only (Apple handles plurals)
- Keyword field is 100 characters max, comma-separated
- Check both popularity AND revenue of top 5 apps (avoid vanity keywords)
- Iterate keywords weekly (scores shift over time)

## Country Codes

Common: `us`, `gb`, `de`, `fr`, `br`, `jp`, `kr`, `no`, `se`, `dk`, `es`, `it`, `au`, `ca`

## How Scores Are Computed

Based on the open-source RespectASO project (AGPL-3.0). Both scores are derived entirely from iTunes Search API results (25 competitor apps per keyword).

**Popularity** uses 6 signals: result count, leader strength (top app reviews), title match density, market depth (median reviews), keyword specificity penalty (multi-word penalty), exact phrase match bonus.

**Difficulty** uses 7 weighted factors: rating volume (30%), dominant players (20%), review velocity (10%), rating quality (10%), market age (10%), publisher diversity (10%), title relevance (10%). Post-processing applies caps for small result sets and weak leaders.

## Rate Limiting

The iTunes Search API has no authentication but rate limits apply. The script sleeps 2 seconds between requests. For batch analysis of 10+ keywords, expect ~20-30 seconds.
