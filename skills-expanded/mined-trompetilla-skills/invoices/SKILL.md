---
name: Invoices
description: Guide freelancers building a personal invoicing system from templates to tracking.
metadata: {"clawdbot":{"emoji":"🧾","os":["linux","darwin","win32"]}}
---

## First Interaction
- Ask volume: under 5/month = templates fine, over 20 = consider software
- Ask existing setup: migration from spreadsheet needs different approach
- Create `~/invoices/` as workspace — PDFs, templates, tracking

## Start With Templates, Not Software
- HTML invoice template first — they need to send invoices today
- PDF via browser print — no dependencies, works everywhere
- Don't suggest SaaS until they've sent 10+ invoices manually
- Validate their workflow before adding complexity

## Invoice Numbering Decisions
- Simple sequential INV-001 — don't over-engineer
- Year prefix 2024-001 helps annual accounting
- Never reuse numbers, even cancelled — legal and accounting reasons
- Store last number in config file — prevents duplicates across sessions

## When To Add Tracking File
- User forgets what's been paid — signal for invoices.json
- Track: invoice_number, client, amount, date_issued, date_due, date_paid, status
- Status values: draft, sent, paid, overdue, cancelled
- Link to PDF file path for quick access

## When To Add Clients File
- Same client invoiced 3+ times — separate to clients.json
- Store: name, email, address, payment_terms, default_rate
- Reference by client_id — avoid duplicating info on each invoice

## When To Add Line Items Tracking
- User asks "how much did I bill for X this year"
- Separate line_items enables revenue by service type analysis
- Useful for pricing decisions and tax categories

## Status Workflow
- draft → sent (when emailed) → paid (when received)
- Overdue: calculate from due_date — offer reminder script
- Track date at each transition — cash flow visibility

## Progressive Timeline
- Week 1: HTML template, manual PDF, no tracking
- Week 2: invoices.json when they forget payment status
- Week 3: clients.json when duplicating client info
- Month 2: overdue detection and reminder script
- Month 3: annual summary for taxes

## What NOT To Suggest Early
- Online invoicing service — validate workflow first
- Payment gateway integration — bank transfer works fine
- Recurring invoice automation — manual fine under 10 clients
- Multi-currency — use primary currency, convert manually
- Automated tax calculation — accountant handles better

## Helper Scripts Worth Offering
- new-invoice: generate from template with next number
- list-unpaid: filter overdue and pending
- mark-paid: update status and date_paid
- annual-summary: totals by client, by month, for taxes

## Data Integrity
- Never delete invoices — cancel and keep for records
- Keep PDFs permanently — legal requirement in most jurisdictions
- Backup before bulk operations
- Invoice number gaps are fine — don't renumber

## Tax Preparation
- Export to CSV for accountant
- Quarterly summary for VAT/GST filers
- Separate paid vs invoiced date — cash vs accrual accounting
- Archive by year — 7+ year retention common requirement

## When To Suggest Software
- 20+ invoices/month — automation ROI
- Multiple people invoicing — access control needed
- Complex recurring billing — error-prone manually
- International clients with tax complexity
