---
name: dunning-emails
description: Use when drafting payment reminder or dunning email sequences from invoice, account, dispute, and customer context while preserving customer trust and requiring human approval before sending.
source: "https://github.com/loopfour/finance-skills"
source_repository: "loopfour/finance-skills"
source_path: "skills/dunning-emails/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Dunning Emails

Use this skill to draft polite, accurate, and escalation-aware payment reminder messages.

## Inputs

- Customer name, contact, invoice number, amount, currency, due date, and payment link or remittance instructions.
- Prior outreach history and any promised payment date.
- Dispute status, service issues, credit memos, or unapplied cash.
- Brand voice and escalation policy.

## Workflow

1. Verify whether the invoice is actually due and collectible.
2. Choose the correct tone based on aging stage:
   - Pre-due: helpful reminder.
   - 1-15 days overdue: operational nudge.
   - 16-45 days overdue: firmer request and ask for payment date.
   - 46+ days overdue: escalation with internal owner copied only if policy allows.
3. Include only facts supported by the input.
4. Provide subject line options and a concise email body.
5. If multiple invoices are involved, summarize totals and attach a statement table.

## Output

Return:

- Suggested stage and rationale.
- Email subject line.
- Email body.
- Internal note for the collector.
- Missing data or approval needed before sending.

## Guardrails

- Never send the email directly.
- Do not imply service suspension, collections agency referral, late fees, or legal action without explicit policy support.
- Do not expose internal notes, customer health scores, or blame language in customer-facing drafts.
- If there is an unresolved dispute, draft a resolution-focused message rather than a payment demand.
