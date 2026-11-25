---
name: vendor-escalation-log
description: Finds every vendor escalation, supplier complaint, and unresolved service failure across procurement email threads — tracking what the issue is, how long it has been open, who owns resolution, and what has been communicated to the vendor. Use when a procurement manager wants a full view of active vendor issues. Triggers on "vendor escalations", "supplier complaints", "vendor issues", "unresolved supplier problems", "vendor escalation log", "what vendor issues are open".
metadata:
  version: 1.0.0
---

# Vendor Escalation Log

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all vendor and supplier email threads for every escalation — delivery
failures, quality issues, invoicing disputes, SLA breaches, service failures,
and unresolved complaints — tracking each from first mention to current status
and flagging those requiring immediate escalation action.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last quarter", "May 2024",
     "since the SLA breach"). Default: the last 90 days. Keep the user's
     natural phrasing for use in the ask input; convert to ISO dates
     separately for the search call.
   - [vendor_scope] — either "all" (default) or the name of a specific
     vendor to focus on.
   - [vendor_clause] — derived. When [vendor_scope] is not "all", set
     to " for vendor [vendor_scope]". When [vendor_scope] is "all", set
     to empty string.

2. Call search with:
   - query: escalate issue complaint failure late missing wrong quality
     dispute invoice error unacceptable unresolved vendor supplier
     (if [vendor_scope] is not "all", append the vendor name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all vendor and supplier email threads from [time_range][vendor_clause]. Identify every escalation, complaint, and unresolved issue — delivery failures, quality problems, invoicing disputes, SLA breaches, service failures, and any situation where a vendor has not met their obligations. For each issue note the vendor, the nature of the problem, when it was first raised, how long it has been open, the current status, who owns resolution, and what has been communicated to the vendor.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Vendor escalation log tracking all open supplier issues and complaints",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this log was generated"
         },
         "escalations": {
           "type": "array",
           "description": "List of every active vendor escalation or unresolved issue",
           "items": {
             "type": "object",
             "description": "A single vendor escalation with full context and status",
             "additionalProperties": false,
             "properties": {
               "vendor": {
                 "type": "string",
                 "description": "Name of the vendor or supplier involved"
               },
               "issue_type": {
                 "type": "string",
                 "description": "Category of escalation or issue",
                 "enum": [
                   "delivery_failure", "quality_issue", "invoicing_dispute",
                   "sla_breach", "service_failure", "communication_failure",
                   "wrong_item", "short_shipment", "pricing_discrepancy", "other"
                 ]
               },
               "issue_description": {
                 "type": "string",
                 "description": "Clear description of what the issue is"
               },
               "first_raised_on": {
                 "type": "string",
                 "description": "ISO8601 date when this issue was first raised in email"
               },
               "days_open": {
                 "type": "number",
                 "description": "Number of days this issue has been unresolved"
               },
               "our_owner": {
                 "type": "string",
                 "description": "Name or role of the internal person responsible for resolving this escalation"
               },
               "severity": {
                 "type": "string",
                 "description": "How serious this issue is in terms of business impact",
                 "enum": ["critical", "high", "medium", "low"]
               },
               "current_status": {
                 "type": "string",
                 "description": "Current state of this escalation",
                 "enum": [
                   "open", "vendor_acknowledged", "resolution_in_progress",
                   "waiting_on_vendor", "waiting_on_internal", "resolved", "disputed"
                 ]
               },
               "last_vendor_communication": {
                 "type": "string",
                 "description": "Summary of the most recent communication with the vendor about this issue"
               },
               "financial_impact": {
                 "type": "number",
                 "description": "Estimated financial impact of this issue in local currency, 0 if not quantifiable"
               },
               "recommended_action": {
                 "type": "string",
                 "description": "Recommended next step to progress or resolve this escalation"
               }
             },
             "required": [
               "vendor", "issue_type", "issue_description", "first_raised_on",
               "days_open", "our_owner", "severity", "current_status",
               "last_vendor_communication", "financial_impact", "recommended_action"
             ]
           }
         },
         "critical_count": {
           "type": "number",
           "description": "Number of escalations at critical severity"
         },
         "waiting_on_vendor_count": {
           "type": "number",
           "description": "Number of escalations currently waiting on a vendor response or action"
         },
         "total_financial_impact": {
           "type": "number",
           "description": "Total estimated financial impact across all open escalations"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of active vendor escalations and most urgent items"
         }
       },
       "required": [
         "as_of", "escalations", "critical_count",
         "waiting_on_vendor_count", "total_financial_impact", "summary"
       ]
     }
   }

4. Present critical escalations first, then waiting_on_vendor items ordered
   by days_open. Lead with critical count, waiting_on_vendor count, and
   total financial impact.

5. Ask: "Would you like me to draft a formal escalation or resolution
   demand email to any of these vendors?"
