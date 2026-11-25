---
name: payment-terms-policy
description: "Creates payment terms and collections policies with net terms, late fee structures, and escalation procedures. Use when establishing how and when clients must pay."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Payment Terms Policy

## When to Use This Skill

Use this skill when you need to:
- Establish standard payment terms for your business
- Create a late payment and collections escalation policy
- Draft payment terms language for contracts and invoices
- Design early payment incentives or late fee structures

**DO NOT** use this skill for creating invoices, pricing strategies, or full client agreements. This is specifically for the payment terms and collections process.

---

## Core Principle

CLEAR PAYMENT TERMS PREVENT 90% OF COLLECTIONS ISSUES — STATE THE RULES UPFRONT, ENFORCE THEM CONSISTENTLY, AND ESCALATE PREDICTABLY.

---

## Phase 1: Business Context

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business type** | "What type of business? (freelance, agency, SaaS, product)" | Service-based |
| **Average invoice amount** | "What is your typical invoice size?" | $1,000-5,000 |
| **Current terms** | "What payment terms do you currently use? (net 30, due on receipt)" | Net 30 |
| **Payment methods accepted** | "How can clients pay? (credit card, ACH, wire, check)" | Credit card + ACH |
| **Late payment issues** | "Are you experiencing late payments now?" | Some |
| **Client type** | "B2B or B2C? Large companies or small businesses?" | B2B small businesses |

**GATE: Do not proceed without business type and typical invoice size.**

---

## Phase 2: Payment Terms Design

### Standard Terms Options

```
## Payment Terms Policy

### Recommended Terms: [Net XX]

| Term Type | When to Use | Risk Level |
|-----------|------------|-----------|
| Due on receipt | Small projects, new clients, under $1,000 | Lowest |
| Net 15 | Standard services, retainer invoices | Low |
| Net 30 | Established clients, B2B standard | Medium |
| Net 45-60 | Enterprise clients only (with justification) | Higher |
| 50% upfront / 50% on delivery | Projects, custom work | Lowest |
| Monthly retainer (due 1st of month) | Ongoing services | Low |

### Selected Terms Structure

**Standard terms:** [Net XX]
**New client terms:** [Due on receipt or 50/50 split]
**Retainer terms:** [Due on 1st, auto-charge preferred]
**Large project terms (>$[X]):** [Milestone payments — 33/33/34 or 50/25/25]
```

### Early Payment Incentives

```
### Early Payment Discount (Optional)

- 2/10 Net 30: 2% discount if paid within 10 days
- 1/15 Net 30: 1% discount if paid within 15 days

Only offer if cash flow timing matters more than the discount cost.
```

### Late Fee Structure

```
### Late Payment Fees

| Days Past Due | Action | Fee |
|--------------|--------|-----|
| 1-7 days | Courtesy reminder email | None |
| 8-15 days | Late notice + late fee applied | [1.5% per month or $X flat] |
| 16-30 days | Second notice, phone call | Additional interest accrues |
| 31-60 days | Final notice, work paused | Services suspended |
| 61-90 days | Collections warning letter | Formal demand |
| 90+ days | Collections agency or legal | External collections |

**Late fee rate:** [1.5% per month / 18% annually — check state usury laws]
**Grace period:** [7 days from due date]
**Compounding:** [Simple interest, not compounding]
```

---

## Phase 3: Collections Process

### Escalation Templates

```
### Email Template: Courtesy Reminder (Day 1-7)

Subject: Friendly reminder — Invoice #[X] due [date]

Hi [Name],

Just a quick reminder that Invoice #[X] for $[amount] was due on [date].
If you have already sent payment, please disregard this message.

You can pay here: [payment link]

Thanks,
[Your name]

---

### Email Template: Late Notice (Day 8-15)

Subject: Past due — Invoice #[X] ($[amount])

Hi [Name],

Invoice #[X] for $[amount] is now [X] days past due. A late fee of $[X]
has been applied per our payment terms.

Please remit payment by [new date] to avoid additional fees. Pay here: [link]

If there is an issue with this invoice, let me know and we can resolve it.

[Your name]

---

### Email Template: Final Notice (Day 31-60)

Subject: Final notice — Invoice #[X] past due

Hi [Name],

Invoice #[X] for $[amount] is now [X] days past due. As stated in our
agreement, services have been paused until the balance is resolved.

Total due (including late fees): $[X]

Please remit payment within 7 days. If we do not receive payment or a
response, we will proceed with formal collections.

[Your name]
```

---

## Phase 4: Policy Document

### Invoice Language

```
## Payment Terms (for invoice footer or contract)

Payment is due within [X] days of invoice date. A late fee of [1.5%]
per month will be applied to balances outstanding beyond the [7]-day
grace period. Client is responsible for all costs of collection,
including reasonable attorney fees. [Business Name] reserves the right
to suspend services on accounts more than [30] days past due.
```

### Implementation Checklist

```
- [ ] Payment terms added to contract template
- [ ] Late fee language added to invoice template
- [ ] Payment link included on every invoice
- [ ] Auto-reminder set up in invoicing software (Day 1, 7, 14, 30)
- [ ] Collections escalation process documented
- [ ] Team trained on enforcement (no exceptions without approval)
- [ ] Late fee rate compliant with state usury laws
```

---

## Example: Freelance Consultant

**Terms:** Net 15 for ongoing clients, 50% upfront for new clients and projects over $5,000. Late fee: 1.5% per month after 7-day grace period. Auto-reminders at Day 1, 7, and 14. Services paused at Day 30.

**Result:** Average days-to-payment dropped from 38 to 14 after implementing clear terms and auto-reminders.

---

## Anti-Patterns

- **No written terms** — verbal agreements lead to "I thought it was net 60." Put terms in writing on every contract and invoice.
- **Terms but no enforcement** — if you never charge late fees, your terms are suggestions. Enforce consistently.
- **Net 60+ for small businesses** — only enterprise clients justify long terms. Small business clients should pay net 15-30.
- **No upfront payment on projects** — custom work without deposits is a risk. Always collect 30-50% before starting.
- **Emotional collections** — follow the escalation process mechanically. Angry emails damage relationships and rarely get you paid faster.

---

## Recovery

- **Currently owed money with no terms in place:** Implement terms going forward. For existing overdue invoices, send a professional reminder and offer a payment plan if needed.
- **Client refuses late fees:** Decide if the relationship is worth it. For valuable clients, waive the fee once but communicate that terms apply going forward.
- **State restricts late fee rates:** Research your state's usury laws. Most states allow 1-1.5% per month for commercial transactions.
- **Client disputes the invoice:** Pause collections. Resolve the dispute first, then restart the clock on payment terms.
