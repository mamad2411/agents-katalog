---
name: churn-analysis
description: "Structures a systematic approach to diagnosing why users leave and designing staged interventions to retain them. Combines quantitative churn metrics with qualitative exit research to produce actionable retention playbooks."
category: customer-intelligence
default_depth: standard
---

# Churn Analysis & Retention Playbook

Read `docs/workflow-contract.md` once per session before applying this skill. Resolve it from the nearest ancestor of this file containing `manifest.json`; all Shipwright paths are relative to that root.

## Description

Structures a systematic approach to diagnosing why users leave and designing staged interventions to retain them. Combines quantitative churn metrics with qualitative exit research to produce actionable retention playbooks.

## When to Use

- Churn rate is above target or trending upward
- Building a retention strategy for the first time
- Post-mortem on a cohort with unexpectedly high churn
- Designing lifecycle email/in-app intervention campaigns
- Evaluating whether a "save" motion (discounts, calls) is effective

## Depth

| Scope | Use When | Sections to Include |
|---|---|---|
| **Light** | Quick pulse on whether churn is worsening or a single cohort needs triage | Define & Measure Churn, Diagnose Root Causes (top 3 only) |
| **Standard** | Building or revising a retention strategy with cross-functional input | All sections |
| **Deep** | Board-level retention review or churn crisis with revenue impact | All sections + cohort-level segmentation, competitive save benchmarks, LTV impact modeling |

**Omit rules:** At Light depth, skip Identify Churn Predictors, Design the Retention Playbook, and Measure the Playbook. Produce only a churn snapshot with top root causes and one recommended next step.

## Framework

### Step 1: Define & Measure Churn

```markdown
## Churn Definition

**Churn event:** [What counts as churn, e.g., "Account cancellation" or "No login in 30 days"]
**Measurement period:** [Monthly / Quarterly]
**Current rate:** [X]% [logo churn / revenue churn]

### Churn Metrics Dashboard
| Metric | Current | 3-Month Trend | Target | Notes |
|---|---|---|---|---|
| Logo churn (monthly) | [X]% | [↑/→/↓] | [target] | % of accounts lost |
| Revenue churn (monthly) | [X]% | [↑/→/↓] | [target] | % of MRR lost |
| Net revenue retention | [X]% | [↑/→/↓] | > 100% | Expansion minus contraction minus churn |
| Gross retention | [X]% | [↑/→/↓] | [target] | Retention without expansion |

### Churn Type Breakdown
| Type | % of Total Churn | Trend | Controllable? |
|---|---|---|---|
| Voluntary, dissatisfied | [X]% | [trend] | Yes, product/experience fixes |
| Voluntary, no longer need | [X]% | [trend] | Partially, positioning/expansion |
| Voluntary, switched to competitor | [X]% | [trend] | Yes, competitive response |
| Voluntary, budget/downsizing | [X]% | [trend] | No, external factor |
| Involuntary, payment failure | [X]% | [trend] | Yes, dunning optimization |
```

### Step 2: Identify Churn Predictors

```markdown
## Leading Indicators of Churn

Analyze behavioral patterns of churned vs. retained users:

| Signal | Churned Users | Retained Users | Predictive Power |
|---|---|---|---|
| Login frequency (last 30 days) | [avg] | [avg] | [High/Med/Low] |
| Core feature usage | [avg] | [avg] | [High/Med/Low] |
| Support tickets (last 90 days) | [avg] | [avg] | [High/Med/Low] |
| Time since last key action | [avg] | [avg] | [High/Med/Low] |
| Team size / collaborators | [avg] | [avg] | [High/Med/Low] |
| Onboarding completion | [%] | [%] | [High/Med/Low] |

### Risk Scoring Model
Combine leading indicators into a churn risk score:

| Risk Tier | Criteria | % of Users | Churn Probability |
|---|---|---|---|
| Critical (Red) | [3+ negative signals] | [X]% | [X]% |
| At Risk (Yellow) | [1-2 negative signals] | [X]% | [X]% |
| Healthy (Green) | [No negative signals] | [X]% | [X]% |
```

### Step 3: Diagnose Root Causes

```markdown
## Root Cause Analysis

### Data Sources for Diagnosis
- [ ] Exit surveys (at cancellation)
- [ ] Win/loss interviews (churned customers)
- [ ] Support ticket analysis (pre-churn patterns)
- [ ] NPS detractor comments
- [ ] Product usage analytics (feature adoption gaps)
- [ ] Competitor analysis (what they're switching to)

### Root Cause Categories
| Category | % of Churn | Key Findings | Evidence |
|---|---|---|---|
| **Product-market fit** | [X]% | [Product doesn't solve their core problem] | [exit survey data] |
| **Usability / complexity** | [X]% | [Too hard to use, not enough training] | [support tickets, TTFV] |
| **Missing features** | [X]% | [Specific capabilities needed] | [feature requests, competitor comparison] |
| **Reliability / bugs** | [X]% | [Trust eroded by outages or data issues] | [incident history, NPS] |
| **Poor onboarding** | [X]% | [Never reached first value] | [activation rates, TTFV] |
| **Value not realized** | [X]% | [Using product but not getting outcomes] | [usage vs. outcomes analysis] |
| **Competitive loss** | [X]% | [Competitor offers better X] | [exit interviews] |
| **Price / budget** | [X]% | [Can't justify the cost] | [exit survey, segment analysis] |
| **Champion left** | [X]% | [Key user departed the organization] | [usage data, CS notes] |
| **Involuntary** | [X]% | [Payment failures not recovered] | [billing data] |
```

### Step 4: Design the Retention Playbook

```markdown
## Retention Playbook

### Prevention Layer (before risk signals appear)
| Intervention | Trigger | Channel | Content | Owner |
|---|---|---|---|---|
| Onboarding optimization | Signup | In-app | Guided setup to first value in < [N] minutes | Product |
| Activation campaign | Day 1-7 | Email + In-app | [N]-step drip teaching core features | Growth |
| Habit formation hooks | Weekly | In-app + Email | Usage summaries, suggested next actions | Product |
| Value reinforcement | Monthly | Email | "Here's what you accomplished this month" | Marketing |

### Intervention Layer (when risk signals appear)
| Risk Signal | Intervention | Channel | Timing | Content |
|---|---|---|---|---|
| Login drop (7+ days) | Re-engagement nudge | Email | Day 8 | "Here's what you missed + quick win" |
| Feature adoption gap | In-app guidance | In-app | On next login | Contextual tooltip for unused key feature |
| Support ticket spike | Proactive CS outreach | Call/Email | Within 24 hours | "I noticed X, can I help?" |
| NPS detractor (0-6) | CS follow-up | Call | Within 48 hours | Understand issue, offer solution |
| Usage decline (30-day) | Win-back campaign | Email | Day 30, 45, 60 | Escalating value reminders |

### Save Layer (at cancellation intent)
| Trigger | Intervention | Content | Effectiveness Target |
|---|---|---|---|
| Clicks "Cancel" | Cancellation flow | Exit survey + save offer | Deflect [X]% |
| Selects "too expensive" | Discount offer | [X]% off for [N] months | Convert [X]% |
| Selects "missing feature" | Feature update promise | "This is on our roadmap for [quarter]" | Convert [X]% |
| Selects "switching to X" | Competitive save | Comparison + migration help | Convert [X]% |
| Completes cancellation | Win-back sequence | Email at 30/60/90 days | Recover [X]% |

### Recovery Layer (after churn)
| Timing | Channel | Content | Goal |
|---|---|---|---|
| Day 30 post-churn | Email | "Here's what's new since you left" | [X]% re-activation |
| Day 60 post-churn | Email | Specific feature announcement relevant to exit reason | [X]% re-activation |
| Day 90 post-churn | Email | Special offer | Final attempt |
```

### Step 5: Measure the Playbook

```markdown
## Retention Metrics

| Metric | Baseline | Target | Review Cadence |
|---|---|---|---|
| Overall churn rate | [X]% | [target] | Monthly |
| Churn by root cause (each) | [X]% | [target] | Monthly |
| Save rate (cancellation deflection) | [X]% | [target] | Weekly |
| Re-engagement email conversion | [X]% | [target] | Weekly |
| Time to intervention (risk → action) | [X] days | < [N] days | Weekly |
| Win-back rate (post-churn recovery) | [X]% | [target] | Monthly |
| Net revenue retention | [X]% | > 100% | Monthly |
```

## Minimum Evidence Bar

**Required inputs:** Churn rate data (logo or revenue) for at least one measurement period, and at least one qualitative source (exit surveys, support tickets, or churned-customer interviews). At Light depth, churn rate data alone is sufficient; qualitative sources are recommended but not required for a quick pulse.

**Acceptable evidence:** Billing/subscription data, product usage analytics, exit survey responses, NPS detractor comments, win/loss interview transcripts, support ticket logs.

**Insufficient evidence:** If you have churn rate numbers but zero qualitative data on why users left, state "Insufficient evidence for Root Cause Analysis" and produce a partial artifact with the churn metrics snapshot completed and root cause and intervention sections marked `[TBD, requires: exit surveys, churned-customer interviews, or support ticket analysis]`. Flag the artifact as draft-only.

**Hypotheses vs. findings:**
- **Findings:** Churn rates, churn type breakdown, and leading indicator correlations must be grounded in data.
- **Hypotheses:** Root cause attributions and predicted intervention effectiveness may be directional, label them "Hypothesis, pending validation" when sourced from fewer than 5 data points.

## Output Format

Produce a Churn Analysis & Retention Playbook with:
1. **Churn Metrics**, current rates, types, trends
2. **Leading Indicators**, behavioral predictors and risk scoring
3. **Root Cause Analysis**, categorized diagnosis with evidence
4. **Retention Options**, framed intervention options across stages (prevention, intervention, save, recovery) with expected impact and trade-offs; does not prescribe which to implement
5. **Measurement Plan**, metrics and review cadence

**Shipwright Signature (required closing):**
6. **Decision Frame**, primary finding on churn drivers and framed retention options with expected churn impact, trade-offs (cost of intervention vs. cost of churn), confidence level with evidence quality, owner, decision date, revisit trigger
7. **Unknowns & Evidence Gaps**, root causes with insufficient qualitative backing, segments with no exit data, untested intervention assumptions
8. **Pass/Fail Readiness**, PASS if churn is consistently defined and quantified, causal claims match available evidence, and uncertainty is explicit. A Light pulse may report causes unknown. Standard/Deep frame supported retention options; FAIL if correlation or an unsupported explanation is asserted as a root cause.
9. **Recommended Next Artifact**, Which Shipwright skill to run next and why

## Common Mistakes to Avoid

- **Treating all churn the same**, Voluntary vs. involuntary, satisfied vs. dissatisfied need different responses
- **Only measuring logo churn**, Revenue churn matters more; losing one enterprise deal > losing 20 free accounts
- **Intervention without diagnosis**, Offering discounts when the problem is usability wastes money and annoys users
- **No prevention layer**, The best retention strategy is getting users to value fast, not saving them at cancellation
- **Ignoring involuntary churn**, Payment failures are often 20-40% of total churn and are highly fixable with dunning optimization

## Weak vs. Strong Output

**Weak:**
> "Root cause: Users are unhappy with the product and leaving."

Restates the churn problem instead of diagnosing it. No segmentation, no evidence, no actionable category.

**Strong:**
> "Root cause: 38% of Q3 churn cited 'missing integrations' in exit surveys (n=42), concentrated in Mid-Market segment. Top 3 requested integrations: Salesforce, HubSpot, Slack. Controllable, product investment required."

Specific category, quantified, sourced from named evidence, tied to a segment, and tagged as controllable.
