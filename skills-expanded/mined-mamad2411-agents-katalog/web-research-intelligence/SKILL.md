---
name: web-research-intelligence
description: Use when searching the web, scraping content, or extracting information from online sources. Use when you need to find current documentation, compare tools, verify facts via web sources, or gather data from multiple websites.
---

# Web Research Intelligence

## Overview

Tactical techniques for finding, extracting, and evaluating information from the web efficiently. Core principle: **search like a researcher, not like a user** — use advanced query patterns, evaluate source credibility, and extract structured data.

## When to Use

- Need current information not in training data (post-cutoff)
- Comparing tools, libraries, or frameworks with real data
- Verifying a claim found in conversation
- Need official documentation, API references, or source code
- Topic requires data from multiple websites

**When NOT to use:** Question is fully answerable from internal knowledge with high confidence; user explicitly wants opinion or creative output without external validation.

## Query Engineering

### Query Patterns

| Pattern | Example | When to Use |
|---------|---------|-------------|
| **Exact phrase** | `"behavioral cloning" RLHF 2025` | Finding specific terms or paper titles |
| **Exclude noise** | `LLM hallucination mitigation -survey -review` | Filtering out meta-content when you want primary sources |
| **Site-restricted** | `site:github.com Qdrant vs Pinecone benchmark` | Finding discussions, issues, or code comparisons |
| **Filetype** | `filetype:pdf "attention is all you need"` | Finding original papers or whitepapers |
| **Date-bounded** | `LangChain agent tutorial after:2024-01-01` | Ensuring recency (when search engine supports it) |
| **OR expansion** | `(RAG OR "retrieval augmented generation") best practices 2025` | Capturing synonymous terms |

### Multi-Angle Search

For any topic, search from **at least 3 angles**:

1. **Official source**: documentation, GitHub repo, company blog
2. **Independent evaluation**: benchmark, comparison article, HN/Reddit discussion
3. **Critical perspective**: limitations, alternatives, "why not X"

**Rule:** If your first 3 queries return the same 2-3 sources, your queries are too narrow. Broaden or rephrase.

## Source Evaluation

### Credibility Tiers

| Tier | Examples | Trust Level |
|------|----------|-------------|
| **Primary** | Official docs, peer-reviewed papers, source code | Highest — verify claims here |
| **Secondary** | Technical blogs by known authors, conference talks | High — good for interpretation |
| **Tertiary** | Tutorial sites, Medium, general tech blogs | Medium — use for orientation only |
| **Discourse** | HN, Reddit, Stack Overflow, GitHub issues | Variable — good for real-world pain points |
| **Marketing** | Vendor landing pages, press releases | Lowest — verify all claims independently |

### Quick Credibility Check

Before extracting information, ask:

1. **Who wrote this?** Are they affiliated with a product they're praising?
2. **When was this published?** Is it still relevant?
3. **What's the evidence?** Benchmarks with methodology, or hand-wavy claims?
4. **Who disagrees?** Search "[topic] problems" or "[tool] limitations"

## Content Extraction

### From Web Pages

When fetching content:

- **Skip:** Navigation, ads, cookie banners, footer links
- **Keep:** Headings, body text, code blocks, tables, citations
- **Preserve:** URLs, author names, publication dates

### From Documentation Sites

- Look for "Getting Started", "Architecture", "API Reference", "Changelog"
- Check version number — ensure it matches what you're advising
- Note deprecation warnings or "migrating from X" guides

### From GitHub

- Check `README.md` for quickstart and features
- Check `CHANGELOG.md` or releases for recent changes
- Check issues with labels `bug`, `help wanted` for maturity signals
- Check `stars`, `last commit date`, `contributor count` for health

## Verification Techniques

### Cross-Reference Check

For any important claim, find **2+ independent sources**:

```
Claim: "Library X is 3x faster than Library Y"
Source A: Benchmark by author of X → [needs confirmation]
Source B: Independent benchmark by unrelated team → [stronger]
Source C: GitHub issue where user confirms in production → [real-world]
```

### Temporal Check

- Check if the source has an update date
- For GitHub repos, check `last commit` and `latest release`
- For documentation, check if there's a version selector
- For benchmarks, check what versions were tested

### Bias Check

- Author works for company selling the product → flag as potential bias
- Blog post is "sponsored" or "partner content" → lower credibility
- Only positive claims with no limitations mentioned → suspicious

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Trusting the first result | Always check 2-3 sources for major claims |
| Ignoring date | Check "last updated" — especially for fast-moving tech |
| Confusing blog opinion with fact | Label opinions as such; separate from benchmarks |
| Missing the official source | Always find docs/README before relying on tutorials |
| Not checking for bias | Note author affiliations and sponsorships |
| Extracting without context | Preserve caveats and limitations from the original |

## Quick Reference: Search Strategy by Goal

| Goal | Primary Source | Secondary Source | Verification |
|------|---------------|------------------|--------------|
| Compare tools | Official docs + GitHub | Independent benchmarks | HN/Reddit real-world experience |
| Learn how to use X | Official tutorial | Blog post with working code | Run the code yourself if possible |
| Verify a claim | Original paper/source | Independent reproduction | Check methodology details |
| Find latest version | GitHub releases | Changelog | PyPI/npm registry |
| Understand limitations | GitHub issues | Critical blog posts | Try it yourself |
