---
name: churn-analysis
description: "Diagnoses customer churn patterns and creates retention intervention strategies with warning signals, win-back triggers, and prevention playbooks. Use when a user is losing customers or subscribers, wants to understand why people leave, or needs to reduce churn rate for a subscription or recurring service."
---

# Churn Analysis & Retention Planner

## When to Use This Skill

- Subscription or membership churn rate is above industry average
- Customers are leaving and you don't know why
- Want to build an early warning system for at-risk customers
- Losing revenue to cancellations faster than acquiring new customers
- Need to prioritize which retention efforts to invest in

## Core Principle

**CHURN IS A SYMPTOM, NOT THE DISEASE. Every churned customer had a moment where the value they received dropped below the price they paid. Find that moment.**

## Workflow

### Step 1: Define the Churn Landscape

Ask the user:
1. What's your business model? (subscription, membership, retainer, repeat purchase)
2. What's your current churn rate? (monthly or annual)
3. How do customers cancel? (self-serve, email, phone, just stop buying)
4. Do you have exit survey data or cancellation reasons?
5. What's your average customer lifetime and LTV?

**Minimum needed: questions 1 and 2. If they don't know churn rate, help them calculate it: customers lost this month / customers at start of month.**

### Step 2: Identify Churn Patterns

Analyze by segment:

| Segment | Typical Churn Pattern | Root Cause |
|---------|----------------------|------------|
| Early churn (0-30 days) | Never activated or engaged | Poor onboarding, unmet expectations |
| Mid-term churn (1-6 months) | Used it, then stopped | Didn't find ongoing value, found alternative |
| Long-term churn (6+ months) | Loyal then left suddenly | Price increase, bad experience, life change |
| Seasonal churn | Predictable drop-offs | Budget cycles, seasonal relevance |
| Involuntary churn | Payment failures | Expired cards, insufficient funds |

### Step 3: Build Warning Signals

Create an early warning dashboard:

| Warning Signal | Risk Level | Timeframe | Action |
|---------------|-----------|-----------|--------|
| No login/purchase in 14 days | Medium | Trigger at day 14 | Send re-engagement email |
| Support ticket unresolved 48+ hrs | High | Immediate | Escalate and follow up |
| Downgraded plan | High | Within 7 days | Personal outreach from account manager |
| Usage dropped 50%+ from average | High | Trigger weekly | Send "We miss you" + value reminder |
| Payment failed | Critical | Same day | Dunning email sequence (3 emails over 7 days) |
| Viewed cancellation page | Critical | Real-time | Trigger retention offer or chat popup |

### Step 4: Create Retention Interventions

For each churn segment, build an intervention:

**Early Churn Prevention:**
- Improve onboarding (guided setup, quick wins in first 48 hours)
- Send "did you know?" emails highlighting unused features
- Assign onboarding buddy or check-in call

**Mid-Term Retention:**
- Monthly value recaps ("Here's what you accomplished this month")
- Feature announcements tied to their use case
- Community engagement invitations

**Long-Term Loyalty:**
- Anniversary recognition and rewards
- Exclusive access to new features or content
- Personal relationship building (handwritten notes, surprise gifts)

**Involuntary Churn Recovery:**
- Pre-dunning: Remind customers before card expires
- Dunning sequence: 3 emails over 7 days with easy update link
- Grace period: Keep access active for 7 days after failed payment

### Step 5: Deliver Churn Reduction Plan

Provide a prioritized action plan with expected impact.

## Examples

### Example 1: SaaS Project Management Tool ($29/mo)

**Current State:** 8.5% monthly churn (industry avg: 5-7%)
**Analysis:**

| Churn Segment | % of Total Churn | Primary Reason |
|--------------|-----------------|----------------|
| Early (0-30 days) | 45% | Users sign up but never create a project |
| Mid-term (1-6 mo) | 30% | "Switched to Notion" or "Too complex for my needs" |
| Long-term (6+ mo) | 10% | Price increases, budget cuts |
| Involuntary | 15% | Failed payments |

**Priority Interventions:**

> **#1 — Fix Onboarding (target: reduce early churn by 50%)**
> - Add a "Create Your First Project" wizard that completes in 2 minutes
> - Send a "Quick Start" email 1 hour after signup with a 3-step guide
> - Trigger a personal email from the founder if no project created by day 3
> - Expected impact: Reduce early churn from 45% to 22% of total, dropping overall churn to ~6.4%
>
> **#2 — Recover Failed Payments (target: recover 40% of involuntary churn)**
> - Email 1 (day 0): "Your payment didn't go through — update in 30 seconds" [direct link]
> - Email 2 (day 3): "Your account is at risk — we'd hate to lose you"
> - Email 3 (day 7): "Last chance to keep your account active"
> - Keep account active with read-only access for 14 days after failure
> - Expected impact: Recover 6% of total churn, dropping to ~6.0%

### Example 2: Online Fitness Membership ($47/mo)

**Current State:** 12% monthly churn
**Top cancellation reasons (from exit survey):**

| Reason | % | Intervention |
|--------|---|-------------|
| "Not seeing results" | 35% | Add monthly progress check-ins + before/after tracking |
| "Don't have time" | 25% | Launch 10-minute express workout series |
| "Too expensive" | 20% | Offer annual plan at 30% discount before cancellation |
| "Boring/repetitive" | 15% | Release new content weekly, send "New This Week" email |
| Other | 5% | Personal outreach |

**Cancellation Save Flow:**
> When member clicks "Cancel":
> 1. Show: "Before you go — what's the #1 reason?" (select from list)
> 2. Based on answer, show targeted offer:
>    - "Not seeing results" → Free 1-on-1 session with a coach
>    - "Don't have time" → "Try our new 10-min express workouts"
>    - "Too expensive" → Annual plan at $29/mo (38% savings)
>    - "Boring" → Preview of new content dropping next week
> 3. If they still cancel: "We'll keep your progress saved. Come back anytime at your current rate."

## Recovery & Fallbacks

- **User has no churn data:** Start tracking today. Set up a simple spreadsheet: date, customer name, reason for leaving, last activity date. Even 30 days of data reveals patterns.
- **Churn rate seems fine but revenue is declining:** Check for downgrades (customers moving to cheaper plans) — this is "revenue churn" even without customer churn.
- **User can't implement automated triggers:** Start with manual interventions. A personal email from the founder to at-risk customers costs nothing and has the highest save rate.
- **Churn is seasonal and predictable:** Don't fight it. Instead, front-load revenue with annual plans, pre-pay discounts, or seasonal packaging.

## Constraints

- **NEVER recommend discounting as the primary retention strategy** — it trains customers to threaten cancellation for discounts
- Focus on finding and fixing the VALUE gap, not the PRICE gap
- Prioritize interventions by ease of implementation AND expected impact
- Always separate voluntary churn (customer chose to leave) from involuntary churn (payment failure)
- Include specific metrics and targets for each intervention
- Exit surveys should be 1-2 questions max — long surveys don't get completed
