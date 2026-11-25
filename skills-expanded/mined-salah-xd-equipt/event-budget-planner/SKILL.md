---
name: event-budget-planner
description: "Creates event budgets with line items, contingency planning, sponsor offset calculations, and ROI projections."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Event Budget Planner

## When to Use This Skill

Use this skill when you need to:
- Create a detailed event budget with line items and cost estimates
- Plan contingency reserves and sponsor revenue offsets
- Project event ROI including ticket revenue, sponsorship, and indirect value
- Build a budget tracking template for pre-event, day-of, and post-event expenses

**DO NOT** use this skill for general business budgets, marketing campaign budgets, or personal event planning. This is for professional or business event financial planning.

---

## Core Principle

AN EVENT BUDGET IS A DECISION-MAKING TOOL, NOT JUST A SPREADSHEET — EVERY LINE ITEM SHOULD CONNECT TO ATTENDEE EXPERIENCE OR REVENUE GENERATION, AND EVERY DOLLAR SHOULD HAVE A CONTINGENCY PLAN.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Event type** | "What kind of event? (conference, workshop, summit, meetup, gala)" | Conference |
| **Expected attendance** | "How many attendees?" | 100-200 |
| **Duration** | "How long? (half day, full day, multi-day)" | Full day |
| **Format** | "In-person, virtual, or hybrid?" | In-person |
| **Total budget** | "What is your maximum budget?" | No default — must be provided |
| **Revenue sources** | "Ticket sales, sponsorships, both, or free event?" | Tickets + sponsorships |

**GATE: Confirm the brief before building the budget.**

---

## Phase 2: Budget Framework

### Expense Categories

```
## Budget Categories (% of total for in-person events)

| Category | % Range | Includes |
|----------|---------|----------|
| Venue | 25-35% | Rental, insurance, permits |
| Catering | 20-30% | Meals, breaks, beverages, dietary |
| AV/Technology | 10-15% | Sound, screens, streaming, wifi |
| Speakers | 5-15% | Fees, travel, hotel, gifts |
| Marketing | 5-10% | Ads, email, design, print |
| Materials | 3-5% | Signage, programs, name badges, swag |
| Staff/Volunteers | 3-5% | Coordinator, day-of staff, volunteer costs |
| Contingency | 10-15% | Unexpected expenses |
```

### Revenue Projections

```
## Revenue Sources

**Ticket Sales:**
| Tier | Price | Expected Qty | Revenue |
|------|-------|-------------|---------|
| Early bird | $[X] | [Y] | $[Z] |
| Regular | $[X] | [Y] | $[Z] |
| VIP | $[X] | [Y] | $[Z] |
| **Total ticket revenue** | | | **$[X]** |

**Sponsorship:**
| Tier | Price | Available | Expected Sold | Revenue |
|------|-------|-----------|-------------|---------|
| Title | $[X] | 1 | 1 | $[X] |
| Gold | $[X] | 3 | 2 | $[X] |
| Silver | $[X] | 5 | 3 | $[X] |
| **Total sponsorship revenue** | | | | **$[X]** |

**Total projected revenue: $[X]**
```

**GATE: Present the budget framework and revenue projections for approval.**

---

## Phase 3: Build

### Detailed Line-Item Budget

```
## Expense Detail

### Venue
| Item | Estimated | Actual | Variance | Notes |
|------|----------|--------|----------|-------|
| Room rental | $[X] | | | |
| Insurance | $[X] | | | |
| Parking | $[X] | | | |
| **Subtotal** | **$[X]** | | | |

### Catering
| Item | Per Person | Qty | Estimated | Actual |
|------|-----------|-----|----------|--------|
| Breakfast | $[X] | [Y] | $[Z] | |
| Lunch | $[X] | [Y] | $[Z] | |
| PM break | $[X] | [Y] | $[Z] | |
| Beverages | $[X] | [Y] | $[Z] | |
| Dietary accommodations | Flat | | $[Z] | |
| **Subtotal** | | | **$[X]** | |

[Continue for each category...]
```

### Break-Even Analysis

```
## Break-Even Calculation

**Total fixed costs:** $[X] (venue, AV, speakers — costs regardless of attendance)
**Variable cost per attendee:** $[Y] (catering, materials, badges)
**Average ticket revenue per attendee:** $[Z]
**Sponsorship revenue (fixed):** $[W]

**Break-even attendees:** (Fixed Costs - Sponsorship) / (Ticket Price - Variable Cost)
= ($[X] - $[W]) / ($[Z] - $[Y])
= [Number] attendees
```

### Cash Flow Timeline

```
## When Money Moves

**6 months out:** Venue deposit (50%), speaker deposits
**3 months out:** Venue balance, AV deposit, marketing spend begins
**1 month out:** Catering final count + payment, materials printing
**Week of:** Staff payments, last-minute supplies
**Day of:** Cash for emergencies, tip fund
**Post-event:** Final invoices, speaker payments, contingency reconciliation
```

---

## Phase 4: Polish

### 1. Contingency Planning

```
## Contingency Scenarios

**If ticket sales are 25% below target:**
- Cut: [Specific items to reduce — swag, upgraded catering, extra AV]
- Impact: Saves $[X], minimal attendee experience impact

**If a major sponsor drops out:**
- Backfill plan: [Approach next-tier prospects, offer custom packages]
- Cut: [Items funded by sponsorship]

**If attendance exceeds capacity:**
- Cap registration at [X]
- Waitlist management
- Consider adding a live stream option
```

### 2. Budget Tracking Template

```
## Weekly Budget Review (during planning phase)

| Category | Budgeted | Committed | Spent | Remaining | Status |
|----------|----------|-----------|-------|-----------|--------|
| Venue | $[X] | $[X] | $[X] | $[X] | On track |
| Catering | $[X] | $[X] | $[X] | $[X] | Over |
| ... | | | | | |
| Contingency | $[X] | $[X] | $[X] | $[X] | |
| **Total** | **$[X]** | **$[X]** | **$[X]** | **$[X]** | |
```

### 3. ROI Calculation

```
## Event ROI

**Direct revenue:** Tickets ($[X]) + Sponsorships ($[X]) = $[Total]
**Total expenses:** $[X]
**Direct profit/loss:** $[X]

**Indirect value (estimate):**
- Email list growth: [X new subscribers] × $[value per sub] = $[X]
- Client leads generated: [X leads] × [conversion rate] × [avg client value] = $[X]
- Brand exposure: [impressions] — qualitative value
- Partnerships formed: [count] — qualitative value

**Total estimated ROI:** $[X] / $[Total expenses] = [X]%
```

---

## Example 1: 150-Person Business Conference

```
Budget: $30,000
Revenue: $25,000 tickets + $12,000 sponsorship = $37,000
Major costs: Venue $8,000, Catering $9,000, AV $4,000, Speakers $3,500
Contingency: $3,000 (10%)
Break-even: 85 attendees
Projected profit: $7,000
```

## Example 2: Free Community Meetup (50 People)

```
Budget: $2,000
Revenue: $1,500 sponsorship + $0 tickets
Major costs: Venue $500 (co-working space), Catering $800, Materials $200
Contingency: $200 (10%)
Break-even: N/A (sponsor-funded)
ROI: Measured in leads and community growth
```

---

## Anti-Patterns

- **No contingency line** — every event has surprises. Budget 10-15% for the unexpected.
- **Underestimating catering** — food costs rise with final counts and dietary requests. Pad by 15%.
- **Ignoring hidden venue costs** — insurance, AV surcharges, overtime fees, and cleanup charges add up. Ask for the full cost breakdown.
- **Optimistic ticket projections** — plan for 70% of your target, not 100%. Budget must work at the conservative number.
- **No cash flow planning** — having the money and having it at the right time are different things. Map when payments are due.
- **Forgetting post-event costs** — speaker final payments, thank-you gifts, recording editing, and final invoices come after the event.

---

## Recovery

- **Budget exceeds available funds:** Cut in order: swag first, then downgrade catering, then reduce AV complexity. Never cut the contingency.
- **Ticket sales are slow:** Increase marketing spend from contingency, add urgency (deadline pricing), or offer group discounts.
- **Sponsor revenue falls short:** Create a la carte sponsorship options at lower price points. Offer "community sponsor" tier at $250-500.
- **User has never budgeted an event:** Start with the percentage guidelines and a comparable event's costs as benchmarks. Adjust after the first event.
