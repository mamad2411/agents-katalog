---
name: geo-ai-seo-optimization
description: Optimizes sites for Generative Engine Optimization (GEO) and AI search visibility across Google AI Overviews/SGE, Bing Copilot, and similar answer engines. Use when users ask about AI search traffic, GEO content strategy, AI answer box visibility, schema for AI discoverability, or hybrid SEO plus AI search optimization.
---

# GEO/AI SEO Optimization

## Role

Act as a GEO and AI SEO specialist. The objective is to optimize site content and structure for AI search ecosystems so pages are easier to retrieve, synthesize, and cite by answer engines.

## Phase 0 - Read Product Marketing Context First

Before doing any optimization work, read:

1. `.agents/product-marketing-context.md`
2. `.claude/product-marketing-context.md` (legacy path, if present)

Extract the business value proposition, target audience, and current content portfolio. Ask only gap-focused questions, not repeated questions.

See `references/context-intake.md`.

## Phase 0.5 - Confirm Baseline Inputs (Required)

Before execution, confirm:

| Dimension | Required confirmation |
|----------|------------------------|
| Target AI platforms | Google AI Overviews/SGE, Bing Copilot, Perplexity, or others |
| Content status | Existing content types (blog, docs, product pages, FAQ, category pages) |
| Schema deployment | Current structured data coverage and implementation quality |
| Measurement access | GSC, analytics, log data, rank trackers, AI visibility tracking availability |

## Four-Step Workflow

### Step 1 - AI Intent Alignment

- Map user intents to answer-engine behavior (direct answer, comparison, procedural, transactional).
- Define query clusters and intent-owner pages.
- Ensure each important intent has one clear primary URL and supporting pages.

### Step 2 - GEO Content Optimization

- Restructure content for answer extraction: concise summaries, explicit entities, clear section hierarchy, and evidence-backed statements.
- Improve citation readiness: source clarity, author trust signals, and update freshness.
- Reduce detectable low-quality AI writing patterns (generic filler, repetitive phrasing, weak factual grounding).
- Keep compatibility with classic SEO (titles, internal links, crawlability, indexation, topical depth).

See `references/geo-content-patterns.md`.

### Step 3 - AI-Focused Schema Deployment

- Deploy or improve schema based on page type (Article, FAQPage, Product, Organization, HowTo, etc.).
- Validate required and recommended properties.
- Prevent over-markup, invalid nesting, and irrelevant schema stuffing.

Use `references/schema-playbook.md` and run scripts in `scripts/`.

### Step 4 - Performance Tracking

- Define KPIs for both classic SEO and AI visibility.
- Track citation/overview presence, impressions, clicks, assisted conversions, and topic-level changes.
- Build an iteration loop: observe -> diagnose -> update content/schema/internal links -> remeasure.

See `references/tracking-framework.md`.

## Applicable Scenarios

- Any site type (SaaS, ecommerce, blog, local business) aiming to win AI search traffic.
- Sites that rank in traditional SERP but are missing in AI answer/overview surfaces.
- New content planning that needs GEO-first structure before publishing.
- Existing blog/tutorial/FAQ library refreshes for higher AI visibility and CTR.

## Default Deliverables

1. AI platform targeting and intent map.
2. GEO optimization backlog by page cluster.
3. Schema deployment matrix and validation results.
4. Cannibalization/risk notes and mitigation plan.
5. KPI dashboard specification and follow-up cycle.

## Scripts

- `scripts/emit_schema_checklist.js`: prints schema checklist templates.
- `scripts/validate_geo_brief_json.js`: validates GEO brief JSON structure.

## Evals

- `evals/output-rubric.md`: quality rubric for final output.
- `evals/scenario-checklist.md`: scenario-level coverage checklist.

