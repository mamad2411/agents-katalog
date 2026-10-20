---
name: growth-seo-orchestrator
description: "Route an SEO/growth task to the right skill among 8 search specialists — intent research, content briefs, site architecture, schema/structured data, programmatic pages at scale, technical audits, AI-search (AEO/GEO) optimization, and Google's official guidance. USE WHEN a user wants to rank, get found, fix SEO, plan content, or show up in AI answers but hasn't named the specific concern."
cluster: growth-seo
version: 1.0.0
---

# Growth-SEO Orchestrator

The single entry skill for SEO and search-growth work. It locates the task on the
**funnel stage × concern** map and delegates to one of 8 specialist spokes. The model every
SEO task shares — **search intent**, the query→page contract, and the E-E-A-T/quality bar —
lives in `growth-seo-core`; read it before mapping keywords to pages or judging whether content
will rank.

## Routing map (intent → spoke)

**Understand the rules**
- "What does Google actually want?" / first principles, Search Console, crawl/index basics → `google-official-seo-guide`

**Research demand & intent**
- Niche / offer / topic → keyword map + audience-question map + an executable research pipeline → `searchintentautomation`
- Turn that demand into a structured, writer-ready brief → `seo-content-brief`

**Plan the site**
- Page hierarchy, navigation, URL structure, internal linking, "what pages do I need" → `site-architecture`

**Produce & enrich content**
- Add/fix structured data, JSON-LD, rich-result eligibility → `schema-markup`
- Build many keyword/location/comparison pages from templates + data → `programmatic-seo`

**Diagnose & optimize**
- Audit, "why am I not ranking," technical/on-page issues, traffic drop, Core Web Vitals → `seo-audit`
- Get cited by LLMs / appear in AI Overviews, ChatGPT, Perplexity (AEO/GEO/LLMO) → `ai-seo`

## Picked-up spokes

Granular execution specialists folded in from the claude-seo library (MIT). The 8 spokes above stay the primary map; route to these when the task is narrower or needs live data. They complement, not replace, the spokes above (e.g. `seo-audit` stays the entry for "why am I not ranking"; drop to `seo-technical`/`seo-page` for a deep crawl/single-page pass).

**Diagnose at finer grain**
- One URL, full on-page + content + schema + image + meta pass with a score card → `seo-page`
- Infrastructure audit — crawlability, indexability, security headers, Core Web Vitals, JS rendering, robots.txt / AI-crawler access, IndexNow → `seo-technical`
- Content-only review — E-E-A-T, readability, thin-content risk, AI-citation readiness → `seo-content`
- Image SEO + CWV — alt text, WebP/AVIF, srcset, lazy loading, CLS → `seo-images`

**Build & validate artifacts**
- Competitor comparison / "X vs Y" / alternatives / roundup pages with schema → `seo-competitor-pages`
- Generate or validate an XML sitemap (format, limits, lastmod, canonical hygiene) → `seo-sitemap`
- Hreflang / international SEO — validate or generate locale alternates → `seo-hreflang`

**Plan & pull live data**
- Full strategic SEO plan/roadmap with industry templates, competitive analysis, KPIs, phasing → `seo-plan`
- Live SEO data (real SERPs, keyword volumes/difficulty/intent, backlinks, on-page, LLM mentions) via the DataForSEO MCP → `seo-dataforseo` (feeds every other spoke when available)

## Standard Operating Flow

1. Locate the task: which funnel stage (understand → research → architect → produce → optimize) and which concern.
2. If it touches **what query a page targets, intent match, or the quality/E-E-A-T bar**, pull the model from `growth-seo-core` first — these decisions cascade into every later step.
3. Delegate to the spoke(s). Multi-step asks fan out in funnel order (e.g. "rank a new section" → `searchintentautomation` → `seo-content-brief` → `site-architecture` → `programmatic-seo`/content → `schema-markup` → `seo-audit`).
4. Return: chosen spoke(s), the target query/intent and page it maps to, the success signal (ranking, rich result, AI citation, traffic), and the next action.

## Guardrails

See `growth-seo-core`. In short: **intent before output** — never produce a page without naming
the query it serves and the intent behind it; one primary query per page (don't cannibalize);
match content type to intent (informational vs commercial vs transactional). Earn rankings with
genuine E-E-A-T, never manipulate; programmatic pages must add real value per URL, not thin
doorways; and AI-search visibility is downstream of the same intent + authority, not a separate
trick. State any change that affects what a URL targets or how it's indexed.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
