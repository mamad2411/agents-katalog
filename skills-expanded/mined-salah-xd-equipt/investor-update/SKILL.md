---
name: investor-update
description: "Creates monthly investor update emails with metrics, highlights, challenges, and asks in a standard format. Use when sending regular updates to investors or advisors."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Investor Update

## When to Use This Skill

Use this skill when you need to:
- Write a monthly or quarterly investor update email
- Report metrics, wins, challenges, and asks in a standardized format
- Maintain transparency and trust with investors and advisors
- Create a reusable template for ongoing investor communications

**DO NOT** use this skill for pitch decks, fundraising materials, or board presentations. This is for regular update communications to existing investors.

---

## Core Principle

INVESTOR UPDATES BUILD TRUST THROUGH CONSISTENCY AND TRANSPARENCY — SHARE BOTH WINS AND CHALLENGES, AND ALWAYS INCLUDE A SPECIFIC ASK.

---

## Phase 1: Update Inputs

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Reporting period** | "What month/quarter is this update for?" | Previous month |
| **Key metrics** | "What are your core metrics? (MRR, users, revenue, growth rate)" | No default — must be provided |
| **Top wins** | "What were the 2-3 biggest wins this period?" | No default — must be provided |
| **Challenges** | "What are the biggest challenges or risks right now?" | No default — must be provided |
| **Asks** | "What do you need help with from investors? (intros, advice, hiring)" | No default — at least one ask |
| **Cash position** | "What is your current cash balance and runway?" | No default — must be provided |

**GATE: Do not proceed without metrics, wins, challenges, and cash position.**

---

## Phase 2: Update Structure

### Standard Investor Update Format

```
Subject: [Company Name] — [Month Year] Update

---

Hi [investors/team],

[1-2 sentence summary of the month — the headline version]

## Key Metrics

| Metric | This Month | Last Month | MoM Change |
|--------|-----------|------------|------------|
| MRR/Revenue | $[X] | $[X] | +/-[X]% |
| Customers/Users | [X] | [X] | +/-[X]% |
| [Key Metric 3] | [X] | [X] | +/-[X]% |
| Cash Balance | $[X] | $[X] | |
| Runway | [X] months | [X] months | |

## Highlights

1. **[Win 1]** — [2-3 sentence description with specific impact]
2. **[Win 2]** — [2-3 sentence description]
3. **[Win 3]** — [2-3 sentence description]

## Challenges

1. **[Challenge 1]** — [What it is + what you are doing about it]
2. **[Challenge 2]** — [What it is + what you are doing about it]

## Product/Business Update

[2-3 sentences on what shipped, what is in progress, or what strategic
decisions were made this month]

## Asks

I could use your help with:
1. **[Specific ask]** — [Context on why and what a good outcome looks like]
2. **[Specific ask]** — [Context]

## What's Next

[2-3 bullet points on priorities for next month]

---

Thanks for your continued support.

[Your name]
[Company]
```

---

## Phase 3: Tone and Content Guidelines

### What to Include

- **Metrics:** Always include the same metrics every month for trendability
- **Context:** Raw numbers without context are useless. "$50K MRR" means nothing — "$50K MRR, up 15% from $43.5K, driven by enterprise deal" means everything.
- **Honesty on challenges:** Investors respect founders who identify problems early. Hiding bad news erodes trust.
- **Specific asks:** "Can you introduce me to..." is better than "looking for connections." Make it easy for investors to help.

### Tone

- Confident but honest — not spin, not doom
- Data-driven — claims backed by numbers
- Concise — aim for 500 words maximum. Investors read dozens of updates.
- Professional but personal — sign off warmly, acknowledge their support

---

## Phase 4: Delivery

### Final Checklist

```
- [ ] All metrics are accurate and match financial records
- [ ] Metrics are consistent with prior updates (same format, same KPIs)
- [ ] At least 1 specific, actionable ask
- [ ] Cash position and runway are current
- [ ] Challenges section is honest and includes mitigation plans
- [ ] Email is under 500 words
- [ ] Sent within the first week of the new month
```

### Delivery Notes

- Send as a plain-text email (not a PDF attachment)
- BCC investors if they do not know each other, CC if they do
- Store a copy in your records for reference
- Track which investors respond — engaged investors are your best resource

---

## Example: SaaS Startup Monthly Update

**Subject:** Acme AI — January 2026 Update

**Summary:** "January was our best month yet — $32K MRR (up 22%), landed our first enterprise customer, and shipped the API integration that was blocking 3 deals."

**Metrics:** MRR $32K (+22%), customers 145 (+18), NRR 112%, cash $180K, runway 8 months.

**Highlight:** "Closed a $2,400/mo enterprise deal with [Company] — our first customer over $1K MRR. This validates the enterprise pricing tier we launched in December."

**Challenge:** "Churn ticked up to 4.2% from 3.1%. Root cause: onboarding friction for non-technical users. We are shipping a guided setup wizard by Feb 15."

**Ask:** "Looking for an intro to a Head of Sales candidate with SaaS experience. If anyone in your network is exploring, I would love an introduction."

---

## Anti-Patterns

- **Skipping months when things are bad** — silence signals problems. The worst months need updates the most.
- **All highlights, no challenges** — investors see through spin. Include at least one honest challenge.
- **Changing metrics every month** — pick 3-5 core metrics and report them identically each month for trend visibility.
- **No ask** — investors want to help. If you never ask, they assume you do not need them.
- **Long-winded narratives** — keep it under 500 words. Save the deep dives for board meetings.

---

## Recovery

- **Embarrassing month (revenue down, churn up):** Lead with what happened, what you learned, and what you are doing about it. Investors back founders who respond to adversity.
- **No investors yet (sending to advisors):** Same format works. Advisors appreciate structured updates and clear asks.
- **First update ever:** Send an introductory email explaining you will send monthly updates and what to expect. Include a brief company overview.
- **Behind on updates:** Send a "catch-up" update covering the missed period. Acknowledge the gap. Resume monthly cadence immediately.
