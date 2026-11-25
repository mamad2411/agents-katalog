---
name: accounts-receivable-collections
description: Use when drafting, reviewing, or organizing accounts receivable follow-ups, invoice collection messages, payment reminder sequences, aging summaries, dispute summaries, customer payment issue notes, or collections escalation plans. Prefer this Skill when the task needs professional tone, invoice facts, dispute handling, escalation path, or cash collection prioritization. Do not use for payment processing, legal threats, credit decisions, or accounting system actions.
meta:
  version: 1
  display_name: 应收账款催收
---

# Accounts Receivable Collections

## Purpose

Create professional, fact-grounded payment follow-up work that protects customer relationships while making payment status, disputes, and next steps clear.

## Use When

Use for:

- invoice reminder emails
- payment follow-up sequences
- aging summary narratives
- dispute summaries
- collections escalation plans
- customer payment issue notes
- AR status reports

## Material Gate

Identify:

- customer, invoice number, amount, due date, currency, payment terms, and aging bucket
- prior reminders, dispute status, promised payment date, and relationship sensitivity
- escalation policy and approved tone

Do not invent invoice facts, payment commitments, penalties, legal threats, or collection authority.

## Workflow

1. Verify invoice facts and aging status from provided material.
2. Classify status: not yet due, due soon, overdue, disputed, promised, escalated, or high-risk.
3. Draft the message with facts, polite ask, payment path, and response deadline.
4. Separate customer-facing language from internal escalation notes.
5. Summarize disputes and required owner action.
6. Prioritize accounts by amount, age, risk, and relationship.
7. Use `html-report-builder` for AR aging or collections reports.

## Checks

- Invoice facts are accurate and visible.
- Tone is firm but professional.
- Disputes are not treated as unwillingness to pay.
- Escalation follows provided policy or is marked as recommendation.
- No legal threat or penalty is invented.

## Outputs

- payment reminder
- collections sequence
- AR aging summary
- dispute summary
- escalation plan
- customer payment note
- cash collection report

## Boundary

This Skill owns AR communication, aging narrative, dispute framing, and collections planning. It does not own payment processing, accounting entries, credit holds, legal action, customer account changes, or external sending.

It must not run shell, Python, Node, npm, curl, MCP, ERP, accounting system, banking, payment, email, CRM, package install, or external API commands by itself; those actions belong to XAgent tools visible in the current session.
