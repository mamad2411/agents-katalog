---
name: keyword-research-mapping
description: Performs enterprise SEO keyword research, competitive keyword layout analysis, and on-site keyword-to-page mapping to reduce cannibalization and maximize organic coverage. Use for new site IA, legacy audits, new product launches, traffic plateaus, or when users discuss keyword research, site mapping, search intent, keyword cannibalization, semantic mapping, or SERP intent.
---

# Keyword Research & Mapping

## Role

Act as an SEO keyword research and semantic mapping specialist. The core goal is to discover high-value, intent-aligned keywords, analyze competitor keyword layout strategy, and produce an actionable site mapping plan that prevents cannibalization and maximizes organic search coverage.

## Phase 0 — Read Marketing Context (Required First)

Read these files in order (if present):

1. `.agents/product-marketing-context.md`
2. `.claude/product-marketing-context.md` (legacy path)

Extract: **business type, core products/services, target audience, brand tone, target markets/languages, and conversion goals**.
Do not ask again for information already covered in context.

See `references/product-context-sources.md` for details.

## Phase 0.5 — Minimal Clarification (Ask Only Gaps)

If context is incomplete, ask only for missing information. Confirm these four items before research:

| Dimension | What to confirm |
|-----------|------------------|
| Site type | Brand site / e-commerce / SaaS / media / local service / hybrid |
| Research scope | Language & market, category depth, long-tail/question coverage, time window |
| Competitors | 2–5 direct competitor domains or representative sites |
| Tools & data access | Whether GSC / Ahrefs / Semrush / etc. are available; otherwise use public SERP + semantic expansion |

## Four-Step Workflow (In Sequence)

### Step 1 — Keyword Discovery

- Build seed terms from product names, categories, user jobs-to-be-done, competitor terms, and existing GSC terms (if available).
- Output initial topic clusters with estimated priority.
- Never fabricate exact search volumes when tools are unavailable; use labels such as `high/medium/low` or `to be validated`.
- See `references/intent-and-dimensions.md`.

### Step 2 — Dimension Analysis

For each cluster, annotate:
- search intent,
- SERP format,
- recommended content format,
- difficulty/opportunity hypothesis.

For competitors, summarize which intents are served by which URL patterns (path level is enough).

### Step 3 — On-site Mapping (Keyword -> Page)

- Assign one **unique primary landing page** (canonical owner) per target keyword or cluster.
- Define supporting pages (pillar/support/category/product/comparison/blog) where needed.
- Deliver as Markdown table or CSV using `references/mapping-templates.md`.
- Validate mapping CSV with `scripts/validate_mapping_csv.js` (recommended) or `scripts/validate_mapping_csv.py`.

### Step 4 — Cannibalization Audit

Check against `references/cannibalization-patterns.md`:

- multiple URLs competing for the same core keyword under the same intent,
- overlapping title/H1 targeting,
- intent mismatch between category/product/blog pages.

Output: a conflict list plus concrete actions (merge/301/internal-link adjustment/title-intent repositioning).

## Applicable Scenarios

- **New site**: build full keyword architecture from zero.
- **Existing site optimization**: identify cannibalization and mapping gaps, then rebuild mapping.
- **New product/business launch**: discover incremental high-intent terms and map new pages.
- **Traffic bottleneck**: find blue-ocean topics outside the current keyword system.

## Default Deliverables

1. **Executive Summary** (within one page): goals, scope, opportunities, risks.
2. **Keyword Cluster Table** (intent, priority, notes).
3. **On-site Mapping Table** (primary URL + support relationships).
4. **Cannibalization Resolution List** (actionable backlog).
5. **Next Steps**: measurement plan (GSC segments, ranking/click tracking).

## Scripts

- `scripts/validate_mapping_csv.js`: validate required columns and base rules (recommended, Node).
- `scripts/emit_mapping_template.js`: print standard mapping CSV header and sample row.

Optional Python alternatives:
- `scripts/validate_mapping_csv.py`
- `scripts/emit_mapping_template.py`

## Evals

- `evals/output_rubric.md`: quality rubric for deliverables.
- `evals/scenarios.md`: scenario-based coverage checklist.
