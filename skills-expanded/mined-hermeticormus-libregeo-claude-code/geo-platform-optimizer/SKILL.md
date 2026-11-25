---
name: geo-platform-optimizer
description: "Per-platform AI search optimization for Google AI Overviews, ChatGPT web search, Perplexity, Gemini, and Bing Copilot: applies each platform's source-selection rules, checklist, and 0-100 readiness score, then writes a prioritized action plan. Use when the user wants to be cited on a specific AI search platform, or to compare readiness across them."
version: 1.0.0
author: geo-seo-claude
tags: [geo, ai-search, platform-optimization, chatgpt, perplexity, gemini, aio]
---

# GEO Platform Optimizer

Only **11% of domains** are cited by BOTH ChatGPT and Google AI Overviews for the same query. Each AI search platform uses different indexes, ranking logic, and source preferences. Platform-specific optimization is foundational to any serious GEO strategy.

## How to Use

1. Collect target URL and the site's primary topic/industry
2. Open `platforms.md` (this skill directory) — it holds the 5 platform sections, each with `How X Selects Sources` rules + 10-item optimization checklist + 0-100 scoring rubric
3. Run each platform's checklist against the site
4. Score each platform on its rubric (0-100)
5. Generate `GEO-PLATFORM-OPTIMIZATION.md` using the output template below

## Platforms Covered

Full rules + checklists + rubrics live in `platforms.md`:

1. **Google AI Overviews (AIO)** — top-10 organic gateway, question-headed Q&A, tables/lists, FAQ pattern
2. **ChatGPT Web Search** — Bing-indexed, Wikipedia/Wikidata entity-driven, authoritative & long-form
3. **Perplexity AI** — Reddit-heavy, community validation, freshness, original research
4. **Google Gemini** — Google ecosystem (YouTube, GBP, Knowledge Graph, Schema.org), multi-modal
5. **Bing Copilot** — Bing WMT + IndexNow, LinkedIn/GitHub/Microsoft Learn, fast load

Do NOT paraphrase or substitute the per-platform rules — read them verbatim from `platforms.md` before scoring.

---

## Cross-Platform Summary

**Universal actions (help ALL platforms)**: Wikipedia/Wikidata entity; YouTube channel; comprehensive well-structured content; Schema.org (Organization + sameAs); fast load + clean HTML; author pages with credentials + sameAs; regular updates with visible dates.

| Priority | Google AIO | ChatGPT | Perplexity | Gemini | Copilot |
|---|---|---|---|---|---|
| #1 | Top-10 ranking | Wikipedia | Reddit presence | YouTube | IndexNow |
| #2 | Q&A structure | Entity graph | Original research | Knowledge Panel | Bing WMT |
| #3 | Tables/lists | Bing SEO | Freshness | Schema.org | LinkedIn |
| #4 | Featured snippets | Reddit | Community forums | GBP | Meta descriptions |

---

## Output Format

Generate **GEO-PLATFORM-OPTIMIZATION.md**:

```markdown
# GEO Platform Optimization Report — [Domain]
Date: [Date]

## Overall Platform Readiness
- Combined GEO Score: XX/100 (average of all platform scores)

## Platform Scores
| Platform | Score | Status |
|---|---|---|
| Google AI Overviews | XX/100 | [Strong/Moderate/Weak] |
| ChatGPT Web Search | XX/100 | [Strong/Moderate/Weak] |
| Perplexity AI | XX/100 | [Strong/Moderate/Weak] |
| Google Gemini | XX/100 | [Strong/Moderate/Weak] |
| Bing Copilot | XX/100 | [Strong/Moderate/Weak] |

Status thresholds: Strong = 70+, Moderate = 40-69, Weak = 0-39

## Platform Details
[Per-platform breakdown with score, gaps found, specific actions]

## Prioritized Action Plan
### Quick Wins (this week)
[Actions that improve multiple platform scores with minimal effort]

### Medium-Term (this month)
[Actions requiring content creation or technical changes]

### Strategic (this quarter)
[Actions requiring entity building, community development, or platform presence]
```
