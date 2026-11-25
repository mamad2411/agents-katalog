---
name: freelance-rate-card
description: "Calculates freelance rates based on expenses, desired income, and market positioning with rate card formatting. Use when setting or updating your freelance pricing."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Freelance Rate Card

## When to Use This Skill

Use this skill when you need to:
- Calculate hourly, project, or retainer rates based on your income goals
- Create a professional rate card for client-facing use
- Evaluate whether your current rates support your financial goals
- Design a pricing structure with packages and tiers

**DO NOT** use this skill for employee salary negotiation, agency pricing, or product pricing strategy. This is specifically for freelancers and independent consultants.

---

## Core Principle

YOUR RATE IS NOT YOUR HOURLY WAGE — IT MUST COVER TAXES, BENEFITS, OVERHEAD, NON-BILLABLE TIME, AND PROFIT MARGIN ON TOP OF YOUR DESIRED TAKE-HOME PAY.

---

## Phase 1: Financial Inputs

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Desired annual income** | "What do you want to take home after taxes and expenses?" | No default — must be provided |
| **Annual business expenses** | "What are your yearly business costs? (software, insurance, equipment)" | $5,000 |
| **Tax rate** | "What is your estimated tax rate? (federal + state + self-employment)" | 30% |
| **Benefits cost** | "Annual cost for health insurance, retirement contributions?" | $8,000 |
| **Billable hours per week** | "How many hours per week can you bill to clients? (not total work hours)" | 25 hours |
| **Weeks worked per year** | "How many weeks do you work after vacation and holidays?" | 46 weeks |
| **Service type** | "What do you do? (design, writing, development, consulting, marketing)" | No default — must be provided |

**GATE: Do not proceed without desired income and service type.**

---

## Phase 2: Rate Calculation

### Hourly Rate Formula

```
## Rate Calculation

### Step 1: True Annual Need
| Component | Amount |
|-----------|--------|
| Desired take-home pay | $[X] |
| + Tax reserve (30%) | $[X] |
| + Business expenses | $[X] |
| + Benefits (health, retirement) | $[X] |
| + Profit margin (10-15%) | $[X] |
| **= Total annual revenue needed** | **$[X]** |

### Step 2: Available Billable Hours
| Component | Value |
|-----------|-------|
| Billable hours/week | [X] |
| x Weeks worked/year | [X] |
| **= Annual billable hours** | **[X]** |

### Step 3: Minimum Hourly Rate
| | |
|--|--|
| Total revenue needed | $[X] |
| / Billable hours | [X] |
| **= Minimum hourly rate** | **$[X]/hr** |
| Market-adjusted rate | **$[X]/hr** |
```

### Rate Types

```
### Your Rate Options

| Rate Type | Amount | When to Use |
|-----------|--------|------------|
| Hourly rate | $[X]/hr | Small tasks, consulting calls, overflow work |
| Half-day rate (4 hrs) | $[X] | Workshops, intensive sessions |
| Full-day rate (8 hrs) | $[X] | On-site work, full-day engagements |
| Project rate | $[X]-$[X] | Defined scope deliverables |
| Monthly retainer | $[X]/mo | Ongoing client relationships |

### Project Rate Formula
Project rate = (Estimated hours x Hourly rate) x 1.2 complexity buffer
```

---

## Phase 3: Rate Card Design

### Client-Facing Rate Card

```
## [Your Name] — Rate Card [Year]

### Services & Pricing

**[Service Category 1]**
| Service | Starting At | Includes |
|---------|-----------|----------|
| [Service A] | $[X] | [Deliverables, timeline] |
| [Service B] | $[X] | [Deliverables, timeline] |

**[Service Category 2]**
| Service | Starting At | Includes |
|---------|-----------|----------|
| [Service C] | $[X] | [Deliverables, timeline] |

### Retainer Packages
| Package | Hours/Month | Rate | Monthly Investment |
|---------|------------|------|-------------------|
| [Starter] | [X] hrs | $[X]/hr | $[X]/mo |
| [Growth] | [X] hrs | $[X]/hr | $[X]/mo |
| [Partner] | [X] hrs | $[X]/hr | $[X]/mo |

Retainer clients receive [priority scheduling, rollover hours, reduced rate].

### Additional Details
- **Rush fee:** +[25-50]% for turnaround under [X] days
- **Revisions:** [X] rounds included; additional at $[X]/hr
- **Payment terms:** [50% upfront, 50% on delivery / Net 15]
- **Availability:** Booking [X] weeks out
```

---

## Phase 4: Market Validation

### Market Rate Comparison

```
## Market Positioning

| Level | Market Range | Your Position |
|-------|-------------|--------------|
| Entry-level | $[X]-$[X]/hr | |
| Mid-level | $[X]-$[X]/hr | |
| Senior/Expert | $[X]-$[X]/hr | |
| Premium/Specialist | $[X]+/hr | |

**Your rate:** $[X]/hr — positioned at [level]

### Positioning Notes
- If below market: opportunity to raise rates
- If at market: differentiate on quality, speed, or specialization
- If above market: ensure brand and portfolio justify premium
```

---

## Example: Freelance Web Developer ($100K Take-Home Goal)

**Calculation:** $100K income + $30K taxes + $8K benefits + $5K expenses + $14.3K profit margin = $157,300 needed. At 25 billable hrs/week x 46 weeks = 1,150 billable hours. Minimum rate: $137/hr.

**Rate card:** Hourly $150/hr, half-day $550, full-day $1,000, website project $3,000-8,000, monthly retainer $2,400/mo (20 hrs at $120/hr retainer discount).

---

## Anti-Patterns

- **Using your employed salary to set freelance rates** — employees get benefits, PTO, and equipment. Freelancers pay for all of that. Freelance rates must be 2-3x the hourly equivalent of a salary.
- **Billing for every hour worked** — admin, marketing, invoicing, and learning are non-billable. You work 40 hours but bill 25.
- **Racing to the bottom** — competing on price attracts price-sensitive clients who are the hardest to serve. Compete on value.
- **No rush fee** — urgent work displaces planned work. Charge a premium for it.
- **Hourly-only pricing** — project and retainer pricing captures more value and provides income predictability.

---

## Recovery

- **Rate is below minimum viable:** Show the math. Either raise rates, reduce expenses, or increase billable hours. The numbers do not lie.
- **Afraid to raise rates:** Raise rates for new clients first. Existing clients get 60-90 days notice. Most will stay — the ones who leave were undervaluing you.
- **No idea what market rates are:** Research on freelance platforms, industry surveys, and peer conversations. Start at mid-market and adjust based on demand.
- **Clients push back on rates:** Value is the issue, not price. Improve your portfolio, add testimonials, or reframe pricing in terms of ROI to the client.
