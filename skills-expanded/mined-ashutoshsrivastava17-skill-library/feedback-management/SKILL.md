---
name: feedback-management
description: >
  Design feedback programs — collection methods, survey design, response workflows,
  closed-loop processes, and reporting cadence.
  TRIGGER when: user says /feedback-management, "design a feedback program", "survey strategy",
  "customer feedback plan", "closed-loop feedback", "feedback collection", or "how should we collect feedback".
argument-hint: "[feedback type, channel, customer segment, or program goal]"
user-invocable: true
---

# Feedback Management Program Design

You are a customer feedback program architect. Design comprehensive feedback
collection and management programs that capture the right signals, at the right
time, through the right channels — and close the loop with customers and
internal stakeholders.

## Process

### Step 1: Define Program Objectives

| Parameter | Description |
|-----------|-------------|
| **Program goal** | Measure satisfaction, identify improvement areas, validate features, reduce churn, track loyalty |
| **Feedback type** | Relationship (periodic health), transactional (event-triggered), strategic (deep discovery) |
| **Customer segments** | Which segments to survey — all, by tier, by lifecycle stage |
| **Existing programs** | Current surveys, collection methods, and their gaps |
| **Decision consumers** | Who will use this data — product, CX, support, executive team |
| **Success metrics** | Response rate, action rate, score improvement, closed-loop rate |

### Step 2: Design Collection Strategy

#### Channel and Method Selection

| Method | Best For | Timing | Expected Response Rate | Effort |
|--------|---------|--------|:---------------------:|--------|
| **In-app survey** | Transactional feedback, feature reactions | Immediately after event | 15-25% | Low |
| **Email survey** | Relationship NPS, detailed feedback | Quarterly or after milestones | 10-20% | Low |
| **SMS survey** | Quick pulse, high-urgency feedback | Post-interaction (within 1 hr) | 20-30% | Low |
| **Post-call IVR** | Support satisfaction | Immediately after call | 5-15% | Medium |
| **In-person / video** | Deep qualitative insights | Scheduled interview | 60-80% (when scheduled) | High |
| **App store prompt** | Public review generation | After positive experience detected | 5-10% | Low |
| **Community forum** | Feature ideas, peer discussion | Ongoing | N/A (passive) | Medium |
| **Customer advisory board** | Strategic direction feedback | Quarterly meetings | 90%+ | High |

#### Survey Design Principles

| Principle | Guideline |
|-----------|-----------|
| **Length** | Max 3 minutes for transactional, max 8 minutes for relationship |
| **Question count** | 1-3 for transactional, 5-10 for relationship, 15-25 for deep research |
| **Scale consistency** | Use the same scale throughout (e.g., 0-10 for NPS, 1-5 for CSAT) |
| **Open-ended questions** | Include at least 1 — "Why did you give this score?" or "What could we improve?" |
| **Skip logic** | Branch based on score to ask relevant follow-ups |
| **Mobile-first** | Design for phone screens; avoid matrices and complex grids |
| **Bias prevention** | Randomize option order, avoid leading questions, neutral framing |

### Step 3: Define Survey Instruments

#### Relationship Survey Template

| # | Question | Type | Logic |
|---|---------|------|-------|
| 1 | On a scale of 0-10, how likely are you to recommend [Product] to a colleague? | NPS (0-10) | Always show |
| 2 | Why did you give that score? | Open text | Always show |
| 3 | How satisfied are you with the following areas? | Matrix (1-5) | Always show |
| | - Product quality | | |
| | - Ease of use | | |
| | - Customer support | | |
| | - Value for price | | |
| 4 | What is the one thing we could do to improve your experience? | Open text | Always show |
| 5 | How likely are you to renew your subscription? | Scale (1-5) | Show if tenure > 6 months |

#### Transactional Survey Template

| # | Question | Type | Logic |
|---|---------|------|-------|
| 1 | How satisfied are you with your recent [interaction type]? | CSAT (1-5) | Always show |
| 2 | How easy was it to [complete the task]? | CES (1-7) | Always show |
| 3 | What could we have done better? | Open text | Show if score <= 3 |
| 4 | What did we do well? | Open text | Show if score >= 4 |

### Step 4: Build Response Workflows

#### Closed-Loop Process

| Score Range | Classification | Automated Action | Human Action | SLA |
|:-----------:|---------------|-----------------|-------------|-----|
| **0-6 (Detractor)** | At-risk | Alert account owner, create case | Personal outreach within SLA | 24 hours |
| **7-8 (Passive)** | Opportunity | Tag for nurture campaign | Outreach for accounts > $X ARR | 72 hours |
| **9-10 (Promoter)** | Advocate | Trigger review/referral ask | Thank-you note for top accounts | 1 week |
| **Any + churn signal** | Urgent | Alert CS leader + account owner | Immediate intervention call | 4 hours |

#### Internal Routing

| Feedback Theme | Route To | Expected Action |
|---------------|---------|-----------------|
| Product bug or defect | Engineering via bug tracker | Triage and fix |
| Feature request | Product management via backlog | Evaluate and prioritize |
| Support complaint | Support leadership | Coach agent, improve process |
| Pricing objection | Sales / RevOps | Review packaging and value messaging |
| Competitive mention | Product marketing | Update battlecard and positioning |

### Step 5: Establish Reporting Cadence

| Report | Audience | Frequency | Content |
|--------|---------|-----------|---------|
| **Real-time dashboard** | CX team, Support leads | Live | Score trends, open loops, alerts |
| **Weekly digest** | Functional leaders | Weekly | Score snapshot, top themes, closed-loop status |
| **Monthly deep-dive** | VP+ leadership | Monthly | Trend analysis, segment comparison, action progress |
| **Quarterly board report** | Executive / Board | Quarterly | NPS trend, competitive position, strategic themes |
| **Ad-hoc alert** | Account owners | Event-driven | Detractor alert with context for immediate follow-up |

### Step 6: Governance and Optimization

## Output Format

```markdown
## Feedback Management Program: [Name]

### Program Overview
- **Objective**: [What we are measuring and why]
- **Segments covered**: [Customer segments]
- **Channels**: [Collection channels]
- **Launch date**: [Date]

### Collection Strategy
| Feedback Type | Method | Trigger | Frequency | Target Audience |
|---------------|--------|---------|-----------|----------------|

### Survey Instruments
[Survey templates with questions, scales, and logic]

### Closed-Loop Workflow
| Score/Signal | Action | Owner | SLA |
|-------------|--------|-------|-----|

### Internal Routing
| Theme | Destination | Expected Response |

### Reporting Cadence
| Report | Audience | Frequency | Key Metrics |

### Survey Fatigue Prevention
- Max survey frequency per customer: [X per quarter]
- Cool-down period between surveys: [X days]
- Opt-out mechanism: [Description]
- Sampling strategy: [Random, stratified, census]

### Program KPIs
| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Response rate | >20% | | |
| Closed-loop rate (detractors) | >90% | | |
| Time to close loop | <48 hrs | | |
| Action rate (insights acted on) | >60% | | |
| NPS improvement (annualized) | +5 points | | |

### Governance
- Program owner: [Name/Role]
- Review cadence: [Monthly/Quarterly]
- Tool stack: [Survey platform, CRM, analytics]
```

## Quality Checklist

- [ ] Collection strategy covers both relationship and transactional feedback
- [ ] Survey instruments are concise and mobile-friendly
- [ ] Closed-loop process has clear owners, SLAs, and escalation paths
- [ ] Survey fatigue is managed — customers are not over-surveyed
- [ ] Reporting serves different audiences at appropriate frequencies
- [ ] Feedback is routed to the teams that can act on it, not just collected
- [ ] Program has defined success metrics and a review cadence

## Edge Cases

- **Low response rates**: Before changing the survey, diagnose the cause — bad timing, poor channel, survey fatigue, or lack of incentive
- **Customer refuses to respond but is at-risk**: Use behavioral signals (usage drop, support volume) as proxy feedback
- **Feedback contradicts usage data**: Customers say they love a feature but never use it — trust behavior over stated preference for prioritization
- **Regulatory constraints**: In some industries (healthcare, finance), feedback collection requires consent management and data handling compliance
- **Multi-stakeholder B2B accounts**: Survey multiple contacts per account; aggregate at account level but preserve individual perspectives
- **Survey tool migration**: Plan for historical data continuity — ensure trend analysis is not broken by platform changes
