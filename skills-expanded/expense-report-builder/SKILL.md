---
name: expense-report-builder
description: Aggregates expense receipts from email by time period, categorizes them by project or client, and returns a structured schema ready for expense tools or accountant submission. Use when a user needs to build an expense report from email receipts. Triggers on "build my expense report", "expense receipts from email", "what did I spend this month", "expenses by client", "expense report for accounting".
metadata:
  version: 1.0.0
---

# Expense Report Builder

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Finds all expense receipts in email for a given period, categorizes each by
expense type and optionally by project or client, and returns a structured
expense report ready for submission to accounting software or an accountant.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("the current month", "last 30 days", "May 2024",
     "since the trip"). Default: the current calendar month. Keep the
     user's natural phrasing for use in the ask input; convert to ISO
     dates separately for the search call.
   - [grouping_scope] — optional grouping for the report. "none"
     (default), "project", or "client".
   - [grouping_clause] — derived. When [grouping_scope] is not "none",
     set to ", grouped by [grouping_scope]". When "none", set to empty
     string.
   - [local_currency] — the currency to convert all totals into (e.g.
     USD, EUR, ILS). No default — must come from the user.

2. Call search with:
   - query: receipt expense reimbursement purchase paid travel meal hotel
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Find all expense receipts and purchase confirmations in email from [time_range][grouping_clause]. For each expense extract: the vendor, the amount, the currency, the date, the expense category, and any project or client it can be associated with based on context. Convert all amounts to [local_currency].
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Expense report for a specific time period built from email receipts",
       "additionalProperties": false,
       "properties": {
         "period_from": {
           "type": "string",
           "description": "ISO8601 start date of the expense report period"
         },
         "period_to": {
           "type": "string",
           "description": "ISO8601 end date of the expense report period"
         },
         "local_currency": {
           "type": "string",
           "description": "Currency all amounts have been converted to"
         },
         "expenses": {
           "type": "array",
           "description": "List of every expense receipt found in email during the period",
           "items": {
             "type": "object",
             "description": "A single expense item extracted from an email receipt",
             "additionalProperties": false,
             "properties": {
               "vendor": {
                 "type": "string",
                 "description": "Name of the vendor or merchant"
               },
               "date": {
                 "type": "string",
                 "description": "ISO8601 date of the expense"
               },
               "original_amount": {
                 "type": "number",
                 "description": "Expense amount in its original currency"
               },
               "original_currency": {
                 "type": "string",
                 "description": "Currency code of the original expense"
               },
               "converted_amount": {
                 "type": "number",
                 "description": "Expense amount converted to local currency"
               },
               "category": {
                 "type": "string",
                 "description": "Type of expense",
                 "enum": [
                   "travel", "accommodation", "meals", "software",
                   "hardware", "office_supplies", "marketing",
                   "professional_services", "communication", "other"
                 ]
               },
               "project_or_client": {
                 "type": "string",
                 "description": "Project or client this expense can be attributed to, empty string if not determinable"
               },
               "notes": {
                 "type": "string",
                 "description": "Any additional context about this expense from the email"
               }
             },
             "required": [
               "vendor", "date", "original_amount", "original_currency",
               "converted_amount", "category", "project_or_client", "notes"
             ]
           }
         },
         "totals_by_category": {
           "type": "array",
           "description": "Subtotal of expenses grouped by category",
           "items": {
             "type": "object",
             "description": "Category subtotal",
             "additionalProperties": false,
             "properties": {
               "category": {
                 "type": "string",
                 "description": "Expense category name"
               },
               "total": {
                 "type": "number",
                 "description": "Total amount for this category in local currency"
               }
             },
             "required": ["category", "total"]
           }
         },
         "grand_total": {
           "type": "number",
           "description": "Total of all expenses in local currency"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of total expenses found and largest categories"
         }
       },
       "required": [
         "period_from", "period_to", "local_currency", "expenses",
         "totals_by_category", "grand_total", "summary"
       ]
     }
   }

4. Present with grand total and category breakdown first, then full itemized
   list grouped by category.

5. Ask: "Would you like this formatted for a specific expense tool like
   Expensify, QuickBooks, or a CSV?"
