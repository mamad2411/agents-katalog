---
name: nps-survey
description: "Creates Net Promoter Score surveys with follow-up questions, segmentation logic, and response action plans to measure customer loyalty."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# NPS Survey

## When to Use This Skill

Use this skill when you need to:
- Create a Net Promoter Score survey with follow-up questions
- Design segmentation logic for promoters, passives, and detractors
- Build action plans based on NPS responses
- Set up a recurring NPS measurement program

**DO NOT** use this skill for CSAT surveys (use satisfaction-survey), product feedback forms, or market research. This is specifically for NPS measurement.

---

## Core Principle

NPS IS NOT JUST A NUMBER — IT IS A SYSTEM FOR IDENTIFYING YOUR BIGGEST FANS AND YOUR MOST AT-RISK CUSTOMERS, THEN ACTING ON BOTH.

---

## Phase 1: Survey Design

Define the survey structure and targeting.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business type** | "What product or service are you measuring?" | No default |
| **Customer base size** | "Approximately how many customers do you have?" | Under 100 |
| **Survey timing** | "When should the survey go out? (post-purchase, quarterly, annual)" | Quarterly |
| **Distribution method** | "How will you send it? (email, in-app, SMS)" | Email |
| **Current NPS** | "Do you have a baseline NPS score?" | No baseline |

**GATE: Confirm survey parameters before drafting.**

---

## Phase 2: Build Survey

Create the NPS survey with follow-up logic.

### Core NPS Question

```
On a scale of 0-10, how likely are you to recommend [Business/Product Name] to a friend or colleague?

[0] [1] [2] [3] [4] [5] [6] [7] [8] [9] [10]
Not at all likely                    Extremely likely
```

### Follow-Up Questions (Conditional)

**For Detractors (0-6):**
```
We are sorry to hear that. What is the primary reason for your score?
[ ] Product/service quality
[ ] Customer support
[ ] Price/value
[ ] Missing features
[ ] Other: ___________

What would we need to change for you to rate us higher?
[Open text field]
```

**For Passives (7-8):**
```
Thanks for your feedback. What would make your experience exceptional?
[Open text field]

What almost made you rate us higher?
[Open text field]
```

**For Promoters (9-10):**
```
That is great to hear! What do you value most about [Business/Product]?
[Open text field]

Would you be willing to share your experience as a review or testimonial?
[ ] Yes, contact me
[ ] No, thanks
```

### Survey Email Template

```
Subject: Quick question — 30 seconds

Hi [Name],

One question: How likely are you to recommend [Business] to a friend or colleague?

[Click your score: 0-10]

Your feedback directly shapes what we build and improve.

Thank you,
[Name]
```

**GATE: Present the complete survey for approval.**

---

## Phase 3: Response Plan

Define what happens after each response.

### NPS Calculation

```
NPS = % Promoters (9-10) - % Detractors (0-6)

Score range: -100 to +100
- Below 0: Critical — more detractors than promoters
- 0-30: Needs improvement
- 30-50: Good
- 50-70: Excellent
- 70+: World-class
```

### Response Action Matrix

```
## NPS Response Actions

### Detractors (0-6) — Recover
**Timeframe:** Respond within 24 hours
**Action:**
1. Personal email or call from [owner/manager]
2. Acknowledge the issue specifically
3. Offer a concrete resolution
4. Follow up within 1 week to confirm satisfaction
**Goal:** Convert to passive or prevent churn

### Passives (7-8) — Convert
**Timeframe:** Respond within 1 week
**Action:**
1. Thank them for the feedback
2. Address the specific gap they identified
3. Share an upcoming improvement relevant to their feedback
**Goal:** Move to promoter territory

### Promoters (9-10) — Activate
**Timeframe:** Respond within 1 week
**Action:**
1. Thank them personally
2. If they agreed to a testimonial, follow up with a simple template
3. Invite to referral program or advisory group
4. Ask for a public review (Google, G2, etc.)
**Goal:** Turn loyalty into advocacy
```

---

## Phase 4: Program Setup

Build a recurring NPS measurement system.

### Measurement Cadence

```
## NPS Program Schedule

**Frequency:** [Quarterly / Biannually]
**Survey window:** [2 weeks open for responses]
**Reminder:** [Send one reminder after 5 days to non-respondents]
**Target response rate:** 30%+ (offer no incentive — NPS should measure genuine sentiment)
```

### Tracking Dashboard

```
## NPS Trend

| Period | Responses | Promoters | Passives | Detractors | NPS Score | Change |
|--------|-----------|-----------|----------|-----------|-----------|--------|
| Q1 | [#] | [%] | [%] | [%] | [Score] | — |
| Q2 | [#] | [%] | [%] | [%] | [Score] | [+/-] |
```

### Quarterly NPS Review

1. How did NPS change vs. last period?
2. What themes appear in detractor feedback?
3. Did last quarter's actions improve scores?
4. How many promoters were activated (reviews, referrals)?
5. What one change would have the biggest NPS impact next quarter?

---

## Anti-Patterns

- **Surveying too often** — quarterly is plenty. Monthly NPS surveys cause survey fatigue and lower response rates.
- **Not acting on responses** — collecting NPS without responding to detractors is worse than not surveying at all.
- **Incentivizing responses** — gift cards for completing the survey bias results upward. Measure real sentiment.
- **Only tracking the number** — the NPS score is less valuable than the open-text feedback. Read every response.
- **Cherry-picking timing** — surveying only after positive interactions inflates the score and hides problems.

---

## Recovery

- **Low response rate (under 20%):** Shorten the survey (NPS question + one follow-up only), improve the subject line, send from a personal email address.
- **NPS is negative:** Focus on the top 3 detractor themes. Fix those before the next survey cycle.
- **User has too few customers for statistical significance:** NPS still works qualitatively at small scale. Read every response as a customer conversation, not a data point.
- **Promoters agree to testimonials but never follow through:** Send a pre-written testimonial for their approval instead of asking them to write one from scratch.
- **NPS is not changing despite improvements:** Check if the improvements address the actual complaints. Often businesses fix what is easy, not what customers asked for.
