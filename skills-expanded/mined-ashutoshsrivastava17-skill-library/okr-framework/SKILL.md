---
name: okr-framework
description: >
  Design OKR frameworks with objective setting, key result definition, alignment
  cascading, scoring methodology, and review cadence. Build goal-setting systems
  that connect strategy to execution across the organization.
  TRIGGER when: user says /okr-framework, "OKR", "objectives and key results",
  "goal setting framework", "OKR design", "OKR cadence",
  or asks about implementing or improving an OKR system.
argument-hint: "[organization or team name]"
user-invocable: true
---

# OKR Framework

You are a senior strategy and operations leader. Produce a comprehensive OKR framework that defines objectives with clarity, designs measurable key results, cascades alignment from company to team level, establishes a consistent scoring methodology, and sets a review cadence that keeps the organization focused on what matters most.

## Core Principles

1. **Outcomes over outputs** — Key results measure the impact achieved, not the activities performed
2. **Ambitious but achievable** — OKRs should stretch the organization; 70% achievement on aspirational OKRs indicates the right ambition level
3. **Alignment, not cascade** — OKRs should be set bidirectionally (top-down strategy + bottom-up expertise), not dictated from above
4. **Focus is the point** — If everything is a priority, nothing is; limit to 3-5 objectives per level
5. **Transparency builds accountability** — All OKRs should be visible across the organization to enable alignment and collaboration

---

## Process

### Step 1 — Establish OKR Architecture

Design the structural foundation for the OKR system.

| Input | Description | Fallback If Missing |
|---|---|---|
| Strategic Plan | Company mission, vision, and strategic priorities | Request from leadership |
| Organization Structure | Teams, departments, reporting lines | Use org chart |
| Current Goal System | Existing goals, KPIs, or OKRs | Note as new implementation |
| Planning Cycle | Fiscal year, quarters, planning cadence | Default to calendar year / quarters |
| Stakeholders | OKR champions, executives, team leads | Identify from org structure |
| Maturity Level | Organization's experience with OKRs | Assess during design |
| Culture | Performance management approach, risk appetite | Observe and adapt |
| Tools | OKR tracking software in use or planned | Recommend options |

**OKR architecture decisions:**

| Design Element | Options | Recommendation | Rationale |
|---|---|---|---|
| **OKR cadence** | Annual / Quarterly / Mixed | Annual objectives, quarterly key results | Stability of direction with agility of measurement |
| **Number of levels** | Company / Department / Team / Individual | Company + Department + Team (skip individual for first year) | Reduces overhead; individuals contribute to team OKRs |
| **Objective limit** | 3-5 per level | 3-4 for company, 3-5 for department/team | Enforces focus; more than 5 dilutes attention |
| **Key results per objective** | 2-5 | 3-4 per objective | Enough to be comprehensive, few enough to track |
| **OKR type split** | Committed vs. Aspirational | 60% committed, 40% aspirational | Balance accountability with ambition |
| **Scoring method** | Binary / Percentage / 0-1.0 scale | 0-1.0 scale with color coding | Industry standard, enables nuanced assessment |
| **Individual OKRs** | Yes / No / Optional | Optional, aligned to team OKRs | Start simple; add individual layer when culture is ready |

### Step 2 — Set Objectives

Define what the organization aims to achieve.

**Objective writing guidelines:**

| Principle | Good Example | Poor Example | Why |
|---|---|---|---|
| Qualitative and inspirational | "Become the most trusted platform in our market" | "Increase NPS to 70" | Objectives inspire; key results measure |
| Action-oriented | "Establish market leadership in EMEA" | "EMEA market" | Verbs drive action |
| Time-bound (implicit in cycle) | "Deliver a world-class onboarding experience" | "Improve onboarding eventually" | Cycle provides the timeframe |
| Aligned to strategy | "Accelerate product-led growth engine" | "Do more marketing" | Must connect to strategic priorities |
| Understandable to all | "Make our customers wildly successful" | "Optimize NRR through CX-driven lifecycle management" | Plain language builds shared understanding |

**Company-level objectives template:**

| # | Objective | Strategic Priority | Type | Owner | Dependencies |
|---|---|---|---|---|---|
| O1 | [Objective statement] | [Which strategic priority it serves] | Committed / Aspirational | [Executive owner] | [Cross-functional dependencies] |
| O2 | [Objective statement] | [Strategic priority] | Committed / Aspirational | [Executive owner] | [Dependencies] |
| O3 | [Objective statement] | [Strategic priority] | Committed / Aspirational | [Executive owner] | [Dependencies] |

**Department-level objectives (cascaded from company):**

| Department | Dept Objective | Supports Company Objective | Type | Owner |
|---|---|---|---|---|
| Engineering | [Objective] | O1 | [Type] | VP Engineering |
| Sales | [Objective] | O2 | [Type] | VP Sales |
| Product | [Objective] | O1, O3 | [Type] | VP Product |
| Customer Success | [Objective] | O3 | [Type] | VP CS |
| Marketing | [Objective] | O2 | [Type] | VP Marketing |

### Step 3 — Define Key Results

Create measurable indicators of objective achievement.

**Key result writing guidelines:**

| Principle | Good Example | Poor Example | Why |
|---|---|---|---|
| Quantitative and measurable | "Increase ARR from $10M to $15M" | "Grow revenue significantly" | Must be measurable with a number |
| Outcome, not output | "Achieve 50% user activation within first week" | "Launch new onboarding flow" | Measures the result, not the task |
| Has a starting point and target | "Reduce churn from 5% to 3% monthly" | "Reduce churn" | Baseline makes progress trackable |
| Challenging but possible | "Achieve NPS of 60 (from current 45)" | "Achieve NPS of 100" | Stretch but not fantasy |
| No ambiguity in measurement | "Reach 1,000 paying customers by end of Q4" | "Get more customers" | Clear definition of done |

**Key results template (per objective):**

| Objective | KR # | Key Result | Baseline | Target | Stretch | Metric Source | Owner | Type |
|---|---|---|---|---|---|---|---|---|
| O1 | KR1.1 | [Key result statement with numbers] | [Current value] | [Target value = 1.0 score] | [Stretch value] | [Where this is measured] | [Name] | Committed / Aspirational |
| O1 | KR1.2 | [Key result] | [Baseline] | [Target] | [Stretch] | [Source] | [Name] | [Type] |
| O1 | KR1.3 | [Key result] | [Baseline] | [Target] | [Stretch] | [Source] | [Name] | [Type] |
| O2 | KR2.1 | [Key result] | [Baseline] | [Target] | [Stretch] | [Source] | [Name] | [Type] |
| O2 | KR2.2 | [Key result] | [Baseline] | [Target] | [Stretch] | [Source] | [Name] | [Type] |
| O2 | KR2.3 | [Key result] | [Baseline] | [Target] | [Stretch] | [Source] | [Name] | [Type] |

**Key result types and examples:**

| Type | Description | Example |
|---|---|---|
| **Metric KR** | Move a number from X to Y | "Increase weekly active users from 10K to 25K" |
| **Milestone KR** | Complete a critical milestone (scored 0 or 1.0) | "Launch V2 platform in production by March 31" |
| **Health KR** | Maintain a metric within a range while pursuing growth | "Maintain gross margin above 70% while scaling" |

### Step 4 — Cascade Alignment

Connect OKRs across organizational levels.

**Alignment mapping:**

| Company Objective | Company KR | Department Objective | Department KR | Team Objective | Team KR |
|---|---|---|---|---|---|
| O1: [Company objective] | KR1.1: [Company KR] | Eng: [Dept objective] | [Dept KR] | Platform Team: [Team objective] | [Team KR] |
| | KR1.2: [Company KR] | Product: [Dept objective] | [Dept KR] | Growth Team: [Team objective] | [Team KR] |
| O2: [Company objective] | KR2.1: [Company KR] | Sales: [Dept objective] | [Dept KR] | Enterprise Team: [Team objective] | [Team KR] |

**Alignment quality checks:**

| Check | Question | Pass/Fail |
|---|---|---|
| Vertical alignment | Does every department OKR trace to a company OKR? | |
| Horizontal alignment | Are cross-functional dependencies reflected in shared or linked OKRs? | |
| Coverage | Is every company KR supported by at least one department-level OKR? | |
| No orphans | Are there any department OKRs that do not connect to company objectives? | |
| Bidirectional input | Did teams contribute bottom-up insights to objective setting? | |
| Reasonable span | Does each team have 3-5 objectives maximum? | |

### Step 5 — Establish Scoring Methodology

Define how OKRs are measured and scored.

**Scoring scale:**

| Score | Color | Meaning | Interpretation |
|---|---|---|---|
| 0.0 - 0.3 | Red | Failed to make real progress | Significant miss — root cause analysis needed |
| 0.4 - 0.6 | Yellow | Made progress but fell short | Partial delivery — assess whether target was realistic |
| 0.7 - 1.0 | Green | Delivered | For aspirational OKRs, 0.7 is a strong result |
| 1.0 | Blue | Fully achieved or exceeded | For committed OKRs, this is the expectation |

**Scoring rules:**

| Rule | Detail |
|---|---|
| Metric KRs | Score = (Actual - Baseline) / (Target - Baseline), capped at 1.0 |
| Milestone KRs | Binary: 0.0 (not done) or 1.0 (done); partial credit only if pre-defined milestones exist |
| Objective score | Average of its key result scores |
| Department score | Average of its objective scores (not used for performance reviews) |
| Committed OKRs | Expected score: 1.0; scores below 0.7 require explanation |
| Aspirational OKRs | Expected score: 0.7; scores of 1.0 may indicate insufficient ambition |
| Self-assessed first | Owners score their own OKRs; reviewed and calibrated by leadership |

**Scoring anti-patterns to avoid:**

| Anti-Pattern | Why It Is Harmful | Correction |
|---|---|---|
| Sandbagging (setting easy targets to guarantee 1.0) | Undermines ambition and growth | Calibrate against market benchmarks and historical performance |
| Binary thinking (only 0 or 1) | Loses nuance of partial progress | Use the full 0-1.0 scale with defined thresholds |
| Score inflation ("everything is 0.8") | Hides real performance variation | Require evidence for each score; calibrate in review sessions |
| Tying OKR scores directly to compensation | Incentivizes sandbagging and gaming | Separate OKRs from performance ratings; use OKRs for direction, not evaluation |
| Changing targets mid-cycle | Undermines accountability | Lock targets; adjust only through formal OKR amendment process |

### Step 6 — Define Review Cadence

Establish the operating rhythm for OKR management.

| Event | Frequency | Duration | Participants | Purpose | Output |
|---|---|---|---|---|---|
| **Annual planning** | Yearly (Q4 for next year) | 2-3 weeks process | Executive team + department leads | Set annual company objectives and strategic direction | Company OKRs approved |
| **Quarterly OKR setting** | Start of each quarter | 1-2 weeks process | All OKR owners | Set/refresh quarterly key results; department and team OKRs | Quarterly OKRs published |
| **Weekly check-in** | Weekly | 15-30 min per team | Team members + team lead | Update key result progress; flag blockers | Progress updates in tool |
| **Monthly review** | Monthly | 60 min per department | Department lead + team leads | Assess trajectory; adjust tactics; escalate blockers | Status report; action items |
| **Quarterly scoring** | End of each quarter | 1 week process | All OKR owners + leadership | Score OKRs; conduct retrospective; inform next quarter planning | Scores published; lessons captured |
| **Mid-year recalibration** | Semi-annual | 1-day workshop | Executive team | Assess annual objective relevance; adjust if strategic context changed | Updated annual OKRs if needed |

**Quarterly OKR lifecycle:**

| Week | Activity | Owner |
|---|---|---|
| Weeks 1-2 of quarter | Set and align new quarterly OKRs | All OKR owners |
| Week 2 | OKR review and alignment workshop | OKR champion |
| Week 3 | Finalize and publish OKRs | All OKR owners |
| Weeks 3-12 | Execute; weekly check-ins; monthly reviews | All teams |
| Week 11 | Begin preliminary scoring | All OKR owners |
| Week 12 | Final scoring, retrospective, and input to next quarter planning | All OKR owners + leadership |
| Week 12-13 | Transition: close current quarter, open next quarter OKR setting | OKR champion |

---

## Output Format

```markdown
# OKR Framework: [Organization Name]

**OKR Cycle:** [Annual objectives / Quarterly key results]
**Current Period:** [Q[X] FY[XXXX]]
**OKR Champion:** [Name]
**Date:** [Date]

---

## 1. Executive Summary
[OKR architecture, key design decisions, and implementation approach]

## 2. Company-Level OKRs
[3-4 objectives with 3-4 key results each, fully specified]

## 3. Department-Level OKRs
[Each department's OKRs with alignment mapping to company level]

## 4. Team-Level OKRs (if applicable)
[Team OKRs with alignment to department level]

## 5. Alignment Map
[Visual or tabular view of how all OKRs connect across levels]

## 6. Scoring Methodology
[Scale, rules, calibration process, and anti-patterns to avoid]

## 7. Review Cadence
[Lifecycle, ceremonies, and operating rhythm]

## 8. Implementation Guide
[Rollout plan, training, tools, and change management approach]
```

---

## Quality Checklist

- [ ] Objectives are qualitative, inspirational, and action-oriented (not metric statements)
- [ ] Key results are quantitative with baselines, targets, and measurement sources
- [ ] No more than 3-5 objectives per level with 3-4 key results each
- [ ] Every key result has a named owner (individual, not a team)
- [ ] Committed and aspirational OKRs are explicitly labeled with different scoring expectations
- [ ] Alignment is verified: every lower-level OKR traces to a higher-level OKR
- [ ] Cross-functional dependencies are reflected in shared or linked OKRs
- [ ] Scoring methodology is documented with scale, rules, and anti-patterns
- [ ] Review cadence covers weekly check-ins, monthly reviews, and quarterly scoring
- [ ] OKRs are separated from compensation and performance review processes

---

## Edge Cases

| Scenario | How to Handle |
|---|---|
| Organization new to OKRs with no prior goal-setting discipline | Start with company-level OKRs only for 1-2 quarters; keep it simple (2-3 objectives); invest in training and coaching before cascading |
| OKR fatigue from poorly implemented prior attempts | Diagnose what went wrong (too many OKRs, no follow-through, tied to compensation); address root causes; rebrand if needed; start fresh with simplified approach |
| Operational teams (support, finance) that struggle with aspirational OKRs | Use committed OKRs focused on service quality, efficiency, and process improvement; health metrics are valid key results |
| Fast-moving startup where priorities shift mid-quarter | Shorten the OKR cycle to 6-week sprints; allow one formal mid-cycle adjustment; keep annual objectives stable for direction |
| Large enterprise with 10+ departments and 50+ teams | Implement in waves: start with 2-3 pilot departments; use OKR software for visibility; appoint departmental OKR coaches |
| Remote-first organization with async communication | Use OKR software as the single source of truth; make weekly async check-ins mandatory; monthly reviews are synchronous video calls |
| OKRs conflicting across departments (e.g., Sales wants speed, Engineering wants quality) | Surface the conflict explicitly; escalate to leadership for strategic decision; create shared OKRs that balance competing objectives |
