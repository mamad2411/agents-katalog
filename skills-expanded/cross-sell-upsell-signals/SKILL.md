---
name: cross-sell-upsell-signals
description: Finds buying signals, adjacent problem mentions, budget hints, and expansion interest in existing customer email threads. Use when a salesperson wants to identify upsell or cross-sell opportunities within their current customer base. Triggers on "cross-sell opportunities", "upsell signals", "which customers might want more", "expansion opportunities", "what else can I sell them".
metadata:
  version: 1.0.0
---

# Cross-Sell and Upsell Signals

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans email threads with existing customers to find signals they have adjacent
problems, growing needs, budget availability, or explicit interest in expanding
— things they mentioned without being asked.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 180 days", "the last 6 months", "May 2024",
     "since the last QBR"). Default: the last 180 days. Keep the user's
     natural phrasing for use in the ask input; convert to ISO dates
     separately for the search call.
   - [account_scope] — either "all" (default) or the name of a specific
     customer account to focus on.
   - [account_clause] — derived. When [account_scope] is not "all", set
     to " for account [account_scope]". When [account_scope] is "all",
     set to empty string.

2. Call search with:
   - query: need problem challenge budget growth expand additional
     (if [account_scope] is not "all", append the account name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads with existing customers from [time_range][account_clause]. For each customer, identify any signal they may be ready for an upsell or cross-sell: mentions of problems we could solve, references to budget or new initiatives, expressions of satisfaction suggesting trust, questions about features beyond what they have, or language suggesting growing needs.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Cross-sell and upsell opportunity report across the customer base",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "opportunities": {
           "type": "array",
           "description": "List of expansion opportunities identified across customer email threads",
           "items": {
             "type": "object",
             "description": "A single expansion opportunity for a specific customer",
             "additionalProperties": false,
             "properties": {
               "customer": {
                 "type": "string",
                 "description": "Name of the customer company"
               },
               "signal_type": {
                 "type": "string",
                 "description": "Category of buying signal detected",
                 "enum": [
                   "adjacent_problem", "budget_hint", "expansion_interest",
                   "satisfaction_signal", "feature_question", "growth_language"
                 ]
               },
               "evidence": {
                 "type": "string",
                 "description": "Quote or paraphrase from the email that surfaces this opportunity"
               },
               "date": {
                 "type": "string",
                 "description": "ISO8601 date when this signal appeared"
               },
               "recommended_action": {
                 "type": "string",
                 "description": "Specific next step recommended to pursue this opportunity"
               },
               "confidence": {
                 "type": "string",
                 "description": "How strong and reliable this signal is",
                 "enum": ["high", "medium", "low"]
               }
             },
             "required": ["customer", "signal_type", "evidence", "date", "recommended_action", "confidence"]
           }
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of the top opportunities found"
         }
       },
       "required": ["as_of", "opportunities", "summary"]
     }
   }

4. Present grouped by customer, ordered by confidence. Lead with total count
   and the highest-confidence opportunity.
