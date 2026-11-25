---
name: license-renewal-tracker
description: Finds every software license, SaaS subscription, and IT service contract approaching renewal or expiry from email — surfacing the deadline, seat count, cost, and whether a renewal decision needs to be made. Use when an IT manager wants to proactively manage the software renewal calendar and avoid unwanted auto-renewals or license lapses. Triggers on "license renewals", "software subscriptions expiring", "IT contract renewals", "SaaS renewal calendar", "which licenses are expiring", "license tracker".
metadata:
  version: 1.0.0
---

# License Renewal Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all IT vendor and software email threads to extract every license,
subscription, and IT service contract with an upcoming renewal or expiry —
surfacing the deadline, cost, seat count, and whether a review, renewal, or
cancellation decision needs to be made before it auto-renews.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 24 months", "the last 2 years", "May 2024",
     "since the SaaS migration"). Default: the last 24 months. Keep
     the user's natural phrasing for use in the ask input; convert to
     ISO dates separately for the search call.
   - [vendor_scope] — either "all" (default) or the name of a specific
     vendor or system to focus on.
   - [vendor_clause] — derived. When [vendor_scope] is not "all", set
     to " for vendor [vendor_scope]". When [vendor_scope] is "all", set
     to empty string.

2. Call search with:
   - query: license renew subscription expire seats maintenance support
     annual renewal auto-renew software contract
     (if [vendor_scope] is not "all", append the vendor or system name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all IT vendor and software email threads from [time_range][vendor_clause]. Identify every software license, SaaS subscription, and IT service contract that has a renewal or expiry date. For each one extract: the vendor and product name, the number of seats or units if mentioned, the annual or total cost if mentioned, the renewal or expiry date, the notice period required to cancel, whether it auto-renews, and any usage or satisfaction signals that could inform a renewal decision.
   - output_format:
   {
   "strict": true,
   "schema": {
   "type": "object",
   "description": "Software license and IT subscription renewal calendar",
   "additionalProperties": false,
   "properties": {
   "as_of": {
   "type": "string",
   "description": "ISO8601 date when this report was generated"
   },
   "licenses": {
   "type": "array",
   "description": "List of every software license or IT subscription with renewal tracking",
   "items": {
   "type": "object",
   "description": "A single license or subscription with renewal details",
   "additionalProperties": false,
   "properties": {
   "vendor": {
   "type": "string",
   "description": "Name of the software vendor or service provider"
   },
   "product": {
   "type": "string",
   "description": "Name of the software or service"
   },
   "license_type": {
   "type": "string",
   "description": "Type of license or subscription",
   "enum": [
   "saas_subscription", "perpetual_license", "maintenance_contract",
   "support_contract", "cloud_service", "security_tool",
   "development_tool", "productivity_suite", "other"
   ]
   },
   "seat_count": {
   "type": "number",
   "description": "Number of seats or licenses, 0 if not specified"
   },
   "annual_cost": {
   "type": "number",
   "description": "Annual cost in local currency, 0 if not found"
   },
   "currency": {
   "type": "string",
   "description": "Currency of the annual cost"
   },
   "renewal_date": {
   "type": "string",
   "description": "ISO8601 renewal or expiry date, empty string if unknown"
   },
   "days_until_renewal": {
   "type": "number",
   "description": "Number of days until renewal or expiry, -1 if unknown"
   },
   "notice_period_days": {
   "type": "number",
   "description": "Days of advance notice required to cancel or modify, 0 if not found"
   },
   "action_deadline": {
   "type": "string",
   "description": "ISO8601 date by which IT must act to avoid unwanted auto-renewal"
   },
   "auto_renews": {
   "type": "boolean",
   "description": "Whether this license auto-renews if no action is taken"
   },
   "usage_signal": {
   "type": "string",
   "description": "Any signals about whether this tool is actively used or valued",
   "enum": ["actively_used", "underused", "complaints_raised", "unknown"]
   },
   "renewal_recommendation": {
   "type": "string",
   "description": "Recommended renewal action based on email signals",
   "enum": [
   "renew_as_is", "renegotiate_seats_or_price",
   "evaluate_alternatives", "cancel", "unknown"
   ]
   },
   "urgency": {
   "type": "string",
   "description": "Urgency of making a renewal decision for this license",
   "enum": ["critical", "high", "medium", "low"]
   }
   },
   "required": [
   "vendor", "product", "license_type", "seat_count", "annual_cost",
   "currency", "renewal_date", "days_until_renewal", "notice_period_days",
   "action_deadline", "auto_renews", "usage_signal",
   "renewal_recommendation", "urgency"
   ]
   }
   },
   "expiring_within_30_days": {
   "type": "number",
   "description": "Number of licenses expiring or auto-renewing within the next 30 days"
   },
   "auto_renewal_risk_count": {
   "type": "number",
   "description": "Number of licenses at risk of unwanted auto-renewal if no action is taken"
   },
   "total_annual_spend": {
   "type": "number",
   "description": "Total annual cost across all identified licenses in local currency"
   },
   "summary": {
   "type": "string",
   "description": "One or two sentence summary of upcoming renewals and most urgent decisions"
   }
   },
   "required": [
   "as_of", "licenses", "expiring_within_30_days",
   "auto_renewal_risk_count", "total_annual_spend", "summary"
   ]
   }
   }

4. Present licenses ordered by urgency then action_deadline. Flag auto-
   renewal risks prominently. Lead with expiring_within_30_days count,
   auto_renewal_risk count, and total annual spend.

5. Ask: "Would you like me to draft a cancellation notice or renewal
   negotiation email for any of these vendors?"