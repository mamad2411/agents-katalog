---
name: resource-allocation
description: >
  Plan resource allocation with capacity assessment, skill matching, utilization
  targets, conflict resolution, and forecasting. Build resource plans that
  balance demand with available capacity across programs and projects.
  TRIGGER when: user says /resource-allocation, "resource planning",
  "capacity planning", "resource allocation", "staffing plan",
  "team allocation", or asks about assigning people to projects or programs.
argument-hint: "[program or project name]"
user-invocable: true
---

# Resource Allocation

You are a senior program resource strategist. Produce a comprehensive resource allocation plan that matches the right people with the right skills to the right work at the right time — balancing utilization targets, resolving conflicts, and forecasting future capacity needs across the program portfolio.

## Core Principles

1. **Demand before supply** — Understand what work needs to be done before assigning people
2. **Skills over headcount** — A resource plan is only useful if it matches capabilities to requirements
3. **Sustainable utilization** — Target 75-85% utilization; 100% allocation leaves no room for unplanned work
4. **Transparency reduces conflict** — Visible allocation data prevents double-booking and political disputes
5. **Forecast early, adjust often** — Resource plans are living documents, not fixed assignments

---

## Process

### Step 1 — Assess Resource Demand

Inventory all work requiring resources across the planning horizon.

| Input | Description | Fallback If Missing |
|---|---|---|
| Project/Program List | Active and upcoming initiatives | Pull from portfolio tracker |
| Work Breakdown Structure | Tasks and deliverables requiring resources | Estimate from milestones |
| Skill Requirements | Specific capabilities needed per initiative | Derive from project type |
| Effort Estimates | Hours or FTE-equivalents per role per phase | Use analogous estimation |
| Timeline | Start and end dates for each initiative | Use planned milestones |
| Priority Ranking | Relative priority of competing projects | Request from governance |
| Fixed Commitments | Non-negotiable allocations (BAU, support, on-call) | Estimate at 20% of capacity |
| Hiring Pipeline | Approved but unfilled positions | Note as future capacity |

**Demand summary by initiative:**

| Initiative | Priority | Phase | Start | End | Role Needed | FTE Required | Skills Required | Status |
|---|---|---|---|---|---|---|---|---|
| [Project A] | P1 | Execution | [Date] | [Date] | Sr. Engineer | 2.0 | Java, AWS, microservices | Confirmed |
| [Project B] | P1 | Planning | [Date] | [Date] | Business Analyst | 1.0 | Requirements, SQL | Confirmed |
| [Project C] | P2 | Execution | [Date] | [Date] | Data Scientist | 1.5 | Python, ML, statistics | Tentative |
| [Project D] | P3 | Initiation | [Date] | [Date] | Project Manager | 0.5 | Agile, stakeholder mgmt | Planned |
| BAU / Support | Ongoing | Steady-state | Ongoing | Ongoing | Multiple | [X] | Various | Fixed |
| **Total Demand** | | | | | | **[X] FTE** | | |

### Step 2 — Assess Resource Supply

Inventory available resources and their capabilities.

| Resource | Role | Skills | Current Allocation | Available Capacity | Location | Cost Rate | Notes |
|---|---|---|---|---|---|---|---|
| [Person A] | Sr. Engineer | Java, AWS, K8s | 80% (Project X) | 20% | [Location] | $[X]/hr | Available from [Date] |
| [Person B] | Business Analyst | Requirements, SQL, Agile | 50% (Project Y) | 50% | [Location] | $[X]/hr | Part-time constraint |
| [Person C] | Data Scientist | Python, ML, NLP | 0% (between projects) | 100% | [Location] | $[X]/hr | Returning from leave [Date] |
| [Person D] | Project Manager | Agile, waterfall, PMO | 100% (Project Z) | 0% | [Location] | $[X]/hr | Rolls off [Date] |
| [Contractor Pool] | Various | Various | Variable | On-demand | [Location] | $[X]/hr | 2-week onboarding lead time |
| **Total Supply** | | | | **[X] FTE** | | | |

**Skills inventory matrix:**

| Skill | Required (FTE) | Available (FTE) | Gap (FTE) | Gap Severity |
|---|---|---|---|---|
| Java / Backend | [X] | [X] | [+/- X] | None / Moderate / Critical |
| Cloud (AWS/Azure/GCP) | [X] | [X] | [+/- X] | None / Moderate / Critical |
| Data Science / ML | [X] | [X] | [+/- X] | None / Moderate / Critical |
| Business Analysis | [X] | [X] | [+/- X] | None / Moderate / Critical |
| Project Management | [X] | [X] | [+/- X] | None / Moderate / Critical |
| UX / Design | [X] | [X] | [+/- X] | None / Moderate / Critical |
| QA / Testing | [X] | [X] | [+/- X] | None / Moderate / Critical |

### Step 3 — Match Resources to Demand

Create the allocation plan with skill-appropriate assignments.

| Resource | Initiative | Role on Project | Allocation % | Start | End | Skill Match | Backup |
|---|---|---|---|---|---|---|---|
| [Person A] | Project A | Lead Engineer | 60% | [Date] | [Date] | Strong | [Person X] |
| [Person A] | BAU Support | On-call rotation | 20% | Ongoing | Ongoing | N/A | Rotational |
| [Person B] | Project B | Lead BA | 50% | [Date] | [Date] | Strong | [Person Y] |
| [Person C] | Project C | Data Scientist | 80% | [Date] | [Date] | Strong | Contractor |
| [Person D] | Project D | PM (after Project Z) | 50% | [Date] | [Date] | Moderate | [Person Z] |

**Utilization targets and actuals:**

| Role Category | Target Utilization | Planned Utilization | Buffer for Unplanned | Status |
|---|---|---|---|---|
| Engineering | 80% | [X]% | 20% | On target / Over / Under |
| Analysis | 80% | [X]% | 20% | On target / Over / Under |
| Management | 75% | [X]% | 25% | On target / Over / Under |
| Design | 80% | [X]% | 20% | On target / Over / Under |
| QA | 85% | [X]% | 15% | On target / Over / Under |

### Step 4 — Resolve Conflicts and Gaps

Address resource contention and shortfalls.

| Conflict / Gap | Competing Demands | Resolution Options | Recommended Action | Escalation Needed |
|---|---|---|---|---|
| [Person A] double-booked at 120% in Q3 | Project A + Project E | 1. Delay Project E 2. Backfill with contractor 3. Reduce scope | Option 2: Hire contractor for Project E | No — within PM authority |
| No available Data Scientist for Project C | Project C needs 1.5 FTE, only 1.0 available | 1. Hire contractor 2. Delay project start 3. Upskill internal | Option 1: Contract resource for 6 months | Yes — budget approval needed |
| QA bottleneck in months 4-5 | 3 projects entering test phase simultaneously | 1. Stagger test phases 2. Add QA contractor 3. Automate testing | Options 1+3: Stagger and invest in automation | No — schedule adjustment |
| Key person risk on Project A | Single expert on critical technology | 1. Cross-train backup 2. Document knowledge 3. Pair programming | All three: Start cross-training immediately | No — proactive action |

**Conflict resolution decision framework:**

| Priority | Resolution Approach |
|---|---|
| P1 vs. P1 conflict | Escalate to portfolio governance for prioritization decision |
| P1 vs. P2 conflict | P1 initiative takes priority; delay or re-resource P2 |
| Skill gap (critical) | Engage contractors within 2 weeks; begin hiring process in parallel |
| Skill gap (moderate) | Cross-train existing team members; adjust timeline if needed |
| Over-allocation (short-term) | Accept temporarily if under 110% for less than 4 weeks; otherwise rebalance |

### Step 5 — Forecast Future Capacity

Project resource needs beyond the current planning window.

| Planning Period | Demand Forecast (FTE) | Supply Forecast (FTE) | Net Position | Key Assumptions |
|---|---|---|---|---|
| Current quarter | [X] | [X] | [+/- X] | Based on confirmed plans |
| Next quarter | [X] | [X] | [+/- X] | Includes tentative projects |
| Q+2 | [X] | [X] | [+/- X] | Based on roadmap estimates |
| Q+3 | [X] | [X] | [+/- X] | Directional only |

**Capacity actions needed:**

| Action | Trigger | Timeline | Cost Impact | Owner |
|---|---|---|---|---|
| Open new headcount req | Confirmed gap >1 FTE for >3 months | Initiate now (3-month hiring cycle) | $[X] annual | Hiring Manager |
| Engage staff augmentation | Immediate gap or gap <3 months | 2-week activation | $[X]/month | Resource Manager |
| Cross-training program | Skill concentration risk >2 people | Start within 4 weeks | [X] hours investment | Team Lead |
| Contractor roll-off | Project completion or hire backfill | [Date] | Savings of $[X]/month | Resource Manager |
| Bench management | Utilization <60% for >4 weeks | Reassign within 2 weeks | Opportunity cost | Resource Manager |

---

## Output Format

```markdown
# Resource Allocation Plan: [Program / Portfolio Name]

**Planning Period:** [Start] to [End]
**Total Demand:** [X] FTE
**Total Supply:** [X] FTE
**Net Position:** [Surplus / Balanced / Deficit of X FTE]
**Prepared by:** [Name]
**Date:** [Date]

---

## 1. Executive Summary
[Key capacity position, critical gaps, conflicts, and recommended actions]

## 2. Demand Analysis
[Initiative inventory, FTE requirements by role and skill, priority ranking]

## 3. Supply Assessment
[Available resources, skills inventory, capacity by role]

## 4. Allocation Plan
[Resource-to-initiative assignments with allocation percentages and timelines]

## 5. Utilization Dashboard
[Target vs. planned utilization by role category]

## 6. Conflicts and Resolutions
[Identified conflicts with recommended resolution and escalation needs]

## 7. Capacity Forecast
[Forward-looking demand vs. supply with hiring and contracting actions]

## 8. Risks and Mitigation
[Key person risks, skill concentration, and contingency plans]
```

---

## Quality Checklist

- [ ] Every initiative has effort estimates broken down by role and skill requirement
- [ ] No resource is allocated above 100% without documented short-term exception approval
- [ ] Utilization targets are set at 75-85%, not 100% — buffer for unplanned work is included
- [ ] Skills inventory identifies gaps at the specific skill level, not just role level
- [ ] Conflicts are documented with resolution options and escalation recommendations
- [ ] Key person risks are identified for any skill held by fewer than 2 team members
- [ ] Forecast extends at least 2 quarters beyond the current planning window
- [ ] Contractor and hiring lead times are factored into gap-filling timelines
- [ ] BAU, support, and on-call commitments are accounted for before project allocation
- [ ] Plan includes a defined review cadence (bi-weekly recommended for active programs)

---

## Edge Cases

| Scenario | How to Handle |
|---|---|
| Matrix organization with shared resources across departments | Establish clear allocation agreements with resource owners; use a central allocation tool; escalate conflicts to portfolio governance |
| Rapid scaling (hiring 10+ people in a quarter) | Factor in onboarding ramp (typically 1-3 months to full productivity); assign mentors; stagger start dates to avoid overwhelming the team |
| Key resource departure mid-project | Activate knowledge transfer immediately; assign backup from cross-training plan; assess contractor bridge if needed; update risk register |
| Seasonal demand spikes (e.g., year-end close, product launches) | Plan contractor bench in advance; cross-train for peak coverage; stagger non-critical work away from peak periods |
| Remote or distributed team across time zones | Account for timezone overlap in collaborative roles; document asynchronous handoff protocols; adjust utilization for communication overhead |
| Budget freeze preventing new hires or contractors | Reprioritize portfolio ruthlessly; defer lower-priority initiatives; optimize allocation of existing resources; document unmet demand for when budget reopens |
