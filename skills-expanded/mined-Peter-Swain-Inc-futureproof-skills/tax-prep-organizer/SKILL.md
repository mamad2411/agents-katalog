---
name: tax-prep-organizer
description: |
  Organizes tax-season readiness with a tiered document checklist, standard-vs-
  itemized deduction optimization, audit-flag scan, and accountant handoff memo.
  Use when the user says "help me get ready for tax season", "organize my tax
  documents", "what deductions am I missing", "prep this for my CPA", or needs
  a structured filing package for 1040, Schedule C, S-Corp, or K-1 returns.
  Compliance prep and document gathering — not bookkeeping or P&L analysis.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="tax-prep-organiser")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including prior-year filing history, known income streams, entity structures, and previously identified deduction categories.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Filing entity**: Individual (1040), sole proprietor (Schedule C), partnership (1065), S-Corp (1120-S), C-Corp (1120), or trust/estate (1041)?
- **Tax year**: Which fiscal or calendar year are we organising for?
- **Income streams**: List all sources — W-2 employment, 1099-NEC/MISC contractor income, rental (Schedule E), investment/capital gains, K-1 pass-throughs, foreign income, other
- **Major life events this year**: Marriage, divorce, home purchase/sale, birth of dependent, business formation/dissolution, relocation, inheritance, retirement account distributions
- **Current state of documents**: Scale of 1–5 (1 = scattered across email/shoebox, 5 = largely organised and digitised)
- **Filing objective**: Maximum refund optimisation, audit-defensible conservative filing, or estimated tax planning for next year?
- **Preparer workflow**: Self-filing (TurboTax, FreeTaxUSA, etc.), CPA/EA-prepared, or hybrid (organise for handoff to professional)?

## Step 3: Do the Work — Tax Document Inventory & Gap Analysis

Construct a comprehensive **Document Collection Matrix** using a four-phase methodology modelled on Big Four tax engagement workflows:

### Phase 1: Income Verification Mapping

For each identified income stream, map the required source documents:

| Income Type | Required Document | IRS Matching Priority | Status |
|---|---|---|---|
| Employment | W-2 (each employer) | **Critical** — IRS receives copy | ☐ |
| Freelance/Contract | 1099-NEC / 1099-MISC (each payer) | **Critical** — IRS receives copy | ☐ |
| Banking Interest | 1099-INT (each institution) | **Critical** — IRS receives copy | ☐ |
| Dividends | 1099-DIV (each brokerage) | **Critical** — IRS receives copy | ☐ |
| Brokerage Sales | 1099-B / Consolidated 1099 | **Critical** — IRS receives copy | ☐ |
| Retirement Distributions | 1099-R | **Critical** — IRS receives copy | ☐ |
| Rental Income | Tenant payment records, 1099-MISC if applicable | Medium | ☐ |
| K-1 Pass-throughs | Schedule K-1 (each entity) | **Critical** — IRS receives copy | ☐ |
| Crypto/Digital Assets | 1099-DA / exchange transaction history | High — new reporting requirements | ☐ |
| Foreign Income | Foreign employer statements, Form 1116 support | High — FBAR/FATCA triggers | ☐ |

Flag any income streams where the user has **not** yet received expected documents and set follow-up deadlines (most 1099s due by January 31; K-1s often delayed until March 15+).

### Phase 2: Deduction & Credit Eligibility Audit

Systematically evaluate each applicable deduction category using a **Standard vs. Itemised Decision Tree**:

**Itemised Deduction Categories (Schedule A):**
1. **State & Local Taxes (SALT)** — property tax + state income/sales tax (capped at $10,000; flag SALT cap impact)
2. **Mortgage Interest** — Form 1098; identify acquisition debt vs. HELOC; $750K limitation analysis
3. **Charitable Contributions** — cash (bank statements, receipts), non-cash (Form 8283 if >$500), QCDs if age 70½+
4. **Medical & Dental** — aggregate against 7.5% AGI floor; flag HSA contributions (Form 5498-SA)
5. **Casualty & Theft Losses** — federally declared disaster areas only

**Above-the-Line Deductions & Adjustments:**
1. Traditional IRA contributions (Form 5498; MAGI phase-out analysis)
2. Student loan interest (Form 1098-E; $2,500 cap)
3. HSA contributions (Form 5498-SA; family vs. individual limit)
4. Self-employment tax deduction (50% of SE tax)
5. Qualified Business Income (QBI) deduction — Section 199A; 20% pass-through; W-2 wage and UBIA limitations
6. Educator expenses ($300 per qualifying educator)
7. Home office deduction — simplified ($5/sq ft, max 300 sq ft) vs. actual expense method

**Credit Eligibility Screen:**
1. Child Tax Credit / Other Dependent Credit — dependent SSN/ITIN verification
2. Child & Dependent Care Credit (Form 2441) — provider EIN required
3. Earned Income Tax Credit — income thresholds, investment income test
4. Education Credits — AOTC vs. Lifetime Learning (Form 1098-T); MAGI phase-outs
5. Energy Credits — Residential Clean Energy (Form 5695); EV credit (Form 8936); manufacturer cap status
6. Estimated Tax Payments — verify Form 1040-ES records against IRS account transcripts

### Phase 3: Entity-Specific Compliance Requirements

For business filers, add:
- **Reasonable compensation analysis** (S-Corp owners — flag if officer compensation appears below market)
- **Depreciation schedule review** — Section 179 vs. bonus depreciation elections; asset disposition (Form 4797)
- **Estimated tax penalty exposure** — safe harbour analysis (110% prior-year tax if AGI >$150K)
- **Required estimated payments for next year** — compute quarterly amounts
- **State nexus review** — multi-state filing obligations from remote work or out-of-state revenue
- **Beneficial Ownership Information (BOI)** reporting reminder if applicable (FinCEN)

### Phase 4: Risk & Audit Flag Scan

Review the emerging return profile for known IRS audit triggers:
1. **Schedule C losses** reported for 3+ consecutive years (hobby loss rule — IRC §183)
2. **Home office deduction** on Schedule C with high ratio to total expenses
3. **Unreported income** — cross-reference bank deposits to declared income streams
4. **Large charitable deductions** disproportionate to AGI (>3% threshold flag)
5. **Round number reporting** across multiple line items
6. **Cryptocurrency transactions** without Form 8949 reporting
7. **Foreign account thresholds** — FBAR ($10K aggregate) and FATCA (Form 8938) analysis
8. **ERC/pandemic credit clawback exposure** if previously claimed

Apply any user-specific `instructions` from FutureProof context — e.g., prior-year carryforwards (capital losses, NOLs, charitable contribution carryovers), estimated payment history, or accountant preferences for document formatting.

## Step 4: Deliver Output

Produce a structured **Tax Preparation Package** with five named deliverables:

### Deliverable 1: Document Collection Checklist
A prioritised, tick-box checklist of every required document organised by:
- **Tier 1 — IRS-matched documents** (must collect before filing; risk of automated notice if omitted)
- **Tier 2 — Deduction/credit substantiation** (high-value items)
- **Tier 3 — Supporting records** (retain for audit defence, not required for filing)

Include expected source, typical arrival date, and action if missing (e.g., "Request duplicate W-2 from employer payroll by February 14; if unavailable, file Form 4852 as substitute").

### Deliverable 2: Deduction Optimisation Memo
A one-page summary containing:
- **Standard vs. Itemised recommendation** with dollar comparison
- **Top 5 deductions/credits by dollar impact** — ranked, with required substantiation for each
- **Missed opportunity flags** — deductions or credits the user may be eligible for but has not mentioned (e.g., "You reported a home office but did not mention internet/utilities allocation")
- **Carryforward items** from prior years surfaced from FutureProof context

### Deliverable 3: Filing Timeline & Milestone Plan
A week-by-week action plan from current date through filing deadline:
- Key document arrival windows
- Preparation milestones
- Extension filing decision point (Form 4868) if documents are delayed (especially K-1s)
- Estimated tax payment deadlines for next year (April 15, June 15, September 15, January 15)

### Deliverable 4: Accountant Handoff Summary *(if applicable)*
A one-page cover memo formatted for CPA/EA handoff:
- Client name, filing status, entity type
- Summary of income streams and estimated AGI range
- Open questions / areas requiring professional judgement
- List of enclosed documents with cross-reference to checklist

### Deliverable 5: Year-Over-Year Comparison Notes
If FutureProof context contains prior-year session data:
- Flag material changes in income, deductions, or credits vs. prior year
- Highlight new compliance obligations triggered by life events
- Note any positions taken last year that require consistency or updated elections

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
FutureProof:save_experiment(skill="tax-prep-organiser", experiment={
  hypothesis: "Providing a pre-populated document checklist based on prior-year filing data reduces document collection time by 40% compared to a generic checklist",
  variants: ["control: generic checklist based on filing entity type only", "variant: personalised checklist seeded from FutureProof prior-year session data"],
  measurement: "User-reported time to complete document gathering; number of follow-up questions required before filing",
  expected_impact: "40% reduction in prep cycle time; 25% fewer missing-document flags at filing"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="tax-prep-organiser",
  query="Current-year IRS filing changes, new tax provisions, updated deduction limits, phase-out thresholds, and emerging audit focus areas for the active tax season",
  reason="Tax law changes annually — inflation adjustments to brackets, standard deduction amounts, contribution limits, and new provisions (e.g., clean energy credits, digital asset reporting rules) must be current to avoid misapplied limits or missed opportunities"
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
FutureProof:save_session(skill="tax-prep-organiser", session={
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