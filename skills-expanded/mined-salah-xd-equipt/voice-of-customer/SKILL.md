---
name: voice-of-customer
description: "Builds Voice of Customer programs with collection methods, analysis frameworks, and insight distribution to drive customer-centric decisions."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Voice of Customer

## When to Use This Skill

Use this skill when you need to:
- Build a systematic Voice of Customer (VoC) program from scratch
- Define collection methods, analysis frameworks, and insight distribution
- Create a feedback loop that turns customer input into business improvements
- Ensure customer perspectives inform product, marketing, and service decisions

**DO NOT** use this skill for analyzing existing feedback (use feedback-analysis), writing surveys, or customer segmentation. This is for designing the overall VoC program.

---

## Core Principle

VOICE OF CUSTOMER IS NOT A SURVEY — IT IS AN ONGOING SYSTEM THAT CAPTURES, ANALYZES, AND ACTS ON WHAT CUSTOMERS SAY, THINK, AND FEEL ACROSS EVERY TOUCHPOINT.

---

## Phase 1: Program Design

Define the scope and goals of the VoC program.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business type** | "What does your business do?" | No default |
| **Customer base** | "How many customers do you have?" | Under 100 |
| **Current feedback** | "How do you collect feedback today?" | Ad hoc, no system |
| **Decisions to inform** | "What business decisions should customer input influence?" | Product, marketing, service |
| **Resources** | "How much time can you dedicate to VoC monthly?" | 2-4 hours |

**GATE: Confirm program goals before designing collection methods.**

---

## Phase 2: Collection System

Design the multi-channel feedback collection system.

### Collection Methods

```
## VoC Collection Channels

| Channel | Method | Frequency | Audience | Owner |
|---------|--------|-----------|----------|-------|
| Surveys | NPS + CSAT | Quarterly | All customers | [Name] |
| Interviews | 1:1 customer calls | Monthly (3-5 calls) | Power users + at-risk | [Name] |
| Support tickets | Tag and categorize themes | Ongoing | All support contacts | [Name] |
| Reviews | Monitor Google, G2, social | Weekly scan | Public reviewers | [Name] |
| Sales conversations | Document objections and requests | Ongoing | Prospects | [Name] |
| Usage data | Track behavior patterns | Monthly analysis | All users | [Name] |
```

### Customer Interview Guide

```
## VoC Interview Template (20 minutes)

1. How would you describe [product/service] to a colleague? (Positioning insight)
2. What problem were you trying to solve when you found us? (Jobs-to-be-done)
3. What is the single most valuable thing we do for you? (Core value prop)
4. If you could change one thing, what would it be? (Improvement priority)
5. What almost made you NOT buy / sign up? (Objection insight)
6. Is there anything you wish we offered that we do not? (Expansion opportunity)
```

**GATE: Present collection system for approval.**

---

## Phase 3: Analysis Framework

Turn raw feedback into actionable insights.

### Tagging System

```
## Feedback Tags

| Category | Tags |
|----------|------|
| Topic | Product, Service, Pricing, Support, Onboarding, Communication |
| Sentiment | Positive, Neutral, Negative |
| Impact | Feature request, Bug/Issue, Praise, Complaint, Suggestion |
| Urgency | Immediate, Next quarter, Backlog |
```

### Monthly VoC Report

```
## Voice of Customer Report — [Month]

### Data Summary
- Surveys collected: [#]
- Interviews completed: [#]
- Support tickets analyzed: [#]
- Reviews monitored: [#]

### Top Themes This Month
1. **[Theme]** — [# mentions] — Sentiment: [Pos/Neg] — "[Representative quote]"
2. **[Theme]** — [# mentions] — Sentiment: [Pos/Neg] — "[Quote]"
3. **[Theme]** — [# mentions] — Sentiment: [Pos/Neg] — "[Quote]"

### Key Insights
- [Insight 1 with business implication]
- [Insight 2 with business implication]

### Recommended Actions
| Action | Based On | Priority | Owner | Deadline |
|--------|----------|----------|-------|----------|
| [Action] | [Data source] | High/Med/Low | [Name] | [Date] |

### Trend Watch
- [Emerging theme to monitor next month]
```

---

## Phase 4: Action Loop

Close the loop between feedback and business action.

### Insight Distribution

```
## Who Gets What

| Audience | Insights | Format | Frequency |
|----------|----------|--------|-----------|
| Product/Development | Feature requests, usability issues | Prioritized list | Monthly |
| Marketing | Customer language, objections, testimonials | Quote library + themes | Monthly |
| Support | Common issues, process gaps | FAQ updates + training | As needed |
| Leadership | Strategic themes, satisfaction trends | Executive summary | Quarterly |
```

### Closing the Loop with Customers

When feedback leads to action, tell the customer:
- "You told us [feedback]. We [action taken]."
- Share via email, product updates, or social media
- This encourages future feedback participation

### Quarterly VoC Review

1. What are the top 3 themes across all channels?
2. Which themes are new vs. recurring?
3. Did last quarter's actions impact satisfaction?
4. What should we prioritize next quarter based on VoC data?
5. Are we collecting from the right channels?

---

## Anti-Patterns

- **Collecting without acting** — feedback without follow-through burns customer goodwill. If you ask, you must act.
- **Only listening to loud voices** — the angriest customer is not representative. Weight feedback by volume and segment.
- **Survey fatigue** — too many surveys kill response rates. Limit to quarterly at most.
- **Ignoring positive feedback** — positive themes reveal competitive advantages. Amplify them.
- **VoC as a one-time project** — this is an ongoing program, not a research project. Build it into the monthly rhythm.

---

## Recovery

- **User has zero feedback data:** Start with 5 customer interviews this month. That is enough to surface initial themes.
- **Customers will not participate in interviews:** Offer value in return — share industry insights during the call, or offer a small credit.
- **Too much data, not enough analysis:** Focus on the top 3 themes only. Depth on a few themes beats breadth on many.
- **User does not have time for a full program:** Start with one channel (monthly interviews OR quarterly surveys). Add channels only after the first one is a habit.
- **Insights are not driving decisions:** Tie each insight to a specific business decision. "Customers want X" is weak. "Customers want X, which we should address in Q2 product update" is actionable.
