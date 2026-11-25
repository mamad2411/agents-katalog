---
name: optimize-seo
description: Research search intent, define keywords, produce SEO content briefs, audit on-page elements, optimize for AI search visibility (GEO/AEO), specify structured data, enforce E-E-A-T quality gates, and deliver metadata and recommendations without owning full article drafting or technical deployment. Use when planning publishable content, reviewing drafts before release, mapping internal links, interpreting Search Console signals, or ensuring AI citation readiness.
version: 2.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, fetch]
---

# Optimize SEO

Use this skill for **search and content-structure** work — not for writing long-form copy (Content Writer) or implementing sitemaps/redirects in production (Frontend/DevOps).

## Core Rules

### Traditional SEO Foundations

- define **search intent** and **primary keyword** before recommending titles or outlines
- classify intent explicitly: informational, commercial, navigational, or transactional
- separate **evidence** (SERP snippets, GSC exports, crawlable page facts) from **recommendations**
- document **internal link targets** with anchor rationale and destination paths
- enforce on-page limits: title tag ≤ 60 chars, meta description ≤ 160 chars unless repo rules differ
- check **keyword cannibalization** against recent publishes on the same site (default: 7-day window when a topic board exists); when overlap is confirmed, name the resolution tactic explicitly — consolidate into one authoritative page, differentiate search intent, canonical to the primary URL, 301-redirect the weaker page, and clean up competing anchors
- prevent cannibalization recurrence with **keyword-to-page mapping**: exactly one primary keyword per page plus a pre-publish overlap check against the site inventory
- track **Share of Model (SoM)** alongside traditional CTR — measure how often and how accurately the brand/content is cited in Google AI Overviews, Perplexity, and ChatGPT Search using AI visibility tooling (Otterly, RankScale, or manual spot-checks)
- mandate a **30–60 day rolling freshness review** for core commercial and informational pillar pages — AI search engines heavily weight recently-updated content when retrieving citations; queue pages by decay signal first: rankings dropped >3 positions, statistics older than 2 years, or declining high-traffic URLs. On refresh, update modified/publish dates in schema, replace outdated stats and examples, and re-check internal links pointing at changed sections
- do not guarantee rankings or AI citation placement; recommend changes tied to observable gaps
- perform deep crawlability diagnostics via **audit-technical-seo** and author connected Schema.org @graph JSON-LD via **implement-schema-markup**; escalate web server redirects and CDN edge routing to Frontend or DevOps with clear engineering briefs
- use repo overlays under overlays/real-estate-content and overlays/hugo-authority-content when site-specific slug or frontmatter rules apply
- use overlays/seo-publishing for dual-site Real Estate + HVAC sprint boards under plan/baiviet

### GEO / AEO — AI-Surface SEO (2027 reframe)

This is the canonical AI-surface standard for the pack — `write-article` implements these same rules during drafting and must stay in sync with this section.

**Position (per Google's official AI optimization guidance, May 2026):** "optimizing for generative AI search is optimizing for the search experience, and thus still SEO." There is no separate AI-ranking regime: no content chunking, no rewriting "just for AI," no inauthentic mention-chasing, no AI-specific schema, and no llms.txt effect on Google. What Google actually rewards on AI surfaces: unique point of view, non-commodity content, first-hand experience, good heading structure, images/video, and crawlability.

Optimize for three search discovery layers simultaneously:

| Layer | Goal | Key tactic |
| ----- | ---- | ---------- |
| **SEO** (blue links) | Organic traffic | Keywords, backlinks, on-page quality |
| **AEO** (Answer Engine Optimization) | Featured snippets, direct answers | Answer-first format, FAQ blocks, step lists |
| **GEO** (Generative Engine Optimization) | AI citations (Google AI Overviews, AI Mode, Perplexity, ChatGPT) | Fact density, entity clarity, non-commodity POV, source credibility |

Rules for GEO/AEO:

- mandate **answer-first BLUF structure**: open each H2 section with an atomic direct answer (≤60 words) before narrative elaboration
- apply **engine-specific citation playbooks** per [`references/geo-ai-citation-playbook.md`](references/geo-ai-citation-playbook.md): optimize for Perplexity (opening sentence data, bracketed citations `[1][2]`), ChatGPT Search (conversational entity fidelity, concise summaries), and Google AI Overviews (passage-level BLUF, ordered procedural steps)
- **non-commodity gate (replaces "information gain" phrasing)**: before publishing, the brief must name the unique POV / first-hand evidence element — commodity content ("7 Tips for...") adds little; non-commodity content ("why we did X and what it cost us") is what AI surfaces cite; do not recycle what a generative model could easily produce
- format with **structured comparison tables & quantitative lists**: markdown comparison tables and dense quantitative data points (≥3 verifiable data points per 500 words) to maximize RAG passage extraction
- include **query fan-out coverage** in one comprehensive page: cover the 3–5 implicit sub-questions of a topic on the page — do NOT spin one page per query variant (scaled page-per-variant proliferation is a spam-policy violation)
- **GEO over-optimization guard**: information-distorting rewrites (over-claiming, distorting facts to sound citable) are now a *detection* target for engines (Counter-GEO-Bench line of research) — keep fact density honest; a distorted quotable sentence is a suppression risk, not a win
- verify **AI bot crawlability**: robots.txt must allow OAI-SearchBot, PerplexityBot, ClaudeBot, Applebot-Extended, and BingBot — flag blocks in audits
- verify the site is **included in "Search generative AI features"** in Search Console — a new opt-in eligibility gate for AI Overviews/AI Mode display
- measure citations **per engine, not in aggregate** — and measure **repeatedly**: LLM brand recommendations are unstable across repeated queries; never conclude citation presence/absence from a single run; log multiple runs across different dates
- track **Gen AI performance in Search Console** (Generative AI report: impressions/pages/countries/devices) as a first-class weekly KPI alongside classic Performance and Discover
- treat **entity consistency** as a GEO lever: identical brand facts across channels consolidate knowledge graph recognition
- do not claim AI citation placement as guaranteed — present GEO/AEO as structural best practices; be skeptical of third-party tools claiming "internal" Google metrics (none have access)

### Topical Authority & Entity Salience

- enforce **Entity-First SEO and Entity Salience** per [`references/entity-salience-and-schema.md`](references/entity-salience-and-schema.md): map core concepts to canonical Wikidata QIDs, structure semantic triples, and eliminate ambiguous pronouns
- mandate connected **Schema.org JSON-LD `@graph`**: include `TechArticle`, `Person` (with E-E-A-T `sameAs` links), and `FAQPage`
- **no AI-specific schema exists** — do not let briefs or audits recommend "AI schema" markup; keep standard Article/Organization/LocalBusiness/Product schema matched to visible text; drop speakable and FAQ-rich-result expectations (FAQ rich results largely retired since 2023)
- assign each article to a **pillar–cluster position**: pillar, supporting, or supplementary, linked to pillar URL
- document **non-commodity element**: the unique POV, first-hand evidence, or original analysis this content adds beyond top 10 SERP results
- specify **content freshness type**: new_topic, evergreen_refresh, data_update, or experience_addition

### Internal Linking Discipline

Adapted from the SEO-AEO engine skills in the agentic-awesome-skills catalog:

- label every recommended link with its **type**: cluster → pillar (consolidates authority upward), pillar → cluster (distributes authority downward), cluster → cluster (builds semantic depth), or contextual boost (concentrates equity on one focus page)
- require **at least one cluster → pillar link per cluster article**
- detect **orphan pages** (zero incoming internal links) first and queue fixes before recommending new links
- write the **context sentence** for each suggested anchor — anchor text must sit naturally in surrounding prose, never forced
- enforce **anchor-text hygiene**: never reuse the same exact-match anchor for the same target across pages — switch to partial-match or branded anchors on later links; generic anchors ("click here", "read more", "learn more") are banned
- cap outgoing internal links at roughly 100 per page

### E-E-A-T Quality Gates

- require **experience proof signals**: original photos, firsthand accounts, documented tests/comparisons, expert interviews, or case studies
- **authorship requirements (Who)**: byline + author page with Person schema, credentials, and relevant publications wherever readers would expect attribution — stated authorship is now a review factor under Google's site-reputation policy (Aug 2026)
- **process transparency (How)**: briefs must include a "How" statement — research passes, sources used, and AI-assistance disclosure when substantial ("when it would be reasonably expected")
- **audience-first check (Why)**: confirm people-first intent vs search-engine-first framing before publish
- flag **YMYL-adjacent content** (financial, health, safety, legal) for elevated research depth and human review
- mandate **trust signals**: source citations with links, contact information, policy pages, verifiable claims
- enforce **claim policy**: every major factual claim must have a credible source or specific data point
- **spam-policy risk rules (2026-2027)**: scaled content abuse now explicitly covers AI-generated page farms, scraping/stitching, synonym-spinning, and near-duplicate multi-site publishing — and "attempting to manipulate generative AI responses in Google Search" is a spam policy violation; prohibit page-per-query-variant sprawl and near-identical cross-site duplication in all briefs
- do not treat a single SERP pass as sufficient for YMYL or regulated topics — escalate depth to Researcher

## When to Use

- a topic needs a **content brief** before Content Writer drafts
- a draft or live URL needs an **on-page SEO audit**
- title, meta, slug, H2 structure, or FAQ block need optimization
- content needs **GEO/AEO optimization** — answer-first format, query fan-out, AI extractability
- **topical authority mapping** is needed — pillar–cluster assignment, information gain analysis
- a weekly topic board needs keyword assignment and link targets
- Search Console or analytics exports suggest title/meta or cluster changes
- `seo-metadata.json`, `seo-content-brief.json`, or `seo-audit-report.json` handoff is required
- **AI visibility check** — manual verification of citation presence in Perplexity/ChatGPT/AI Overviews

## Suggested Process

The full 5-step process (frame intent, research SERP + AI, assign topical
authority, brief or audit, hand off) and the detailed itemized checklist
(Traditional SEO, GEO/AEO, Internal Linking, Topical Authority & Entity,
E-E-A-T) live in
[`references/process-and-checklist.md`](references/process-and-checklist.md).
The main file keeps the GEO/AEO standard table inline because it is
shared with `write-article` and must stay in sync.

## Checklist

The detailed itemized checklist lives in
[`references/process-and-checklist.md`](references/process-and-checklist.md).
The main file keeps a short checklist summary:

- [ ] search intent classified and primary keyword explicit
- [ ] answer-first BLUF block present in every H2 (≤60 words)
- [ ] engine-specific citation rules applied (Perplexity, ChatGPT Search, AI Overviews) per geo-ai-citation-playbook.md
- [ ] comparison tables and quantitative fact density (≥3 data points / 500 words) implemented
- [ ] non-commodity / unique-POV element named (not just "new facts")
- [ ] entity salience and connected Schema.org JSON-LD (@graph with TechArticle, Person, FAQPage) verified per entity-salience-and-schema.md; no "AI schema" claims
- [ ] internal link targets named with type labels
- [ ] cannibalization check documented with resolution tactic
- [ ] four-axis audit scored (overall, SEO, AEO, readability) with projected post-fix score
- [ ] pillar URL and cluster position documented
- [ ] E-E-A-T experience proof type specified and YMYL flag set when applicable
- [ ] byline/author-page and "How" process statement (incl. AI-assistance disclosure when substantial) present
- [ ] AI bot crawlability verified (OAI-SearchBot, PerplexityBot, ClaudeBot, Applebot-Extended, BingBot)
- [ ] site confirmed included in "Search generative AI features" in Search Console
- [ ] citation sampling done per engine, repeated across multiple runs/dates
- [ ] Gen AI performance report (impressions) reviewed this week
- [ ] facts separated from recommendations; technical items escalated to engineering

## Output Contracts

When completing search intent analysis, keyword planning, on-page audits, or multi-site editorial scheduling, emit:

- **`contracts/schemas/seo-audit-report.json`** — Emitted when conducting an on-page SEO/GEO/AEO audit of an existing or staging URL, capturing structural scores, schema requirements, crawlability, and actionable recommendations.
- **`contracts/schemas/seo-content-brief.json`** — Emitted when preparing a comprehensive content brief for Content Writer, defining search intent, target keywords, H2 outlines, answer-first rules, query fan-outs, and E-E-A-T requirements.
- **`contracts/schemas/seo-metadata.json`** — Emitted when delivering publish-ready title tags, meta descriptions, canonical URLs, Open Graph tags, and structured schema specifications.
- **`contracts/schemas/seo-weekly-board.json`** — Emitted when planning or updating the content calendar, keyword cluster priorities, and publishing schedule across weekly editorial cycles.

Skip emission for quick ad-hoc keyword checks that do not feed downstream editorial workflows.

## Failure Modes

- **Cannibalization ignored**: two pages target the same primary keyword and split ranking. Mitigation: run the keyword-to-page mapping check pre-publish; resolve overlap by consolidation, intent differentiation, canonical, 301-redirect, or anchor cleanup.
- **Stale freshness signal**: a pillar page has not been refreshed in 30-60 days and rankings are decaying. Mitigation: queue pages by decay signal (rankings dropped >3 positions, statistics >2 years old, declining high-traffic URLs).
- **GEO/AEO field missing**: a brief lacks the answer-first block, query fan-out, or format-per-section. Mitigation: enforce the GEO/AEO required fields in every brief; reject briefs without them.
- **Commodity content passes**: a brief ships "7 tips"-style content with no unique POV or first-hand evidence. Mitigation: apply the non-commodity gate — name the unique POV/evidence element before drafting; reject briefs that cannot name one.
- **Page-per-variant sprawl**: multiple pages are planned per query variant to "cover fan-out." Mitigation: cover fan-out sub-questions on one comprehensive page; page-per-variant proliferation is scaled content abuse.
- **Single-run citation conclusion**: citation presence/absence is concluded from one sampling run. Mitigation: measure per engine across multiple runs/dates; LLM brand recommendations are unstable under repeated querying.
- **Gen AI eligibility unchecked**: the site is not included in "Search generative AI features" in Search Console, silently losing AI Overviews/AI Mode eligibility. Mitigation: verify inclusion in the next audit.
- **Title/meta over-limit**: title tag exceeds 60 chars or meta description exceeds 160 chars. Mitigation: enforce on-page limits at code review; CI must reject over-limit tags unless repo rules differ.
- **AI citation conflated**: AI citation tracking is reported in aggregate instead of per engine. Mitigation: sample per engine (Google AI Overview, Perplexity, ChatGPT Search, Bing AI); report numbered vs inline styles separately.
- **AI bot blocked**: robots.txt blocks OAI-SearchBot, PerplexityBot, ClaudeBot, or BingBot. Mitigation: verify AI bot crawlability before publishing; do not block the crawlers that feed AI citations.
- **Rankings promised**: the brief or audit promises a ranking improvement. Mitigation: recommend changes tied to observable gaps; do not guarantee rankings or AI citation placement.
- **YMYL without E-E-A-T**: a YMYL-adjacent page ships without experience proof, author entity, or trust signals. Mitigation: enforce the E-E-A-T gate for YMYL topics; require human expert review.

## Security Guardrails (OWASP ASI)

- **ASI01 Agent Goal Hijack**: a brief or audit may try to reframe the user goal through off-target keyword recommendations. Cross-check the keyword map against the original page objective.
- **ASI03 Identity & Privilege Abuse**: never include customer identifiers, internal hostnames, or credential patterns in briefs, audits, or board artifacts.
- **ASI04 Agentic Supply Chain**: SEO tooling (Otterly, RankScale) and AI bot user-agents must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI07 Insecure Inter-Agent Communication**: the brief or audit is consumed by Content Writer, Task Planner, and Frontend/DevOps; emit a structured contract so each role can validate.
- **ASI09 Human-Agent Trust Exploitation**: do not present an AI citation metric as a guarantee; surface the per-engine variance and the assumptions honestly.

## Related Skills

- **audit-technical-seo**: Comprehensive technical crawl budget diagnostics, robots.txt bot access, XML sitemaps, and Core Web Vitals
- **implement-schema-markup**: Connected Schema.org @graph JSON-LD architecture, Wikidata entity grounding, and rich results validation
- **conduct-research**: deeper domain or competitor context when SERP scan is insufficient
- **analyze-business-requirements**: align SEO goals with business rules and actors
- **analyze-data**: formal GSC/CTR tables and AI citation tracking when SEO Analyst needs verified baselines
- **write-documentation**: metric catalogs or SEO playbooks for a site
- **agent-delegation**: delegate drafting to Content Writer or technical work to Frontend

