---
name: freebird-framework
description: The Freebird product development pipeline — phases, agent roles, artifact flow, and input/output mapping between steps. Use when understanding the full pipeline structure, determining what inputs a phase needs, or identifying what artifacts each agent produces.
---

# Freebird Framework

The Freebird Framework is a structured product development pipeline that takes a product from initial research through discovery, planning, specification, and evaluation. Each phase produces artifacts that the next phase consumes directly.

## Pipeline Overview

```
Phase 1: Discovery          Phase 2: Planning
─────────────────          ─────────────────
User Research       ──┐    Impact Estimation   ──┐
Competitive Analysis──┤    Feature Prioritization─┤
Customer Segmentation─┤ ──▶ PRD Development    ──┤ ──▶
Product Strategy    ──┘    User Journey Mapping──┘

Phase 3: Specification      Phase 4: Evaluation
──────────────────         ─────────────────────
Feature Spec        ──┐    Product Evaluation   ──┐
Acceptance Criteria ──┤    Launch GTM           ──┤
Product QA          ──┤ ──▶ Post-Mortem         ──┘
Product Design Brief──┘
```

## Phase 1: Discovery

**Purpose:** Answer *"What should we build and why?"*

### Step 1: User Research
- **Plugin:** `product-discovery`
- **Agent:** `user-research` (Opus)
- **Inputs:** Raw interviews, surveys, usability tests, support tickets, app reviews, NPS/CSAT data
- **Outputs:** Research Summary, Insight Map, User Needs Document
- **Output file:** `.freebird-cycle/01-user-research.md`

### Step 2: Competitive Analysis
- **Plugin:** `product-discovery`
- **Agent:** `competitive-analysis` (Sonnet)
- **Inputs:** Competitor products, market data, current product capabilities
- **Outputs:** Gap Matrix, Positioning Map, Strategic Recommendations
- **Output file:** `.freebird-cycle/02-competitive-analysis.md`

### Step 3: Customer Segmentation
- **Plugin:** `product-discovery`
- **Agent:** `customer-segmentation` (Opus)
- **Inputs:** Market data, business context, user research, competitive landscape
- **Outputs:** Segment Definitions, ICP Document, TAM Estimate
- **Output file:** `.freebird-cycle/03-customer-segments.md`

### Step 4: Product Strategy
- **Plugin:** `product-discovery`
- **Agent:** `product-strategy` (Opus)
- **Inputs:** ICP, competitive landscape, business goals, user research
- **Outputs:** Product Strategy Document, Monetization Model, Roadmap Priorities
- **Output file:** `.freebird-cycle/04-product-strategy.md`

**Phase 1 Checkpoint:** Present all four artifacts for review before proceeding to Planning.

---

## Phase 2: Planning

**Purpose:** Answer *"What are we building this cycle?"*

### Step 5: Impact Estimation
- **Plugin:** `product-planning`
- **Agent:** `impact-estimation` (Sonnet)
- **Inputs:** Product strategy, feature backlog, ICP, competitive gaps, engineering capacity
- **Outputs:** Impact Scores (RICE), Effort Estimates, Outcome Projections
- **Output file:** `.freebird-cycle/05-impact-estimates.md`

### Step 6: Feature Prioritization
- **Plugin:** `product-planning`
- **Agent:** `feature-prioritization` (Sonnet)
- **Inputs:** Impact scores, effort estimates, constraints, strategic priorities
- **Outputs:** Stack-Ranked Feature Backlog with rationale
- **Output file:** `.freebird-cycle/06-feature-backlog.md`

### Step 7: PRD Development
- **Plugin:** `product-planning`
- **Agent:** `prd-development` (Opus)
- **Inputs:** Product strategy, prioritized backlog, stakeholder input, prior evaluation reports
- **Outputs:** PRD, Stack-Ranked Feature Backlog for the cycle
- **Output file:** `.freebird-cycle/07-prd.md`

### Step 8: User Journey Mapping
- **Plugin:** `product-planning`
- **Agent:** `user-journeys` (Opus)
- **Inputs:** PRD, user research, existing product flows
- **Outputs:** Customer Journey Maps, Edge Case Registry, KPI Acceptance Criteria
- **Output file:** `.freebird-cycle/08-user-journeys.md`

**Phase 2 Checkpoint:** Present PRD and journey maps for review before proceeding to Specification.

---

## Phase 3: Specification

**Purpose:** Answer *"How exactly should this be built?"*

### Step 9: Feature Specification
- **Plugin:** `product-specification`
- **Agent:** `feature-spec` (Opus)
- **Inputs:** PRD, customer journey maps, edge case registry
- **Outputs:** Feature Specs (UI + backend), Definition of Done
- **Output file:** `.freebird-cycle/09-feature-specs.md`

### Step 10: Acceptance Criteria
- **Plugin:** `product-specification`
- **Agent:** `acceptance-criteria` (Sonnet)
- **Inputs:** Feature specs, customer journey maps, edge case registry
- **Outputs:** Acceptance Criteria Document, Definition of Done, Quality Gates
- **Output file:** `.freebird-cycle/10-acceptance-criteria.md`

### Step 11: Product QA
- **Plugin:** `product-specification`
- **Agent:** `product-qa` (Sonnet)
- **Inputs:** Acceptance criteria, customer journey maps, edge case registry
- **Outputs:** Test Case Definitions, Coverage Requirements, Regression Criteria
- **Output file:** `.freebird-cycle/11-test-cases.md`

### Step 12: Product Design Brief
- **Plugin:** `product-specification`
- **Agent:** `product-design-brief` (Sonnet)
- **Inputs:** Feature specs, customer journey maps, brand guidelines
- **Outputs:** Design Brief, Interaction Requirements, Visual Direction Notes
- **Output file:** `.freebird-cycle/12-design-briefs.md`

**Phase 3 Checkpoint:** Present all specification artifacts for review before proceeding to Evaluation.

---

## Phase 4: Evaluation

**Purpose:** Answer *"Did it work, and what do we do next?"*

### Step 13: Product Evaluation
- **Plugin:** `product-evaluation`
- **Agent:** `product-evaluation` (Opus)
- **Inputs:** Shipped feature, acceptance criteria, KPIs, customer journey maps, PRD
- **Outputs:** Evaluation Report (gap analysis, KPI assessment, recommendations)
- **Output file:** `.freebird-cycle/13-evaluation-report.md`

### Step 14: Launch GTM
- **Plugin:** `product-evaluation`
- **Agent:** `launch-gtm` (Sonnet)
- **Inputs:** Evaluation report, feature specs, acceptance criteria, user segments
- **Outputs:** Launch Plan, Rollout Strategy, Monitoring Dashboard Requirements
- **Output file:** `.freebird-cycle/14-launch-plan.md`

### Step 15: Post-Mortem
- **Plugin:** `product-evaluation`
- **Agent:** `post-mortem` (Sonnet)
- **Inputs:** Evaluation report, cycle timeline, team feedback, incident logs
- **Outputs:** Post-Mortem Report, Improvement Recommendations, Process Changes
- **Output file:** `.freebird-cycle/15-post-mortem.md`

---

## Artifact Flow Summary

| Step | Produces | Consumed By |
|------|---------|-------------|
| 01 user-research | Research insights | 03, 04, 07, 08 |
| 02 competitive-analysis | Gap matrix, positioning | 04, 05 |
| 03 customer-segmentation | ICP, TAM, segments | 04, 07, 08 |
| 04 product-strategy | Strategy, roadmap | 05, 07 |
| 05 impact-estimation | RICE scores | 06 |
| 06 feature-backlog | Prioritized backlog | 07 |
| 07 prd | PRD | 08, 09, 13 |
| 08 user-journeys | Journey maps, edge cases | 09, 10, 11, 12 |
| 09 feature-specs | Feature specs | 10, 12 |
| 10 acceptance-criteria | AC, DoD, quality gates | 11, 13 |
| 11 test-cases | Test case definitions | 13 |
| 12 design-briefs | Design briefs | (design team external) |
| 13 evaluation-report | Evaluation, gaps, KPIs | 14, 15 |
| 14 launch-plan | Rollout plan | (engineering, comms) |
| 15 post-mortem | Improvements | (feeds next cycle's step 07) |

## State File Schema

`.freebird-cycle/state.json`:

```json
{
  "product": "Product description",
  "status": "in_progress",
  "current_step": 1,
  "current_phase": 1,
  "completed_steps": [],
  "files_created": [],
  "started_at": "ISO_TIMESTAMP",
  "last_updated": "ISO_TIMESTAMP"
}
```

## Running a Partial Cycle

The pipeline can be entered at any phase if prior phases have already been completed:

- **Start at Phase 2:** Requires `.freebird-cycle/04-product-strategy.md` to exist
- **Start at Phase 3:** Requires `.freebird-cycle/07-prd.md` and `.freebird-cycle/08-user-journeys.md` to exist
- **Start at Phase 4:** Requires `.freebird-cycle/10-acceptance-criteria.md` to exist
