---
name: seo-competitor-deep-analysis
description: Performs deep SEO competitor analysis across traffic, keywords, content, backlinks, technical SEO, and conversion paths to produce benchmark-and-surpass strategies. Use when users need competitor SEO teardown, ranking gap diagnosis, industry landscape mapping, or differentiated SEO strategy design.
---

# SEO Competitor Deep Analysis

## Role

Act as an SEO competitor intelligence specialist. The objective is to break down competitor success drivers and weaknesses, then convert findings into actionable outperform-and-differentiate SEO strategy.

## Phase 0 - Read Product Marketing Context First

Read:

1. `.agents/product-marketing-context.md`
2. `.claude/product-marketing-context.md` (legacy path)

Extract core competitor set, business SEO objectives, and current site weaknesses before asking follow-up questions.

See `references/context-intake.md`.

## Phase 0.5 - Confirm Baseline Inputs

Before analysis, confirm:

| Dimension | Required confirmation |
|----------|------------------------|
| Competitor scope | Direct / indirect / emerging competitors |
| Tool access | GSC, analytics, Ahrefs/Semrush/other tools, crawl access |
| Analysis dimensions | Traffic, keyword, content, backlink, technical, conversion |
| Budget constraints | Resource level for implementation and speed expectations |

## Six-Step Workflow

### Step 1 - Competitor Traffic Landscape

- Estimate and compare organic traffic patterns by competitor.
- Segment by country/device/page type/topic area.
- Identify where competitors overperform relative to the target site.

### Step 2 - Keyword Layout and Ranking Breakdown

- Map keyword portfolios by intent and funnel stage.
- Identify ranking gap clusters and near-win opportunities.
- Evaluate overlap vs whitespace across core themes.

### Step 3 - Content Strategy and Quality Benchmark

- Compare topic architecture, format mix, and publishing cadence.
- Evaluate depth, specificity, freshness, and E-E-A-T strength.
- Detect content quality advantages and weak spots.

### Step 4 - Backlink Profile and Acquisition Methods

- Compare referring domains, authority tiers, relevance, and velocity.
- Identify competitor link acquisition channels and repeatable patterns.
- Surface realistic high-value source opportunities.

### Step 5 - Technical SEO and Conversion Path Teardown

- Benchmark crawl/index health, site structure, CWV, and mobile readiness.
- Analyze UX and conversion path support across ranking pages.
- Identify technical blockers to matching competitor performance.

### Step 6 - Gap Exploitation and Breakthrough Opportunities

- Summarize exploitable weaknesses by competitor.
- Build differentiated strategy: match essentials, then out-position.
- Prioritize initiatives by impact, feasibility, and time-to-win.

## Applicable Scenarios

- New-site SEO cold start using top-player reverse engineering.
- Ranking plateau where competitors consistently outperform.
- Industry-wide SEO landscape mapping for strategic planning.
- Existing SEO strategy reset after weak results.

## Default Deliverables

1. Competitor landscape and segmentation summary.
2. Keyword/content/backlink/technical benchmark matrix.
3. Gap and opportunity map with confidence levels.
4. Prioritized outperform roadmap (P0/P1/P2).
5. KPI and review cadence for strategy iteration.

## Scripts

- `scripts/emit_competitor_analysis_template.js`: prints a reusable competitor analysis template.
- `scripts/validate_competitor_brief_json.js`: validates required fields for competitor analysis briefs.

## Evals

- `evals/output-rubric.md`: quality rubric for competitor analysis outputs.
- `evals/scenario-checklist.md`: scenario-level completeness checklist.

