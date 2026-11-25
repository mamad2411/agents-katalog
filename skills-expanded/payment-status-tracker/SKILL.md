---
name: payment-status-tracker
description: Finds payment confirmations, outstanding invoices, and overdue items across email to give a clear picture of what has been paid and what is still owed. Use when a user wants to know which invoices are paid and which are outstanding. Triggers on "what invoices are unpaid", "payment status", "what do I still owe", "overdue payments", "outstanding invoices".
metadata:
  version: 1.0.0
---

# Payment Status Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Matches invoices received in email against payment confirmations to determine
what has been paid, what is still outstanding, and what is overdue based on
due dates mentioned in the emails.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last quarter", "May 2024",
     "since billing started"). Default: the last 90 days. Keep the
     user's natural phrasing for use in the ask input; convert to ISO
     dates separately for the search call.
   - [direction_scope] — which side to analyze. "both" (default),
     "payables" (what you owe others), or "receivables" (what others
     owe you).
   - [direction_clause] — derived. When [direction_scope] is "both",
     set to empty string. When "payables", set to ", focused on
     payables". When "receivables", set to ", focused on receivables".

2. Call search with:
   - query: invoice payment confirmation paid receipt overdue outstanding due
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all invoice and payment emails from [time_range][direction_clause]. Match each invoice against any payment confirmation found. For each invoice determine: the vendor or client, the amount, the due date, and whether a payment confirmation exists in email. Flag anything overdue based on the due date versus today.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Payment status report showing paid and outstanding invoices",
       "additionalProperties": false,
       "properties": {
         "period_from": {
           "type": "string",
           "description": "ISO8601 start date of the period reviewed"
         },
         "period_to": {
           "type": "string",
           "description": "ISO8601 end date of the period reviewed"
         },
         "direction": {
           "type": "string",
           "description": "Whether this report covers money owed out, money owed in, or both",
           "enum": ["payables", "receivables", "both"]
         },
         "items": {
           "type": "array",
           "description": "List of every invoice with its payment status",
           "items": {
             "type": "object",
             "description": "A single invoice and its current payment status",
             "additionalProperties": false,
             "properties": {
               "counterparty": {
                 "type": "string",
                 "description": "The vendor, client, or company the invoice relates to"
               },
               "invoice_number": {
                 "type": "string",
                 "description": "Invoice number or reference, empty string if not found"
               },
               "amount": {
                 "type": "number",
                 "description": "Invoice amount"
               },
               "currency": {
                 "type": "string",
                 "description": "Currency code of the invoice amount"
               },
               "invoice_date": {
                 "type": "string",
                 "description": "ISO8601 date the invoice was issued"
               },
               "due_date": {
                 "type": "string",
                 "description": "ISO8601 payment due date, empty string if not found"
               },
               "payment_status": {
                 "type": "string",
                 "description": "Current payment status based on email evidence",
                 "enum": ["paid", "outstanding", "overdue", "unknown"]
               },
               "payment_date": {
                 "type": "string",
                 "description": "ISO8601 date payment was confirmed in email, empty string if not paid"
               },
               "days_overdue": {
                 "type": "number",
                 "description": "Number of days past due date, 0 if not overdue"
               }
             },
             "required": [
               "counterparty", "invoice_number", "amount", "currency",
               "invoice_date", "due_date", "payment_status",
               "payment_date", "days_overdue"
             ]
           }
         },
         "total_outstanding": {
           "type": "number",
           "description": "Sum of all outstanding and overdue amounts"
         },
         "total_overdue": {
           "type": "number",
           "description": "Sum of all overdue amounts only"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of paid vs outstanding vs overdue items"
         }
       },
       "required": [
         "period_from", "period_to", "direction", "items",
         "total_outstanding", "total_overdue", "summary"
       ]
     }
   }

4. Present with outstanding and overdue items first, ordered by days overdue
   descending. Then show paid items. Lead with summary totals.

5. Ask: "Would you like me to draft payment reminder emails for any overdue
   items?"
