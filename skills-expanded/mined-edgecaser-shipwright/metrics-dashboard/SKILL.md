---
name: metrics-dashboard
description: "Defines a product metrics architecture: North Star metric, input metrics, guardrail metrics, and counter-metrics. Produces a dashboard specification that connects daily tactical metrics to strategic outcomes. Based on the Amplitude/Sean Ellis North Star framework and Reforge metrics methodology."
category: measurement
default_depth: standard
---

# Metrics Dashboard Design

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Defines a product metrics architecture: North Star metric, input metrics, guardrail metrics, and counter-metrics. Produces a dashboard specification that connects daily tactical metrics to strategic outcomes. Based on the Amplitude/Sean Ellis North Star framework and Reforge metrics methodology.

## When to Use

- Setting up metrics for a new product or feature
- Redesigning a metrics framework that's become noisy or misaligned
- Aligning teams on what "success" means quantitatively
- Preparing for a data-informed planning cycle

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick alignment on what to measure for a new feature | North Star Metric, Input Metrics |
| **Standard** | Setting up metrics for a product area or redesigning a stale framework | All sections |
| **Deep** | Org-wide metrics overhaul or board-level reporting setup | All sections + metric dependency map, instrumentation plan with engineering owners, data quality audit |

**Omit rules:** At Light depth, skip Guardrail Metrics, Counter-Metrics, and Dashboard Specification. Produce only the North Star definition and input metric decomposition.

## Framework

### Step 1: Define the North Star Metric

The single metric that best captures the value your product delivers to customers.

**Criteria for a good North Star:**
- Reflects customer value delivered (not just business revenue)
- Is a leading indicator of sustainable business success
- Is actionable by the product team
- Is measurable with current instrumentation

```markdown
## North Star Metric

**Metric:** [Name, e.g., "Weekly active projects with 3+ collaborators"]
**Definition:** [Precise technical definition, what counts, what doesn't]
**Current value:** [baseline]
**Target:** [goal by date]
**Why this metric:** [How it captures customer value delivery]

**Validation checklist:**
- [ ] If this metric goes up, the business gets healthier
- [ ] If the business gets healthier, this metric goes up
- [ ] The product team can directly influence this metric
- [ ] We can measure it reliably today
```

### Step 2: Map Input Metrics

Input metrics are the levers that drive the North Star. They decompose the North Star into actionable components.

```markdown
## Input Metrics (levers that drive the North Star)

### North Star = [formula showing how inputs compose]
Example: Weekly Active Projects = New Projects Created × Activation Rate × Retention Rate

| Input Metric | Definition | Current | Target | Owner |
|---|---|---|---|---|
| New projects created/week | Projects created by new + existing users | [N] | [target] | Growth |
| Activation rate | % of new projects that reach [milestone] in 7 days | [%] | [target] | Onboarding |
| Weekly retention | % of active projects still active the following week | [%] | [target] | Core product |
| Collaborators per project | Avg users per active project | [N] | [target] | Collaboration |
```

### Step 3: Define Guardrail Metrics

Guardrails ensure you're not gaming the North Star at the expense of something important.

```markdown
## Guardrail Metrics (must NOT degrade)

| Guardrail | Definition | Threshold | Why It Matters |
|---|---|---|---|
| Page load time (p95) | 95th percentile load time | < 3 seconds | Growth can't come at the cost of performance |
| Error rate | % of API requests returning errors | < 0.5% | Reliability is table stakes |
| Support ticket volume | Tickets per 1,000 active users | < [N] | Feature quality shouldn't burden support |
| NPS | Net Promoter Score (quarterly) | > [N] | Quantitative growth without qualitative satisfaction is unsustainable |
```

### Step 4: Add Counter-Metrics

Counter-metrics detect when an optimization in one area causes harm in another.

```markdown
## Counter-Metrics (watch for negative side effects)

| Optimization | Counter-Metric | Watch For |
|---|---|---|
| Increasing activation | Time-to-churn | Are we activating low-quality users who churn fast? |
| Growing seat count | Usage per seat | Are new seats actually using the product? |
| Reducing onboarding steps | Support tickets from new users | Did we cut too much and confuse people? |
```

### Step 5: Dashboard Specification

```markdown
## Dashboard Layout

### Executive View (weekly review)
- North Star metric: [trend line, WoW change]
- Input metrics: [sparklines with targets]
- Guardrails: [status indicators, green/yellow/red]

### Team View (daily)
- Input metrics with daily granularity
- Segmented by: [cohort, platform, plan type]
- Anomaly alerts: [when metric moves >2 standard deviations]

### Experiment View (per experiment)
- Treatment vs. control for target metric
- Statistical significance indicator
- Impact on guardrail metrics

## Data Sources
| Metric | Source System | Update Frequency | Known Limitations |
|---|---|---|---|
| [Metric] | [Analytics tool] | [Real-time / Daily / Weekly] | [Data delay, sampling, etc.] |

## Alert Rules
| Condition | Severity | Notify | Action |
|---|---|---|---|
| North Star drops >10% WoW | Critical | [Slack channel + PagerDuty] | Investigate within 2 hours |
| Guardrail crosses threshold | Warning | [Slack channel] | Review within 24 hours |
| Input metric misses target 3 weeks running | Info | [Weekly review agenda] | Discuss in planning |
```

## Minimum Evidence Bar

**Required inputs:** Product or feature description, target user segment, at least one known business objective, current instrumentation capabilities.

**Acceptable evidence:** Existing analytics data, user research findings, business KPIs, product usage logs, stakeholder interviews about what "success" means.

**Insufficient evidence:** If user value is unclear, return candidate definitions and targeted research questions. If instrumentation or baselines are missing, produce a measurement design with implementation gaps; a discovery framework cannot itself instrument the product. Do not label the dashboard operational until data availability is verified.

**Hypotheses vs. findings:**
- **Findings:** Current metric baselines, existing instrumentation gaps, known data source limitations, must be grounded in evidence.
- **Hypotheses:** Proposed North Star rationale, input metric decomposition, predicted counter-metric risks, must be labeled as assumptions to validate.

## Output Format

Produce a Metrics Architecture Document with:
1. **North Star Metric**, definition, rationale, target
2. **Input Metrics**, decomposition of the North Star into actionable levers
3. **Guardrail Metrics**, what must not degrade
4. **Counter-Metrics**, side effect detection
5. **Dashboard Specification**, layout, data sources, alert rules

**Shipwright Signature (required closing):**
6. **Decision Frame**, recommended North Star with rationale, trade-off vs. alternative candidates, confidence with evidence quality (data availability, instrumentation readiness), owner, decision date, revisit trigger
7. **Unknowns & Evidence Gaps**, metrics that cannot be instrumented yet, unvalidated causal assumptions in the input metric decomposition
8. **Pass/Fail Readiness**, PASS for a measurement design if user value, metric definitions and input decomposition are justified and missing instrumentation is explicit. Operational readiness additionally requires verified collection and baselines. FAIL if the North Star is a vanity metric or unavailable data is represented as measured.
9. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Revenue as North Star**, Revenue is a lagging business metric, not a product health indicator
- **Too many metrics**, 1 North Star, 3-5 inputs, 3-4 guardrails. More than that and nothing gets attention.
- **No guardrails**, Without guardrails, teams optimize the North Star by degrading everything else
- **Vanity metrics**, Page views, total registered users, and "downloads" feel good but don't drive decisions
- **Unmeasurable metrics**, If you can't instrument it today, it can't be a North Star today

## Weak vs. Strong Output

**Weak:**
> "North Star Metric: Monthly Active Users."

No definition of "active," no validation against the four criteria, no connection to customer value, MAU is a vanity metric in disguise.

**Strong:**
> "North Star Metric: Weekly teams completing at least one shared workflow. Definition: distinct team accounts where 2+ members execute a collaborative workflow within a 7-day window. Current: 1,240. Target: 2,000 by Q3. Why: captures both activation and collaboration value, validated against all four criteria."

Precise definition, measurable baseline, target with timeline, and explicit rationale tying the metric to customer value.
