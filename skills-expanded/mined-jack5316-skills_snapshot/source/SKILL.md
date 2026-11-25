---
name: source
description: Find the best Substack, newsletter, blog, Twitter post, podcast, wiki, article, YouTube video on a particular subject. Use when user asks for content recommendations, wants to learn about a topic, or needs the best sources on any subject.
---

# Source Finder Skill (/source)

Discover the very best content sources on any topic. From Substack newsletters to YouTube videos, this skill helps you find high-quality recommendations across multiple content formats.

## Quick Start

```bash
python3 _scripts/source_finder.py "your topic here"
```

## What It Does

1. **Comprehensive Content Search** - Recommends sources across 7+ content categories
2. **Expert Curation** - AI-powered recommendations based on quality and relevance
3. **Structured Output** - Organized recommendations with clear descriptions
4. **Reading Path** - Suggested order to explore the content
5. **Quick Start** - Top 2-3 essential sources highlighted

## Content Categories

- **Substack Newsletters** - High-quality newsletters on Substack
- **Blogs** - Excellent personal and professional blogs
- **Twitter/X** - Insightful threads, posts, and accounts to follow
- **Podcasts** - Top podcasts and specific episode recommendations
- **Articles** - Long-form articles and essays
- **YouTube Videos** - Educational channels and videos
- **Wikis & References** - Comprehensive reference sources

## Options

- `topic`: The subject to find content sources for (required)
- `--save`: Save output to vault in Sources/ directory

## Examples

```bash
# Find sources on machine learning
python3 _scripts/source_finder.py "machine learning"

# Find sources on philosophy of mind
python3 _scripts/source_finder.py "philosophy of mind"

# Save results to vault
python3 _scripts/source_finder.py "product management" --save

# Find sources on personal knowledge management
python3 _scripts/source_finder.py "personal knowledge management" --save
```

## Output

- **Terminal**: Markdown-formatted content recommendations
- **Saved note**: `Sources/Source Guide - [topic] - YYYY-MM-DD.md`

## Why This Matters

- **Curated Quality** - Skip the noise, get directly to the best content
- **Time Savings** - Avoid endless searching and scrolling
- **Multi-format** - Find content in your preferred format
- **Learning Path** - Get guidance on where to start and what to explore next
- **Knowledge Building** - Build a comprehensive understanding of any topic efficiently
