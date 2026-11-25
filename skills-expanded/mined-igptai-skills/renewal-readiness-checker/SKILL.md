---
name: renewal-readiness-checker
description: Assesses how ready each customer is to renew based on their email sentiment, engagement level, open issues, and any renewal conversations already in progress. Use when a CSM wants to prioritize renewal efforts and understand where each account stands ahead of renewal. Triggers on "renewal readiness", "which customers will renew", "renewal risk", "who is ready to renew", "renewal pipeline", "renewal outlook".
metadata:
  version: 1.0.0
---

# Renewal Readiness Checker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Reviews email history with customers approaching renewal and produces a
readiness score for each — based on sentiment, engagement, open issues,
whether renewal has been discussed, and any signals that suggest the
renewal may be at risk.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 180 days", "the last 6 months", "May 2024",
     "since the last renewal"). Default: the last 180 days. Keep the
     user's natural phrasing for use in the ask input; convert to ISO
     dates separately for the search call.
   - [account_scope] — either "all" (default) or the name of a specific
     account to focus on.
   - [account_clause] — derived. When [account_scope] is not "all", set
     to " for account [account_scope]". When [account_scope] is "all",
     set to empty string.

2. Call search with:
   - query: renewal contract renew upcoming expiry continue agreement
     (if [account_scope] is not "all", append the account name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all customer email threads from [time_range][account_clause]. For each customer where a contract renewal is upcoming or has been discussed, assess their renewal readiness based on: overall sentiment in recent emails, level of engagement and responsiveness, any open issues or complaints that could affect renewal, whether renewal has been discussed directly, and any signals suggesting they are likely or unlikely to renew.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Renewal readiness assessment across customer accounts",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this assessment was generated"
         },
         "accounts": {
           "type": "array",
           "description": "List of customer accounts assessed for renewal readiness",
           "items": {
             "type": "object",
             "description": "Renewal readiness assessment for a single customer account",
             "additionalProperties": false,
             "properties": {
               "customer": {
                 "type": "string",
                 "description": "Name of the customer company"
               },
               "renewal_date": {
                 "type": "string",
                 "description": "ISO8601 estimated or known renewal date, empty string if unknown"
               },
               "days_to_renewal": {
                 "type": "number",
                 "description": "Number of days until renewal, -1 if unknown"
               },
               "readiness_score": {
                 "type": "string",
                 "description": "Overall renewal readiness assessment",
                 "enum": ["strong", "likely", "uncertain", "at_risk", "unlikely"]
               },
               "sentiment": {
                 "type": "string",
                 "description": "Overall customer sentiment based on recent email tone",
                 "enum": ["very_positive", "positive", "neutral", "negative", "very_negative"]
               },
               "engagement_level": {
                 "type": "string",
                 "description": "How actively engaged this customer has been in recent communications",
                 "enum": ["high", "medium", "low", "disengaged"]
               },
               "renewal_discussed": {
                 "type": "boolean",
                 "description": "Whether renewal has been explicitly discussed in email"
               },
               "open_issues": {
                 "type": "array",
                 "description": "Unresolved issues that could negatively affect renewal",
                 "items": {
                   "type": "string",
                   "description": "A single open issue affecting this renewal"
                 }
               },
               "positive_signals": {
                 "type": "array",
                 "description": "Positive indicators that support renewal",
                 "items": {
                   "type": "string",
                   "description": "A single positive renewal signal"
                 }
               },
               "recommended_action": {
                 "type": "string",
                 "description": "Recommended next step to progress or protect this renewal"
               }
             },
             "required": [
               "customer", "renewal_date", "days_to_renewal", "readiness_score",
               "sentiment", "engagement_level", "renewal_discussed",
               "open_issues", "positive_signals", "recommended_action"
             ]
           }
         },
         "at_risk_count": {
           "type": "number",
           "description": "Number of accounts with at_risk or unlikely renewal readiness"
         },
         "strong_count": {
           "type": "number",
           "description": "Number of accounts with strong or likely renewal readiness"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of the renewal pipeline health"
         }
       },
       "required": [
         "as_of", "accounts", "at_risk_count", "strong_count", "summary"
       ]
     }
   }

4. Present accounts ordered by days to renewal, with at_risk and unlikely
   accounts highlighted. Lead with at_risk count and the most urgent renewal.

5. Ask: "Would you like me to draft renewal outreach emails for any of
   these accounts?"
