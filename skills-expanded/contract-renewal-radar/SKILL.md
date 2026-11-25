---
name: contract-renewal-radar
description: Finds every vendor and supplier contract approaching its renewal or expiry date from email — surfacing the deadline, notice period, auto-renewal risk, and whether a renegotiation conversation should be initiated. Use when a procurement manager wants to proactively manage contract renewals and avoid unwanted auto-renewals. Triggers on "contract renewals", "expiring vendor contracts", "supplier contract expiry", "auto-renewal risk", "which contracts are coming up", "renewal radar".
metadata:
  version: 1.0.0
---

# Contract Renewal Radar

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans email for every vendor and supplier contract referenced, extracts
expiry and renewal dates, identifies notice periods, flags auto-renewal
risks, and returns a deadline-ordered calendar so procurement can act
before contracts renew unfavorably or lapse unexpectedly.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 24 months", "the last 2 years", "May 2024",
     "since procurement reset"). Default: the last 24 months. Keep the
     user's natural phrasing for use in the ask input; convert to ISO
     dates separately for the search call.
   - [category_scope] — either "all" (default) or a specific supplier
     category to focus on (e.g. "SaaS", "logistics", "raw materials").
   - [category_clause] — derived. When [category_scope] is not "all",
     set to " for [category_scope] vendors". When [category_scope] is
     "all", set to empty string.

2. Call search with:
   - query: contract renew expire notice period auto-renewal terminate
     extend renegotiate vendor supplier agreement
     (if [category_scope] is not "all", append the category to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all vendor and supplier email threads from [time_range][category_clause] that reference contracts or agreements. For each contract identify: the vendor, the type of agreement, the expiry or renewal date, the notice period required to cancel or renegotiate, whether the contract auto-renews, the annual value if mentioned, and whether a renegotiation or cancellation should be considered based on any satisfaction signals in the email thread.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Vendor contract renewal radar showing all upcoming expiries and renewal deadlines",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "contracts": {
           "type": "array",
           "description": "List of every vendor contract with renewal or expiry tracking",
           "items": {
             "type": "object",
             "description": "A single vendor contract with renewal deadline details",
             "additionalProperties": false,
             "properties": {
               "vendor": {
                 "type": "string",
                 "description": "Name of the vendor or supplier"
               },
               "contract_type": {
                 "type": "string",
                 "description": "Type of vendor agreement",
                 "enum": [
                   "saas_subscription", "service_agreement", "supply_contract",
                   "maintenance_contract", "licensing_agreement", "framework_agreement",
                   "master_service_agreement", "other"
                 ]
               },
               "description": {
                 "type": "string",
                 "description": "Brief description of what this contract covers"
               },
               "expiry_date": {
                 "type": "string",
                 "description": "ISO8601 date the contract expires or auto-renews, empty string if unknown"
               },
               "days_until_expiry": {
                 "type": "number",
                 "description": "Number of days until expiry or auto-renewal, -1 if unknown"
               },
               "notice_period_days": {
                 "type": "number",
                 "description": "Days of advance notice required to cancel or prevent auto-renewal, 0 if not found"
               },
               "action_deadline": {
                 "type": "string",
                 "description": "ISO8601 date by which procurement must act to avoid unwanted auto-renewal or expiry"
               },
               "auto_renews": {
                 "type": "boolean",
                 "description": "Whether this contract auto-renews if no action is taken"
               },
               "annual_value": {
                 "type": "number",
                 "description": "Annual contract value in local currency, 0 if not found"
               },
               "currency": {
                 "type": "string",
                 "description": "Currency of the annual value"
               },
               "satisfaction_signal": {
                 "type": "string",
                 "description": "Overall satisfaction with this vendor based on email signals",
                 "enum": ["positive", "neutral", "negative", "unknown"]
               },
               "renewal_recommendation": {
                 "type": "string",
                 "description": "Recommended action for this contract renewal",
                 "enum": [
                   "renew_as_is", "renegotiate_before_renewal", "evaluate_alternatives",
                   "cancel", "let_expire", "unknown"
                 ]
               },
               "urgency": {
                 "type": "string",
                 "description": "Urgency level for taking action on this contract",
                 "enum": ["critical", "high", "medium", "low"]
               }
             },
             "required": [
               "vendor", "contract_type", "description", "expiry_date",
               "days_until_expiry", "notice_period_days", "action_deadline",
               "auto_renews", "annual_value", "currency", "satisfaction_signal",
               "renewal_recommendation", "urgency"
             ]
           }
         },
         "critical_count": {
           "type": "number",
           "description": "Number of contracts requiring critical urgency action"
         },
         "auto_renewal_risk_count": {
           "type": "number",
           "description": "Number of contracts at risk of unwanted auto-renewal if no action is taken"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of upcoming renewals and most urgent actions"
         }
       },
       "required": [
         "as_of", "contracts", "critical_count", "auto_renewal_risk_count", "summary"
       ]
     }
   }

4. Present ordered by urgency then action_deadline. Lead with critical count
   and auto_renewal_risk count. Flag any contracts with negative satisfaction
   signals that are approaching auto-renewal.

5. Ask: "Would you like me to draft a cancellation notice or renegotiation
   request for any of these vendors?"
