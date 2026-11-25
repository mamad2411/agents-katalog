---
name: vendor-commitment-tracker
description: Tracks every commitment made by vendors across active procurement relationships — delivery promises, SLA guarantees, price holds, product availability assurances, and service level commitments — surfacing those that are unconfirmed or at risk of not being met. Use when a procurement manager wants to hold vendors accountable to what they promised. Triggers on "vendor commitments", "what have vendors promised", "vendor accountability", "supplier commitments", "what did the vendor agree to", "vendor promises".
metadata:
  version: 1.0.0
---

# Vendor Commitment Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all vendor and supplier email threads to extract every commitment made
by a vendor — delivery dates promised, SLA guarantees given, price holds
agreed, stock availability confirmed — and tracks whether each has been
fulfilled or remains open and unverified.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last quarter", "May 2024",
     "since the master agreement"). Default: the last 90 days. Keep
     the user's natural phrasing for use in the ask input; convert to
     ISO dates separately for the search call.
   - [vendor_scope] — either "all" (default) or the name of a specific
     vendor to focus on.
   - [vendor_clause] — derived. When [vendor_scope] is not "all", set
     to " for vendor [vendor_scope]". When [vendor_scope] is "all", set
     to empty string.

2. Call search with:
   - query: commit deliver guarantee promise confirm by available stock
     price hold SLA service level vendor supplier
     (if [vendor_scope] is not "all", append the vendor name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all vendor and supplier email threads from [time_range][vendor_clause]. For each vendor, extract every commitment they made — delivery date promises, SLA guarantees, price holds, stock availability confirmations, service level commitments, and any other formal or informal assurance. For each commitment determine whether there is evidence of fulfillment in subsequent emails or whether it remains open and unverified.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Vendor commitment tracker across all active supplier relationships",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "commitments": {
           "type": "array",
           "description": "List of every vendor commitment found across supplier email threads",
           "items": {
             "type": "object",
             "description": "A single vendor commitment with fulfillment status",
             "additionalProperties": false,
             "properties": {
               "vendor": {
                 "type": "string",
                 "description": "Name of the vendor or supplier who made this commitment"
               },
               "commitment_description": {
                 "type": "string",
                 "description": "Clear description of what the vendor committed to"
               },
               "commitment_type": {
                 "type": "string",
                 "description": "Category of vendor commitment",
                 "enum": [
                   "delivery_date", "sla_guarantee", "price_hold", "stock_availability",
                   "quality_standard", "service_level", "lead_time", "exclusivity",
                   "support_response_time", "other"
                 ]
               },
               "made_on": {
                 "type": "string",
                 "description": "ISO8601 date the commitment was made"
               },
               "due_by": {
                 "type": "string",
                 "description": "ISO8601 date by which the commitment should be fulfilled, empty string if open-ended"
               },
               "evidence": {
                 "type": "string",
                 "description": "Quote or paraphrase from email documenting this commitment"
               },
               "fulfillment_status": {
                 "type": "string",
                 "description": "Current fulfillment status based on email evidence",
                 "enum": ["fulfilled", "open", "at_risk", "missed", "unknown"]
               },
               "days_until_due": {
                 "type": "number",
                 "description": "Number of days until the commitment is due, negative if already past due"
               },
               "risk_level": {
                 "type": "string",
                 "description": "Risk level if this commitment is not fulfilled on time",
                 "enum": ["critical", "high", "medium", "low"]
               },
               "recommended_action": {
                 "type": "string",
                 "description": "Recommended action to verify or enforce this commitment"
               }
             },
             "required": [
               "vendor", "commitment_description", "commitment_type", "made_on",
               "due_by", "evidence", "fulfillment_status", "days_until_due",
               "risk_level", "recommended_action"
             ]
           }
         },
         "at_risk_count": {
           "type": "number",
           "description": "Number of vendor commitments rated as at_risk or missed"
         },
         "by_vendor": {
           "type": "array",
           "description": "Summary of commitment status grouped by vendor",
           "items": {
             "type": "object",
             "description": "Commitment status summary for a single vendor",
             "additionalProperties": false,
             "properties": {
               "vendor": {
                 "type": "string",
                 "description": "Name of the vendor"
               },
               "open_count": {
                 "type": "number",
                 "description": "Number of open commitments from this vendor"
               },
               "at_risk_count": {
                 "type": "number",
                 "description": "Number of at-risk or missed commitments from this vendor"
               },
               "reliability_signal": {
                 "type": "string",
                 "description": "Overall reliability signal for this vendor based on commitment history",
                 "enum": ["reliable", "mostly_reliable", "inconsistent", "unreliable", "unknown"]
               }
             },
             "required": ["vendor", "open_count", "at_risk_count", "reliability_signal"]
           }
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of vendor commitment health and most critical open items"
         }
       },
       "required": ["as_of", "commitments", "at_risk_count", "by_vendor", "summary"]
     }
   }

4. Present at_risk and missed commitments first, ordered by risk_level then
   days_until_due. Lead with at_risk count and the most critical open item.

5. Ask: "Would you like me to draft a vendor accountability email for any
   at-risk or missed commitments?"
