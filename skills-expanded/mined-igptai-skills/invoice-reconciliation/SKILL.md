---
name: invoice-reconciliation
description: Extracts all invoices from connected email datasources, normalizes amounts to the user's local currency, and returns a structured schema ready for accountant export. Use when a freelancer or finance person needs to reconcile invoices received across multiple currencies. Triggers on "invoice reconciliation", "invoices from email", "collect my invoices", "how much do I owe", "invoices in different currencies", "send invoices to accountant".
metadata:
  version: 1.0.0
---

# Invoice Reconciliation

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Finds all invoices received via email, extracts the amount, currency, sender,
and date for each, converts every amount to the user's local currency, and
returns a clean structured schema the user can send directly to their accountant
or import into accounting software.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("the current month", "last 30 days", "May 2024").
     Default: the current calendar month. Keep the user's natural
     phrasing for use in the ask input; convert to ISO dates separately
     for the search call.
   - [local_currency] — the currency to convert all amounts into (e.g.
     USD, EUR, ILS). No default — must come from the user.

2. Call search with:
   - query: invoice receipt billing payment due amount
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Find all invoices and billing emails received in [time_range]. For each invoice extract: the sender company or name, the invoice number if present, the invoice date, the amount due, and the currency. Then convert each amount to [local_currency] using current exchange rates. Return every invoice as a structured record.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Invoice reconciliation report for a specific time period",
       "additionalProperties": false,
       "properties": {
         "period_from": {
           "type": "string",
           "description": "ISO8601 start date of the reconciliation period"
         },
         "period_to": {
           "type": "string",
           "description": "ISO8601 end date of the reconciliation period"
         },
         "local_currency": {
           "type": "string",
           "description": "The currency all amounts have been converted to (e.g. USD, EUR, ILS)"
         },
         "invoices": {
           "type": "array",
           "description": "List of every invoice found in email during the period",
           "items": {
             "type": "object",
             "description": "A single invoice extracted from email",
             "additionalProperties": false,
             "properties": {
               "sender": {
                 "type": "string",
                 "description": "Company or person who sent the invoice"
               },
               "invoice_number": {
                 "type": "string",
                 "description": "Invoice number or reference, empty string if not found"
               },
               "invoice_date": {
                 "type": "string",
                 "description": "ISO8601 date of the invoice"
               },
               "original_amount": {
                 "type": "number",
                 "description": "The invoice amount in its original currency"
               },
               "original_currency": {
                 "type": "string",
                 "description": "The currency code of the original invoice amount (e.g. USD, EUR, GBP)"
               },
               "converted_amount": {
                 "type": "number",
                 "description": "The invoice amount converted to the user's local currency"
               },
               "converted_currency": {
                 "type": "string",
                 "description": "The local currency code the amount was converted to"
               },
               "due_date": {
                 "type": "string",
                 "description": "ISO8601 payment due date, empty string if not found"
               },
               "status": {
                 "type": "string",
                 "description": "Payment status based on email evidence",
                 "enum": ["paid", "unpaid", "unknown"]
               }
             },
             "required": [
               "sender", "invoice_number", "invoice_date",
               "original_amount", "original_currency",
               "converted_amount", "converted_currency",
               "due_date", "status"
             ]
           }
         },
         "total_converted": {
           "type": "number",
           "description": "Sum of all invoice amounts converted to local currency"
         },
         "total_unpaid_converted": {
           "type": "number",
           "description": "Sum of all unpaid invoice amounts converted to local currency"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of total invoices found, total amount, and any unpaid items"
         }
       },
       "required": [
         "period_from", "period_to", "local_currency", "invoices",
         "total_converted", "total_unpaid_converted", "summary"
       ]
     }
   }

4. Present as a clean table with one row per invoice. Lead with the summary
   line showing total count, total amount, and total unpaid.

5. Ask: "Would you like me to export this as a CSV format for your accountant?"
