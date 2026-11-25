---
name: deep-research
description: Produces thorough, multi-source cited research reports from web and news without paid APIs. Use when the user asks for deep research, landscape analysis, competitive intel, market research, or a cited report needing broad source coverage.
---

# deep-research

Multi-source web research that ends in a structured, fully cited report - not a summary of one page.

## Core Principles

- Every factual claim gets an inline citation. No citation, no claim.
- Cross-reference: two independent sources before treating something as established. Single-source claims get flagged as unverified.
- Prefer sources from the last 12 months. Note when older data is the only data available.
- Acknowledge gaps explicitly. Say "insufficient data found" rather than filling holes.
- No hallucination. If search turns up nothing credible, report that and stop.

## When to Use

- User asks for deep research, a research report, or "look into X thoroughly"
- Landscape, market, competitive, or technology scans needing breadth
- Questions where a quick answer would be irresponsible (policy, pricing, regulation, fast-moving tech)
- Deliverable is a saved report, not chat-only bullets

## When NOT to Use

- User wants a one-line answer or a single-source lookup
- The question is about code in this repo (read the codebase instead)
- Paid or authenticated sources are required and unavailable
- Real-time data (live prices, scores, stock tickers) — search results may be stale

## Tooling

This skill needs two capabilities, not two specific tools:

1. **Web search** — to discover sources.
2. **Page fetch** — to read a source in full.

Use whatever the host agent exposes for each. Discover them at runtime (list your available tools and pick the closest match) rather than assuming a fixed name. Common equivalents: search → `WebSearch` / `web_search` / `search_web` / `tavily`; fetch → `WebFetch` / `web_fetch` / `fetch_web_content`. If no search tool is configured, fall back to a shell-based search (e.g. a DuckDuckGo CLI) or tell the user a search backend is required before proceeding.

## Implementation Guide

Copy this checklist and track progress:

```
- [ ] Step 1: Scope the question
- [ ] Step 2: Decompose into sub-questions
- [ ] Step 3: Search broadly (15–30 sources)
- [ ] Step 4: Deep-read key sources (3–5)
- [ ] Step 5: Synthesize report
- [ ] Step 6: Save and deliver
```

**Step 1: Scope.** Ask 1–2 clarifying questions only when scope, audience, or time horizon is ambiguous. Otherwise state your assumptions in the report's methodology section.

**Step 2: Decompose.** Break the topic into 3–5 sub-questions. Each sub-question gets its own search pass.

**Step 3: Search.** Use whatever web-search capability your environment
provides to discover sources — the built-in web search tool if you have one
(named `WebSearch`, `web_search`, `search_web`, `tavily`, `brave-search`, or similar), otherwise a search MCP server or a shell/HTTP search command. Run separate queries per sub-question plus variant phrasings. Prioritize, in order:

1. Official docs, government sites, standards bodies
2. Academic papers and institutional research
3. Reputable news and industry analysts
4. Primary sources (company blogs, SEC filings, release notes)
5. Community sources only when nothing better exists — label them as such

Aim for 15–30 distinct sources across web and news. Track title, URL, date,
and one-line relevance as you go.

**Step 4: Deep-read.** Pick 3–5 sources that carry the most weight. Fetch full page content using whatever fetch capability you have — a built-in page-fetch tool (named `WebFetch`, `web_fetch`, `fetch_web_content`, `page-dump`, or similar), a fetch MCP server, or a shell command (`curl`, `wget`) as a last resort. Extract quotes, numbers, and definitions - not just headlines.

**Step 5: Synthesize.** Write the report using the template below. Group findings by theme, not by source order. Inline citations as markdown links: `[claim text](url)`.

**Step 6: Save.** Write to `research/[slug]/report.md` in the project root. Slug = lowercase, hyphenated topic (e.g. `ai-coding-assistants-2026`). Deliver a short summary in chat with the file path.

## Report Template

```markdown
# [Topic Title]

## Executive Summary
[3–5 sentences. Highest-confidence findings only.]

## [Themed Section 1]
[Findings with inline [citations](url). Flag unverified claims.]

## [Themed Section 2]
...

## Key Takeaways
- [Actionable or decision-relevant bullet]

## Sources
| Source | Date | Type | Notes |
|--------|------|------|-------|
| [Title](url) | YYYY-MM | official / academic / news / community | one line |

## Methodology
[Sub-questions searched, date of research, assumptions made, known gaps.]
```

## Review Checklist

Before delivering:

- [ ] Every factual sentence has a citation or an explicit "unverified" flag
- [ ] At least two sources support each major conclusion
- [ ] Recency noted where it matters; stale data flagged
- [ ] Gaps and conflicts between sources acknowledged
- [ ] Report saved to `research/[slug]/report.md`
- [ ] No claims beyond what sources support
