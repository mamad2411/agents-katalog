---
name: gene
description: Manage the gene pool — compounding library of proven skill improvement strategies. Use when user asks to view genes, check gene pool, apply a gene, or /gene.
---

# Gene Pool (/gene)

Implements EvoMap's Genome Evolution Protocol (GEP) locally: a content-addressable library
of proven improvement strategies that grows more powerful with each skill evolution cycle.

Every successful `skill-evolve` improvement extracts a Gene — the pattern of what was broken
and how it was fixed. Future improvements try matching genes first (free, instant) before
falling back to AI generation. Confidence compounds: each re-application increases the gene's
trust score.

**Gene types** (EvoMap-inspired):
- `repair` — fixes missing structure (Output section, code blocks, short descriptions)
- `optimize` — improves trigger clarity and invocation precision
- `innovate` — rewrites for clarity when no structural issue is detected

## Usage

```bash
# View all genes in the pool (sorted by confidence)
python3 _scripts/skill_evolution.py gene list

# Filter by type
python3 _scripts/skill_evolution.py gene list --type repair

# Gene pool statistics (most proven gene, average confidence)
python3 _scripts/skill_evolution.py gene stats

# Manually apply a specific gene to a skill
python3 _scripts/skill_evolution.py gene apply --id <gene_id> --skill <skill_name>
```

Genes are automatically extracted and applied during `/skill skill-evolve evolve`. You rarely
need to invoke this skill directly — the compounding happens in the background.

## Output

`_logs/gene_pool.json` — the growing library of proven strategies (content-addressable by SHA256)
