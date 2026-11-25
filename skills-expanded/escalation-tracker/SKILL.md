---
name: escalation-tracker
description: Finds every customer escalation across email threads — open complaints, unresolved support issues, executive escalations, and SLA breaches — and tracks their current status. Use when a CSM or support manager wants a full view of active escalations. Triggers on "active escalations", "open complaints", "escalation tracker", "what escalations are open", "unresolved issues", "customer escalations".
metadata:
  version: 1.0.0
---

# Escalation Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans customer email threads for every escalation — explicit escalation
requests, unresolved complaints that have grown in severity, executive
involvement, SLA breach mentions, and any issue where the customer's
language or behavior signals they are past normal support tolerance.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 60 days", "the last 2 months", "May 2024",
     "since the incident"). Default: the last 60 days. Keep the user's
     natural phrasing for use in the ask input; convert to ISO dates
     separately for the search call.
   - [account_scope] — either "all" (default) or the name of a specific
     customer account to focus on.
   - [account_clause] — derived. When [account_scope] is not "all", set
     to " for account [account_scope]". When [account_scope] is "all",
     set to empty string.

2. Call search with:
   - query: escalate urgent critical unacceptable SLA breach executive
     complaint unresolved frustrated
     (if [account_scope] is not "all", append the account name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all customer email threads from [time_range][account_clause]. Identify every active escalation — explicit requests to escalate, complaints that have gone unresolved and grown in severity, situations where an executive was looped in, SLA breach mentions, and any issue where the customer's language indicates they are past normal patience. For each escalation note the customer, the nature of the issue, how long it has been open, who is involved on both sides, and the current status.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Active escalation tracker across all customer accounts",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "escalations": {
           "type": "array",
           "description": "List of every active escalation found in customer email threads",
           "items": {
             "type": "object",
             "description": "A single active customer escalation with full context",
             "additionalProperties": false,
             "properties": {
               "customer": {
                 "type": "string",
                 "description": "Name of the customer company"
               },
               "contact": {
                 "type": "string",
                 "description": "Name or role of the primary customer contact in this escalation"
               },
               "escalation_type": {
                 "type": "string",
                 "description": "Category of escalation",
                 "enum": [
                   "explicit_escalation_request", "unresolved_complaint",
                   "executive_involvement", "sla_breach", "product_failure",
                   "billing_dispute", "service_quality", "other"
                 ]
               },
               "issue_description": {
                 "type": "string",
                 "description": "Clear description of what the escalation is about"
               },
               "opened_on": {
                 "type": "string",
                 "description": "ISO8601 date when this escalation first appeared in email"
               },
               "days_open": {
                 "type": "number",
                 "description": "Number of days this escalation has been unresolved"
               },
               "our_owner": {
                 "type": "string",
                 "description": "Name or role of the internal person responsible for resolving this escalation"
               },
               "severity": {
                 "type": "string",
                 "description": "How severe this escalation is based on customer language and business impact",
                 "enum": ["critical", "high", "medium", "low"]
               },
               "current_status": {
                 "type": "string",
                 "description": "Current state of this escalation based on most recent email",
                 "enum": ["open", "in_progress", "waiting_on_us", "waiting_on_customer", "resolved"]
               },
               "last_update_summary": {
                 "type": "string",
                 "description": "Brief summary of the most recent email activity on this escalation"
               },
               "recommended_action": {
                 "type": "string",
                 "description": "Recommended immediate action to progress or resolve this escalation"
               }
             },
             "required": [
               "customer", "contact", "escalation_type", "issue_description",
               "opened_on", "days_open", "our_owner", "severity",
               "current_status", "last_update_summary", "recommended_action"
             ]
           }
         },
         "critical_count": {
           "type": "number",
           "description": "Number of escalations at critical severity"
         },
         "waiting_on_us_count": {
           "type": "number",
           "description": "Number of escalations currently waiting on an internal response or action"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of active escalations and most urgent items"
         }
       },
       "required": [
         "as_of", "escalations", "critical_count", "waiting_on_us_count", "summary"
       ]
     }
   }

4. Present critical escalations first, then waiting_on_us items, then the
   rest by days open. Lead with critical count and waiting_on_us count.

5. Ask: "Would you like me to draft a customer-facing update for any of
   these escalations?"
