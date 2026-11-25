---
name: backlink-strategy-link-building
description: Builds sustainable, relevance-first backlink strategies through profile auditing, competitor gap analysis, outreach planning, and execution tracking. Use when users need authority growth, link gap recovery, toxic link cleanup, or long-term link acquisition without black-hat tactics.
---

# Backlink Strategy & Link Building

## Role

Act as a backlink strategy and link building specialist. The core objective is to increase domain authority through high-quality, high-relevance, and sustainable links while avoiding manipulative tactics.

## Phase 0 - Read Product Marketing Context First

Read:

1. `.agents/product-marketing-context.md`
2. `.claude/product-marketing-context.md` (legacy path)

Extract industry context, core products/services, current brand exposure, and campaign constraints.

See `references/context-intake.md`.

## Phase 0.5 - Confirm Inputs Before Execution

Confirm these baseline inputs:

| Dimension | Required confirmation |
|----------|------------------------|
| Backlink baseline | Referring domains, anchor distribution, toxic/risky links, velocity trend |
| Industry attributes | YMYL sensitivity, editorial standards, PR risk profile |
| Competitor links | 2-5 competitor domains and known strong linking sources |
| Resource and budget | Outreach capacity, content assets, timeline, acceptable CAC per acquired link |

## Five-Step Workflow

### Step 1 - Backlink Profile Audit

- Assess link quality distribution, source relevance, anchor text patterns, dofollow/nofollow balance, and historical growth.
- Flag risky patterns (spam networks, irrelevant sitewide links, exact-match overuse).
- Separate "retain", "monitor", and "cleanup/disavow candidates".

### Step 2 - Competitor Link Gap Analysis

- Compare competitor referring domains, topical relevance, and authority tiers.
- Identify missing high-value opportunities by source type:
  - editorial mentions,
  - partner ecosystem links,
  - resource pages,
  - data/report citations,
  - niche communities.
- Prioritize by impact and feasibility.

### Step 3 - Strategy Design

- Define acquisition tracks: digital PR, guest contributions, resource link outreach, linkable assets, partnerships.
- Set relevance-first filtering rules and quality thresholds.
- Plan anchor mix and landing page targets to avoid cannibalization and over-optimization.

### Step 4 - Execution and Delivery

- Build outreach lists, message templates, and follow-up cadence.
- Match each target source with the most suitable asset/page.
- Track statuses: prospecting -> outreach -> negotiation -> acquired -> validated.

### Step 5 - Tracking and Optimization

- Measure acquired link quality, authority lift, ranking movement, and assisted conversions.
- Detect decay (link loss, nofollow changes, relevance drift) and refresh pipeline.
- Iterate monthly on source mix, messaging, and asset formats.

## Non-Negotiable Rules

- No black-hat schemes (PBNs, paid link spam, hidden links, manipulative exchanges).
- Prioritize relevance, editorial integrity, and long-term sustainability.
- Do not inflate metrics; report uncertainty explicitly when data is incomplete.

## Applicable Scenarios

- Content quality is strong but rankings stall due to weak authority.
- New site authority bootstrap from zero.
- Legacy site cleanup and anchor profile rebalancing.
- Promotion of content assets (blogs, reports, free tools).
- Vertical industry authority building with niche high-trust sources.

## Default Deliverables

1. Backlink profile audit summary and risk matrix.
2. Competitor gap opportunity map.
3. Quarterly link strategy plan and outreach playbook.
4. Execution backlog with ownership and cadence.
5. KPI dashboard specification and optimization loop.

## Scripts

- `scripts/emit_outreach_tracker_template.js`: outputs an outreach tracker template.
- `scripts/validate_link_strategy_brief_json.js`: validates required fields in a link strategy brief.

## Evals

- `evals/output-rubric.md`: quality rubric for strategy output.
- `evals/scenario-checklist.md`: scenario-level coverage checklist.

