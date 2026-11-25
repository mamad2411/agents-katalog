---
name: product-hunt
description: Find the best shiny new tools from Product Hunt. Fetches the daily feed, curates top products with AI, and saves a digest to your vault. Use when you want to discover new tools, check what's trending on Product Hunt, or /product-hunt.
---

# Product Hunt Skill (/product-hunt)

Find the **best shiny new tools** from [Product Hunt](https://www.producthunt.com). Fetches the daily feed, parses top products, and uses AI to curate the most valuable tools for dev work, AI workflows, productivity, and knowledge management.

## Quick Start

```bash
# Fetch and curate (AI picks the best)
python3 _scripts/product_hunt.py

# Raw list, no AI
python3 _scripts/product_hunt.py --no-ai

# Print to terminal instead of saving
python3 _scripts/product_hunt.py --print
```

## Options

- `-c, --count N` — Max products to fetch (default: 25)
- `--no-ai` — Skip AI curation; output raw list only
- `--print` — Print to stdout instead of saving to vault

## Examples

```bash
# Default: fetch 25 products, AI curate, save to Sources/
python3 _scripts/product_hunt.py

# More products, raw list
python3 _scripts/product_hunt.py --count 40 --no-ai

# Preview without saving
python3 _scripts/product_hunt.py --print
```

## Output

- **Terminal**: Progress and final content
- **Saved note** (default): `Sources/Product Hunt Digest - YYYY-MM-DD.md`

## What It Does

1. **Fetches** — Product Hunt Atom feed (no API key required)
2. **Parses** — Product name, tagline, maker, URL
3. **Curates** — AI selects top picks for dev tools, AI workflows, productivity
4. **Saves** — Markdown digest with [[wikilinks]] for Obsidian

## Related

- `/skill-grab` — Best skills from skills.sh
- `/hn` — Hacker News digest
- `/ai-brief` — Morning AI news brew
