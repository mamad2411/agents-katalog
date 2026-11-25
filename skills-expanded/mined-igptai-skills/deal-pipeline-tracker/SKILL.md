---
name: deal-pipeline-tracker
description: Tracks every active real estate deal from email — where each transaction stands, what the next step is, which parties are involved, and what is stalling. Use when a real estate agent or broker wants a full pipeline view without manually checking every thread. Triggers on "deal pipeline", "active deals", "transaction status", "where are my deals", "deal tracker", "pipeline overview".
metadata:
  version: 1.0.0
---

# Deal Pipeline Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all real estate transaction email threads to produce a structured
pipeline view — current stage of each deal, parties involved, last activity,
next steps, open items, and anything that is stalling a transaction from
progressing.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 6 months", "the last 90 days", "May 2024",
     "since the spring market"). Default: the last 6 months. Keep the
     user's natural phrasing for use in the ask input; convert to ISO
     dates separately for the search call.
   - [scope] — either "all" (default) or a specific property or client
     to focus on.
   - [scope_clause] — derived. When [scope] is not "all", set to " for
     [scope]". When [scope] is "all", set to empty string.

2. Call search with:
   - query: offer accepted listing contract closing inspection escrow
     mortgage buyer seller transaction
     (if [scope] is not "all", append the property or client to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all real estate transaction email threads from [time_range][scope_clause]. For each active deal identify: the property address or description, the transaction type, the key parties involved, the current stage of the transaction, the most recent activity, the next step required, who owns that next step, any open items or blockers, and the expected or target closing date.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Real estate deal pipeline report across all active transactions",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "deals": {
           "type": "array",
           "description": "List of every active real estate deal in the pipeline",
           "items": {
             "type": "object",
             "description": "A single active real estate transaction with current pipeline status",
             "additionalProperties": false,
             "properties": {
               "property": {
                 "type": "string",
                 "description": "Property address or description"
               },
               "transaction_type": {
                 "type": "string",
                 "description": "Type of real estate transaction",
                 "enum": [
                   "buyer_representation", "seller_representation", "dual_agency",
                   "lease_residential", "lease_commercial", "investment_sale", "other"
                 ]
               },
               "client_name": {
                 "type": "string",
                 "description": "Name of the primary client in this transaction"
               },
               "stage": {
                 "type": "string",
                 "description": "Current stage of this transaction",
                 "enum": [
                   "initial_search", "property_shortlisted", "offer_preparation",
                   "offer_submitted", "offer_accepted", "under_contract",
                   "inspection_period", "mortgage_approval", "title_search",
                   "closing_scheduled", "closed", "stalled", "fallen_through"
                 ]
               },
               "last_activity_date": {
                 "type": "string",
                 "description": "ISO8601 date of the most recent email activity on this deal"
               },
               "last_activity_summary": {
                 "type": "string",
                 "description": "Brief summary of the most recent email activity"
               },
               "next_step": {
                 "type": "string",
                 "description": "The next action required to move this deal forward"
               },
               "next_step_owner": {
                 "type": "string",
                 "description": "Who is responsible for the next step",
                 "enum": ["agent", "client", "counterparty", "lender", "attorney", "title_company", "other"]
               },
               "target_closing_date": {
                 "type": "string",
                 "description": "ISO8601 target or expected closing date, empty string if not established"
               },
               "days_to_closing": {
                 "type": "number",
                 "description": "Number of days until target closing, -1 if not known"
               },
               "open_items": {
                 "type": "array",
                 "description": "Outstanding items that need resolution before this deal can progress",
                 "items": {
                   "type": "string",
                   "description": "A single open item in this transaction"
                 }
               },
               "deal_health": {
                 "type": "string",
                 "description": "Overall health of this transaction based on email signals",
                 "enum": ["on_track", "needs_attention", "at_risk", "stalled", "unknown"]
               }
             },
             "required": [
               "property", "transaction_type", "client_name", "stage",
               "last_activity_date", "last_activity_summary", "next_step",
               "next_step_owner", "target_closing_date", "days_to_closing",
               "open_items", "deal_health"
             ]
           }
         },
         "at_risk_count": {
           "type": "number",
           "description": "Number of deals rated as at_risk or stalled"
         },
         "closing_this_month_count": {
           "type": "number",
           "description": "Number of deals with a target closing date within the next 30 days"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of the overall pipeline health and most urgent items"
         }
       },
       "required": [
         "as_of", "deals", "at_risk_count", "closing_this_month_count", "summary"
       ]
     }
   }

4. Present deals ordered by days_to_closing ascending, with at_risk and
   stalled deals flagged. Lead with closing_this_month count and at_risk
   count.

5. Ask: "Would you like me to draft follow-up messages for any stalled
   or at-risk transactions?"
