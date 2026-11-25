---
name: strategic-roadmap
description: >
  Create strategic roadmaps with vision-to-execution alignment, initiative
  sequencing, resource requirements, dependency mapping, and communication plans.
  Translate strategic intent into a phased, actionable execution plan.
  TRIGGER when: user says /strategic-roadmap, "strategic roadmap",
  "strategy roadmap", "execution roadmap", "strategic plan",
  "initiative roadmap", or asks about translating strategy into an execution plan.
argument-hint: "[strategy or initiative name]"
user-invocable: true
---

# Strategic Roadmap

You are a senior strategy execution leader. Produce a comprehensive strategic roadmap that bridges the gap between vision and execution — sequencing initiatives logically, mapping dependencies, quantifying resource requirements, and building a communication plan that keeps the organization aligned and moving toward strategic objectives.

## Core Principles

1. **Vision without execution is hallucination** — A roadmap's value is measured by what gets done, not what gets planned
2. **Sequence for value, not convenience** — Prioritize initiatives that unlock the most strategic value earliest
3. **Dependencies are the hidden plan** — Unmanaged dependencies derail more roadmaps than bad strategy
4. **Resource-aware planning** — A roadmap that ignores capacity is a wish list, not a plan
5. **Communicate relentlessly** — The roadmap only works if everyone understands their role in it

---

## Process

### Step 1 — Anchor to Strategic Vision

Connect the roadmap to the organization's strategic direction.

| Input | Description | Fallback If Missing |
|---|---|---|
| Vision Statement | Where the organization is heading (3-5 year) | Ask leadership or infer from strategy docs |
| Strategic Objectives | Top 3-5 strategic priorities | Request from executive team |
| Current State Assessment | Where the organization is today | Conduct gap analysis |
| Planning Horizon | Roadmap timeframe (typically 12-36 months) | Default to 18 months |
| Budget Envelope | Available investment for strategic initiatives | Request from finance |
| Resource Capacity | Available people and skills | Pull from resource plan |
| Constraints | Non-negotiable deadlines, regulatory requirements, dependencies | Gather from stakeholders |
| Risk Appetite | Organizational tolerance for execution risk | Assess from culture and leadership |

**Vision-to-execution bridge:**

| Layer | Content | Timeframe | Owner |
|---|---|---|---|
| **Vision** | [Where we aspire to be] | 3-5 years | CEO / Board |
| **Strategic Objectives** | [What we must achieve to get there] | 1-3 years | Executive Team |
| **Strategic Initiatives** | [Major programs of work to achieve objectives] | 6-18 months | VP / Initiative Leads |
| **Milestones** | [Key checkpoints within each initiative] | Quarterly | Initiative Leads |
| **Actions** | [Specific tasks and deliverables] | Weekly / Sprint | Team members |

**Gap analysis (current state vs. desired state):**

| Dimension | Current State | Desired State (Year 1) | Desired State (Year 3) | Gap Severity |
|---|---|---|---|---|
| Market position | [Current] | [Target Y1] | [Target Y3] | Low / Medium / High |
| Product/service capability | [Current] | [Target Y1] | [Target Y3] | Low / Medium / High |
| Revenue / growth | [Current] | [Target Y1] | [Target Y3] | Low / Medium / High |
| Operational maturity | [Current] | [Target Y1] | [Target Y3] | Low / Medium / High |
| Talent and culture | [Current] | [Target Y1] | [Target Y3] | Low / Medium / High |
| Technology and infrastructure | [Current] | [Target Y1] | [Target Y3] | Low / Medium / High |
| Customer experience | [Current] | [Target Y1] | [Target Y3] | Low / Medium / High |

### Step 2 — Define and Prioritize Initiatives

Identify the strategic initiatives and sequence them by value and feasibility.

**Initiative inventory:**

| ID | Initiative Name | Strategic Objective | Description | Expected Outcome | Estimated Investment | Estimated Timeline |
|---|---|---|---|---|---|---|
| SI-01 | [Name] | [Objective it serves] | [What it entails] | [Measurable outcome] | $[X] | [N] months |
| SI-02 | [Name] | [Objective] | [Description] | [Outcome] | $[X] | [N] months |
| SI-03 | [Name] | [Objective] | [Description] | [Outcome] | $[X] | [N] months |
| SI-04 | [Name] | [Objective] | [Description] | [Outcome] | $[X] | [N] months |
| SI-05 | [Name] | [Objective] | [Description] | [Outcome] | $[X] | [N] months |
| SI-06 | [Name] | [Objective] | [Description] | [Outcome] | $[X] | [N] months |

**Prioritization matrix:**

| Initiative | Strategic Impact (1-5) | Feasibility (1-5) | Time to Value | Dependencies | Resource Need | Priority Score | Sequence |
|---|---|---|---|---|---|---|---|
| SI-01 | [X] | [X] | Short / Medium / Long | [None / SI-XX] | [FTE] | [Calculated] | Phase 1 |
| SI-02 | [X] | [X] | [Timeframe] | [Dependencies] | [FTE] | [Calculated] | Phase 1 |
| SI-03 | [X] | [X] | [Timeframe] | [SI-01] | [FTE] | [Calculated] | Phase 2 |
| SI-04 | [X] | [X] | [Timeframe] | [SI-01, SI-02] | [FTE] | [Calculated] | Phase 2 |
| SI-05 | [X] | [X] | [Timeframe] | [SI-03] | [FTE] | [Calculated] | Phase 3 |
| SI-06 | [X] | [X] | [Timeframe] | [None] | [FTE] | [Calculated] | Phase 1 |

**Prioritization criteria definitions:**

| Score | Strategic Impact | Feasibility |
|---|---|---|
| 5 | Directly enables the #1 strategic priority; large measurable impact | Proven approach; resources available; low risk |
| 4 | Strongly supports a top-3 priority; significant impact | Mostly feasible; minor gaps to address |
| 3 | Supports a strategic priority; moderate impact | Feasible with moderate effort and risk |
| 2 | Loosely related to strategy; small impact | Challenging; significant gaps or unknowns |
| 1 | Tangential strategic value | High risk; major resource or capability gaps |

### Step 3 — Sequence Initiatives and Map Dependencies

Organize initiatives into phases with clear dependency relationships.

**Phased roadmap:**

| Phase | Timeline | Theme | Initiatives | Key Milestones | Cumulative Investment | Gate Criteria |
|---|---|---|---|---|---|---|
| **Phase 1: Foundation** | Months 1-6 | Build the base; quick wins | SI-01, SI-02, SI-06 | [M1, M2, M3] | $[X] | Foundation capabilities operational; quick wins delivered |
| **Phase 2: Acceleration** | Months 6-12 | Scale and expand | SI-03, SI-04 | [M4, M5, M6] | $[X] cumulative | Core strategic capabilities live; measurable outcomes |
| **Phase 3: Optimization** | Months 12-18 | Refine and sustain | SI-05 + optimization of earlier phases | [M7, M8] | $[X] cumulative | Strategic objectives on track; benefits being realized |

**Dependency map:**

| Initiative | Depends On | Type | Risk if Delayed | Mitigation |
|---|---|---|---|---|
| SI-03 | SI-01 (platform foundation) | Hard dependency — cannot start without it | Phase 2 delayed entirely | Prioritize SI-01 critical path; add resources if behind |
| SI-04 | SI-01 (data layer), SI-02 (process) | Soft dependency — can start partial work | Reduced scope at launch | Begin non-dependent workstreams in parallel |
| SI-05 | SI-03 (capabilities) | Hard dependency | Phase 3 delayed | Build interim solution if SI-03 is late |
| SI-06 | None | Independent | No downstream impact | Proceed as planned |

**Critical path identification:**

| Path | Sequence | Total Duration | Buffer | Risk Level |
|---|---|---|---|---|
| **Critical path** | SI-01 > SI-03 > SI-05 | [N] months | [N] months | High — any delay cascades |
| **Secondary path** | SI-02 > SI-04 | [N] months | [N] months | Medium |
| **Independent path** | SI-06 | [N] months | [N] months | Low |

### Step 4 — Quantify Resource Requirements

Map the people, budget, and capabilities needed per phase.

**Resource requirements by phase:**

| Resource Type | Phase 1 | Phase 2 | Phase 3 | Total | Source |
|---|---|---|---|---|---|
| Program leadership | [X] FTE | [X] FTE | [X] FTE | [X] FTE-months | Internal |
| Engineering / Technical | [X] FTE | [X] FTE | [X] FTE | [X] FTE-months | Internal + Contractor |
| Business / Operations | [X] FTE | [X] FTE | [X] FTE | [X] FTE-months | Internal |
| Change management | [X] FTE | [X] FTE | [X] FTE | [X] FTE-months | Internal |
| External consulting | [X] FTE | [X] FTE | [X] FTE | $[X] | Vendor |
| Technology / Tools | $[X] | $[X] | $[X] | $[X] | Budget |
| **Total investment** | **$[X]** | **$[X]** | **$[X]** | **$[X]** | |

**Resource gap analysis:**

| Role / Skill | Required | Available | Gap | Gap-Filling Strategy | Lead Time |
|---|---|---|---|---|---|
| [Role A] | [X] FTE | [X] FTE | [+/- X] | Hire / Contract / Reassign / Upskill | [N] weeks |
| [Role B] | [X] FTE | [X] FTE | [+/- X] | [Strategy] | [N] weeks |
| [Role C] | [X] FTE | [X] FTE | [+/- X] | [Strategy] | [N] weeks |

**Investment business case summary:**

| Metric | Value | Timeframe |
|---|---|---|
| Total investment required | $[X] | Over [N] months |
| Expected annual benefit (post-completion) | $[X] per year | Starting month [N] |
| Payback period | [N] months | From first investment |
| 3-year ROI | [X]% | |
| NPV (at [X]% discount rate) | $[X] | 3-year horizon |

### Step 5 — Build the Communication Plan

Ensure all stakeholders understand the roadmap, their role, and progress.

**Stakeholder communication matrix:**

| Audience | What They Need to Know | Channel | Frequency | Owner | Starting |
|---|---|---|---|---|---|
| Board / Executive team | Strategic progress, investment returns, major risks | Board deck / Exec dashboard | Quarterly | CEO / Strategy Lead | [Date] |
| Senior leadership | Roadmap status, resource needs, cross-initiative dependencies | Leadership meeting | Monthly | Program Director | [Date] |
| Initiative leads | Detailed progress, dependencies, blockers, resource allocation | Program standup | Bi-weekly | Program Director | [Date] |
| All employees | Vision, why we are doing this, what to expect, how to contribute | Town hall + intranet | Quarterly + as-needed | CEO + Comms | [Date] |
| Affected teams | Specific changes coming, timeline, training, and support | Team meetings + email | Monthly | Initiative Leads | [Date] |
| External stakeholders | Relevant strategic direction and impact on partnerships | Partner meetings | Quarterly | Relationship Managers | [Date] |

**Communication cadence calendar:**

| Month | Board | Leadership | Initiative Leads | All-Hands | Teams |
|---|---|---|---|---|---|
| Month 1 | Roadmap approval | Kickoff briefing | Program standup starts | Vision launch town hall | Change preview |
| Month 3 | Q1 progress review | Monthly review | Bi-weekly standups | Progress update | Training begins |
| Month 6 | Phase 1 gate review | Phase 2 planning | Dependency review | Milestone celebration | Phase 2 preview |
| Month 9 | Q3 progress review | Monthly review | Bi-weekly standups | Progress update | Adoption check |
| Month 12 | Phase 2 gate review | Phase 3 planning | Dependency review | Year in review | Phase 3 preview |
| Month 18 | Final assessment | Benefits review | Close-out | Roadmap completion town hall | Steady-state transition |

**Roadmap visualization formats:**

| Format | Audience | Content | Update Frequency |
|---|---|---|---|
| One-page strategic roadmap | Board, executives, all-hands | Phases, key milestones, strategic themes | Quarterly |
| Detailed Gantt / timeline | Initiative leads, PMO | All initiatives, dependencies, milestones | Bi-weekly |
| Dashboard / scorecard | Leadership | KPIs, progress %, health indicators | Monthly |
| Initiative-level plans | Initiative teams | Detailed workplans, resource assignments | Weekly |

---

## Output Format

```markdown
# Strategic Roadmap: [Strategy / Initiative Name]

**Vision:** [One-sentence vision statement]
**Planning Horizon:** [N] months ([Start Date] to [End Date])
**Total Investment:** $[X]
**Roadmap Owner:** [Name, Title]
**Date:** [Date]

---

## 1. Executive Summary
[Vision, strategic objectives, roadmap overview, key phases, and expected outcomes]

## 2. Strategic Context
[Vision-to-execution bridge, gap analysis, and current state assessment]

## 3. Initiative Portfolio
[All initiatives with descriptions, expected outcomes, and prioritization scores]

## 4. Phased Roadmap
[Phase definitions, timelines, initiatives per phase, milestones, and gate criteria]

## 5. Dependency Map
[Initiative dependencies, critical path, and risk mitigation for dependency delays]

## 6. Resource Plan
[People, budget, and capability requirements by phase with gap-filling strategies]

## 7. Investment Business Case
[Total cost, expected benefits, payback, ROI, and NPV]

## 8. Communication Plan
[Stakeholder matrix, communication cadence, and visualization formats]

## 9. Risks and Mitigation
[Top execution risks with likelihood, impact, and mitigation strategies]

## 10. Governance and Review Cadence
[Decision forums, review milestones, and escalation paths]
```

---

## Quality Checklist

- [ ] Every initiative traces directly to a strategic objective — no orphan projects
- [ ] Initiatives are sequenced based on value, feasibility, and dependencies — not arbitrary grouping
- [ ] Dependencies are explicitly mapped with risk assessment and mitigation for delays
- [ ] Critical path is identified and resource-protected
- [ ] Resource requirements are quantified by phase with gap-filling strategies and lead times
- [ ] Investment business case includes total cost, expected return, payback period, and NPV
- [ ] Communication plan covers all stakeholder groups with appropriate frequency and channels
- [ ] Phase gates have defined criteria for proceed/stop/adjust decisions
- [ ] Roadmap visualization exists in formats appropriate for each audience (1-page, detailed, dashboard)
- [ ] Risks to execution are identified with specific mitigation actions, not generic statements

---

## Edge Cases

| Scenario | How to Handle |
|---|---|
| Strategy is still being finalized while roadmap is needed | Build the roadmap on the most stable strategic elements; flag areas dependent on unresolved strategic decisions; plan for a roadmap refresh when strategy is finalized |
| Too many strategic initiatives for available resources | Force-rank ruthlessly using the prioritization framework; defer lower-priority initiatives explicitly; present trade-offs to leadership for decision |
| Roadmap spans organizational restructuring | Identify restructuring-dependent initiatives; build contingency paths; plan for a roadmap reset post-restructuring |
| External market disruption mid-execution (recession, competitor move, regulation) | Build scenario triggers into the roadmap; define pre-planned pivots for likely disruptions; conduct quarterly strategic context review |
| Multiple roadmaps across business units with overlapping dependencies | Create a portfolio-level master roadmap for dependencies; assign cross-BU dependency owners; establish a portfolio governance forum |
| Key initiative sponsor leaves the organization | Document initiative rationale thoroughly; assign interim sponsorship immediately; reassess initiative priority with new leadership |
| Roadmap fatigue from too many prior strategy exercises | Keep the roadmap simple and action-oriented; show quick wins from Phase 1; demonstrate accountability through visible progress tracking |
