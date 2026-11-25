---
name: search-ready
description: Audit, implement, or verify technical SEO, indexation, content, schema, and AI search visibility and controls. Use when preparing or maintaining a live site for search and answer engines.
license: MIT
---

# Search readiness

Make a real site easier to crawl, index, understand, serve, and cite. Work from live behavior, repository intent, and search data as separate evidence classes.

## Choose a mode

- **Audit:** diagnose live and repository issues without changing files.
- **Implement:** apply approved fixes and verify deployment behavior.
- **Content opportunity:** research live queries, competitors, and audience questions.
- **Structured data:** select, implement, and validate eligible markup.
- **AI discovery:** evaluate crawler policy, Search Console and page-level AI controls, answer-ready content, entity clarity, and agent aids such as `llms.txt`.
- **Maintenance:** compare the present state with prior evidence and define recurring checks.

Route by site type when relevant: SaaS/docs, editorial, commerce, local, or international. Do not use an equal-weight generic score across unlike sites.

Social preview tags, share images, and share links belong to the `social-sharing` skill. Hand that work over. Keep only the search side here: Google picks Search and Discover thumbnails from `og:image` and schema.org image markup (see [technical SEO](references/technical-seo.md#structured-data)).

## Workflow

1. Confirm canonical production host, important routes/templates, audience, conversion action, locales, site type, and repository access. Inspect available Search Console/Bing data (including Google's Generative AI performance report and Bing's AI Performance report), analytics, logs, prior audits, and deployment configuration before asking questions.
2. Fetch representative live URLs and inspect rendered HTML, source HTML where useful, headers, redirects, robots, sitemap/indexes, canonicals, hreflang, metadata, structured data, internal links, status behavior, and rendering dependencies.
3. Compare live behavior with repository intent. Label observed live behavior, source intent, search-platform data, and recommendation separately.
4. Inventory indexable route classes and assign each a search job. Diagnose duplicates, soft 404s, thin/orphaned pages, faceted/paginated states, accidental noindex, canonical conflicts, redirect chains, and sitemap coverage.
5. Prioritize blockers by likely impact on crawl, index, serve, comprehension, user experience, and business value. Character counts and checklist totals do not set priority.
6. Research live result formats, branded/category queries, competitors, and source ecosystems when the task needs content or citation evidence. Treat rankings and snippets as time-sensitive and date every observation.
7. Improve content around real questions and defensible claims. Preserve natural structure; do not force question headings, FAQs, word counts, or statistics at arbitrary intervals. Keep FAQ content where it answers what readers actually ask.
8. Add structured data only when it matches visible content and a feature the search engine documents today. FAQ and HowTo markup earn no Google rich result (FAQ stopped showing 7 May 2026). Validate syntax and eligibility separately.
9. Treat AI-search practices by confidence: provider-documented controls (per-crawler robots rules, Google's Search generative AI control, snippet controls), standard accessible content, agent conventions such as `llms.txt`, and unsupported speculation. Google Search does not use `llms.txt`; never present it as a ranking or citation lever. Never promise rankings or citations.
10. Do not change a Search Console AI control, add snippet limits, or block a crawler without the owner's decision. Each trades visibility and traffic for control.
11. Re-fetch the deployed result, run relevant validators and performance checks, compare route samples, and report remaining blockers and maintenance needs.

## Load conditional references

- Read [technical SEO](references/technical-seo.md) for route sampling, diagnostics, structured data, implementation patterns, and validation.
- Read [AI-search workflow](references/ai-search-workflow.md) only for answer engines, citations, crawler policy, AI controls, measurement, or entity/content work.
- Read [AI-search reference](references/ai-search-reference.md) only for conditional schema, crawler and control records, `llms.txt`, and outreach patterns.

This file controls prioritization, safety, output, and verification.

## Primary sources to fetch

Checked 2026-11-04. Fetch the page that governs a claim at run time before naming a user agent, control, report, or rich result. If this date is more than about 90 days old, read the Search Central updates log first. Never copy a user-agent list from this file or from memory.

| Operator | What it governs | URL |
|---|---|---|
| Google Search | Change log for docs, rich results, controls | https://developers.google.com/search/updates |
| Google Search | Guidance for AI Overviews and AI Mode | https://developers.google.com/search/docs/fundamentals/ai-optimization-guide |
| Google Search | Snippet controls in AI features | https://developers.google.com/search/docs/appearance/ai-features |
| Google Search | Rich results that exist today | https://developers.google.com/search/docs/appearance/structured-data/search-gallery |
| Search Console | Search generative AI control | https://support.google.com/webmasters/answer/16908024 |
| Search Console | Generative AI performance report | https://support.google.com/webmasters/answer/16984139 |
| Google crawlers | Crawler and robots tokens, including Google-Extended | https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers |
| Bing | Webmaster Guidelines | https://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a |
| Bing | AI Performance report | https://www.bing.com/webmasters/help/ai-performance-9f8e7d6c |
| OpenAI | Crawlers and user agents | https://developers.openai.com/api/docs/bots (platform.openai.com/docs/bots redirects here) |
| Anthropic | Crawlers and user agents | https://support.claude.com/en/articles/8896518 |
| Perplexity | Crawlers and user agents | https://docs.perplexity.ai/docs/resources/perplexity-crawlers |
| Apple | Applebot and Applebot-Extended | https://support.apple.com/en-us/119829 |
| Chrome Lighthouse | Experimental Agentic Browsing audits | https://developer.chrome.com/docs/lighthouse/agentic-browsing/scoring |
| llms.txt | The proposal (v2) | https://llmstxt.org/ |

## Output contract

Return mode-relevant sections:

- scope and evidence sources, each with its retrieval date;
- prioritized findings with affected URLs/templates, severity, confidence, and fix;
- live-vs-repository discrepancies;
- route-level metadata/schema/indexation matrix;
- implemented changes with file paths;
- content opportunities grounded in dated evidence;
- validator and deployed verification results;
- unresolved blockers, decisions left to the owner, and maintenance cadence.

## Verify

- Representative templates and edge states were sampled, not just the homepage.
- Live response, rendered content, and repository intent are distinguished.
- Indexation claims use search-platform evidence when available and are otherwise qualified.
- Schema matches visible content and passes relevant validation. No finding asks for FAQ or HowTo markup to earn a Google rich result.
- Redirects, canonicals, robots, sitemap, hreflang, status codes, and rendering agree.
- Performance claims identify lab versus field data.
- AI-search recommendations state evidence confidence, name the product a control or file affects, and cite the source with its retrieval date.
