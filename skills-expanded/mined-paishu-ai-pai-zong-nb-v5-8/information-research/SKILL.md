---
name: information-research
description: Use for research, source discovery, source-backed synthesis, article/paper/repository analysis, market or product information gathering, freshness checks, and citation-aware summaries. Use when the user asks to look up, compare, investigate, analyze an external source, or produce a sourced research brief.
---

# Information Research

## Purpose

Produce source-backed research with clear freshness and evidence boundaries.

Use this for:
- Web/source research.
- Paper, article, or repository analysis.
- Market, product, company, tool, or standard comparisons.
- Current information, quotes, links, citations, and source freshness checks.

## Workflow

1. Clarify the research question only when scope materially affects the result.
2. Identify whether facts are current, versioned, high-stakes, or source-specific.
3. Use available web/search/repo/document tools when needed; prefer primary sources for technical claims.
4. Separate verified facts from inference.
5. Summarize findings around the user's decision, not around every source read.
6. Preserve links, dates, versions, and uncertainty when relevant.

## Required Checks

- Current or unstable facts must be verified with an available source.
- Technical documentation should use official docs, source code, specs, or papers before blogs.
- External repository analysis should record commit, branch, or snapshot when available.
- If browsing or source access is unavailable, state that the answer is limited to local or provided context.

## Avoid

- Do not present unverified memory or model recall as current fact.
- Do not cite sources that were not actually opened or inspected.
- Do not over-quote copyrighted text; summarize instead.
- Do not turn ordinary research into a durable skill unless the user asks to distill it.

## Output

For research briefs, include:

```markdown
结论：
- ...

依据：
- Source / date / version where relevant

不确定性：
- ...
```

