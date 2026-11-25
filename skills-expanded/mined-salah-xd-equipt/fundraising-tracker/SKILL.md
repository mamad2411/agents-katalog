---
name: fundraising-tracker
description: "Creates fundraising pipeline trackers with investor stages, valuation calculations, and term sheet comparisons. Use when managing an active fundraising process."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Fundraising Tracker

## When to Use This Skill

Use this skill when you need to:
- Organize and track an active fundraising pipeline
- Compare term sheets and investment offers
- Calculate dilution and valuation scenarios
- Create a structured fundraising process with timelines and milestones

**DO NOT** use this skill for writing pitch decks, building financial models, or managing post-raise investor relations. This is for tracking the fundraising process itself.

---

## Core Principle

FUNDRAISING IS A SALES PROCESS — TRACK IT LIKE A PIPELINE WITH STAGES, CONVERSION RATES, AND DEADLINES TO MAINTAIN MOMENTUM AND LEVERAGE.

---

## Phase 1: Fundraise Parameters

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Raise amount** | "How much are you raising?" | No default — must be provided |
| **Round type** | "What type of round? (pre-seed, seed, Series A, bridge, SAFE)" | Seed |
| **Valuation range** | "What pre-money valuation are you targeting?" | No default — must be discussed |
| **Instrument** | "SAFE, convertible note, or priced round?" | SAFE |
| **Timeline** | "When do you need to close?" | 3 months |
| **Current investors in pipeline** | "How many investors have you contacted or plan to contact?" | Will build list |

**GATE: Do not proceed without raise amount and round type.**

---

## Phase 2: Pipeline Tracker

### Investor Pipeline

```
## Fundraising Pipeline: [Round Type] — $[Amount]

### Pipeline Summary
| Stage | Count | % of Pipeline |
|-------|-------|--------------|
| Target list | [X] | [X]% |
| Outreach sent | [X] | [X]% |
| First meeting | [X] | [X]% |
| Follow-up / diligence | [X] | [X]% |
| Term sheet / verbal | [X] | [X]% |
| Committed | [X] | [X]% |
| Passed | [X] | [X]% |

### Detailed Pipeline
| Investor | Type | Check Size | Stage | Last Contact | Next Step | Notes |
|----------|------|-----------|-------|-------------|-----------|-------|
| [Name] | [VC/Angel/Fund] | $[X] | [Stage] | [Date] | [Action] | |
| [Name] | [VC/Angel/Fund] | $[X] | [Stage] | [Date] | [Action] | |

### Pipeline Stages
1. **Target** — Identified, researching fit
2. **Outreach** — Email/intro sent, awaiting response
3. **First Meeting** — Introductory call or meeting scheduled/completed
4. **Follow-up** — Second meeting, diligence, or partner meeting
5. **Term Sheet** — Received term sheet or verbal commitment
6. **Committed** — Signed docs, wiring funds
7. **Passed** — Declined or went cold
```

---

## Phase 3: Term Sheet Comparison and Dilution

### Term Sheet Comparison

```
## Term Sheet Comparison

| Term | Investor A | Investor B | Investor C |
|------|-----------|-----------|-----------|
| Investment amount | $[X] | $[X] | $[X] |
| Instrument | [SAFE/Note/Priced] | | |
| Pre-money valuation | $[X] | $[X] | $[X] |
| Valuation cap (if SAFE) | $[X] | $[X] | $[X] |
| Discount rate | [X]% | [X]% | [X]% |
| Pro-rata rights | [Yes/No] | | |
| Board seat | [Yes/No] | | |
| Information rights | [Yes/No] | | |
| Liquidation preference | [X]x | | |
| Anti-dilution | [Broad/Narrow/None] | | |
| Founder vesting | [Terms] | | |
| **Founder-friendliness** | **[1-10]** | **[1-10]** | **[1-10]** |
```

### Dilution Calculator

```
## Dilution Scenarios

### Current Cap Table
| Shareholder | Shares | % Ownership |
|------------|--------|------------|
| Founder(s) | [X] | [X]% |
| Existing investors | [X] | [X]% |
| Option pool | [X] | [X]% |
| **Total** | **[X]** | **100%** |

### Post-Round Cap Table (at $[X]M valuation)
| Shareholder | Shares | % Ownership | Dilution |
|------------|--------|------------|---------|
| Founder(s) | [X] | [X]% | -[X]% |
| Existing investors | [X] | [X]% | -[X]% |
| New investors | [X] | [X]% | New |
| Option pool | [X] | [X]% | |
| **Total** | **[X]** | **100%** | |
```

---

## Phase 4: Process Management

### Fundraising Timeline

```
## Fundraising Timeline

| Week | Milestone | Target |
|------|-----------|--------|
| Week 1-2 | Build target list, warm intros | [X] investors contacted |
| Week 3-4 | First meetings | [X] meetings completed |
| Week 5-6 | Follow-ups, partner meetings | [X] in diligence |
| Week 7-8 | Term sheets expected | [X] term sheets |
| Week 9-10 | Negotiate and close | Signed commitments |
| Week 11-12 | Wire funds, legal close | Money in bank |
```

### Weekly Review Checklist

```
- [ ] Pipeline updated with latest stages and dates
- [ ] Follow-ups sent within 48 hours of every meeting
- [ ] New intros requested from existing network
- [ ] Investor update sent to committed investors
- [ ] Documents ready for any investor entering diligence
```

---

## Example: $500K Pre-Seed SAFE

**Pipeline:** 40 investors targeted, 25 outreach sent, 12 first meetings, 4 in diligence, 2 verbal commits ($150K + $100K). Need $250K more from remaining pipeline.

**Valuation:** $5M cap SAFE. At conversion: founders retain 88% post-round (12% to investors, including option pool refresh to 10%).

---

## Anti-Patterns

- **Fundraising without a pipeline** — spray-and-pray wastes time. Build a targeted list of 30-50 investors who invest in your stage, sector, and check size.
- **Stopping outreach after first term sheet** — the best leverage is multiple term sheets. Keep the pipeline active until you sign.
- **Not tracking follow-ups** — investors move slowly. If you do not follow up within 48 hours, you lose momentum.
- **Accepting the first term sheet without comparison** — unless the terms are exceptional, wait for 2-3 options. Every term is negotiable.
- **Sharing cap table with every investor** — share cap table only during diligence with serious investors. Protect this information.

---

## Recovery

- **No warm intros:** Cold email with a strong one-line hook (traction metric + ask). Expect 10-15% response rate. Increase volume.
- **All investors passing:** Reassess — is it timing, valuation, traction, or pitch? Get feedback from investors who passed.
- **Fundraise taking longer than planned:** Shorten the timeline by creating urgency (other investor interest, closing deadline). Consider bridge financing from angels.
- **Oversubscribed (too much interest):** Increase the round size, raise the valuation cap, or select investors who bring strategic value beyond capital.
