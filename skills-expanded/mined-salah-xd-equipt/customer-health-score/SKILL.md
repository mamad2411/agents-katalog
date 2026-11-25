---
name: customer-health-score
description: "Designs customer health scoring models with engagement metrics, risk indicators, and intervention triggers to prevent churn proactively."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Customer Health Score

## When to Use This Skill

Use this skill when you need to:
- Build a scoring model that identifies at-risk customers before they churn
- Define engagement metrics and risk indicators for customer accounts
- Create intervention triggers and playbooks for different health levels
- Prioritize customer success efforts based on objective health data

**DO NOT** use this skill for NPS surveys, customer segmentation by value, or sales pipeline scoring. This is for ongoing customer health monitoring.

---

## Core Principle

CUSTOMER HEALTH IS A LEADING INDICATOR — BY THE TIME A CUSTOMER TELLS YOU THEY ARE LEAVING, THE DECISION WAS MADE WEEKS AGO. A HEALTH SCORE GIVES YOU THOSE WEEKS BACK.

---

## Phase 1: Define Health Signals

Identify what healthy and unhealthy customers look like.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business model** | "Subscription, project-based, retainer, or product?" | Subscription |
| **Healthy customer profile** | "Describe your most engaged, happiest customer. What do they do?" | No default |
| **Churn signals** | "Think of customers who left. What did they do (or stop doing) before leaving?" | No default |
| **Data available** | "What customer data do you track? (login frequency, usage, support tickets, payment history)" | Basic — email engagement, payment |
| **Customer count** | "How many active customers do you have?" | Under 50 |

**GATE: Confirm health signals before building the scoring model.**

---

## Phase 2: Build Scoring Model

Create a weighted health score from 0-100.

### Health Score Components

```
## Customer Health Score Model

**Score range:** 0-100
**Healthy:** 70-100
**At risk:** 40-69
**Critical:** 0-39

### Scoring Components

| Component | Weight | Metric | Scoring |
|-----------|--------|--------|---------|
| Engagement | 30% | [Usage frequency, login rate, feature adoption] | 0-30 points |
| Relationship | 25% | [Communication responsiveness, meeting attendance, feedback participation] | 0-25 points |
| Financial | 25% | [Payment timeliness, expansion revenue, contract length] | 0-25 points |
| Satisfaction | 20% | [NPS, CSAT, support ticket sentiment] | 0-20 points |
```

### Component Scoring Detail

For each component, define the scoring tiers:

```
### Engagement Score (0-30 points)

| Behavior | Points | Rationale |
|----------|--------|-----------|
| Active weekly (uses product/service regularly) | 30 | Fully engaged |
| Active biweekly | 20 | Moderately engaged |
| Active monthly | 10 | Low engagement — intervention needed |
| Inactive 30+ days | 0 | Critical — immediate outreach |

### Relationship Score (0-25 points)

| Behavior | Points |
|----------|--------|
| Responds to outreach within 48 hours | 10 |
| Attends scheduled meetings/calls | 10 |
| Provides feedback when asked | 5 |

### Financial Score (0-25 points)

| Behavior | Points |
|----------|--------|
| Pays on time consistently | 15 |
| Has expanded (upsold, renewed, added services) | 10 |
| Late payments or disputes | -10 |

### Satisfaction Score (0-20 points)

| Signal | Points |
|--------|--------|
| NPS 9-10 (Promoter) | 20 |
| NPS 7-8 (Passive) | 10 |
| NPS 0-6 (Detractor) | 0 |
| Support complaints increasing | -5 |
```

**GATE: Present scoring model for validation.**

---

## Phase 3: Intervention Playbooks

Define actions for each health zone.

### Intervention Matrix

```
## Health Zone Actions

### Healthy (70-100) — Nurture and Expand
**Check-in frequency:** Monthly
**Actions:**
- Send value-add content and tips
- Identify upsell or referral opportunities
- Request testimonials or case studies
- Invite to advisory board or beta programs

### At Risk (40-69) — Engage and Recover
**Check-in frequency:** Biweekly
**Actions:**
- Personal outreach from account owner (not automated)
- Identify specific decline — which component dropped?
- Offer training, support, or strategy session
- Address any unresolved issues immediately

### Critical (0-39) — Save or Prepare
**Check-in frequency:** Weekly
**Actions:**
- Escalate to business owner
- Direct phone call or video meeting (not email)
- Ask explicitly: "What would need to change for this to work?"
- Offer concession if appropriate (discount, extended trial, service credit)
- If unrecoverable, conduct exit interview for learning
```

### Alert System

```
## Health Score Alerts

| Trigger | Alert | Action |
|---------|-------|--------|
| Score drops below 70 | Email to account owner | Schedule check-in within 5 days |
| Score drops below 40 | Email to business owner | Call customer within 48 hours |
| Score drops 20+ points in one period | Urgent flag | Same-day outreach |
| Score increases above 80 | Opportunity flag | Send referral or upsell prompt |
```

---

## Phase 4: Operationalize

Make health scoring part of the regular business rhythm.

### Scoring Cadence

- **Monthly:** Update all customer health scores
- **Weekly:** Review any customers flagged as Critical
- **Quarterly:** Analyze trends — is overall health improving or declining?

### Health Dashboard

```
## Customer Health Overview — [Month]

| Health Zone | Count | % of Total | Revenue at Risk |
|-------------|-------|-----------|----------------|
| Healthy (70-100) | [#] | [%] | — |
| At Risk (40-69) | [#] | [%] | $[X] |
| Critical (0-39) | [#] | [%] | $[X] |

**Average health score:** [X]
**Trend:** Improving / Stable / Declining
```

### Quarterly Calibration

Review and adjust the model quarterly:
1. Did health scores predict actual churn?
2. Are the component weights right?
3. Are any metrics too hard to collect consistently?
4. Do the intervention playbooks work?

---

## Anti-Patterns

- **Score without action** — a health score is useless if no one acts on it. Every zone needs a defined playbook.
- **Over-complicated model** — start with 3-4 components. Adding 10 metrics makes the score hard to maintain and interpret.
- **Scoring only on gut feel** — the score must be based on observable, measurable behaviors, not "I think they are happy."
- **Ignoring healthy customers** — high health scores need attention too. Neglected promoters become passives.
- **Static model** — customer behavior patterns change. Recalibrate the model quarterly.

---

## Recovery

- **User does not track enough data:** Start with what is available — even payment history and email response rate create a useful 2-component score.
- **Too few customers to score:** Under 10 customers, skip the score and maintain a simple traffic-light status (green/yellow/red) with monthly check-ins.
- **Health score does not predict churn:** The wrong metrics are being weighted. Analyze actual churned customers and reverse-engineer which signals mattered.
- **User cannot act on scores (no time):** Automate healthy-zone nurturing (drip emails, tips). Spend manual time only on at-risk and critical accounts.
- **All customers show as healthy but churn happens:** The scoring thresholds are too generous. Lower the "healthy" threshold and add more sensitive indicators.
