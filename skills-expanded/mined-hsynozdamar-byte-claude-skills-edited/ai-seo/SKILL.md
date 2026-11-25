---
name: ai-seo
description: "Optimizing content to be cited by AI search engines and LLMs (AEO, GEO, llms.txt, agent readiness). Use when someone wants to appear in AI answers. Not for classic SEO audits."
metadata:
  version: 2.5.0
---

# AI SEO

Goal: get content cited by AI search (Google AI Overviews and AI Mode, ChatGPT, Perplexity, Claude, Gemini, Copilot). Classic ranking gets you listed; AI systems select passages by quality, structure and relevance, so a well-structured page can be cited from page 2 or 3.

If `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`, or legacy `product-marketing-context.md`), read it first and ask only what it does not cover. Otherwise ask: which 10-20 queries matter, whether the brand appears in AI answers today, what content types exist, and which competitors are cited where this site is not.

## Two regimes

- **Google AI Overviews / AI Mode** run on core Search ranking and quality systems. Google states (AI features guide) that no special markup or files are needed, that chunking or writing separate "AI content" risks the scaled-content-abuse policy, and that there is no AI-specific Search Console report. Optimize for people: E-E-A-T, original information, semantic HTML, clean indexability.
- **ChatGPT, Claude, Perplexity, Copilot** reward extractable structure (answer blocks, FAQs, comparison tables), machine-readable files, and third-party mentions (Reddit, Wikipedia, review sites) more than rank.

Structure that helps the second group is ordinary good organization, so apply it to both. Default: write for people, organize for clarity.

Coverage matters more than single keywords: Google fans each query out into related sub-queries, so plan the 5-10 related questions around a topic and cover the cluster. Detail, stats and the ChatGPT fan-out extraction: [references/google-stance-and-fanout.md](references/google-stance-and-fanout.md).

## Audit

1. Run 10-20 key queries across Google, ChatGPT and Perplexity; record who is cited. Run each 3-5 times and report a rate with n ("cited 3/5, n=5"), since answers are non-deterministic.
2. For each competitor win, compare structure, authority signals, freshness, schema and third-party presence.
3. Check each priority page for extractability: definition in the first paragraph, self-contained answer blocks, sourced statistics, comparison tables, FAQ, schema, named author, updated within 6 months, query-shaped headings.
4. Check robots.txt for blocks on GPTBot, ChatGPT-User, PerplexityBot, ClaudeBot, anthropic-ai, Google-Extended, Bingbot. A blocked bot cannot cite you. To opt out of training only, block CCBot and allow the search bots.

Tables, metrics, monitoring tools and the DIY monthly check: [references/audit-and-monitoring.md](references/audit-and-monitoring.md).

## Optimize: structure, authority, presence

**Structure.** AI extracts passages, not pages.
- Lead each section with the direct answer; keep answer passages to 40-60 words.
- H2/H3 phrased like the queries people type; tables for comparisons, numbered lists for processes, one idea per paragraph.
- Block templates (definition, steps, comparison, pros/cons, FAQ, statistic): [references/content-patterns.md](references/content-patterns.md).

**Authority.** In the Princeton GEO study (KDD 2024, on Perplexity) citing sources gave +40% visibility, statistics +37%, expert quotations +30%; keyword stuffing gave -10%. Add dated statistics from original sources, named authors with credentials, a visible "Last updated" date, and refresh competitive pages at least quarterly. Full table: [references/authority-and-presence.md](references/authority-and-presence.md).

**Presence.** Third-party sources often outweigh the brand's own site: Wikipedia, Reddit, LinkedIn, review sites (G2, Capterra), industry roundups, YouTube, podcasts. Treat each as one surface in a portfolio, because citation mixes shift overnight with retrieval updates. Per-surface notes are in the same authority-and-presence file; YouTube anatomy in [references/youtube-ai-citations.md](references/youtube-ai-citations.md).

## Content formats (dated, volatile)

As of ChatGPT 5.6 (Aug 2026), listicle citations fell 50.5% and comparison-page citations 32.1% while `site:` and "official" retrieval surged, so primary sources and owned pages (product, docs, pricing) gain. Comparisons still work on Google AIO, Gemini and Perplexity. Evergreen winners: original research, definitive guides, official pages with extractable structure. Weak: thin, gated, PDF-only or undated content without an author. Per-platform format table and LinkedIn numbers: [references/format-volatility.md](references/format-volatility.md). Per-content-type tactics (SaaS pages, blog, alternatives, docs, local/ecom): [references/content-types.md](references/content-types.md).

Citation is not recommendation. Being recommended depends on web-wide consensus (reviews, forums, analysts, press). In one 100-query B2B study, 69% of AI Overview citations earned by self-promotional "best [category]" listicles appeared in answers recommending competitors. Visibility ladder and strategy: [references/citations-vs-recommendations.md](references/citations-vs-recommendations.md).

## Machine-readable layer

Buying agents skip products whose pricing they cannot parse. Publish pricing as plain text or markdown (`/pricing.md`), add `/llms.txt` (llmstxt.org), keep primary content server-rendered with semantic HTML and labelled controls, and add schema (`Article`, `FAQPage`, `HowTo`, `Product`, `Organization`). Google says none of this is needed for its own AI features; it helps other engines. Template, schema table, agentic checklist: [references/machine-readable-and-agents.md](references/machine-readable-and-agents.md). Run the access/discovery/parseability audit first: [references/agent-readiness.md](references/agent-readiness.md). OKF bundles (Google, June 2026, no confirmed ranking effect): [references/okf.md](references/okf.md). Platform-specific ranking factors and robots.txt config: [references/platform-ranking-factors.md](references/platform-ranking-factors.md).

## Guardrails from Google's guide

Serve one body of content to people and AI, in normal paragraphs and headings. Real participation earns mentions on Reddit and Wikipedia, so skip fabricated citations. Mass-produced thin variations violate spam policy; AI-generated content that meets Search Essentials is fine. Keep content open and rendered, since gated or JS-only content is invisible to both Search and agents.

## Related skills

`seo-audit` (technical and on-page), `schema` (structured data), `content-strategy`, `competitors` (comparison pages), `programmatic-seo`, `copywriting`. Tool registry: `../../tools/REGISTRY.md` (semrush, ahrefs, gsc, ga4).
