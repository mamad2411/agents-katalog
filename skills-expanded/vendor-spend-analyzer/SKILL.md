---
name: vendor-spend-analyzer
description: Calculates total spend per vendor over a time period from email receipts and invoices, identifying the largest vendors and spend trends. Use when a user wants to understand where their money is going across vendors. Triggers on "vendor spend", "where am I spending money", "top vendors by spend", "spend analysis", "how much am I paying each vendor".
metadata:
  version: 1.0.0
---

# Vendor Spend Analyzer

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Aggregates all payment receipts, invoices, and billing emails by vendor to
calculate total spend per vendor over a period. Identifies the largest spend
categories, flags unexpected increases, and returns a ranked vendor spend
breakdown.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to analyze. The user may give
     this in any form ("last 12 months", "the last year", "May 2024",
     "since the budget reset"). Default: the last 12 months. Keep the
     user's natural phrasing for use in the ask input; convert to ISO
     dates separately for the search call.
   - [local_currency] — the currency to convert all totals into (e.g.
     USD, EUR, ILS). No default — must come from the user.

2. Call search with:
   - query: invoice receipt payment billing charge vendor
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all invoices, receipts, and billing emails from [time_range]. For each vendor calculate the total amount paid across all transactions in that period. Convert all amounts to [local_currency]. Rank vendors by total spend and identify the category of spend for each.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Vendor spend analysis report for a specific time period",
       "additionalProperties": false,
       "properties": {
         "period_from": {
           "type": "string",
           "description": "ISO8601 start date of the analysis period"
         },
         "period_to": {
           "type": "string",
           "description": "ISO8601 end date of the analysis period"
         },
         "local_currency": {
           "type": "string",
           "description": "Currency all amounts have been converted to"
         },
         "vendors": {
           "type": "array",
           "description": "List of vendors ranked by total spend descending",
           "items": {
             "type": "object",
             "description": "A single vendor with aggregated spend data",
             "additionalProperties": false,
             "properties": {
               "vendor": {
                 "type": "string",
                 "description": "Name of the vendor or service provider"
               },
               "total_spend": {
                 "type": "number",
                 "description": "Total amount paid to this vendor in local currency over the period"
               },
               "transaction_count": {
                 "type": "number",
                 "description": "Number of individual invoices or charges from this vendor"
               },
               "category": {
                 "type": "string",
                 "description": "Type of service or product this vendor provides",
                 "enum": [
                   "saas", "hosting", "freelancer", "agency", "supplier",
                   "travel", "office", "legal", "finance", "marketing", "other"
                 ]
               },
               "billing_frequency": {
                 "type": "string",
                 "description": "How often this vendor bills based on email pattern",
                 "enum": ["monthly", "annual", "one_time", "irregular", "unknown"]
               },
               "last_charge_date": {
                 "type": "string",
                 "description": "ISO8601 date of the most recent charge from this vendor"
               }
             },
             "required": [
               "vendor", "total_spend", "transaction_count", "category",
               "billing_frequency", "last_charge_date"
             ]
           }
         },
         "totals_by_category": {
           "type": "array",
           "description": "Total spend aggregated by vendor category",
           "items": {
             "type": "object",
             "description": "Category spend subtotal",
             "additionalProperties": false,
             "properties": {
               "category": {
                 "type": "string",
                 "description": "Vendor category name"
               },
               "total": {
                 "type": "number",
                 "description": "Total spend in this category in local currency"
               },
               "percentage_of_total": {
                 "type": "number",
                 "description": "This category's share of total spend as a percentage"
               }
             },
             "required": ["category", "total", "percentage_of_total"]
           }
         },
         "grand_total": {
           "type": "number",
           "description": "Total spend across all vendors in local currency"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of total spend, top vendor, and largest category"
         }
       },
       "required": [
         "period_from", "period_to", "local_currency", "vendors",
         "totals_by_category", "grand_total", "summary"
       ]
     }
   }

4. Present with category breakdown first, then ranked vendor list. Lead with
   grand total and the top 3 vendors by spend.

5. Ask: "Would you like me to flag any vendors worth reviewing or renegotiating?"
