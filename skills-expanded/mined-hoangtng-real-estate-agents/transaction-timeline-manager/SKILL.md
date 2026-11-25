---
name: transaction-timeline-manager
description: Generate a complete contract-to-close transaction timeline with every milestone, deadline, owner, and status tracker for any real estate transaction. Use this skill whenever a user asks for a transaction checklist, closing timeline, escrow timeline, contingency tracker, or "what happens after an offer is accepted." Also use when a deal is already open and the user needs to know what's due next, who owns it, and what's at risk. Produces a fully dated milestone table, vendor contact sheet, and deal-at-risk alert if issues are flagged.
---

# Transaction Timeline Manager

Builds a complete, dated transaction timeline for any real estate deal — from accepted offer through recording. This is Chen's work: every deadline tracked, every owner named, nothing left to memory.

## What You Need From the User

- **Accepted date** (or today's date if not yet accepted)
- **Target close date** (or number of days: 21 / 30 / 45 / 60)
- **Transaction type:** standard purchase / cash / new construction / short sale / REO
- **Contingency periods:** inspection days, loan days, appraisal contingency
- **Key parties:** buyer agent, listing agent, escrow/title company, lender (if known)
- **State:** some timelines are state-specific (e.g. attorney states vs. escrow states)

If close date is unknown, default to 30-day close and note the assumption.

## Output Format

### Part 1: Full Timeline

```markdown
## Transaction Timeline
**Property:** [Address]
**Accepted Date:** [Date] | **Target Close:** [Date] ([X] days)
**Buyer Agent:** [Name] | **Listing Agent:** [Name]
**Escrow/Title:** [Company] | **Lender:** [Name / Company]

---

### MILESTONES

| Day | Due Date | Task | Owner | ⚠️ | Status |
|-----|----------|------|-------|----|--------|
| 0 | [date] | Executed contract to escrow/title | TC | | ⬜ |
| 0 | [date] | EMD wire instructions sent to buyer | TC | | ⬜ |
| 1 | [date] | Earnest money deposited | Buyer | ⚠️ | ⬜ |
| 1 | [date] | Open escrow confirmation received | Escrow | | ⬜ |
| 1 | [date] | Disclosure package sent to buyer | Listing Agent | | ⬜ |
| 2 | [date] | Inspection ordered | Buyer Agent | | ⬜ |
| 3 | [date] | Disclosures signed and returned | Buyer | | ⬜ |
| 3 | [date] | HOA docs ordered (if applicable) | TC | | ⬜ |
| 5 | [date] | Loan application confirmed with lender | TC | | ⬜ |
| [X] | [date] | **INSPECTION DEADLINE** | Buyer | 🚨 | ⬜ |
| [X+3] | [date] | Seller inspection response deadline | Seller | ⚠️ | ⬜ |
| [X+3] | [date] | Repair agreement signed (if applicable) | Both | | ⬜ |
| [X+5] | [date] | Appraisal ordered confirmed | Lender | | ⬜ |
| [X+10] | [date] | Appraisal completed | Appraiser | | ⬜ |
| [Y] | [date] | **APPRAISAL CONTINGENCY DEADLINE** | Buyer | 🚨 | ⬜ |
| [Z] | [date] | **LOAN CONTINGENCY DEADLINE** | Buyer | 🚨 | ⬜ |
| [Z+3] | [date] | Final loan approval (clear to close) | Lender | ⚠️ | ⬜ |
| [Z+5] | [date] | Closing disclosure issued (3-day rule) | Lender | ⚠️ | ⬜ |
| [Close-2] | [date] | Final walkthrough scheduled | Buyer Agent | | ⬜ |
| [Close-1] | [date] | Buyer funds wired to escrow | Buyer | 🚨 | ⬜ |
| [Close-1] | [date] | Loan docs sent to escrow | Lender | ⚠️ | ⬜ |
| [Close] | [date] | **CLOSE OF ESCROW / RECORDING** 🎉 | Escrow | | ⬜ |
| [Close] | [date] | Keys released to buyer | Listing Agent | | ⬜ |

**Legend:** 🚨 = Hard deadline (missing = deal at risk) | ⚠️ = Time-sensitive | ⬜ = Incomplete | ✅ = Complete
```

### Part 2: Vendor Contact Sheet

```markdown
## Vendor Contact Sheet: [Address]

| Role | Name | Company | Phone | Email |
|------|------|---------|-------|-------|
| Buyer's Agent | [Name] | [Agency] | [Phone] | [Email] |
| Listing Agent | [Name] | [Agency] | [Phone] | [Email] |
| Escrow Officer | [Name] | [Title Co.] | [Phone] | [Email] |
| Loan Officer | [Name] | [Lender] | [Phone] | [Email] |
| Loan Processor | [Name] | [Lender] | [Phone] | [Email] |
| Inspector | [Name] | [Company] | [Phone] | [Email] |
| Appraiser | [Name] | [Company] | [Phone] | [Email] |
| HOA Manager | [Name] | [HOA] | [Phone] | [Email] |
```

### Part 3: Deal-at-Risk Alert (only if user flags a problem)

If the user describes a delay, missed deadline, or issue, generate this automatically:

```markdown
## 🚨 DEAL AT RISK ALERT
**Property:** [Address]
**Risk Type:** [ ] Financing  [ ] Appraisal  [ ] Inspection  [ ] Title  [ ] Buyer hesitation
**Risk Level:** [ ] Watch  [ ] Moderate  [ ] Critical
**Date Identified:** [Date]
**Deadline Affected:** [Date]

**What happened:**
[Clear, factual description]

**Immediate actions taken:**
1. [Action — completed at time]
2. [Action — in progress]

**Notified:**
- [ ] Listing Agent — [time]
- [ ] Buyer's Agent — [time]  
- [ ] Managing Broker (if Critical) — [time]

**Resolution options:**
- Option A: [description + timeline]
- Option B: [description + timeline]

**Recommended:** Option [X] — [why]
**Next update by:** [time/date]
```

## Behavior Notes

- Always calculate and print actual calendar dates, not just day numbers. If the accepted date is known, compute everything forward.
- 🚨 Milestones are hard deadlines — flag them clearly. Missing these can cost the buyer their deposit or kill the deal.
- If the user says "we're at day 10 and the lender hasn't ordered the appraisal yet" — immediately assess whether a contingency deadline is at risk and generate the deal-at-risk alert.
- For cash transactions: remove financing and appraisal milestones, shorten the timeline to 14–21 days.
- For attorney states (NY, NJ, MA, CT, etc.): add attorney review period (typically 3–5 business days from acceptance) as the first milestone.
- Always note: "Reminder deadlines should be set 48 hours before every 🚨 milestone."
