---
name: subscription-tracker
description: Finds every recurring SaaS, service, and vendor subscription buried in receipt and billing emails. Use when a user wants to see all their active subscriptions, identify forgotten recurring charges, or audit monthly spend. Triggers on "what subscriptions do I have", "recurring charges", "monthly bills", "SaaS subscriptions", "what am I paying for every month".
metadata:
  version: 1.0.0
---

# Subscription Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans email history for recurring billing patterns — subscription confirmations,
renewal notices, and monthly or annual charge receipts — and compiles a full
list of active subscriptions with amounts, billing frequency, and renewal dates.

---

## Workflow

1. Before calling any tool, collect this value from the user. Offer the
   default and let the user override it; do not invent a value they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 13 months", "the last year", "May 2024",
     "since the credit card change"). Default: the last 13 months (to
     catch both monthly and annual subscriptions). Keep the user's
     natural phrasing for use in the ask input; convert to ISO dates
     separately for the search call.

2. Call search with:
   - query: subscription renewal receipt billing monthly annual charge
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Find all recurring subscriptions and billing emails from [time_range]. For each unique subscription identify: the service name, the billing amount, the billing frequency, the most recent charge date, and the next renewal date if mentioned. Flag any that appear to have been cancelled or that stopped renewing mid-period.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Complete subscription audit across all email billing history",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "subscriptions": {
           "type": "array",
           "description": "List of every recurring subscription identified in email",
           "items": {
             "type": "object",
             "description": "A single recurring subscription or service",
             "additionalProperties": false,
             "properties": {
               "service": {
                 "type": "string",
                 "description": "Name of the subscription service or vendor"
               },
               "amount": {
                 "type": "number",
                 "description": "Recurring charge amount per billing cycle"
               },
               "currency": {
                 "type": "string",
                 "description": "Currency code of the charge (e.g. USD, EUR)"
               },
               "frequency": {
                 "type": "string",
                 "description": "How often this subscription is billed",
                 "enum": ["monthly", "annual", "quarterly", "weekly", "unknown"]
               },
               "last_charge_date": {
                 "type": "string",
                 "description": "ISO8601 date of the most recent charge found in email"
               },
               "next_renewal_date": {
                 "type": "string",
                 "description": "ISO8601 date of the next expected renewal, empty string if unknown"
               },
               "status": {
                 "type": "string",
                 "description": "Whether this subscription appears to be currently active or cancelled",
                 "enum": ["active", "cancelled", "unknown"]
               },
               "category": {
                 "type": "string",
                 "description": "Type of service this subscription provides",
                 "enum": [
                   "saas_productivity", "saas_dev_tools", "saas_marketing",
                   "saas_finance", "hosting", "storage", "communication",
                   "media", "professional_service", "other"
                 ]
               }
             },
             "required": [
               "service", "amount", "currency", "frequency",
               "last_charge_date", "next_renewal_date", "status", "category"
             ]
           }
         },
         "total_monthly_equivalent": {
           "type": "number",
           "description": "Total estimated monthly cost across all active subscriptions normalized to a single currency"
         },
         "currency_note": {
           "type": "string",
           "description": "Note about which currency the total is expressed in and any multi-currency caveats"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of total subscriptions found, estimated monthly cost, and any notable items"
         }
       },
       "required": [
         "as_of", "subscriptions", "total_monthly_equivalent",
         "currency_note", "summary"
       ]
     }
   }

4. Present as a table grouped by category, ordered by amount descending.
   Lead with total monthly equivalent and count of active subscriptions.

5. Ask: "Would you like me to flag subscriptions you might want to cancel
   or review?"
