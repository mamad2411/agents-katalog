---
name: listing-expiry-tracker
description: Finds every active listing agreement referenced in email and surfaces those approaching expiry — including the expiry date, notice requirements, and whether the seller has indicated intent to renew or withdraw. Use when an agent wants to proactively manage listing agreement renewals before they lapse. Triggers on "listing expiry", "listing agreements expiring", "listings coming up for renewal", "which listings are expiring", "listing renewal", "expiring listings".
metadata:
  version: 1.0.0
---

# Listing Expiry Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans email for every active listing agreement, extracts expiry and renewal
dates, flags those approaching expiry, and surfaces any signals from the
seller about their intent — so agents can act before a listing lapses or
a competitor steps in.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 18 months", "the last 1.5 years", "May 2024",
     "since the listing season"). Default: the last 18 months. Keep
     the user's natural phrasing for use in the ask input; convert to
     ISO dates separately for the search call.
   - [scope] — either "all" (default) or a specific property or seller
     to focus on.
   - [scope_clause] — derived. When [scope] is not "all", set to " for
     [scope]". When [scope] is "all", set to empty string.

2. Call search with:
   - query: listing agreement expires renew extension withdraw exclusive
     listing period seller
     (if [scope] is not "all", append the property or seller to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads from [time_range][scope_clause] referencing listing agreements. For each active listing identify: the property, the seller, the listing agreement start and expiry date, the type of listing agreement, any notice period required to cancel or extend, whether the seller has indicated any intent to renew, extend, withdraw, or relist with another agent, and how many days until the listing expires.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Listing expiry tracker for all active listing agreements",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "listings": {
           "type": "array",
           "description": "List of every active listing with expiry and renewal status",
           "items": {
             "type": "object",
             "description": "A single listing agreement with expiry details",
             "additionalProperties": false,
             "properties": {
               "property": {
                 "type": "string",
                 "description": "Address or description of the listed property"
               },
               "seller_name": {
                 "type": "string",
                 "description": "Name of the seller or listing client"
               },
               "listing_type": {
                 "type": "string",
                 "description": "Type of listing agreement",
                 "enum": [
                   "exclusive_right_to_sell", "exclusive_agency", "open_listing",
                   "net_listing", "pocket_listing", "other"
                 ]
               },
               "listed_date": {
                 "type": "string",
                 "description": "ISO8601 date the listing agreement began, empty string if unknown"
               },
               "expiry_date": {
                 "type": "string",
                 "description": "ISO8601 date the listing agreement expires, empty string if unknown"
               },
               "days_until_expiry": {
                 "type": "number",
                 "description": "Number of days until the listing expires, -1 if unknown"
               },
               "notice_period_days": {
                 "type": "number",
                 "description": "Days of notice required to cancel or not renew, 0 if not mentioned"
               },
               "action_deadline": {
                 "type": "string",
                 "description": "ISO8601 date by which the agent must act to secure renewal or extension"
               },
               "seller_intent_signal": {
                 "type": "string",
                 "description": "Any signal from the seller about their renewal or relisting intent",
                 "enum": [
                   "likely_to_renew", "likely_to_withdraw", "considering_other_agents",
                   "wants_price_reduction", "no_signal", "unknown"
                 ]
               },
               "list_price": {
                 "type": "number",
                 "description": "Current listing price, 0 if not found"
               },
               "currency": {
                 "type": "string",
                 "description": "Currency of the listing price"
               },
               "urgency": {
                 "type": "string",
                 "description": "Urgency level for the agent to take action on this listing",
                 "enum": ["critical", "high", "medium", "low"]
               },
               "recommended_action": {
                 "type": "string",
                 "description": "Recommended next step to protect or renew this listing"
               }
             },
             "required": [
               "property", "seller_name", "listing_type", "listed_date",
               "expiry_date", "days_until_expiry", "notice_period_days",
               "action_deadline", "seller_intent_signal", "list_price",
               "currency", "urgency", "recommended_action"
             ]
           }
         },
         "expiring_within_30_days": {
           "type": "number",
           "description": "Number of listings expiring within the next 30 days"
         },
         "at_risk_of_withdrawal": {
           "type": "number",
           "description": "Number of listings where the seller has signaled they may withdraw or relist elsewhere"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of upcoming listing expiries and most urgent actions"
         }
       },
       "required": [
         "as_of", "listings", "expiring_within_30_days",
         "at_risk_of_withdrawal", "summary"
       ]
     }
   }

4. Present ordered by urgency then by days until expiry. Lead with
   expiring_within_30_days and at_risk_of_withdrawal counts.

5. Ask: "Would you like me to draft a listing renewal conversation email
   for any of these sellers?"
