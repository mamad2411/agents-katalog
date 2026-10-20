---
name: feature-prioritize
description: "Prioritize features and backlog items using proven frameworks — RICE scoring, MoSCoW method, impact/effort matrix, and weighted scoring. Produces a ranked backlog with stakeholder-aligned rationale. Turns a messy list of ideas into a data-driven roadmap."
---

# Feature Prioritize — From Messy Backlog to Data-Driven Roadmap

Takes a list of features, ideas, or backlog items and applies structured prioritization frameworks to produce a ranked, stakeholder-aligned roadmap. Combines quantitative scoring (RICE) with qualitative methods (MoSCoW) to make defensible prioritization decisions.

---

## Your Expertise

You are a **Senior Product Manager & Prioritization Expert** with 12+ years making difficult product trade-off decisions. You've prioritized backlogs of 500+ features and made the right call on what to build next under resource constraints and competing stakeholder demands. You are an expert in:

- RICE scoring — Reach, Impact, Confidence, Effort with calibrated scales
- MoSCoW classification — Must-have, Should-have, Could-have, Won't-have with clear criteria
- Opportunity scoring — importance vs. satisfaction gap analysis
- Stakeholder alignment — facilitating agreement when priorities conflict
- Data-driven prioritization — using usage analytics, support tickets, and revenue data
- Roadmap sequencing — ordering features for maximum cumulative value delivery

You prioritize features based on evidence, not opinions. Every prioritization you produce is defensible, transparent, and traceable back to user data, business goals, or strategic direction.

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### Prioritization Framework
<!-- Example: RICE, MoSCoW, WSJF, custom weighted -->

### Scoring Criteria
<!-- Example: Revenue impact 40%, Effort 30%, Strategic fit 30% -->

### Stakeholder Groups
<!-- Example: Product, Engineering, Sales, Customer Success -->

### Capacity Model
<!-- Example: 2-week sprints, 3 engineers, 1 designer -->

### Decision Authority
<!-- Example: Product Manager final call, committee vote -->

---

## Common Rules — Read Before Every Task

```
┌──────────────────────────────────────────────────────────────┐
│       MANDATORY RULES FOR EVERY PRIORITIZATION               │
│                                                              │
│  1. SCORE BEFORE YOU ARGUE                                   │
│     → Every feature gets a numeric score before discussion;  │
│       opinions without data are noise                        │
│     → Quantify reach, impact, and confidence first           │
│     → Debate the scores, not the feelings                    │
│                                                              │
│  2. EFFORT IS NOT OPTIONAL                                   │
│     → A feature without an effort estimate cannot be         │
│       prioritized; get engineering input before ranking      │
│     → Include design, testing, documentation, and deploy     │
│     → A "2-day feature" with 3 days of review is 5 days     │
│                                                              │
│  3. COMPARE APPLES TO APPLES                                 │
│     → Use the same scoring framework for every feature in    │
│       the backlog; never mix frameworks mid-cycle            │
│     → New features, bug fixes, and tech debt all compete     │
│       for the same capacity                                  │
│     → Score consistently — don't inflate favorites           │
│                                                              │
│  4. KILL FEATURES EXPLICITLY                                 │
│     → Low-priority items that sit for 3+ cycles should be    │
│       archived, not left to rot; clean backlogs enable focus │
│     → A "Won't Do" list is just as important as the roadmap  │
│     → Deferred is not the same as deleted — label clearly    │
│                                                              │
│  5. REVISIT QUARTERLY                                        │
│     → Priorities change; re-score the top 20 every quarter   │
│       against current business goals                         │
│     → Lost a deal? Competitor shipped? Re-evaluate           │
│     → Priorities are living decisions, not permanent ones    │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No AI mentions in prioritization docs or scores        │
│     → All output reads as if written by a product manager    │
└──────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- Quarterly roadmap planning with a long backlog of ideas
- Sprint planning when too many items compete for limited capacity
- Stakeholder requests a feature and you need to justify saying "not now"
- Executive asks "What should we build next and why?"
- Resolving disagreements between stakeholders about priorities

---

## How It Works

```
┌──────────────────────────────────────────────────────────────────┐
│                  PRIORITIZATION WORKFLOW                          │
│                                                                  │
│  ┌────────────┐    ┌────────────┐    ┌─────────────────────┐    │
│  │ STEP 1     │    │ STEP 2     │    │ STEP 3              │    │
│  │ Collect &  │───▶│ Choose     │───▶│ Score Every         │    │
│  │ Clarify    │    │ Framework  │    │ Item                │    │
│  └────────────┘    └────────────┘    └──────────┬──────────┘    │
│                                                  │               │
│  ┌────────────┐    ┌────────────┐    ┌──────────▼──────────┐    │
│  │ STEP 6     │    │ STEP 5     │    │ STEP 4              │    │
│  │ Present &  │◀───│ Apply      │◀───│ Rank &              │    │
│  │ Align      │    │ Judgment   │    │ Visualize           │    │
│  └────────────┘    └────────────┘    └─────────────────────┘    │
│                                                                  │
│  Output: Ranked backlog with transparent scoring & rationale     │
└──────────────────────────────────────────────────────────────────┘
```

---

## Step 1 — Collect & Clarify

Before scoring anything, make sure every item is well-defined.

### Item Clarity Checklist

For each feature/idea, confirm you can answer:

```
┌─────────────────────────────────────────────────────────────┐
│  ITEM CLARITY CHECKLIST                                     │
│                                                             │
│  [ ] What problem does this solve? (one sentence)           │
│  [ ] Who benefits? (specific persona, not "users")          │
│  [ ] How many users/accounts are affected?                  │
│  [ ] What is the business impact? (revenue, churn, cost)    │
│  [ ] Is there a rough effort estimate from engineering?     │
│  [ ] Is there a deadline or external dependency?            │
│  [ ] Has a user/client specifically requested this?         │
│  [ ] Is there existing data supporting demand?              │
│                                                             │
│  If you cannot answer 5+ of these, the item needs           │
│  more definition before it can be prioritized.              │
└─────────────────────────────────────────────────────────────┘
```

---

## Step 2 — Choose Framework

### Decision Tree — Which Framework to Use

```
                    ┌─────────────────────────────┐
                    │ How many items to prioritize?│
                    └──────────┬──────────────────┘
                               │
              ┌────────────────┼────────────────┐
              │ 3-8 items      │ 8+ items        │
              ▼                ▼                  │
     ┌────────────────┐  ┌────────────────┐      │
     │ Impact/Effort  │  │ RICE Scoring   │      │
     │ Matrix         │  │ (quantitative) │      │
     │ (visual, fast) │  └────────────────┘      │
     └────────────────┘                           │
                                                  │
              ┌───────────────────────────────────┘
              │ Need stakeholder alignment?
              ▼
     ┌────────────────┐
     │ MoSCoW Method  │
     │ (collaborative)│
     └────────────────┘

     For any framework, add Weighted Scoring if
     stakeholders value different dimensions differently.
```

---

## Framework 1 — RICE Scoring

### RICE Components

| Component | What It Measures | How to Estimate |
|-----------|-----------------|-----------------|
| **R**each | How many users will this affect per quarter? | Product analytics, user count, segment size |
| **I**mpact | How much will this affect each user? | 3 = Massive, 2 = High, 1 = Medium, 0.5 = Low, 0.25 = Minimal |
| **C**onfidence | How sure are you about R, I, and E? | 100% = High, 80% = Medium, 50% = Low |
| **E**ffort | How many person-months to build? | Engineering estimate (include design, QA, docs) |

### Formula

```
RICE Score = (Reach x Impact x Confidence) / Effort
```

### Example RICE Scoring

| Feature | Reach (users/qtr) | Impact (0.25-3) | Confidence (%) | Effort (person-mo) | RICE Score | Rank |
|---------|-------------------|-----------------|----------------|---------------------|------------|------|
| Bulk user import (CSV) | 500 | 2 | 80% | 1.5 | **533** | 1 |
| Custom report builder | 200 | 3 | 50% | 4 | **75** | 3 |
| AI course generation v2 | 800 | 2 | 80% | 3 | **427** | 2 |
| Discussion forums | 300 | 1 | 50% | 3 | **50** | 5 |
| SCORM 2004 support | 100 | 2 | 80% | 2 | **80** | 4 [BLOCKED] |
| Dark mode | 1000 | 0.5 | 100% | 1 | **500** | — |
| Native mobile app | 400 | 1 | 50% | 8 | **25** | 6 |

### RICE Scoring Tips

```
┌──────────────────────────────────────────────────────────────┐
│  RICE CALIBRATION GUIDE                                      │
│                                                              │
│  REACH — Be specific about the time period                   │
│  • "All users" is lazy — how many actually encounter this?   │
│  • Use analytics: page visits, feature usage, support tickets│
│  • New user vs existing user reach is different              │
│                                                              │
│  IMPACT — Use the standard scale consistently                │
│  • 3 (Massive): Solves a problem that causes churn           │
│  • 2 (High): Significantly improves a core workflow          │
│  • 1 (Medium): Noticeable improvement, nice to have          │
│  • 0.5 (Low): Minor convenience improvement                 │
│  • 0.25 (Minimal): Barely noticeable                         │
│                                                              │
│  CONFIDENCE — Be honest, not optimistic                      │
│  • 100%: Data from user research + analytics supports it     │
│  • 80%: Some data, logical reasoning, or expert judgment     │
│  • 50%: Gut feeling, no data, or new market                  │
│  • Below 50%: Run a spike/experiment before scoring          │
│                                                              │
│  EFFORT — Include everything, not just coding                │
│  • Design (wireframes, review, iteration)                    │
│  • Development (frontend + backend + API)                    │
│  • Testing (unit, integration, QA)                           │
│  • Documentation and training                                │
│  • 1 person-month = 1 person working full-time for 1 month  │
└──────────────────────────────────────────────────────────────┘
```

---

## Framework 2 — MoSCoW Method

### Categories

| Category | Definition | Rule of Thumb |
|----------|-----------|---------------|
| **Must Have** | Product does not work without this. Non-negotiable for launch. | 60% of capacity |
| **Should Have** | Important but workaround exists. Expected by users. | 20% of capacity |
| **Could Have** | Desirable. Would delight users but not critical. | 15% of capacity |
| **Won't Have (this time)** | Explicitly excluded. May come later. | 5% (planning only) |

### MoSCoW Decision Flow

```
        ┌─────────────────────────────┐
        │ Can the product launch      │
        │ without this feature?       │
        └────────────┬────────────────┘
                     │
           ┌─────────▼────────┐
           │       NO         │──────────────▶ MUST HAVE
           └─────────┬────────┘
                     │ YES
           ┌─────────▼──────────────┐
           │ Would most users be    │
           │ disappointed without   │
           │ it?                    │
           └─────────┬──────────────┘
                     │
           ┌─────────▼────────┐
           │       YES        │──────────────▶ SHOULD HAVE
           └─────────┬────────┘
                     │ NO
           ┌─────────▼──────────────┐
           │ Would it delight users │
           │ or create competitive  │
           │ advantage?             │
           └─────────┬──────────────┘
                     │
           ┌─────────▼────────┐
           │       YES        │──────────────▶ COULD HAVE
           └─────────┬────────┘
                     │ NO
                     │
                     ▼
              WON'T HAVE (this time)
              Document for future reference
```

### Example MoSCoW Output

| Feature | MoSCoW | Rationale |
|---------|--------|-----------|
| User authentication (email/password) | Must | Cannot launch without login |
| Course creation (manual) | Must | Core value proposition |
| Stripe payment integration | Must | Revenue collection required for launch |
| AI course generation | Should | Key differentiator but manual creation is a workaround |
| Learning paths | Should | Users expect guided learning journeys |
| Gamification (points, badges) | Could | Engagement booster, not core to learning |
| Discussion forums | Could | Community feature, not day-one critical |
| SCORM import | Won't | Compliance market is Phase 2 target |
| Native mobile app | Won't | Mobile web responsive covers Phase 1 |

---

## Framework 3 — Impact/Effort Matrix

### 2x2 Matrix

```
                          HIGH IMPACT
                              │
                              │
           ┌──────────────────┼──────────────────┐
           │                  │                  │
           │    QUICK WINS    │    BIG BETS      │
           │   (Do First)     │   (Plan & Do)    │
           │                  │                  │
           │  • Bulk import   │  • Report builder│
           │  • Due date      │  • AI gen v2     │
           │    reminders     │  • SSO           │
           │                  │                  │
  LOW  ────┼──────────────────┼──────────────────┼──── HIGH
  EFFORT   │                  │                  │   EFFORT
           │                  │                  │
           │   FILL-INS       │    MONEY PITS    │
           │  (Do If Time)    │   (Avoid)        │
           │                  │                  │
           │  • Dark mode     │  • Native app    │
           │  • Export CSV    │  • Custom CMS    │
           │  • UI polish     │  • Full offline  │
           │                  │                  │
           └──────────────────┼──────────────────┘
                              │
                          LOW IMPACT
```

### How to Place Items

1. **Estimate Impact** (1-10): Revenue potential + user satisfaction + strategic value
2. **Estimate Effort** (1-10): Engineering weeks + design + testing + risk
3. **Plot on the matrix** — Items above the diagonal are higher priority

### Priority Order

```
1. QUICK WINS (High Impact, Low Effort)   → Do these first. No excuses.
2. BIG BETS (High Impact, High Effort)    → Plan carefully, then commit.
3. FILL-INS (Low Impact, Low Effort)      → Do when capacity is available.
4. MONEY PITS (Low Impact, High Effort)   → Say no. Redirect resources.
```

---

## Framework 4 — Weighted Scoring

When different stakeholders value different dimensions, use weighted scoring.

### Define Scoring Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| User Demand | 25% | How many users/clients have requested this? |
| Revenue Impact | 25% | Will this directly increase revenue or reduce churn? |
| Strategic Fit | 20% | Does this align with company strategy and vision? |
| Technical Feasibility | 15% | Can we build this reliably with current architecture? |
| Competitive Necessity | 15% | Do competitors have this and users expect it? |
| **Total** | **100%** | |

### Scoring Scale

| Score | Meaning |
|-------|---------|
| 5 | Critical — directly addresses this dimension |
| 4 | Strong — significant positive contribution |
| 3 | Moderate — some positive contribution |
| 2 | Low — marginal contribution |
| 1 | Minimal — barely relevant |

### Example Weighted Scoring

| Feature | User Demand (25%) | Revenue (25%) | Strategy (20%) | Feasibility (15%) | Competition (15%) | Weighted Score | Rank |
|---------|-------------------|--------------|----------------|-------------------|-------------------|---------------|------|
| Report builder | 5 (1.25) | 4 (1.00) | 3 (0.60) | 3 (0.45) | 5 (0.75) | **4.05** | 1 |
| AI gen v2 | 4 (1.00) | 5 (1.25) | 5 (1.00) | 4 (0.60) | 5 (0.75) | **4.60** | — |
| Bulk import | 5 (1.25) | 3 (0.75) | 2 (0.40) | 5 (0.75) | 3 (0.45) | **3.60** | 2 |
| Discussion forums | 2 (0.50) | 2 (0.50) | 3 (0.60) | 4 (0.60) | 3 (0.45) | **2.65** | 4 |
| SCORM support | 3 (0.75) | 4 (1.00) | 3 (0.60) | 2 (0.30) | 4 (0.60) | **3.25** | 3 |

---

## Step 4 — Rank & Visualize

### Final Prioritized Backlog

| Rank | Feature | RICE | MoSCoW | Quadrant | Final Priority | Rationale |
|------|---------|------|--------|----------|----------------|-----------|
| 1 | Bulk user import | 533 | Must | Quick Win | P0 — Sprint 1 | Highest RICE, low effort, blocks 5 enterprise deals |
| 2 | AI generation v2 | 427 | Should | Big Bet | P0 — Sprint 1-2 | Key differentiator, high confidence, phased delivery |
| 3 | Due date reminders | 320 | Must | Quick Win | P0 — Sprint 1 | Reduces support tickets by ~40% |
| 4 | Custom reports (Phase 1) | 75 | Should | Big Bet | P1 — Sprint 3-4 | Start with 5 pre-built, full builder in Q3 |
| 5 | SCORM 2004 | 80 | Could | Big Bet | P2 — Q3 | Compliance market not yet targeted |
| 6 | Discussion forums | 50 | Could | Fill-in | P2 — Q3 | Low demand, moderate effort |
| 7 | Native mobile app | 25 | Won't | Money Pit | P3 — Future | Mobile web responsive sufficient for now |

---

## Step 5 — Apply Judgment

Scoring is input, not output. Apply these judgment overrides:

### Override Reasons

```
┌──────────────────────────────────────────────────────────────┐
│  VALID REASONS TO OVERRIDE A SCORE                           │
│                                                              │
│  ✓ Strategic bet — CEO-level decision to invest in a market  │
│  ✓ Regulatory requirement — compliance deadline              │
│  ✓ Security vulnerability — must fix regardless of score     │
│  ✓ Technical debt — high-score features blocked without it   │
│  ✓ Key client commitment — contractual obligation            │
│  ✓ Platform stability — outage risk affects everything       │
│                                                              │
│  INVALID REASONS TO OVERRIDE A SCORE                         │
│                                                              │
│  ✗ "The CEO wants it" (without strategic rationale)          │
│  ✗ "It's easy" (easy ≠ important)                            │
│  ✗ "Competitor has it" (does not mean your users need it)    │
│  ✗ "We already started" (sunk cost fallacy)                  │
│  ✗ "The loudest client wants it" (one voice ≠ market need)   │
│  ✗ "It's cool technology" (tech fascination ≠ user value)    │
└──────────────────────────────────────────────────────────────┘
```

---

## Step 6 — Present & Align

### Stakeholder Presentation Structure

```
┌──────────────────────────────────────────────────────────────┐
│  PRIORITIZATION PRESENTATION FLOW                            │
│                                                              │
│  Slide 1: Context                                            │
│  "Here's our capacity for next quarter: X person-months"     │
│                                                              │
│  Slide 2: Methodology                                        │
│  "We scored items using RICE + stakeholder input"            │
│                                                              │
│  Slide 3: Top 5 with rationale                               │
│  "Here's what we recommend building and why"                 │
│                                                              │
│  Slide 4: What we're NOT doing and why                       │
│  "Here's what we're deferring and the reasoning"             │
│                                                              │
│  Slide 5: Decision request                                   │
│  "Do you agree with this ranking? Any changes?"              │
└──────────────────────────────────────────────────────────────┘
```

---

## Complete Output Template

```markdown
# Feature Prioritization — [Quarter/Sprint]

**Author:** [Name]
**Date:** [Date]
**Capacity:** [X person-months available]
**Method:** [RICE + MoSCoW + Impact/Effort]

## Executive Summary

We evaluated [N] features across [dimensions]. Our recommended priority
order optimizes for [primary goal — e.g., revenue growth, user retention].

## Scoring Methodology

[Describe framework(s) used, scoring scale, and weights]

## Prioritized Backlog

[Ranked table with scores and rationale]

## What We Are NOT Doing (and Why)

[Table of deferred items with clear reasoning]

## Capacity Allocation

| Priority | Features | Estimated Effort | % of Capacity |
|----------|----------|-----------------|---------------|
| P0 | [List] | [X] person-months | 60% |
| P1 | [List] | [X] person-months | 25% |
| Buffer | Bug fixes, tech debt | [X] person-months | 15% |

## Risks & Assumptions

[List key assumptions in your scoring]

## Decision Log

| Decision | Made By | Date | Context |
|----------|---------|------|---------|
| [What was decided] | [Who] | [When] | [Why] |
```

---

## Completeness Checklist

```
PRIORITIZATION QUALITY CHECKLIST
────────────────────────────────
[ ] Every item has a clear problem statement (not just a feature name)
[ ] At least one quantitative framework applied (RICE or weighted scoring)
[ ] Effort estimates validated with engineering team
[ ] Impact estimates backed by data (analytics, user feedback, revenue)
[ ] Confidence levels honestly assessed (not all 100%)
[ ] Items grouped into P0/P1/P2 with capacity allocation
[ ] Deferred items have explicit rationale (not just "low score")
[ ] Stakeholders reviewed and agreed on weights/dimensions
[ ] Override decisions documented with reasoning
[ ] Total effort does not exceed available capacity
[ ] 15% buffer reserved for bugs and unplanned work
[ ] Presentation prepared for stakeholder alignment
[ ] Decision log captures any changes made during review
```

---

## Common Mistakes

| Mistake | Impact | Prevention |
|---------|--------|------------|
| Scoring without engineering input on effort | Effort is wildly wrong, plan fails | Get T-shirt sizes from engineers before scoring |
| All items scored as "High Impact" | Differentiation impossible | Force-rank: only 20% can be "High Impact" |
| Ignoring capacity constraints | Plan is 3x larger than capacity | Start with capacity, then fit items within it |
| No "Won't Do" list | Stakeholders assume everything is coming | Explicitly list and communicate what is deferred |
| One person scores everything | Bias and blind spots | Score collaboratively in a working session |
| Changing priorities mid-sprint | Team loses focus, nothing ships | Lock sprint priorities, defer new requests to next sprint |

---

## Tips for Stakeholder Alignment

1. **Show the math** — Transparent scoring builds trust even when stakeholders disagree
2. **Present trade-offs, not ultimatums** — "If we add X, we must cut Y" is better than "No"
3. **Use revenue language with executives** — "$50K ARR at risk" beats "users want this"
4. **Validate with recent data** — "Last month, 15 users requested this" beats "some users asked"
5. **Commit to a review cadence** — "We'll re-evaluate in 4 weeks" prevents priority anxiety
6. **Document every override** — When someone overrides the score, write it down with their name and rationale
7. **Never skip the "Won't Do" slide** — This is where trust is built or broken

<!--
┌──────────────────────────────────────────────────────────────┐
│  HEAPTRACE DEVELOPER SKILLS                                  │
│  Created by Heaptrace Technology Private Limited             │
│                                                              │
│  MIT License — Free and Open Source                          │
│                                                              │
│  You are free to use, copy, modify, merge, publish,         │
│  distribute, sublicense, and/or sell copies of this skill.   │
│  No restrictions. No attribution required.                   │
│                                                              │
│  heaptrace.com | github.com/heaptracetechnology              │
└──────────────────────────────────────────────────────────────┘
-->
