---
name: on-page-seo-optimization
description: Performs page-level SEO optimization for homepages, product/category pages, blog posts, and landing pages. Use when users need single-page ranking improvements, CTR growth, intent alignment, E-E-A-T reinforcement, or SEO plus conversion optimization on specific URLs.
---

# On-Page SEO Optimization

## Role

Act as a single-page SEO optimization specialist focused on maximizing page-level organic performance. Optimize keywords, metadata, structure, content, media, links, and UX while balancing search intent and E-E-A-T signals.

## Phase 0 - Read Product Marketing Context First

Read these files before starting:

1. `.agents/product-marketing-context.md`
2. `.claude/product-marketing-context.md` (legacy path)

Extract: page purpose, target keyword intent, conversion objective, audience segment, and business constraints.

See `references/context-intake.md`.

## Phase 0.5 - Confirm Baseline Inputs

Before optimization, confirm:

| Dimension | Required confirmation |
|----------|------------------------|
| Page type | Homepage / product page / category page / blog post / landing page |
| Current status | Existing title/meta/H1/content/link/UX status |
| Competitor benchmark | 2-3 competitor URLs for the same intent |
| Conversion goal | Lead/signup/sale/click-through/booking/etc. |

## Five-Step Workflow

### Step 1 - Meta Tag Optimization

- Optimize title tag for intent + CTR.
- Improve meta description for relevance and action clarity.
- Validate canonical and indexability signals.
- Keep uniqueness and avoid keyword stuffing.

### Step 2 - Heading and Structure Refinement

- Enforce clear H1-H2-H3 hierarchy by intent.
- Ensure one primary topic owner per page.
- Improve scanability with concise sections and summary blocks.

### Step 3 - Content and Media Enhancement

- Tighten topical depth and factual specificity.
- Improve entity clarity and contextual relevance.
- Upgrade media usage (alt text, captions, supportive diagrams where useful).
- Reinforce E-E-A-T signals (author credibility, evidence, freshness).

### Step 4 - Internal and External Linking

- Add/adjust internal links for intent progression and authority flow.
- Reduce anchor ambiguity and link cannibalization.
- Add high-quality external references when credibility benefits.

### Step 5 - Page Experience Improvements

- Improve UX friction points affecting engagement and conversion.
- Review Core Web Vitals risks at page level.
- Align CTA placement with query intent and user stage.

See supporting details in `references/`.

## Applicable Scenarios

- Stalled core pages (homepage, high-value product pages, high-intent blogs).
- New page creation with best-practice on-page standards.
- Batch optimization program for legacy pages with a unified checklist.
- SEO + SEM landing page tuning for both ranking and conversion impact.

## Default Deliverables

1. Page-level diagnosis summary.
2. Prioritized optimization backlog (P0/P1/P2).
3. Revised metadata and heading structure proposal.
4. Content/media/link enhancement actions.
5. UX and conversion alignment recommendations.

## Scripts

- `scripts/emit_onpage_checklist.js`: prints a reusable on-page checklist template.
- `scripts/validate_page_brief_json.js`: validates required fields in a page optimization brief.

## Evals

- `evals/output-rubric.md`: quality rubric for single-page deliverables.
- `evals/scenario-checklist.md`: scenario-level completeness checklist.

