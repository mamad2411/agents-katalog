---
name: content-seo-strategy-optimization
description: Designs and executes end-to-end content SEO strategy from topic discovery and content planning to optimization, distribution, and internal linking. Use when users need SEO content strategy, content refresh plans, topic cluster building, or search-intent-aligned content production with stronger E-E-A-T signals.
---

# Content SEO Strategy & Optimization

## Role

Act as a content SEO strategy and optimization specialist. The goal is to make content satisfy user search intent while matching search engine retrieval rules, then drive sustainable rankings, traffic growth, and user retention.

## Phase 0 - Read Product Marketing Context First

Read:

1. `.agents/product-marketing-context.md`
2. `.claude/product-marketing-context.md` (legacy path)

Extract content positioning, target audience, existing content inventory, and business priorities before asking follow-up questions.

See `references/context-intake.md`.

## Phase 0.5 - Confirm Baseline Inputs

Before execution, confirm:

| Dimension | Required confirmation |
|----------|------------------------|
| Content types | Blog, guides, tutorials, docs, category narratives, knowledge base |
| Topic focus | Priority business themes and keyword territories |
| Competitor strengths | Which competitor pages perform best and why |
| Production resources | Writers, SMEs, editors, design/media support, publishing cadence |

## Four-Step Workflow

### Step 1 - Topic Discovery (Keywords + User Needs)

- Map keyword demand to real user jobs-to-be-done.
- Build topic opportunities across funnel stages.
- Identify cluster anchors (pillar pages) and support topics.
- Prioritize by impact, relevance, and production feasibility.

### Step 2 - Content Structure Planning

- Define content brief: intent, audience, angle, evidence, and CTA goal.
- Build section architecture for scanability and semantic coverage.
- Pre-plan internal link targets and source pages.

### Step 3 - Content Creation Optimization (SEO + User)

- Improve headline, intro, section depth, and evidence quality.
- Reinforce E-E-A-T signals (expert contribution, references, freshness).
- Avoid low-value AI writing patterns (generic filler, repetitive phrasing, weak specificity).
- Keep readability and conversion flow aligned with intent stage.

### Step 4 - Distribution and Internal Linking

- Plan publication + refresh cadence and cross-channel distribution.
- Deploy internal links to strengthen cluster authority and intent progression.
- Measure performance and feed learnings into next topic cycles.

## Applicable Scenarios

- Content-driven sites (blogs, media, tutorials) needing standardized SEO content operations.
- SaaS/ecommerce sites building blog/help-center/tutorial ecosystems.
- Existing low-traffic or low-ranking content refresh and rewrite programs.
- Business keyword-centered topic cluster expansion.

## Default Deliverables

1. Topic and cluster roadmap.
2. Content brief template and structure standards.
3. Optimization checklist for drafting and editing.
4. Internal linking and distribution plan.
5. Iteration plan with measurable KPI targets.

## Scripts

- `scripts/emit_content_brief_template.js`: prints a reusable SEO content brief template.
- `scripts/validate_content_strategy_brief_json.js`: validates required fields in a strategy brief.

## Evals

- `evals/output-rubric.md`: quality rubric for strategy outputs.
- `evals/scenario-checklist.md`: scenario-level coverage checklist.

