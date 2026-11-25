---
name: ai-brief
description: Morning brew of AI news worth your time. Fetches ArXiv, HN, Reddit, skills.sh, and world news APIs (NewsAPI, World News API, GNews) then synthesizes an AI-focused brief. Use when you want your daily AI digest, morning AI news, or /ai-brief.
---

# AI Brief (/ai-brief)

A morning brew of AI news — curated from ArXiv, Hacker News, Reddit, skills.sh, and world news APIs, filtered and synthesized into what's actually worth your time.

## Quick Start

```bash
python3 _scripts/ai_brief.py
```

## What It Does

1. **Fetches** (in sequence): ArXiv papers, HN top stories, Reddit (MachineLearning, LocalLLaMA, etc.), trending skills from skills.sh, world news via NewsAPI/World News API/GNews
2. **Synthesizes** with AI: filters to AI-relevant content, produces a concise brief with Must-Read, Research Highlights, Community Buzz, Tools & Skills, and a one-liner takeaway

## Options

| Flag | Description |
|------|--------------|
| `--skip-fetch` | Use today's existing digests only (don't run source scripts) |
| `--no-save` | Print to stdout only, don't save to vault |

## Examples

```bash
# Full run: fetch all sources + synthesize
python3 _scripts/ai_brief.py

# Best practice: run org-daily first, then reuse its outputs (no duplicate fetching)
python3 _scripts/org_skill.py --daily && python3 _scripts/ai_brief.py --skip-fetch

# AI-focused synthesis only (reuse today's existing digest files)
python3 _scripts/ai_brief.py --skip-fetch

# Preview without saving
python3 _scripts/ai_brief.py --no-save
```

## vs org-daily

| | org-daily | ai-brief |
|---|---|---|
| **Purpose** | Broad daily curation | AI-focused synthesis |
| **Sources** | ArXiv, HN, Reddit, TopHub, Twitter, agent news | ArXiv, HN, Reddit, skills.sh, world news APIs |
| **Output** | Raw digest notes in Sources/ | Single synthesized brief |
| **When** | Runs all sources in parallel | Run after org-daily with `--skip-fetch` |

## Output

- **Path:** `Sources/AI Brief - YYYY-MM-DD.md`
- **Format:** Must-Read → Research Highlights → Community Buzz → Tools & Skills → One-Liner
- Uses [[wikilinks]] for concepts

## Pipeline

Run via pipeline:

```bash
python3 _scripts/pipeline.py --run ai-brief
```

## Configuration

Uses existing config:
- `_scripts/arxiv_topics.txt` — ArXiv search topics (LLM, transformers, etc.)
- `_scripts/subreddits.txt` — Reddit (MachineLearning, LocalLLaMA, etc.)
- `_scripts/twitter_accounts.txt` — Optional; add AI accounts for Twitter section
