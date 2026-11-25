---
name: supplier-risk-signals
description: Scans vendor and supplier email threads for early warning signals of supplier risk — financial instability hints, capacity constraints, quality deterioration, key contact turnover, communication breakdown, and dependency concentration risk. Use when a procurement manager wants a proactive risk scan of their supplier base. Triggers on "supplier risk", "vendor risk signals", "supplier early warning", "supply chain risk", "which vendors are risky", "supplier risk assessment".
metadata:
  version: 1.0.0
---

# Supplier Risk Signals

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Reads vendor and supplier email threads for the early warning signals that
experienced procurement managers recognize as precursors to supplier failure
— capacity constraints, financial pressure language, key contact changes,
quality degradation patterns, and communication deterioration — and returns
a structured risk register.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last quarter", "May 2024",
     "since the supply chain disruption"). Default: the last 90 days.
     Keep the user's natural phrasing for use in the ask input; convert
     to ISO dates separately for the search call.
   - [category_scope] — either "all" (default) or a specific supplier
     category to focus on.
   - [category_clause] — derived. When [category_scope] is not "all",
     set to " for [category_scope] vendors". When [category_scope] is
     "all", set to empty string.

2. Call search with:
   - query: capacity constraint shortage delay restructuring changes
     departing new contact quality issues financial pressure supply chain
     (if [category_scope] is not "all", append the category to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all vendor and supplier email threads from [time_range][category_clause]. Identify early warning signals of supplier risk for each vendor — hints of financial pressure or instability, capacity or supply constraints mentioned, quality degradation patterns, key contact changes or turnover, communication delays or deterioration, delivery pattern changes, and any language suggesting the vendor may be under stress or unreliable. Also flag any suppliers where we have dangerous single-source dependency based on email context.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Supplier risk register based on early warning signals from email",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "risk_signals": {
           "type": "array",
           "description": "List of every supplier risk signal detected across vendor email threads",
           "items": {
             "type": "object",
             "description": "A single supplier risk signal with context and recommended response",
             "additionalProperties": false,
             "properties": {
               "vendor": {
                 "type": "string",
                 "description": "Name of the vendor or supplier showing this risk signal"
               },
               "risk_type": {
                 "type": "string",
                 "description": "Category of supplier risk",
                 "enum": [
                   "financial_instability", "capacity_constraint", "quality_deterioration",
                   "key_contact_turnover", "communication_breakdown", "delivery_pattern_change",
                   "single_source_dependency", "pricing_volatility", "regulatory_issue", "other"
                 ]
               },
               "description": {
                 "type": "string",
                 "description": "Clear description of what the risk signal is and why it is a concern"
               },
               "evidence": {
                 "type": "string",
                 "description": "Quote or paraphrase from email that surfaces this risk signal"
               },
               "date": {
                 "type": "string",
                 "description": "ISO8601 date when this signal first appeared"
               },
               "severity": {
                 "type": "string",
                 "description": "Potential severity if this risk materializes into a supply disruption",
                 "enum": ["critical", "high", "medium", "low"]
               },
               "business_impact": {
                 "type": "string",
                 "description": "What business impact a failure of this supplier would cause"
               },
               "mitigation_options": {
                 "type": "array",
                 "description": "Potential mitigation actions to reduce exposure to this supplier risk",
                 "items": {
                   "type": "string",
                   "description": "A single mitigation option"
                 }
               },
               "recommended_action": {
                 "type": "string",
                 "description": "Recommended immediate action to assess or mitigate this risk"
               }
             },
             "required": [
               "vendor", "risk_type", "description", "evidence", "date",
               "severity", "business_impact", "mitigation_options", "recommended_action"
             ]
           }
         },
         "by_vendor": {
           "type": "array",
           "description": "Risk summary grouped by vendor showing overall risk profile",
           "items": {
             "type": "object",
             "description": "Risk summary for a single vendor",
             "additionalProperties": false,
             "properties": {
               "vendor": {
                 "type": "string",
                 "description": "Name of the vendor"
               },
               "signal_count": {
                 "type": "number",
                 "description": "Number of risk signals detected for this vendor"
               },
               "highest_severity": {
                 "type": "string",
                 "description": "Highest severity level found across all signals for this vendor",
                 "enum": ["critical", "high", "medium", "low"]
               },
               "overall_risk_rating": {
                 "type": "string",
                 "description": "Overall risk rating for this supplier relationship",
                 "enum": ["critical", "high", "medium", "low", "monitor"]
               }
             },
             "required": ["vendor", "signal_count", "highest_severity", "overall_risk_rating"]
           }
         },
         "critical_vendor_count": {
           "type": "number",
           "description": "Number of vendors rated at critical overall risk"
         },
         "single_source_dependencies": {
           "type": "array",
           "description": "Vendors identified as single-source dependencies with no apparent backup supplier",
           "items": {
             "type": "string",
             "description": "Name of a vendor representing a single-source dependency risk"
           }
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of overall supplier risk landscape and most critical exposures"
         }
       },
       "required": [
         "as_of", "risk_signals", "by_vendor", "critical_vendor_count",
         "single_source_dependencies", "summary"
       ]
     }
   }

4. Present critical and high severity signals first, ordered by severity
   then by vendor overall risk rating. Lead with critical vendor count and
   single source dependencies.

5. Ask: "Would you like me to draft a supplier risk review or contingency
   planning brief for any critical vendors?"
