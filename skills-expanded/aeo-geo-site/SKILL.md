---
name: aeo-geo-site
description: >-
  use this when building or updating a website for SEO plus AEO/GEO (AI
  assistants, ChatGPT, Copilot, Gemini) so pages are machine-readable,
  intent-clear, and citable
---
# AEO / GEO site (Microsoft + execution)

Source frame: Microsoft Advertising, Jennifer Myers (author), and Paul Longo (executive sponsor), *From discovery to influence: A guide to AEO and GEO* (Jan 2026), as summarized in [Alex Groberman](https://www.linkedin.com/pulse/new-microsoft-just-revealed-how-get-traffic-from-alex-groberman-5af0c). Primary PDF: https://about.ads.microsoft.com/content/dam/sites/msa-about/global/common/content-lib/pdf/from-discovery-to-influence-a-guide-to-aeo-and-geo.pdf

Use this whenever you ship or restyle site pages meant to be found, understood, cited, or recommended by AI search, assistants, browsers, or agents. SEO remains the foundation. AEO adds clarity. GEO adds trust.

## Shift to optimize for

| Layer | Goal | Old SEO bias | New bar |
| --- | --- | --- | --- |
| SEO | Be found | Keywords, rankings, clicks | Crawlable, fast, indexable pages |
| AEO | Be understood | Thin keyword copy | Clear, structured, extractable answers |
| GEO | Be chosen / cited | Soft claims | Credible, consistent, justified facts |

Competition moves from “being found” to “being chosen.” Visibility is earned by how clearly AI systems understand the entity, trust the brand, and can act on the data.

## Three data planes (control all that apply)

1. **Crawled web data** — what AI learned and what live search finds: brand reputation, category authority, expert mentions, crawlable HTML.
2. **Structured feeds / APIs** — catalogs, sitemaps, `llms.txt`, markdown twins, JSON-LD, public APIs. Precision and control live here. (Retail: product feeds. Content sites: entity pages, video objects, FAQ, design law, markdown negotiation.)
3. **Live website data** — what an agent sees on visit: current copy, media, reviews, working CTAs. If the live page lies or fails, the agent fails even if feeds were perfect.

Never cloak: **same HTML to bots and users.** Extra formats (markdown via `Accept`, `llms.txt`) are additive, not different facts.

## Three action pillars

### 1. Technical foundations and structured data

AI needs structure and consistency more than clever prose.

- Server-rendered HTML first. Honor `robots`, sitemap, canonicals, `dateModified` when content changes.
- JSON-LD that matches visible content. Prefer real schema types for the product:
  - Content / media sites: `Organization`, `WebSite`, `WebPage`, `FAQPage`, `VideoObject`, `ImageObject`, `BreadcrumbList`, `ContactPoint`
  - Retail (when applicable): `Product`, `Offer`, `AggregateRating`, `Review`, `Brand`, `ItemList`
- Machine-readable twins where useful: markdown negotiation, `llms.txt`, public `design.md` or equivalent brand law for agents.
- Dynamic fields stay fresh: price/availability/SKU/GTIN for commerce; titles, publish dates, canonical URLs, AI-use disclosures for content.
- Localized signals when relevant: `inLanguage`, `priceCurrency`, address that matches real ops.
- Images: descriptive alt text; `ImageObject` when it adds citability.
- After meaningful ships, rescan agent-readiness (e.g. is-agentic) and fix Essential misses before soft polish.

### 2. Intent-driven content enrichment (AEO)

Optimize for questions and extraction, not keyword stuffing.

- Front-load: who it is for, what problem it solves, what it is (and is not).
- Headings that mirror real reader / buyer / user questions.
- Modular, citable blocks: short paragraphs, Q&A, feature lists, comparison only when honest and on-brand.
- Use-case framing (“ready in 20 minutes”, “works with your existing CI”) over vague slogans.
- Video / media pages: transcript or plain-language summary, still + outbound watch URL, VideoObject.
- Relationships when real: “goes with”, related recipes or docs pages, related FAQs. Do not invent entities.
- Prefer one clear answer per section. Avoid em-dashes, hedge piles, and low-trust hype.

SEO vs AEO vs GEO in one line:

- SEO: “waterproof rain jacket”
- AEO: “lightweight packable waterproof rain jacket with ventilation”
- GEO: “best-rated by X, 4.8 stars, 180-day returns” (only if true and verifiable)

### 3. Trust and credibility (GEO)

AI systems prioritize verifiable truth and penalize low-trust language.

- Consistent entity: same name, same facts, same URLs across site, social profiles, video channels, schema.
- Proof you can show: reviews, press, certifications, expert mentions, official sameAs links — only real ones.
- FAQ and help content that answers hard questions honestly (including “no”, “not yet”, disclosures).
- Contact / trust pages when recommended (email, privacy, no fake forms).
- No exaggerated claims, no fake social proof, no Ivy-league wallpaper, no “#1” without a source.
- Brand voice stays calm and specific. Copy locks and design law beat trend copy.

## Pre-ship checklist (every page or wave)

- [ ] Primary reader job is named (developer evaluating, agent citing, buyer comparing, …)
- [ ] H1 and first viewport answer that job without fluff
- [ ] Visible facts match JSON-LD and any markdown twin
- [ ] FAQ or Q-shaped headings where intent is question-shaped
- [ ] Images have useful alt; no type burned into photos unless brand allows it
- [ ] CTA points at the real product surface (signup, docs, buy URL, contact) — not a maze
- [ ] `noindex` only for experiments; production pages in sitemap when indexable
- [ ] No cloaking; Accept negotiation serves the same facts
- [ ] Trust lines are true and on-brand (disclosures, AI-use notes, location, team)
- [ ] Soft claims and competitor digs stay off

## Anti-patterns

- Ranking-only pages with nothing an assistant can quote
- Schema that invents ratings, products, or team members
- Different bot HTML vs user HTML
- Paywall / survey funnels as “content”
- Keyword stuffing, unverifiable superlatives, fear-based or comparison claims when brand forbids them
- Shipping a feed or schema type you cannot keep fresh

## How to run on a task

1. Read brand / design law and existing schema patterns on the site.
2. Name the intent cluster and the entity (recipe, docs page, org, product).
3. Draft or restyle with pillar 2 copy shape first, then pillar 1 markup, then pillar 3 trust links.
4. Wire markdown / `llms.txt` / sitemap as needed.
5. Verify with a live fetch (HTML + markdown Accept) and an agent-readiness scan after merge.

Retail-specific feed/checkout work only when the site actually sells. For a content or docs site, treat articles, docs pages, and FAQ entities as the catalog and keep the door pointing at the real product (e.g. the app signup or the docs), not a fake shop.
