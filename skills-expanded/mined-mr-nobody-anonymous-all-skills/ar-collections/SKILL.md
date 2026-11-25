---
name: ar-collections
description: Use when reviewing accounts receivable aging, prioritizing overdue invoices, preparing collector worklists, identifying disputed balances, and recommending next collection actions for finance operators.
source: "https://github.com/loopfour/finance-skills"
source_repository: "loopfour/finance-skills"
source_path: "skills/ar-collections/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# AR Collections

Use this skill to turn an AR aging report and account context into a prioritized, source-backed collections plan.

## Inputs

Ask for the missing items only when they are necessary:

- AR aging export with customer, invoice, due date, amount, currency, aging bucket, and owner.
- Customer notes, payment promises, dispute status, and prior outreach.
- Materiality threshold, collection policy, and escalation rules.
- Customer health context, contract status, open support tickets, or renewal timing.

## Workflow

1. Normalize the aging view by customer, invoice, due date, amount, aging bucket, and dispute status.
2. Separate true collection work from administrative cleanup: unapplied cash, credits, duplicate invoices, invalid contacts, and invoices already under dispute.
3. Rank accounts by action priority using amount, days overdue, relationship risk, dispute status, payment history, and upcoming renewal or churn risk.
4. Assign a recommended next action for each account: reminder, statement resend, dispute resolution, sales/customer-success escalation, executive escalation, payment plan, write-off review, or no action.
5. Flag missing evidence and assumptions. Do not invent payment commitments or customer history.

## Output

Return:

- Executive summary: total past due, material exposure, urgent accounts, and main blockers.
- Priority table with customer, invoice count, past-due amount, oldest due date, status, owner, next action, and evidence.
- Dispute and cleanup queue.
- Outreach drafts only when requested.
- Approval list for sensitive actions such as executive escalation, service hold, payment plan, write-off, or legal referral.

## Guardrails

- Do not threaten suspension, legal action, or credit reporting unless the user's policy explicitly allows it.
- Do not mark invoices as collectible if source data shows an active dispute, billing error, or unapplied payment.
- Keep customer-facing language factual and calm.
- Clearly distinguish recommendations from actions already taken.
