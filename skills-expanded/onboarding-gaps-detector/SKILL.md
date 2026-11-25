---
name: onboarding-gaps-detector
description: Finds gaps, delays, and unresolved issues in the onboarding journey for new customers by scanning onboarding-related email threads. Use when a CSM wants to identify which customers are stuck in onboarding or where the onboarding process is consistently breaking down. Triggers on "onboarding gaps", "stuck in onboarding", "onboarding issues", "new customer setup problems", "onboarding delays", "what's blocking onboarding".
metadata:
  version: 1.0.0
---

# Onboarding Gaps Detector

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans onboarding-related email threads for new customers to find gaps —
missed steps, unanswered setup questions, delayed responses, blocked
integrations, confusion about next steps, and any pattern suggesting a
customer's onboarding is stalling or at risk.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 6 months", "the last 90 days", "May 2024",
     "since launch"). Default: the last 6 months. Keep the user's
     natural phrasing for use in the ask input; convert to ISO dates
     separately for the search call.
   - [account_scope] — either "all" (default) or the name of a specific
     new customer to focus on.
   - [account_clause] — derived. When [account_scope] is not "all", set
     to " for account [account_scope]". When [account_scope] is "all",
     set to empty string.

2. Call search with:
   - query: onboarding setup getting started welcome integration configure
     training access credentials
     (if [account_scope] is not "all", append the account name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all onboarding-related email threads from [time_range][account_clause]. For each new customer being onboarded, identify every gap or issue in their onboarding journey: unanswered setup questions, delayed responses from our side, blocked integrations or access issues, steps that appear to have been skipped, confusion about what to do next, and any point where onboarding momentum stalled. Also look for any pattern across multiple customers suggesting a systemic onboarding weakness.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Onboarding gap analysis for new customers",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "customer_gaps": {
           "type": "array",
           "description": "List of onboarding gaps found per customer",
           "items": {
             "type": "object",
             "description": "Onboarding gaps for a single customer",
             "additionalProperties": false,
             "properties": {
               "customer": {
                 "type": "string",
                 "description": "Name of the customer company being onboarded"
               },
               "onboarding_started": {
                 "type": "string",
                 "description": "ISO8601 date when onboarding communications began"
               },
               "onboarding_status": {
                 "type": "string",
                 "description": "Overall status of this customer's onboarding",
                 "enum": ["on_track", "stalled", "at_risk", "completed", "unknown"]
               },
               "gaps": {
                 "type": "array",
                 "description": "List of specific onboarding gaps or issues for this customer",
                 "items": {
                   "type": "object",
                   "description": "A single onboarding gap or issue",
                   "additionalProperties": false,
                   "properties": {
                     "gap_type": {
                       "type": "string",
                       "description": "Category of onboarding gap",
                       "enum": [
                         "unanswered_question", "delayed_response", "access_issue",
                         "integration_blocker", "skipped_step", "confusion_about_next_steps",
                         "missing_training", "technical_issue", "other"
                       ]
                     },
                     "description": {
                       "type": "string",
                       "description": "Clear description of this onboarding gap"
                     },
                     "days_unresolved": {
                       "type": "number",
                       "description": "Number of days this gap has been open without resolution"
                     },
                     "severity": {
                       "type": "string",
                       "description": "How much this gap is impeding the customer's onboarding progress",
                       "enum": ["critical", "high", "medium", "low"]
                     },
                     "recommended_action": {
                       "type": "string",
                       "description": "Recommended step to resolve this onboarding gap"
                     }
                   },
                   "required": [
                     "gap_type", "description", "days_unresolved",
                     "severity", "recommended_action"
                   ]
                 }
               }
             },
             "required": [
               "customer", "onboarding_started", "onboarding_status", "gaps"
             ]
           }
         },
         "systemic_patterns": {
           "type": "array",
           "description": "Recurring gap types or issues found across multiple customers suggesting a systemic onboarding weakness",
           "items": {
             "type": "string",
             "description": "A systemic pattern or recurring issue identified across multiple onboarding journeys"
           }
         },
         "stalled_count": {
           "type": "number",
           "description": "Number of customers whose onboarding has stalled or is at risk"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of onboarding health and key systemic issues found"
         }
       },
       "required": [
         "as_of", "customer_gaps", "systemic_patterns", "stalled_count", "summary"
       ]
     }
   }

4. Present stalled and at_risk customers first. Lead with stalled count and
   the most critical individual gap. Highlight systemic patterns prominently
   as they indicate process improvements needed.

5. Ask: "Would you like me to draft a check-in email for any customers whose
   onboarding has stalled?"
