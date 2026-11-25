---
name: retainer-usage-tracker
description: Tracks retainer hour and budget usage across active consulting retainer clients — how much has been used, what is remaining, whether any client is burning through their retainer unusually fast, and whether renewal conversations are needed. Use when a consultant wants to manage retainer utilization proactively. Triggers on "retainer usage", "how many hours have I used", "retainer balance", "retainer burn rate", "retainer renewal", "retainer tracker".
metadata:
  version: 1.0.0
---

# Retainer Usage Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans retainer client email threads to reconstruct usage patterns — work
requested and delivered, hours or budget referenced, retainer renewal
discussions, and any signals that a client is over-using or under-using
their retainer — so the consultant can manage each relationship proactively.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the current month", "May 2024",
     "since the renewal"). Default: the last 90 days. Keep the user's
     natural phrasing for use in the ask input; convert to ISO dates
     separately for the search call.
   - [client_scope] — either "all" (default) or the name of a specific
     retainer client to focus on.
   - [client_clause] — derived. When [client_scope] is not "all", set to
     " for client [client_scope]". When [client_scope] is "all", set to
     empty string.

2. Call search with:
   - query: retainer hours budget used remaining balance renewal monthly
     allocation this month included
     (if [client_scope] is not "all", append the client name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all retainer client email threads from [time_range][client_clause]. For each retainer client identify: the agreed retainer scope or hours if mentioned, what work has been requested and delivered under the retainer, any references to hours used or budget consumed, whether the client appears to be over-using or under-using the retainer, and whether a renewal or retainer adjustment conversation has been raised or is needed.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Retainer usage tracker across all active retainer engagements",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "retainers": {
           "type": "array",
           "description": "List of every active retainer engagement with usage status",
           "items": {
             "type": "object",
             "description": "Usage status for a single retainer client",
             "additionalProperties": false,
             "properties": {
               "client": {
                 "type": "string",
                 "description": "Name of the retainer client"
               },
               "retainer_type": {
                 "type": "string",
                 "description": "Type of retainer arrangement",
                 "enum": [
                   "hourly_bucket", "monthly_fixed", "project_based",
                   "availability_retainer", "unknown"
                 ]
               },
               "agreed_scope": {
                 "type": "string",
                 "description": "Description of what is included in this retainer as referenced in email, empty string if not found"
               },
               "agreed_hours_or_budget": {
                 "type": "string",
                 "description": "The agreed monthly hours or budget as stated in email, empty string if not found"
               },
               "renewal_date": {
                 "type": "string",
                 "description": "ISO8601 date the retainer renews or expires, empty string if unknown"
               },
               "days_until_renewal": {
                 "type": "number",
                 "description": "Number of days until the retainer renews, -1 if unknown"
               },
               "usage_signal": {
                 "type": "string",
                 "description": "Assessment of retainer usage based on email activity patterns",
                 "enum": [
                   "over_using", "on_track", "under_using", "unknown"
                 ]
               },
               "work_delivered_this_period": {
                 "type": "array",
                 "description": "Summary of work delivered under this retainer in the current period",
                 "items": {
                   "type": "string",
                   "description": "A single piece of work delivered or in progress"
                 }
               },
               "out_of_scope_requests": {
                 "type": "array",
                 "description": "Requests made by this client that appear to fall outside the retainer scope",
                 "items": {
                   "type": "string",
                   "description": "A single out-of-scope request"
                 }
               },
               "renewal_signal": {
                 "type": "string",
                 "description": "Whether the client has signaled intent about renewing the retainer",
                 "enum": [
                   "likely_to_renew", "uncertain", "at_risk", "renewal_discussed", "no_signal"
                 ]
               },
               "recommended_action": {
                 "type": "string",
                 "description": "Recommended action to manage this retainer relationship"
               }
             },
             "required": [
               "client", "retainer_type", "agreed_scope", "agreed_hours_or_budget",
               "renewal_date", "days_until_renewal", "usage_signal",
               "work_delivered_this_period", "out_of_scope_requests",
               "renewal_signal", "recommended_action"
             ]
           }
         },
         "over_using_count": {
           "type": "number",
           "description": "Number of retainer clients showing over-usage signals"
         },
         "at_risk_renewal_count": {
           "type": "number",
           "description": "Number of retainer clients where renewal is uncertain or at risk"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of retainer portfolio health and most urgent actions"
         }
       },
       "required": [
         "as_of", "retainers", "over_using_count", "at_risk_renewal_count", "summary"
       ]
     }
   }

4. Present over-using clients first, then at-risk renewals, then the rest
   ordered by days until renewal. Lead with over_using count and
   at_risk_renewal count.

5. Ask: "Would you like me to draft a retainer review or renewal email
   for any of these clients?"
