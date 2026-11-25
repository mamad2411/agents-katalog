---
name: saas-cancellation-flow
description: "Designs cancellation flows with retention offers, feedback collection, and win-back sequence triggers. Use when building or optimizing subscription cancellation experiences."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# SaaS Cancellation Flow

## When to Use This Skill

Use this skill when you need to:
- Design a cancellation flow that retains users without being manipulative
- Build retention offers matched to specific cancellation reasons
- Create an exit survey that produces actionable data
- Set up win-back email triggers for cancelled accounts

**DO NOT** use this skill for churn prevention (pre-cancellation interventions), pricing changes, or customer support scripts. This is for the cancellation flow UX and messaging.

---

## Core Principle

A CANCELLATION FLOW RESPECTS THE USER'S DECISION WHILE OFFERING GENUINE ALTERNATIVES — DARK PATTERNS DESTROY TRUST AND GENERATE CHARGEBACKS. MAKE IT EASY TO LEAVE AND WORTH STAYING.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Product and pricing** | "What is the product and what do plans cost?" | No default — must be provided |
| **Current cancellation rate** | "What percentage of users cancel per month?" | Unknown |
| **Top cancellation reasons** | "Why do users cancel? List the top 3-5 reasons." | No default — must be provided |
| **Current flow** | "What is the cancellation process today?" | Email support to cancel |
| **Retention budget** | "Are you willing to offer discounts or credits to save accounts?" | Yes, within limits |
| **Billing provider** | "What handles your billing? Stripe, Paddle, custom?" | Stripe |

**GATE: Confirm the brief before designing the flow.**

---

## Phase 2: Design the Flow

### Cancellation Flow Steps

```
1. User clicks "Cancel Subscription"
   ↓
2. Exit Survey (required, 1 question)
   ↓
3. Matched Retention Offer (based on survey answer)
   ↓
4a. User accepts offer → Subscription continues
4b. User declines → Confirmation page
   ↓
5. Confirmation + what they lose + when access ends
   ↓
6. Win-back sequence triggered (Day 3, 7, 30)
```

### Exit Survey Design

One primary question with 5-7 options:

```
"We are sorry to see you go. What is the main reason you are cancelling?"

○ Too expensive
○ Not using it enough
○ Missing a feature I need
○ Switching to another tool
○ Business is closing/pausing
○ Had a bad experience
○ Other: [text field]
```

**Rules:**
- One question only (completion rate drops with each additional question)
- Required before proceeding (but do not hide the cancel button)
- Optional text field for elaboration
- No guilt-tripping language

**GATE: Confirm the flow and survey before writing offers and copy.**

---

## Phase 3: Write

### Retention Offers by Reason

| Reason | Offer | Copy |
|--------|-------|------|
| Too expensive | 30% off for 3 months | "We would love to keep you. How about 30% off for the next 3 months while you evaluate the ROI?" |
| Not using it enough | Free strategy call | "Let us help you get more value. Book a free 15-minute setup call and we will optimize your account." |
| Missing a feature | Roadmap preview + timeline | "That feature is on our roadmap for [month]. Want to stay and be first to try it?" |
| Switching to another tool | Feature comparison | "Before you go — here is how we compare on [key differentiator]. Would a [specific improvement] change your mind?" |
| Business closing | Pause option (90 days) | "We get it. You can pause your subscription for up to 90 days and pick up where you left off." |
| Bad experience | Escalation to founder | "I am sorry about your experience. Can I connect you with [founder name] directly to make it right?" |

### Confirmation Page Copy

```
## Your subscription has been cancelled

**What happens next:**
- You have access until [billing cycle end date]
- Your data will be saved for 90 days
- You can reactivate anytime from your account settings

**What you will lose access to:**
- [Key feature 1]
- [Key feature 2]
- [Key feature 3]

We would love to have you back. If anything changes, your account is one click away.
```

### Win-Back Email Sequence

| Email | Timing | Subject | Approach |
|-------|--------|---------|----------|
| 1 | Day 3 | "Your account is still here" | Acknowledge departure, no pressure |
| 2 | Day 7 | "Here is what you are missing" | Highlight new features or improvements |
| 3 | Day 30 | "Come back — [special offer]" | Discount or credit offer |

---

## Phase 4: Polish

### 1. Metrics to Track

```
## Cancellation Flow Metrics

- **Save rate:** % of users who start cancellation but accept a retention offer
- **Exit survey completion rate:** % who answer the survey question
- **Top cancellation reasons:** Ranked by frequency
- **Win-back conversion rate:** % who reactivate within 30/60/90 days
- **Time to cancel:** Seconds from "Cancel" click to confirmation (keep under 60)
- **Chargeback rate:** Should decrease with a transparent flow
```

### 2. Legal and UX Compliance

- Cancel button must be findable within 2 clicks from account settings
- No hidden or greyed-out cancel options
- No requiring phone calls or emails to cancel
- Confirmation email sent immediately after cancellation
- Data retention policy clearly stated
- Comply with applicable regulations (FTC, EU consumer protection)

### 3. Quality Checklist

```
## Cancellation Flow Checklist

- [ ] Cancel option is findable within 2 clicks
- [ ] Exit survey is 1 question with 5-7 options
- [ ] Retention offers are matched to specific cancellation reasons
- [ ] Offers have clear terms and limits (not unlimited discounts)
- [ ] Confirmation page shows what the user loses and when access ends
- [ ] Data retention policy is stated on the confirmation page
- [ ] Confirmation email sends immediately
- [ ] Win-back sequence triggers on cancellation (Day 3, 7, 30)
- [ ] Time to complete cancellation is under 60 seconds
- [ ] No dark patterns (hidden buttons, guilt trips, mandatory calls)
```

---

## Example

**Product:** Project management SaaS, $29/month

**Retention offer (too expensive):**
"We hear you — $29/month is an investment. We can offer you 3 months at $19/month while you evaluate whether the time savings justify the cost. That is $30 back in your pocket. [Accept Offer] [No thanks, cancel]"

**Win-back email (Day 30):**
```
Subject: We have made some changes since you left

Hey [Name],

Since you cancelled, we have shipped:
- [New feature 1]
- [Improvement relevant to their cancellation reason]

Come back and try it free for 7 days — no commitment, no credit card.

[Reactivate My Account]
```

---

## Anti-Patterns

- **Dark patterns** — hiding the cancel button, requiring calls, or adding unnecessary steps. Users will chargeback and leave angry.
- **Same offer for every reason** — a discount does not help someone whose business is closing. Match the offer to the reason.
- **No exit survey** — cancellations without data are wasted learning opportunities.
- **Guilt-tripping copy** — "Are you sure you want to abandon your progress?" is manipulative. Be respectful.
- **No win-back sequence** — 20-30% of cancellers are recoverable within 90 days. Silence after cancellation leaves money on the table.

---

## Recovery

- **Cannot offer discounts:** Offer a plan downgrade, feature pause, or extended trial instead.
- **No data on why users cancel:** Implement the exit survey immediately. Even 2 weeks of data reveals patterns.
- **Users complain the flow is too long:** Cut steps. Survey + one offer + confirmation is the maximum. If it takes more than 60 seconds, simplify.
- **High chargeback rate:** Your cancellation flow is too hard to find or complete. Fix the UX immediately.
