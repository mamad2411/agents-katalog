---
name: "gl-break-tracer"
description: "Investigating a general ledger reconciliation break, unexplained variance in a trial balance, subledger-to-GL mismatch, or a month-end close discre..."
---

# GL Break Tracer

## When to activate

Investigating a general ledger reconciliation break, unexplained variance in a trial balance, subledger-to-GL mismatch, or a month-end close discrepancy. Use when a numeric difference exists between two representations of the same financial position and the root cause is unknown.

## When NOT to use

Posting journal entries or adjustments. This skill diagnoses only — a resolver (human or separate workflow) posts any fixes after review. Do not use this skill to propose posting without a qualified accountant sign-off.

## Instructions

Three-phase investigation:

**Phase 1 — GL Layer**

Read the GL account balance. Identify the reporting period, account code, and entity. Extract the net movement and ending balance. Record the source (ERP system, report name, run date).

**Phase 2 — Subledger Layer**

Pull the corresponding subledger or supporting schedule. Sum the subledger balances for the same period and account scope. Compare to the GL ending balance:

```
net difference = GL balance − subledger total
```

If net difference = 0, no break exists. If non-zero, proceed to Phase 3.

**Phase 3 — Attribute Comparison**

For each line item contributing to the break, identify the attribute that differs:

- Date (cutoff mismatch)
- Amount (rounding, currency conversion, duplicate entry)
- Counterparty (miscoded vendor/customer)
- Currency (FX rate applied differently)
- Cost center or business unit (intercompany allocation error)
- Transaction type (misclassified posting)

Root cause statement format: `"[GL side] [action] because [subledger reason]"`

Example: `"GL debit posted on 2026-05-31 because subledger entry dated 2026-06-01 — cutoff mismatch"`

**Output format (JSON):**

```json
{
  "break_amount": 12450.00,
  "currency": "USD",
  "root_cause": "GL debit posted on 2026-05-31; subledger entry dated 2026-06-01 (cutoff mismatch)",
  "owner": "AP Team",
  "action": "adjust",
  "action_detail": "Reclassify GL entry to June period; post reversing JE dated 2026-06-01",
  "verification": "Rerun reconciliation after posting — break should clear to zero"
}
```

**Action types:**

| Type | Meaning |
|------|---------|
| `monitor` | Watch but take no action yet — difference is timing-related and expected to self-clear |
| `adjust` | Post a correcting journal entry to resolve the break |
| `raise-ticket` | Escalate to upstream system owner — root cause is a system or feed error outside accounting's control |
| `suppress` | Known permanent difference — document and obtain sign-off; exclude from future reconciliation |

**Safety gate:** This skill produces a diagnosis and recommended action. All proposed journal entries must be reviewed and approved by a qualified accountant before posting. Never post directly from this skill's output.

## Example

**Input:** "The AP subledger shows $45,230 in outstanding invoices but the AP GL account shows $57,680 for the same period. Trace the $12,450 break and identify the root cause."

**Expected output:**

```json
{
  "break_amount": 12450.00,
  "currency": "USD",
  "root_cause": "Two GL entries totaling $12,450 have no matching subledger records — likely manual journal entries posted directly to the GL account bypassing the AP module",
  "owner": "AP Team",
  "action": "raise-ticket",
  "action_detail": "Identify the manual JEs by querying GL transactions with no subledger reference for the period. Determine if they are valid (reclassification) or erroneous (duplicate). Escalate to GL Controller for review.",
  "verification": "After resolution, rerun AP reconciliation — break should clear to zero or be suppressed with documented rationale"
}
```

---
