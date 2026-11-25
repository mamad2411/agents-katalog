---
name: it-vendor-commitment-tracker
description: Tracks every commitment made by IT vendors and managed service providers from email — support SLA promises, implementation timelines, patch delivery commitments, uptime guarantees, and training deliverables — surfacing those that are unverified or at risk of being missed. Use when an IT manager wants to hold technology vendors accountable to what they committed. Triggers on "IT vendor commitments", "what has the vendor promised", "vendor SLA commitments", "MSP commitments", "vendor accountability IT", "what support did they promise".
metadata:
  version: 1.0.0
---

# IT Vendor Commitment Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all IT vendor and managed service provider email threads to extract
every commitment made — support response time promises, implementation
milestones, patch and update delivery schedules, uptime guarantees, training
commitments, and any other formal or informal assurance — and tracks
whether each has been delivered or remains open.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last quarter", "May 2024",
     "since the new MSP started"). Default: the last 90 days. Keep the
     user's natural phrasing for use in the ask input; convert to ISO
     dates separately for the search call.
   - [vendor_scope] — either "all" (default) or the name of a specific
     IT vendor or MSP to focus on.
   - [vendor_clause] — derived. When [vendor_scope] is not "all", set
     to " for vendor [vendor_scope]". When [vendor_scope] is "all", set
     to empty string.

2. Call search with:
   - query: SLA response time uptime commit deliver implement patch update
     training support guarantee promise timeline vendor MSP
     (if [vendor_scope] is not "all", append the vendor name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all IT vendor and managed service provider email threads from [time_range][vendor_clause]. For each vendor, extract every commitment they made — support response time promises, implementation and delivery timelines, patch and update schedules, uptime or availability guarantees, training and onboarding commitments, and any other formal or informal assurance given by the vendor. For each commitment determine whether it has been fulfilled based on email evidence or whether it remains open.
   - output_format:
   {
   "strict": true,
   "schema": {
   "type": "object",
   "description": "IT vendor commitment tracker across all technology vendor relationships",
   "additionalProperties": false,
   "properties": {
   "as_of": {
   "type": "string",
   "description": "ISO8601 date when this report was generated"
   },
   "commitments": {
   "type": "array",
   "description": "List of every IT vendor commitment found across email threads",
   "items": {
   "type": "object",
   "description": "A single IT vendor commitment with fulfillment tracking",
   "additionalProperties": false,
   "properties": {
   "vendor": {
   "type": "string",
   "description": "Name of the IT vendor or managed service provider"
   },
   "commitment_description": {
   "type": "string",
   "description": "Clear description of what the vendor committed to"
   },
   "commitment_type": {
   "type": "string",
   "description": "Category of IT vendor commitment",
   "enum": [
   "support_sla", "implementation_timeline", "patch_delivery",
   "uptime_guarantee", "training_delivery", "feature_roadmap",
   "security_update", "response_time", "escalation_path", "other"
   ]
   },
   "made_on": {
   "type": "string",
   "description": "ISO8601 date the commitment was made"
   },
   "due_by": {
   "type": "string",
   "description": "ISO8601 date by which the commitment should be fulfilled, empty string if ongoing"
   },
   "evidence": {
   "type": "string",
   "description": "Quote or paraphrase from email documenting this commitment"
   },
   "fulfillment_status": {
   "type": "string",
   "description": "Current fulfillment status based on email evidence",
   "enum": ["fulfilled", "open", "at_risk", "missed", "ongoing", "unknown"]
   },
   "days_until_due": {
   "type": "number",
   "description": "Number of days until the commitment is due, negative if past due, -1 if ongoing"
   },
   "sla_breach": {
   "type": "boolean",
   "description": "Whether this commitment represents a confirmed or likely SLA breach"
   },
   "risk_level": {
   "type": "string",
   "description": "Risk to IT operations if this commitment is not fulfilled",
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
   "sla_breach", "risk_level", "recommended_action"
   ]
   }
   },
   "sla_breach_count": {
   "type": "number",
   "description": "Number of confirmed or likely SLA breaches across all vendors"
   },
   "at_risk_count": {
   "type": "number",
   "description": "Number of commitments rated as at_risk or missed"
   },
   "by_vendor": {
   "type": "array",
   "description": "Commitment reliability summary grouped by vendor",
   "items": {
   "type": "object",
   "description": "Commitment summary for a single IT vendor",
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
   "sla_breach_count": {
   "type": "number",
   "description": "Number of SLA breaches for this vendor"
   },
   "reliability_signal": {
   "type": "string",
   "description": "Overall reliability signal for this vendor based on commitment history",
   "enum": ["reliable", "mostly_reliable", "inconsistent", "unreliable", "unknown"]
   }
   },
   "required": ["vendor", "open_count", "sla_breach_count", "reliability_signal"]
   }
   },
   "summary": {
   "type": "string",
   "description": "One or two sentence summary of IT vendor commitment health and most critical gaps"
   }
   },
   "required": [
   "as_of", "commitments", "sla_breach_count",
   "at_risk_count", "by_vendor", "summary"
   ]
   }
   }

4. Present SLA breaches and at_risk commitments first, ordered by risk_level.
   Lead with sla_breach count and at_risk count.

5. Ask: "Would you like me to draft a formal SLA breach notice or vendor
   escalation email for any of these items?"