---
name: market-awareness-analyzer
description: "Analyzes market awareness distribution from a PR/FAQ document using built-in web search, Apify actors for Google Trends and Reddit, and news/YouTube via Apify or direct API. Use when (1) you have a PR/FAQ and need content strategy recommendations, (2) determining what keywords to target for each awareness stage, (3) creating a content calendar based on where your market sits, (4) validating PR/FAQ positioning against actual market search behavior, or (5) finding content gaps and placement opportunities. Triggers on phrases like 'analyze my PR/FAQ,' 'content strategy for,' 'keyword research,' 'where is my market,' 'what content should I create,' 'awareness stage analysis.' Uses Claude's built-in `WebSearch` for SERP/news, Apify actors (via `mcp__Apify__call-actor`) for Trends/Reddit/YouTube. Optional SparkToro data (manual input). Use problem-awareness-discovery skill BEFORE this one if you don't yet have a validated PR/FAQ."
---

# Market Awareness Analyzer

Transform a PR/FAQ into validated keyword targets and content strategy recommendations based on where the market actually sits across the 5 Awareness Stages.

## Workflow Overview

```
1. EXTRACT PR/FAQ elements (problem, solution, buyer, user)
2. GENERATE awareness-stage keywords (Stage 2, 3, 4)
3. VALIDATE with search tools (web, trends, news, YouTube, Reddit)
4. SYNTHESIZE market awareness distribution
5. RECOMMEND content strategy + placement opportunities
6. GENERATE comprehensive markdown report
```

## Input Requirements

**Required:** PR/FAQ document containing:
- Problem statement
- Solution description
- Target buyer (decision maker)
- Target user (daily practitioner)
- Key benefits/differentiators
- FAQ section (optional but helpful)

**Optional:** SparkToro data, known competitors, existing keywords.

## Phase 1: PR/FAQ Element Extraction

Extract structured elements:

| Category | Elements |
|----------|----------|
| **Problem** | Core pain, symptoms, consequences, triggering events |
| **Solution** | Category, differentiators, mechanism, outcome |
| **Buyer** | Title, responsibilities, decision criteria |
| **User** | Title, daily activities, pain points |

## Phase 2: Keyword Generation

Generate 10-15 keywords per awareness stage.

See [references/keyword-patterns.md](references/keyword-patterns.md) for patterns.

**Stage 2 (Problem-Aware):**
- Pattern: "why [symptom]" / "how to fix [problem]"
- Focus: Problem language, not solution language

**Stage 3 (Solution-Aware):**
- Pattern: "best [category]" / "[solution type] comparison"
- Focus: Category shopping, feature seeking

**Stage 4 (Product-Aware):**
- Pattern: "[product] vs" / "[product] review"
- Focus: Direct comparisons, decision-stage

## Phase 3: Multi-Source Validation

Each source maps to a directly-callable tool. See [references/tool-execution.md](references/tool-execution.md) for the exact invocation patterns.

| Source | Tool | Purpose |
|--------|------|---------|
| Web | Built-in `WebSearch` | SERP intent, competitor content |
| Trends | Apify `apify/google-trends-scraper` via `mcp__Apify__call-actor` | Relative volume, rising queries |
| News | Built-in `WebSearch` (filter to news domains) | Forcing functions, media angles |
| YouTube | Apify `apify/youtube-scraper` via `mcp__Apify__call-actor` | Content gaps, creator landscape |
| Reddit | Apify `trudax/reddit-scraper` via `mcp__Apify__call-actor` | Language validation, sentiment |

## Phase 4: Distribution Synthesis

Estimate market distribution:

| Stage | Signals |
|-------|---------|
| Unaware | Cannot reach via content marketing |
| Problem-Aware | Problem query volume, Reddit frustration posts |
| Solution-Aware | Category query volume, comparison searches |
| Product-Aware | Branded searches, review queries |
| Most-Aware | Existing customer signals |

## Phase 5: Content Strategy

Based on distribution, recommend priorities.

See [references/content-matrix.md](references/content-matrix.md) for detailed recommendations.

**If Stage 2 dominant (>40%):**
- Create problem-validation content
- "Why [symptom] happens", "Hidden cost of [problem]"

**If Stage 3 dominant (>40%):**
- Create category education content
- "How to evaluate [solution category]", "Buyer's guide"

**If Stage 4 dominant (>30%):**
- Create comparison/proof content
- "[Product] vs [Alternative]", case studies, ROI calculators

**Also identify:**
- External forcing functions to position around
- Content placement opportunities (podcasts, publications)
- What NOT to create (waste of resources)

## SparkToro Integration

If provided, integrate audience data for:
- Content placement targets (podcasts, publications)
- Influencer identification per stage
- Keyword expansion
- ICP validation

See [references/sparktoro-integration.md](references/sparktoro-integration.md).

## Phase 6: Report Generation

Generate a comprehensive markdown report as the final deliverable.

**File location:** `/mnt/user-data/outputs/Market_Awareness_Analysis_[Product_Name].md`

**Report sections:**
1. Executive Summary (2-3 sentences)
2. PR/FAQ Elements Extracted (problem, solution, personas)
3. Keyword Research Results (by stage with tables)
4. Multi-Source Validation Results (Trends, Web, Reddit, News)
5. Market Awareness Distribution (visual + evidence table)
6. Strategic Recommendations (content priority, calendar, placement)
7. PR/FAQ Alignment Assessment (language alignment score)
8. Appendix (tools used, keywords researched)

See [references/report-template.md](references/report-template.md) for complete template.

**Delivery:**
1. Create report with `create_file` tool
2. Present to user with `present_files` tool
3. Offer DOCX/PPTX conversion if requested

## Output Format

Generate and save a comprehensive markdown report. See [references/report-template.md](references/report-template.md) for the complete template structure.

**Key sections include:**
- Executive Summary
- PR/FAQ Elements Extracted
- Keyword Research Results (by stage)
- Multi-Source Validation Results
- Market Awareness Distribution (with visual diagram)
- Strategic Recommendations (content priority, calendar, what NOT to create)
- PR/FAQ Alignment Assessment
- Appendix

**Always deliver as a file** saved to `/mnt/user-data/outputs/` and presented to user.

## Critical Reminders

1. Extract PR/FAQ elements BEFORE generating keywords
2. Validate keywords with search data, don't assume
3. Cross-reference multiple sources for confidence
4. Recommend specific content, not just data
5. Include what NOT to create
6. Identify forcing functions for timing
