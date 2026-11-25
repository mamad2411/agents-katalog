---
name: churn-signal-detector
description: Detects early warning churn signals across customer email threads — dissatisfaction language, reduced engagement, competitor mentions, escalating complaints, and disengagement patterns. Use when a customer success manager wants to know which customers are at risk of churning. Triggers on "churn signals", "which customers are at risk", "churn risk", "who might cancel", "at-risk customers", "churn early warning".
metadata:
  version: 1.0.0
---

# Churn Signal Detector

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all customer email threads for the language and behavioral patterns that
precede churn — dissatisfaction signals, complaints going unresolved, reduced
engagement, competitor mentions, and anything suggesting a customer's commitment
to the relationship is weakening.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last 3 months", "May 2024",
     "since the last QBR"). Default: the last 90 days. Keep the user's
     natural phrasing for use in the ask input; convert to ISO dates
     separately for the search call.
   - [account_scope] — either "all" (default) or the name of a specific
     customer account to focus on.
   - [account_clause] — derived. When [account_scope] is not "all", set
     to " for account [account_scope]". When [account_scope] is "all",
     set to empty string.

2. Call search with:
   - query: unhappy frustrated cancel disappointed alternative competitor
     considering switching not working not happy
     (if [account_scope] is not "all", append the account name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all customer email threads from [time_range][account_clause]. Identify every churn signal across all accounts — dissatisfaction language, unresolved complaints, mentions of competitors or alternatives, reduced response frequency, requests for cancellation information, escalating frustration, and any pattern where a customer's engagement or satisfaction appears to be declining. For each signal note the customer, the type of signal, the evidence, and how serious the churn risk appears.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Churn risk report across the customer base",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "churn_signals": {
           "type": "array",
           "description": "List of every churn signal detected across customer email threads",
           "items": {
             "type": "object",
             "description": "A single churn signal for a specific customer",
             "additionalProperties": false,
             "properties": {
               "customer": {
                 "type": "string",
                 "description": "Name of the customer company showing this churn signal"
               },
               "contact": {
                 "type": "string",
                 "description": "Name or role of the customer contact who expressed this signal"
               },
               "signal_type": {
                 "type": "string",
                 "description": "Category of churn signal",
                 "enum": [
                   "dissatisfaction_language", "unresolved_complaint",
                   "competitor_mention", "cancellation_inquiry",
                   "reduced_engagement", "escalating_frustration",
                   "feature_gap_complaint", "value_question", "other"
                 ]
               },
               "evidence": {
                 "type": "string",
                 "description": "Quote or paraphrase from email that surfaces this churn signal"
               },
               "date": {
                 "type": "string",
                 "description": "ISO8601 date when this signal appeared"
               },
               "churn_risk": {
                 "type": "string",
                 "description": "Assessment of how likely this customer is to churn based on signals found",
                 "enum": ["critical", "high", "medium", "low"]
               },
               "recommended_action": {
                 "type": "string",
                 "description": "Recommended immediate action to reduce churn risk for this customer"
               }
             },
             "required": [
               "customer", "contact", "signal_type", "evidence",
               "date", "churn_risk", "recommended_action"
             ]
           }
         },
         "at_risk_customers": {
           "type": "array",
           "description": "Deduplicated list of customers with at least one churn signal, ordered by risk",
           "items": {
             "type": "object",
             "description": "A single at-risk customer with aggregated risk assessment",
             "additionalProperties": false,
             "properties": {
               "customer": {
                 "type": "string",
                 "description": "Name of the customer company"
               },
               "highest_risk_level": {
                 "type": "string",
                 "description": "The highest churn risk level found for this customer",
                 "enum": ["critical", "high", "medium", "low"]
               },
               "signal_count": {
                 "type": "number",
                 "description": "Total number of churn signals detected for this customer"
               },
               "primary_concern": {
                 "type": "string",
                 "description": "The main reason this customer appears at risk in one sentence"
               }
             },
             "required": ["customer", "highest_risk_level", "signal_count", "primary_concern"]
           }
         },
         "critical_count": {
           "type": "number",
           "description": "Number of customers with critical churn risk"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of overall churn risk across the customer base"
         }
       },
       "required": [
         "as_of", "churn_signals", "at_risk_customers", "critical_count", "summary"
       ]
     }
   }

4. Present at-risk customers ordered by risk level first, then the detailed
   signals. Lead with critical count and the most at-risk account.

5. Ask: "Would you like me to draft a rescue outreach email for any of these
   customers?"
