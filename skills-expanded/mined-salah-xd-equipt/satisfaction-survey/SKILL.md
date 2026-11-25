---
name: satisfaction-survey
description: "Creates customer satisfaction (CSAT) surveys with touchpoint-specific questions and benchmarking frameworks for measuring service quality."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Satisfaction Survey

## When to Use This Skill

Use this skill when you need to:
- Create a CSAT survey tied to specific customer touchpoints
- Design questions that produce actionable, measurable feedback
- Build benchmarking frameworks to track satisfaction over time
- Set up a recurring satisfaction measurement program

**DO NOT** use this skill for NPS surveys (use nps-survey), market research, or product feedback forms. This is specifically for measuring customer satisfaction with interactions and experiences.

---

## Core Principle

CSAT MEASURES HOW WELL YOU DELIVERED ON A SPECIFIC PROMISE AT A SPECIFIC MOMENT — UNLIKE NPS (LOYALTY) OR CES (EFFORT), CSAT TELLS YOU WHETHER THE CUSTOMER GOT WHAT THEY EXPECTED RIGHT NOW.

---

## Phase 1: Define Touchpoints

Identify which customer interactions to measure.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business type** | "What product or service do you provide?" | No default |
| **Touchpoints** | "At which moments do you interact with customers? (purchase, onboarding, support, delivery)" | No default |
| **Measurement goal** | "Are you measuring a specific interaction or overall satisfaction?" | Specific touchpoint |
| **Distribution method** | "How will you send surveys? (email, in-app, post-interaction)" | Email |
| **Current CSAT baseline** | "Have you measured satisfaction before?" | No baseline |

### Touchpoint Map

```
## Touchpoint Measurement Plan

| Touchpoint | When to Survey | Method | Target Response Rate |
|-----------|---------------|--------|---------------------|
| Post-purchase | Within 24 hours | Email | 25%+ |
| Post-onboarding | Day 7-14 | Email | 30%+ |
| Post-support | After ticket closed | In-ticket link | 20%+ |
| Post-delivery | After deliverable received | Email | 25%+ |
| Periodic check-in | Quarterly | Email | 30%+ |
```

**GATE: Confirm touchpoints before designing the survey.**

---

## Phase 2: Build Survey

Create touchpoint-specific CSAT surveys.

### CSAT Question Format

```
How satisfied were you with [specific interaction]?

[ 1 - Very Dissatisfied ]
[ 2 - Dissatisfied ]
[ 3 - Neutral ]
[ 4 - Satisfied ]
[ 5 - Very Satisfied ]
```

**CSAT Score = (# of 4s and 5s / Total responses) x 100**

### Survey Templates by Touchpoint

**Post-Purchase Survey:**
```
1. How satisfied are you with your purchase experience? (1-5)
2. How easy was the buying process? (1-5)
3. What, if anything, almost stopped you from buying? [Open text]
4. Anything we could improve? [Open text]
```

**Post-Support Survey:**
```
1. How satisfied are you with the support you received? (1-5)
2. Was your issue resolved? (Yes / Partially / No)
3. How would you describe the response time? (Too slow / About right / Fast)
4. Any suggestions to improve our support? [Open text]
```

**Post-Delivery Survey:**
```
1. How satisfied are you with what was delivered? (1-5)
2. Did the deliverable meet your expectations? (Exceeded / Met / Below)
3. What did you like most? [Open text]
4. What could be improved? [Open text]
```

**Quarterly Overall Survey:**
```
1. Overall, how satisfied are you with [Business Name]? (1-5)
2. Which area are you most satisfied with? [Multiple choice: Product / Support / Communication / Value]
3. Which area needs the most improvement? [Same options]
4. Is there anything specific you would like us to change? [Open text]
```

### Survey Email Template

```
Subject: Quick feedback? (Takes 60 seconds)

Hi [Name],

[One sentence about the recent interaction — "You just [completed purchase / received support / got your deliverable]."]

I would love your quick feedback:

**How satisfied were you?** [Click a number: 1-5]

Your response helps us improve. Thank you!

[Name]
```

**GATE: Present survey for review before building benchmarks.**

---

## Phase 3: Benchmarking

Set up measurement and tracking frameworks.

### CSAT Dashboard

```
## CSAT Dashboard — [Period]

### Overall
| Period | Responses | CSAT Score | Trend |
|--------|-----------|-----------|-------|
| [Month 1] | [#] | [%] | — |
| [Month 2] | [#] | [%] | [+/-%] |

### By Touchpoint
| Touchpoint | Responses | CSAT Score | Target | Status |
|-----------|-----------|-----------|--------|--------|
| Post-purchase | [#] | [%] | 85%+ | On/Off Target |
| Post-support | [#] | [%] | 90%+ | On/Off Target |
| Post-delivery | [#] | [%] | 85%+ | On/Off Target |
```

### Industry Benchmarks

| Industry | Average CSAT |
|----------|-------------|
| SaaS | 78% |
| E-commerce | 80% |
| Professional services | 82% |
| Healthcare | 74% |

Target: 5-10 points above your industry average.

### Segmentation Analysis

Break CSAT by customer segment to find hidden patterns:
- By customer tenure (new vs. long-term)
- By plan level (free vs. paid vs. premium)
- By use case or product line

---

## Phase 4: Act

Convert satisfaction data into improvements.

### Response Protocol

```
## CSAT Response Actions

| Score | Action | Timeframe |
|-------|--------|-----------|
| 1-2 (Dissatisfied) | Personal outreach to understand and resolve | Within 48 hours |
| 3 (Neutral) | Follow-up email asking what would improve the experience | Within 1 week |
| 4-5 (Satisfied) | Thank-you email + request for review or referral | Within 1 week |
```

### Monthly CSAT Review

1. What is the overall CSAT trend?
2. Which touchpoint has the lowest score? Why?
3. What themes appear in open-text responses?
4. What one change would improve the lowest-scoring touchpoint?
5. Have previous improvements impacted scores?

### Closing the Loop

After implementing changes based on CSAT feedback:
- Notify respondents that their feedback led to changes
- Re-measure the touchpoint to confirm improvement
- Share CSAT improvements with the team

---

## Anti-Patterns

- **Surveying every interaction** — sending a survey after every email creates fatigue. Survey key moments only.
- **Long surveys** — more than 5 questions kills completion rates. Keep CSAT surveys under 2 minutes.
- **Not acting on low scores** — collecting satisfaction data without follow-up is worse than not asking.
- **Only measuring overall satisfaction** — touchpoint-specific CSAT reveals where problems live. Overall CSAT hides them.
- **Celebrating high scores without investigating** — 90% CSAT with 10% response rate may mean only happy customers respond.

---

## Recovery

- **Low response rates:** Shorten the survey to 1-2 questions. Improve the subject line. Send within 1 hour of the interaction.
- **CSAT score drops suddenly:** Check for a specific incident or process change that coincides with the drop. Do not assume a trend from one period.
- **All responses are 4-5 (suspiciously high):** Add an open-text question that invites criticism: "What is the ONE thing we could do better?"
- **User has no survey tool:** Use a simple Google Form or Typeform free tier. Even a reply-to-this-email format works at small scale.
- **User is not sure which touchpoints to measure:** Start with post-support (highest signal for improvement) and post-purchase (highest signal for marketing).
