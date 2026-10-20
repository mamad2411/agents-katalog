---
name: invoice-reconciliation
description: Reconcile invoices, receipts, payments, purchase orders, accounts receivable, accounts payable, duplicate charges, and unmatched transaction tables.
---

# invoice-reconciliation

## Purpose

Match invoices and payments so exceptions are easy to review.

## Workflow

1. Identify source tables: invoices, payments, receipts, purchase orders, bank lines, or vendor/customer statements.
2. Normalize dates, identifiers, counterparties, currencies, and amounts.
3. Match exact records first, then near matches by amount, date range, and counterparty.
4. Separate matched, partially matched, duplicate, missing, and unclear records.
5. Produce an exception table for follow-up.

## Required Checks

- Do not alter source records unless explicitly asked.
- Do not assume a match when identifiers or amounts conflict.
- Mark currency, tax, fee, and timing differences.

## Output

Return reconciliation summary, match table, exception table, duplicate candidates, and follow-up actions.
