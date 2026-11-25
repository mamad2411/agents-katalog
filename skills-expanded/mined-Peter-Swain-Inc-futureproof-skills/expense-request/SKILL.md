---
name: expense-request
description: |
  Prepares audit-ready expense requests and reimbursement claims with policy
  compliance checks, threshold-based approval routing, and approver briefing
  notes. Use when the user says "submit an expense", "file a reimbursement",
  "get this purchase pre-approved", "is this within policy", or needs help
  drafting a T&E claim with the right documentation and GL coding. Single
  expense submission — not budgeting or accounts payable management.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="expense-request")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including known expense policies, approval hierarchies, cost centre mappings, preferred vendors, currency conventions, and historical submission patterns.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Expense type**: What category does this fall under? (travel, meals & entertainment, software/SaaS subscription, professional development, office supplies, client-related, equipment, miscellaneous)
- **Amount and currency**: What is the total amount (or estimated amount for pre-approvals)?
- **Business justification**: What is the business purpose and expected outcome of this expenditure?
- **Date(s) of expense**: When was/will the expense be incurred?
- **Receipt status**: Are receipts, invoices, or supporting documents available?
- **Urgency**: Is there a submission deadline, reimbursement cycle cut-off, or time-sensitive approval requirement?
- **Any known policy constraints**: Spending limits, pre-approval requirements, restricted vendors, or flagged categories they are aware of?

If FutureProof context contains the user's company expense policy, approval thresholds, or cost centre structure, pre-populate known fields and confirm rather than re-ask.

## Step 3: Validate Policy Compliance

Perform a structured compliance review against the applicable expense policy framework:

1. **Threshold analysis** — Does the amount fall within auto-approval limits, manager-approval limits, or executive/finance-approval limits? Identify the correct approval tier.
2. **Category eligibility** — Is the expense type permissible under company policy? Flag restricted or prohibited categories (e.g., alcohol, first-class travel without executive pre-approval, personal items).
3. **Pre-approval requirement check** — Does this expense category or amount require pre-approval before the expenditure is incurred? If yes, has it been obtained?
4. **Documentation sufficiency** — Are the required supporting documents present? (Itemised receipts, not credit card summaries; vendor invoices with tax IDs where applicable; attendee lists for meals/entertainment; conference agendas for professional development)
5. **Per diem and rate cap review** — For travel-related expenses, does the claimed amount fall within applicable per diem rates, mileage reimbursement rates, or lodging caps?
6. **Duplicate and split-submission detection** — Cross-reference against `recent_sessions` to flag potential duplicate submissions or patterns that suggest expense splitting to avoid approval thresholds.
7. **Tax and regulatory compliance** — Identify VAT/GST recoverability, fringe benefit tax implications, or jurisdiction-specific reporting requirements (e.g., meals entertainment percentage deductibility, gift reporting thresholds).

Apply any user-specific `instructions` from FutureProof context — such as company-specific policy overrides, department-level restrictions, or known audit focus areas.

## Step 4: Construct the Expense Request Package

Produce a complete, submission-ready **Expense Request Package** containing:

### 4a. Expense Request Form
A structured document with:
- **Requestor details**: Name, employee ID, department, cost centre
- **Expense line items**: Date, vendor/payee, category, description, amount (local currency), amount (reporting currency if applicable), GL code
- **Total amount requested**
- **Business justification statement**: A concise, audit-defensible narrative (2–3 sentences) linking the expense to a specific business objective, client engagement, or operational requirement
- **Approval routing**: Named approver(s) based on threshold tier, with escalation path if primary approver is unavailable

### 4b. Compliance Summary Memo
- **Policy compliance status**: COMPLIANT / COMPLIANT WITH CONDITIONS / NON-COMPLIANT
- **Flags and conditions**: Any items requiring additional justification, retroactive pre-approval, or exception requests — with recommended remediation language
- **Risk rating**: LOW / MEDIUM / HIGH based on audit exposure (amount, category sensitivity, documentation gaps)

### 4c. Supporting Document Checklist
An itemised list of required attachments with status indicators:
- ✅ Obtained
- ⚠️ Missing — action required (with specific instruction on what to obtain)
- ℹ️ Not applicable

### 4d. Approver Briefing Note (if amount exceeds standard threshold)
A one-paragraph summary designed for the approver — covering business rationale, policy alignment, and any context that accelerates approval without back-and-forth.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Recommend Process Improvements

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Based on the current submission and historical patterns from `recent_sessions`, provide:

- **Efficiency recommendations**: Opportunities to batch similar expenses, use corporate cards to reduce receipt handling, or leverage preferred vendor agreements for better rates
- **Policy gap observations**: Where the user's expense pattern suggests the policy is unclear or creates unnecessary friction — recommend specific clarification requests to Finance
- **Cost optimisation notes**: Alternative vendors, booking windows, or procurement channels that would reduce the expense amount for equivalent business outcomes

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="expense-request", experiment={
  hypothesis: "Pre-populating cost centre and GL codes from historical submission patterns reduces expense request preparation time and error rate",
  variants: ["control: manual field entry each session", "variant: auto-populated fields with user confirmation"],
  measurement: "Time to complete expense request package and number of correction cycles before approval",
  expected_impact: "40% reduction in preparation time and 25% fewer rejection-resubmission loops"
})
```

## Step 7: Request Research

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:request_research(skill="expense-request",
  query="Corporate expense policy best practices 2024, IRS and HMRC documentation requirements for business expense deductibility, and emerging T&E management automation standards",
  reason="Ensure compliance guidance reflects current regulatory requirements and incorporates leading-practice expense governance frameworks used by Big Four advisory firms"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="expense-request", session={
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