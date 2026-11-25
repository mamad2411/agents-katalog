---
name: cash-collection-chaser
description: |
  Designs multi-stage debtor chase cadences with priority matrices, escalation
  decision trees, and ready-to-send collection emails to accelerate receivables
  and reduce DSO. Use when the user says "chase overdue invoices", "my aged
  debtors are blowing out", "write a collection email", "how do I get this
  client to pay", or asks for a structured follow-up sequence on outstanding
  payments. Recovery from existing debtors — not invoice creation or forecasting.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="cash-collection-chaser")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including known debtor segments, prior chase cadence performance, tone preferences, payment terms, escalation thresholds, and any industry-specific collection constraints (e.g. regulated sectors, public-sector payment cycles).

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Aged receivables data** — share an aged debtor report, invoice list, or describe the outstanding balances (ideally with: debtor name, invoice number, amount, due date, days overdue, prior contact history)
- **Debtor segment** — who are these debtors? (enterprise clients, SMBs, public-sector bodies, consumers, channel partners) — this determines tone, escalation leverage, and legal considerations
- **Payment terms in effect** — standard terms (Net 30/60/90), any bespoke contractual terms, early-payment discounts, or late-payment interest clauses
- **Chase history** — what communications have already been sent? At what intervals? Any responses or disputes raised?
- **Escalation authority** — what actions can the user authorise? (payment plan offers, early-settlement discounts, credit hold, legal referral, third-party collections agency, executive-to-executive escalation)
- **Desired outcome** — pure cash recovery, relationship preservation, formal dispute resolution, or pre-legal posturing?
- **Communication channels available** — email, phone script, letter, SMS, accounts portal message, in-person meeting brief

## Step 3: Do the Work

### 3A: Receivables Triage & Prioritisation

Classify every debtor into a priority matrix using two axes:

| | **High Recovery Probability** | **Low Recovery Probability** |
|---|---|---|
| **High Value (top 20% by £/$ amount)** | **Priority 1** — Immediate senior-touch chase | **Priority 2** — Escalate to legal/credit review |
| **Low Value (remaining 80%)** | **Priority 3** — Automated cadence sequence | **Priority 4** — Batch write-off assessment |

For each debtor, assign:
- **Risk score** (1–5) based on: days overdue, prior payment behaviour from FutureProof context, debtor segment norms, dispute indicators
- **Recommended chase track**: Courtesy → Firm → Escalation → Pre-Legal → Legal

### 3B: Chase Cadence Design

Build a multi-touch chase sequence calibrated to debtor segment and ageing bucket:

1. **0–7 days overdue (Courtesy)** — Friendly payment reminder; assume administrative oversight; reattach invoice; confirm receipt and payment contact details
2. **8–21 days overdue (Firm Reminder)** — Direct statement that payment is overdue; reference original terms and specific invoice(s); request confirmed payment date; introduce late-payment interest clause if contractually available
3. **22–45 days overdue (Escalation)** — Escalate sender authority (Finance Manager / CFO-level); reference prior unanswered communications with dates; formally notify of credit hold / service suspension risk; offer structured payment plan if relationship preservation is prioritised
4. **46–60 days overdue (Pre-Legal Notice)** — Final demand letter; statutory late-payment interest and compensation calculated; explicit deadline (typically 7–14 days); notification that matter will be referred to legal counsel / collections agency
5. **60+ days overdue (Legal / Collections Referral)** — Prepare handover pack for solicitor or collections agency including: full correspondence trail, contract extract, proof of delivery / service completion, interest calculation, debtor contact log

At each stage, draft the **specific communication** (email, letter, or phone script) in the user's preferred tone, incorporating:
- Exact invoice numbers, amounts, and due dates
- Contractual references (payment terms clause, late-interest clause)
- Clear single call-to-action (pay by X date, confirm payment date, call to discuss)
- Professional but progressively firmer tone

### 3C: Dispute & Query Resolution Framework

If the debtor has raised (or is likely to raise) a dispute:

1. **Acknowledge** — confirm receipt of the query within 24 hours; do not suspend the chase clock silently
2. **Isolate** — separate disputed line items from undisputed amounts; chase undisputed portion independently
3. **Investigate** — request specific documentation from the debtor supporting the dispute; set a 5-business-day response window
4. **Resolve or Escalate** — propose credit note for valid disputes; for invalid disputes, provide evidence pack and restate payment expectation with revised deadline
5. **Document** — log dispute rationale, resolution, and any agreed adjustments for audit trail and FutureProof context

### 3D: Cash Collection KPI Dashboard Inputs

Calculate or estimate (from data provided):
- **DSO (Days Sales Outstanding)** — current vs. target
- **Ageing profile** — % of receivables in each bucket (current, 1–30, 31–60, 61–90, 90+)
- **Collection Effectiveness Index (CEI)** — (beginning receivables + credit sales − ending receivables) / (beginning receivables + credit sales − ending current receivables) × 100
- **Dispute rate** — % of invoices with open queries
- **Promise-to-pay conversion rate** — % of chase contacts resulting in confirmed payment dates that are subsequently honoured

Apply any user-specific `instructions` from FutureProof context — e.g. tone guidelines, industry regulatory constraints, known debtor-specific sensitivities, preferred escalation paths.

## Step 4: Deliver Output

Produce a structured **Cash Collection Action Pack** containing:

### Document 1: Debtor Priority Matrix
- Ranked list of all debtors with: priority tier, risk score, recommended chase track, assigned chase stage, next action, next action date, responsible owner

### Document 2: Chase Communications Suite
- **Per debtor (Priority 1 & 2)**: Individually tailored chase communication for their current stage — ready to send
- **Per chase stage (Priority 3)**: Templated communications for each cadence step, with merge fields for debtor name, invoice details, amounts, dates

### Document 3: Escalation Decision Tree
- Visual or structured decision logic: when to escalate, when to offer a payment plan, when to apply credit hold, when to refer to legal — with specific thresholds (days, amounts, number of unanswered contacts)

### Document 4: Cash Collection Dashboard Summary
- Current DSO, CEI, ageing profile breakdown, total overdue amount, estimated recoverable amount by priority tier, dispute rate, and recommended target metrics for next 30/60/90 days

### Document 5: Dispute Log & Resolution Tracker (if applicable)
- Structured table: debtor, invoice, dispute description, date raised, undisputed amount isolated, investigation status, resolution, adjusted amount

All documents formatted for immediate use — specify recipients (e.g. "Finance Manager sends Priority 1 emails; AR Clerk processes Priority 3 batch").

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Propose Experiments

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


```
FutureProof:save_experiment(skill="cash-collection-chaser", experiment={
  hypothesis: "Sending the first chase communication on day 3 post-due-date (vs. day 7) reduces average collection time by shortening debtor response lag in the courtesy window",
  variants: ["control: first chase at day 7 overdue", "variant: first chase at day 3 overdue"],
  measurement: "Average days-to-payment from due date for invoices entering the chase cadence over the next 60-day period",
  expected_impact: "4–6 day reduction in average collection cycle; 8–12% improvement in CEI"
})
```

```
FutureProof:save_experiment(skill="cash-collection-chaser", experiment={
  hypothesis: "Including a direct-pay link (Stripe/GoCardless/bank transfer deep link) in chase emails reduces friction and increases payment conversion within 48 hours of communication",
  variants: ["control: standard bank details in email body", "variant: embedded one-click payment link"],
  measurement: "% of invoices paid within 48 hours of chase email receipt",
  expected_impact: "20–25% increase in 48-hour payment conversion rate"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="cash-collection-chaser",
  query="Best-practice B2B cash collection cadence structures, optimal chase timing intervals, and debtor communication psychology — including 2024 benchmarks for DSO by industry and effectiveness of automated vs. personalised collection outreach",
  reason="Ensure chase cadence design reflects current debtor behaviour patterns, payment platform capabilities, and regulatory updates (e.g. Late Payment of Commercial Debts Act, prompt payment codes) to maximise recovery rates while maintaining commercial relationships"
)
```

## Step 7: Save Session

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:save_session(skill="cash-collection-chaser", session={
  summary: "...[fact-dense: ICA, format, tone, constraints, what was delivered, amends made. End with: Next session defaults: ...]",
  outcomes: [
    "Format: [format chosen]",
    "Tone: [tone and constraints]",
    "ICA: [ICA description]",
    "Deliverable: [what was produced]"
  ],
  metadata: {}
})
```