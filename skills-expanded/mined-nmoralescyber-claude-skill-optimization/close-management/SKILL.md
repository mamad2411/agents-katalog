---
name: close-management
description: Orchestrates the month-end / quarter-end financial close — sequences tasks by dependency, tracks owners and blockers, and enforces the close-by-day-N calendar. Use this skill whenever the user says close the books, run the month-end close, what's the close calendar, where are we on close, what's blocking close, status of close, build a close checklist, accelerate the close, close retrospective, soft close, hard close, lock the period, close-by-B+5 / B+10 / B+3, or describes orchestrating a recurring period-end close cycle. This is the orchestrator — it does NOT do the actual work. It defers to finance:reconciliation for account tie-outs, finance:journal-entry for booking adjustments, finance:financial-statements for producing the P&L/BS/CF, finance:variance-analysis for explaining flux, finance:audit-support for SOX testing, and data:build-dashboard for KPI/SaaS-metric views. Tuned for a Puerto Rico-domiciled cybersecurity SaaS startup (Hacienda, Act 60/20/22, IVU, patente municipal, bilingual filings, multi-year SaaS / milestone pen-test / MSSP recurring revenue rec). Defining characteristic: "sequence + track + escalate the close cycle; delegate every line of work to a sibling skill."
---

# Close Management

Orchestrator for month-end / quarter-end close. Sequences work, tracks owners, surfaces blockers, escalates slips. Does not perform reconciliations, post entries, build statements, or write variance commentary itself.

> Disclaimer: this skill assists with close orchestration but does not provide tax, accounting, or financial advice. All close output must be reviewed by a qualified Puerto Rico CPA before filing or distribution.

## When to use vs. when to delegate

| Use this skill when... | Delegate to... |
|---|---|
| Planning the close calendar / setting B+N target | (this skill) |
| Tracking task status, owners, blockers, slips | (this skill) |
| Daily close standup / status note | (this skill) |
| Running the close retrospective | (this skill) |
| Tying GL to subledger / bank / third-party | `finance:reconciliation` |
| Booking accruals, depreciation, deferred revenue, prepaid amort | `finance:journal-entry` |
| Producing the P&L / BS / CF / footnotes | `finance:financial-statements` |
| Explaining the WHY behind a flux | `finance:variance-analysis` |
| SOX control testing during close | `finance:audit-support` |
| Operational / SaaS KPI views (ARR, NRR, CAC) outside GAAP | `data:build-dashboard` |
| Investigating a single anomalous transaction | `data:analyze` |

If a request is "close the books AND tell me why margin moved," run close-management to orchestrate, then chain `finance:variance-analysis` for the WHY.

## The close cycle (canonical chain)

```
close-management   ─orchestrates→
  └─ finance:reconciliation   (per account: bank, AR, AP, intercompany, FX)
      └─ finance:journal-entry   (book any adjustments found)
          └─ finance:financial-statements   (produce P&L / BS / CF)
              └─ finance:variance-analysis   (explain flux to leadership)
                  └─ finance:audit-support   (if SOX-relevant deficiency surfaces)
```

Every close-management task that has actual debits/credits, tie-outs, or output documents must name the responsible sibling skill in the task line.

## Calendar discipline — pick a target B+N up front

| Target | When it fits | Prerequisites |
|---|---|---|
| **B+3** | High-automation, continuous-rec org | Auto recurring JEs, real-time subledger feed, pre-close cut-offs done |
| **B+5** | Default for a cybersec SaaS startup | Standard recurring JEs scripted; Stripe + payroll + bank feeds tied weekly |
| **B+10** | Manual / first-year / acquisition month | Manual reconciliations OK; build automation backlog from retro |

State the target on Day -2. Every task carries an absolute due day (e.g. "Due B+2 EOD"). A task missing its day is a defect.

### B+N picker decision tree

```
Is this an audited year-end or a quarter that feeds a board package?
  YES → add 2 days to your normal target (year-end / quarterly close > monthly)
  NO  → continue
Are recurring JEs (depreciation, prepaid amort, deferred rev) automated?
  NO  → B+10 minimum
  YES → continue
Are bank, Stripe, payroll subledgers reconciled WEEKLY (not just at close)?
  NO  → B+10
  YES → continue
Are revenue rec rules for SaaS, pen-test, MSSP documented and applied without judgment-calls each month?
  NO  → B+10 (then build the rev-rec policy, then re-target)
  YES → continue
Are PR-specific items (Hacienda WH, IVU, patente, Act 60) accrued continuously, not month-end-only?
  NO  → B+10 → improve, then B+5
  YES → B+5 default
Do you have automated IC matching, real-time subledger feeds, and a controller dedicated to close?
  YES → B+3 stretch target
```

### Quarter-end / year-end overlay (add to monthly close)

| Add at quarter-end (Q1/Q2/Q3) | Add at Q4 / year-end |
|---|---|
| 480.6 series withholding statements | All quarter-end items + |
| OCIF quarterly filing (if regulated) | 1099 / 480.6 annual generation |
| Patente municipal true-up | Annual Act 60 grantee compliance report |
| SaaS metrics quarterly board pack | DACO annual filings if applicable |
| ARR / NRR quarter cohort refresh | External audit prep handoff (`finance:audit-support`) |
| Equity quarterly (409A trigger check) | 1120 / Hacienda 480 corporate return prep |
|  | Cyber-insurance renewal quote cycle (often year-end aligned) |

Add 2-5 days to the monthly B+N target for quarters; add 5-15 days for year-end.

### Holiday / PR calendar discipline

PR has more federal-PLUS-commonwealth holidays than most US-mainland startups expect (Three Kings Day, Constitution Day, Discovery, etc.). Publish the close calendar against the actual PR business-day calendar — "B+5" means 5 PR business days, NOT calendar days. If close month contains a PR holiday, target shifts +1 automatically.

## Pre-close (B-2 → B-1)

- [ ] Publish close calendar with B+N target, owners, deadlines (this skill)
- [ ] Confirm cut-off rules with AP, AR, payroll, treasury, Stripe, MSSP billing
- [ ] Verify ERP / Stripe / Gusto (or local PR payroll) / bank feeds are healthy
- [ ] Pre-rec bank, Stripe, AR through B-3 (delegate: `finance:reconciliation`)
- [ ] Open-PO sweep for accrual estimates (delegate: `finance:journal-entry` for the entries themselves)
- [ ] Confirm PR-specific obligations not yet booked: IVU collected vs. remitted, patente municipal accrual, Hacienda withholding (services 7%, professional 10%, etc.)
- [ ] If month is also quarter-end: flag Act 60 grantee compliance items, 480-series withholding accruals, FOMENTO-related deferrals

## Close days — task list with owners and delegations

Every line: `[ ] Task — Owner (role) — Due B+N — Delegate to: skill`

### B+1 — Subledger close + Level-1 entries (no upstream dependencies)

- [ ] Confirm sub-ledger period-end processing complete — Controller — B+1 AM — (this skill)
- [ ] Cash receipts/disbursements posted through month-end — Staff acct — B+1 AM — `finance:journal-entry`
- [ ] AP accrual (goods/services received not invoiced) — AP lead — B+1 EOD — `finance:journal-entry`
- [ ] Payroll entry + period-straddle accrual (incl. PR SUTA, FUTA, Hacienda WH, ASUME, SINOT, choferil) — Payroll — B+1 EOD — `finance:journal-entry`
- [ ] Fixed asset depreciation run — Staff acct — B+1 EOD — `finance:journal-entry`
- [ ] Prepaid amort (cyber-insurance premium, SOC 2 audit prepay, GRC tooling annual prepays, pen-test retainers) — Staff acct — B+1 EOD — `finance:journal-entry`
- [ ] Intercompany transactions posted both sides — Staff acct — B+1 EOD — `finance:journal-entry`
- [ ] Stripe payout reconciliation (gross → net of fees, refunds, chargebacks) — AR lead — B+1 EOD — `finance:reconciliation`

### B+2 — Revenue rec + Level-2 reconciliations

- [ ] Revenue rec — multi-year SaaS contracts (ASC 606 ratable, deferred rev waterfall) — Revenue acct — B+2 AM — `finance:journal-entry`
- [ ] Revenue rec — milestone-based pen-test fees (% complete or POB delivery) — Revenue acct — B+2 AM — `finance:journal-entry`
- [ ] Revenue rec — MSSP recurring services (monitoring, IR retainer) — Revenue acct — B+2 AM — `finance:journal-entry`
- [ ] Bank reconciliation (operating, payroll, FX, PR-domiciled accounts) — Treasury — B+2 — `finance:reconciliation`
- [ ] AR subledger to GL — AR lead — B+2 — `finance:reconciliation`
- [ ] AP subledger to GL — AP lead — B+2 — `finance:reconciliation`
- [ ] FX revaluation on USD-denominated balances held by non-US entities (if applicable) — Staff acct — B+2 — `finance:journal-entry`

### B+3 — Balance sheet recs + adjusting entries

- [ ] All BS account reconciliations complete — Controller — B+3 — `finance:reconciliation`
- [ ] Adjusting JEs from rec exceptions posted — Staff acct — B+3 — `finance:journal-entry`
- [ ] Intercompany rec + eliminations — Staff acct — B+3 — `finance:reconciliation`
- [ ] Preliminary trial balance issued — Controller — B+3 EOD — `finance:financial-statements`
- [ ] Preliminary flux scan (anything > $X or > Y%) — Controller — B+3 EOD — `finance:variance-analysis`

### B+4 — Tax + draft statements + management review

- [ ] Federal income tax provision — Tax — B+4 AM — `finance:journal-entry`
- [ ] PR Hacienda income tax provision (regular + Act 60 4%/preferential where applicable) — Tax — B+4 AM — `finance:journal-entry`
- [ ] IVU sales tax accrual / true-up (state 10.5% + municipal 1%) — Tax — B+4 AM — `finance:journal-entry`
- [ ] Patente municipal accrual (volume of business tax) — Tax — B+4 AM — `finance:journal-entry`
- [ ] Equity roll-forward (founder stock, option grants, 83(b) tracking) — Controller — B+4 — `finance:journal-entry`
- [ ] Draft P&L / BS / CF — Controller — B+4 EOD — `finance:financial-statements`
- [ ] Detailed flux analysis with driver decomposition — FP&A — B+4 EOD — `finance:variance-analysis`
- [ ] Management review (founder + fractional CFO) — Founder + CFO — B+4 EOD — (this skill: capture decisions)

### B+5 — Hard close + distribution

- [ ] Final adjustments from review posted — Staff acct — B+5 AM — `finance:journal-entry`
- [ ] Hard close: lock period in ERP — Controller — B+5 AM — (this skill: enforce lock)
- [ ] Reporting package: English (board/investors) + Spanish (where required for PR filings, e.g. Hacienda, OCIF, DTRH) — Controller — B+5 — `finance:financial-statements`
- [ ] SaaS metrics view (ARR, NRR, gross retention, CAC, payback, magic number) — FP&A — B+5 — `data:build-dashboard`
- [ ] Forecast / re-projection refresh — FP&A — B+5 — (chain to `finance:variance-analysis` if flux drives plan revision)
- [ ] Close retrospective — Controller — B+5 EOD — (this skill)

## Status tracking — the daily standup artifact

Produce this every close day at the same time (e.g. 9 AM AST). Keep it under one screen.

```markdown
# Close Status — [Period] — Day B+[N]   Target: B+[T]

## RAG
- Overall: GREEN / YELLOW / RED
- Slip risk to B+[T]: [hours, days, none]

## Completed since last standup
- [Task] — [Owner]

## In flight
- [Task] — [Owner] — [% done] — [ETA]

## Blocked (escalation needed)
- [Task] — [Owner] — Blocked by: [what + who] — Asked since: [time] — Escalate to: [name]

## At risk (will miss its B+N if nothing changes)
- [Task] — [Owner] — Original due: B+[N] — Forecast: B+[N+x] — Mitigation: [what we'll do]

## Decisions needed today
- [Question] — Decider: [name] — Needed by: [time]
```

## Blocker SLA table — escalate on the clock, not on vibes

| Blocker age (business hours) | Action | Who acts |
|---|---|---|
| 0 – 2 h | Owner pings blocker-owner directly | Task owner |
| 2 – 4 h | Add to standup, ping blocker-owner's manager | Task owner |
| 4 – 8 h | Auto-escalate to controller; controller intervenes | Controller |
| 8 – 24 h | Founder is paged (Slack DM + SMS); blocker becomes a calendar item | Controller → Founder |
| > 24 h | Close-date slip risk goes RAG=RED; explicit decision: slip the close OR move task to next period | Founder |

A blocker entry without a `blocked_since` timestamp is a defect. Fix on the spot.

## Late-task runbook (when a task is going to miss its B+N)

1. **Detect** — owner flags "At Risk" in standup the moment forecast > original B+N (do not wait for the actual miss).
2. **Triage** — is this task on the critical path? (See critical-path section.)
   - **On critical path** → controller convenes a 15-min huddle within 1 hour. Either (a) re-assign with help, (b) compress downstream, or (c) approve a slip.
   - **Off critical path** → re-baseline due date in the task list; note in standup; no huddle needed.
3. **Document** — `slip_reason`, `mitigation`, `new_due`, `decided_by` written to the standup artifact same day.
4. **Retro signal** — every approved slip becomes a retrospective topic. Repeated slips on the same task → automation candidate.

## Owner attribution rules

- Every task names exactly one human owner (not a team, not "Finance"). A team can support, but accountability is singular.
- Owner is named at calendar-publish time (B-2). Reassignment after that requires controller note in the standup.
- If owner is OOO during their task's window, a backup is named in the calendar — backup is named WITH the original (e.g. "Owner: Maria / Backup: Luis"), not improvised at the moment.
- "Controller" and "Founder" are valid owner labels for sign-off / decision tasks. Everything else gets a person's name.

## Status definitions

- **Not Started** — waiting on a dependency; dependency name MUST be cited
- **In Progress** — actively being worked; has an ETA
- **Complete** — done AND reviewed by a second person
- **Blocked** — cite the blocker, the owner of the blocker, and time-since-asked
- **At Risk** — will miss its B+N day; mitigation plan required

A task with no owner, no due day, or status "In Progress" with no ETA is a defect — fix on the spot.

## Dependency map (gating logic)

**Gating rule (enforce at the standup):** A task in Level N+1 cannot start until ALL Level N tasks are GREEN (Complete + reviewed). The only exception is a controller-approved "early start" written into the standup artifact with explicit risk note.

**Within a level, parallelize aggressively** — independent reconciliations, independent JE families, and independent revenue streams (SaaS / pen-test / MSSP) all run in parallel. Sequencing is between levels, not within.

```
LEVEL 1  — start B+1, no upstream
  cash entries, payroll, depreciation, prepaid amort, AP accruals, IC posting, Stripe payout

LEVEL 2  — needs Level 1
  bank rec, AR/AP subledger rec, revenue rec (SaaS/pen-test/MSSP), FX reval

LEVEL 3  — needs Level 2
  all BS recs, IC rec + eliminations, adjusting JEs, preliminary TB, preliminary flux

LEVEL 4  — needs Level 3
  Federal + PR tax provisions, IVU/patente accruals, equity roll-fwd, draft statements, detailed flux

LEVEL 5  — needs Level 4
  management review, final adjustments, hard close / period lock, reporting package (EN + ES),
  SaaS dashboard refresh, forecast update, retrospective
```

## Critical path

`Cash + AP/AR + revenue rec  →  subledger recs  →  BS recs  →  tax provision (incl. PR layer)  →  draft statements  →  management review  →  hard close`

Anything off the critical path can slip a day without slipping the close. Anything on it cannot. Owners of critical-path tasks get named in every standup until done.

### Critical-path enforcement table

| If a critical-path task is... | Then... |
|---|---|
| On track | Standard standup mention |
| At risk | Controller huddle within 1 hour; mitigation written same standup |
| Late by < 4h | Compress downstream (parallelize, cut a non-critical task) |
| Late by 4-8h | Founder informed; close date confirmed or revised |
| Late by > 8h | Close date slips by 1 day OR task moves to next period (founder decides) |
| Late and recurring (3+ closes) | Automation candidate — added to retro queue with named DRI |

## Puerto Rico-specific overlays (do not forget)

- **Hacienda withholding** — services 7%, professional services 10%, rent 10% (verify current rates); accrue if not yet remitted.
- **IVU** — 10.5% state + 1% municipal on taxable sales; B2B SaaS may be exempt under specific exemption certificates — confirm certificate is on file.
- **Patente municipal** — volume-of-business tax owed to municipality of operations; accrue ratably.
- **Act 60 (formerly Acts 20/22)** — if grantee, 4% corporate tax on eligible export-services income. Track grantee compliance: PR-sourced employee count, charitable donation requirement, annual report. Surface deficiencies during close.
- **DTRH / SINOT / ASUME / choferil / chauffeur insurance** — payroll-side employer obligations; reconcile remittances during payroll close.
- **Bilingual filings** — DACO consumer, OCIF financial regulator, OCS (insurance), and certain Hacienda forms require Spanish; reporting package must include Spanish version when filing-bound.
- **Quarter-end add-ons** — 480.6 series withholding statements, OCIF quarterly (if regulated), municipality patente true-ups.

## Cybersecurity / SaaS revenue-rec gotchas

- **Multi-year SaaS** — recognize ratably over service period; deferred revenue waterfall must roll forward each close. Watch for upfront payment vs. annual billing — they hit cash and AR differently but same revenue rec.
- **Milestone pen-test** — POB by deliverable (kickoff, fieldwork, draft report, final report); recognize per ASC 606 over time or point-in-time depending on contract terms. Document the judgment.
- **MSSP recurring services** (24x7 monitoring, IR retainer, vCISO) — ratable; if usage-based component (e.g., per-endpoint), monthly true-up needed.
- **Setup / onboarding fees** — generally combined with the SaaS POB and recognized ratably unless they have standalone value.
- **Cyber-insurance premium** — prepaid asset, amortize ratably; large premium increases need a flux note.
- **Compliance program spend** — SOC 2 audit fees, pen-test fees as a customer (not provider), GRC tool subscriptions; classify consistently as G&A vs. R&D vs. COGS based on the policy and stick with it.

If any of these is unfamiliar to the close team, do NOT improvise — chain to `finance:journal-entry` and let that skill handle the entry, citing the contract.

## Cut-off rules (enforce, don't apologize)

| Cut-off | Time |
|---|---|
| Vendor invoice receipt for current period | B-1 EOD |
| Expense reports for current period | B-1 EOD |
| AP accrual estimates from department leads | B+1 noon AST |
| Stripe payout window for the month | calendar month boundary in UTC |
| Bank statement availability | B+1 AM |
| Last journal entry before soft close | B+4 EOD |
| Last journal entry before hard close | B+5 AM |

A late submission does not move the close date. It either (a) goes into next period or (b) requires founder sign-off to delay the close.

## Close metrics — track every cycle

| Metric | Target |
|---|---|
| Days to hard close | trend toward stated B+N |
| # late tasks | 0 |
| # blockers > 4h unresolved | 0 |
| # post-soft-close adjusting entries | trend down |
| # rec exceptions | trend down |
| # restatements after close | 0 |
| % critical-path tasks on-time | 100% |

## Close retrospective (always run)

1. What slipped on the critical path and why?
2. Which sibling skill was unclear about ownership? (improve the handoff)
3. Which PR-specific item bit us this month?
4. What recurring JE can we automate before next close?
5. Which rec can move to continuous (not month-end)?
6. Did the SaaS dashboard answer the questions we got from leadership? If not, refine in `data:build-dashboard`.

## Anti-patterns

- **Doing the work inside this skill** — if it's a JE, a rec, a statement, or a variance write-up, hand off.
- **Tasks without owner or due day** — defect, fix on the spot.
- **Silent slips** — a slip not raised in the standup is a process failure.
- **Generic 5-day calendar with no PR layer** — Hacienda / IVU / patente / Act 60 must appear by name.
- **English-only reporting package when filing-bound** — Spanish version required for some PR filings.
- **Booking pen-test or MSSP revenue without checking the POB** — recognize per contract, not per invoice.
- **Treating cyber-insurance renewal as expense in month of payment** — it's prepaid, amortize.
- **Closing without a SaaS metrics view** — GAAP statements alone don't tell the founder what they need (ARR, NRR, CAC, payback, magic number).

## Output of a close-management run

1. The close calendar (target B+N, owners, due days, delegations)
2. The dependency-gated task list
3. The daily standup artifact (per day)
4. The blocker / escalation log
5. The close metrics scorecard
6. The retrospective notes
7. Suggested chain: at hard close, chain `finance:financial-statements` for the package, `finance:variance-analysis` for the flux narrative, `data:build-dashboard` for the SaaS-metric view, and `finance:audit-support` if any SOX-flagged deficiency surfaced.
