---
name: onboarding-flow
description: "Designs customer onboarding flows with welcome steps, milestone triggers, and success checkpoints to reduce churn and speed time-to-value."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Onboarding Flow

## When to Use This Skill

Use this skill when you need to:
- Design a customer onboarding sequence from purchase to first success
- Create welcome emails, milestone triggers, and success checkpoints
- Reduce early churn by getting customers to value faster
- Standardize the post-purchase experience

**DO NOT** use this skill for employee onboarding (use onboarding-checklist), sales funnels, or product demos. This is for the experience AFTER someone becomes a customer.

---

## Core Principle

THE GOAL OF ONBOARDING IS NOT TO TEACH EVERYTHING — IT IS TO GET THE CUSTOMER TO THEIR FIRST WIN AS FAST AS POSSIBLE, BECAUSE EARLY WINS CREATE RETENTION.

---

## Phase 1: Define Success

Identify what customer success looks like before designing the flow.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Product/service** | "What did the customer just buy?" | No default |
| **First win** | "What is the first success moment for a new customer?" | No default |
| **Time to value** | "How quickly should a customer experience that first win?" | Within 7 days |
| **Current onboarding** | "What happens after someone buys today?" | Welcome email only |
| **Drop-off points** | "Where do new customers get stuck or stop engaging?" | No default |
| **Delivery method** | "How do you deliver? (self-serve, done-with-you, done-for-you)" | Self-serve |

**GATE: Confirm the first win definition before designing the flow.**

---

## Phase 2: Map the Flow

Design the onboarding sequence step by step.

### Onboarding Flow Template

```
## Customer Onboarding Flow: [Product/Service Name]

**Goal:** Get customer to [first win] within [timeframe]

### Step 1: Welcome (Immediate — within minutes of purchase)
**Trigger:** Purchase confirmed
**Action:** Send welcome email
**Content:**
- Thank them and confirm what they bought
- Set expectations (what happens next, when to expect it)
- Provide ONE clear first action (not five)
- Include support contact for questions

### Step 2: Quick Start (Day 1)
**Trigger:** Welcome email opened or 24 hours post-purchase
**Action:** [Send quick-start guide / Schedule kickoff call / Grant access]
**Content:**
- The simplest path to the first win
- Remove all friction (pre-filled templates, default settings, step 1 of 3)
- Video walkthrough if applicable

### Step 3: First Milestone (Day 2-3)
**Trigger:** Customer completes first action OR 48 hours pass
**Action:** Check-in email or message
**Content:**
- If they completed the action: celebrate and guide to next step
- If they have not: gentle nudge with a "stuck?" offer of help

### Step 4: First Win (Day 3-7)
**Trigger:** Customer achieves first success metric
**Action:** Congratulations message + next steps
**Content:**
- Acknowledge the win
- Show what is possible next
- Introduce advanced features or next-level value

### Step 5: Habit Formation (Day 7-30)
**Trigger:** Time-based or usage-based
**Action:** Ongoing engagement sequence
**Content:**
- Tips, use cases, and success stories
- Feature highlights they have not used
- Invitation to community or advanced resources
```

**GATE: Present the flow for review before writing the actual content.**

---

## Phase 3: Write Content

Create the specific messages and materials for each step.

### Welcome Email Template

```
Subject: You're in! Here's your first step

Hi [Name],

Welcome to [Product/Service]!

Here is exactly what to do right now:

**Step 1:** [Single, clear action with link]

That is it. Do that one thing and you will be [benefit] by [timeframe].

If you get stuck, reply to this email — I read every one.

[Name]

P.S. [Set expectation for next touchpoint: "Tomorrow I will send you..."]
```

### Check-In Email Template

```
Subject: Quick check — did you [action]?

Hi [Name],

Just checking in — have you had a chance to [specific action from onboarding]?

**If yes:** Great! Your next step is [next action + link].

**If no:** No worries. Here is the easiest way to get started:
[1-2 sentence simplified instruction]

Most customers who [complete this step] see [specific benefit] within [timeframe].

Need help? [Support link or reply option]

[Name]
```

### Milestone Celebration Template

```
Subject: You did it — [specific achievement]

Hi [Name],

You just [specific milestone]. That is a big deal.

Here is what customers like you do next:
1. [Next feature or action]
2. [Advanced use case]

Keep going — you are building momentum.

[Name]
```

---

## Phase 4: Optimize

Set up tracking and continuous improvement.

### Onboarding Metrics

```
## Onboarding Dashboard

| Metric | Target | Current |
|--------|--------|---------|
| Welcome email open rate | 70%+ | — |
| First action completion rate | 50%+ within 48 hours | — |
| Time to first win | [X days] | — |
| 30-day retention rate | 85%+ | — |
| Support tickets during onboarding | Decreasing | — |
```

### Drop-Off Analysis

At each step, track how many customers proceed to the next step. Fix the step with the biggest drop-off first.

### Quarterly Review

1. Where are customers getting stuck?
2. What questions come up repeatedly? (Add answers to onboarding)
3. How fast are customers reaching first win vs. target?
4. What do retained customers have in common during onboarding?

---

## Anti-Patterns

- **Information dump on Day 1** — sending a 10-page guide overwhelms. One action per touchpoint.
- **No first action** — saying "explore the platform" is not an action. "Click here to create your first [X]" is.
- **Generic onboarding** — if possible, customize by use case, plan level, or stated goal.
- **No follow-up after welcome** — one email is not onboarding. The first 7-30 days need a designed sequence.
- **Assuming customers will figure it out** — they will not. They will churn. Guide them explicitly.

---

## Recovery

- **Customers are not opening welcome emails:** Improve subject line, send from a personal name (not "noreply"), and test send time.
- **Customers complete onboarding but still churn:** The first win may not be meaningful enough. Redefine what success looks like.
- **User has no email automation tool:** Start with manual emails for the first 10 customers. Templates make this feasible. Automate once the flow is proven.
- **Product is too complex for a 7-day onboarding:** Extend the timeline but keep the first win within 48 hours. Early momentum matters more than complete training.
- **User sells a one-time product (not subscription):** Onboarding still matters — it drives reviews, referrals, and repeat purchases. Focus on helping them USE what they bought.
