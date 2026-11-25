---
name: offer-status-tracker
description: Tracks the status of every active job offer from email — what has been sent, what is pending response, what has been accepted or declined, and what is in negotiation. Use when an HR manager wants a real-time view of all outstanding offers. Triggers on "offer status", "outstanding offers", "which offers are pending", "offer tracker", "who has accepted", "offer pipeline".
metadata:
  version: 1.0.0
---

# Offer Status Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Finds every job offer referenced in email, determines the current status of
each — sent, pending, accepted, declined, or in negotiation — and flags any
that have been outstanding too long without a response.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last 3 months", "May 2024",
     "since the comp band update"). Default: the last 90 days. Keep
     the user's natural phrasing for use in the ask input; convert to
     ISO dates separately for the search call.
   - [role_scope] — either "all" (default) or the name of a specific
     role to focus on.
   - [role_clause] — derived. When [role_scope] is not "all", set to
     " for role [role_scope]". When [role_scope] is "all", set to empty
     string.

2. Call search with:
   - query: offer letter compensation package accept decline negotiate
     start date salary signing
     (if [role_scope] is not "all", append the role name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all hiring-related email threads from [time_range][role_clause]. Identify every job offer that has been made or discussed. For each offer determine: the candidate name, the role, the date the offer was sent, the current status based on the most recent email, any negotiation points being discussed, the expected start date if mentioned, and whether this offer has been outstanding for an unusually long time without resolution.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Active job offer status tracker across all open roles",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "offers": {
           "type": "array",
           "description": "List of every job offer found in email with current status",
           "items": {
             "type": "object",
             "description": "A single job offer and its current status",
             "additionalProperties": false,
             "properties": {
               "candidate_name": {
                 "type": "string",
                 "description": "Full name of the candidate the offer was made to"
               },
               "role": {
                 "type": "string",
                 "description": "The position being offered"
               },
               "offer_sent_date": {
                 "type": "string",
                 "description": "ISO8601 date the offer was sent, empty string if not confirmed"
               },
               "status": {
                 "type": "string",
                 "description": "Current status of this offer",
                 "enum": [
                   "sent_awaiting_response", "in_negotiation", "verbally_accepted",
                   "formally_accepted", "declined", "withdrawn", "expired", "unknown"
                 ]
               },
               "days_outstanding": {
                 "type": "number",
                 "description": "Number of days since the offer was sent with no final resolution"
               },
               "negotiation_points": {
                 "type": "array",
                 "description": "Active negotiation items being discussed for this offer",
                 "items": {
                   "type": "string",
                   "description": "A single negotiation point such as salary, equity, start date, or benefits"
                 }
               },
               "expected_start_date": {
                 "type": "string",
                 "description": "ISO8601 expected start date if mentioned, empty string if unknown"
               },
               "urgency": {
                 "type": "string",
                 "description": "How urgently this offer needs attention to avoid losing the candidate",
                 "enum": ["high", "medium", "low"]
               },
               "recommended_action": {
                 "type": "string",
                 "description": "Recommended next step for this offer"
               }
             },
             "required": [
               "candidate_name", "role", "offer_sent_date", "status",
               "days_outstanding", "negotiation_points", "expected_start_date",
               "urgency", "recommended_action"
             ]
           }
         },
         "pending_count": {
           "type": "number",
           "description": "Number of offers currently awaiting a response or in negotiation"
         },
         "accepted_count": {
           "type": "number",
           "description": "Number of offers accepted in the period"
         },
         "declined_count": {
           "type": "number",
           "description": "Number of offers declined in the period"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of the current offer pipeline and any urgent items"
         }
       },
       "required": [
         "as_of", "offers", "pending_count", "accepted_count",
         "declined_count", "summary"
       ]
     }
   }

4. Present pending and in-negotiation offers first, ordered by urgency then
   days outstanding. Lead with pending count and the most time-sensitive offer.

5. Ask: "Would you like me to draft a follow-up or check-in message for
   any of these candidates?"
