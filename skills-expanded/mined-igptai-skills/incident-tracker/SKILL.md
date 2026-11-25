---
name: incident-tracker
description: Finds every IT incident, outage, system failure, and unresolved technical issue reported across email threads — tracking what broke, when, who is affected, current resolution status, and what is still open. Use when an IT manager wants a real-time incident view from email without checking a separate ticketing system. Triggers on "IT incidents", "open incidents", "system outages", "what's broken", "incident status", "IT issues tracker".
metadata:
  version: 1.0.0
---

# Incident Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all IT-related email threads for every incident, outage, system
failure, and unresolved technical issue — extracting what is affected,
who reported it, when it started, the current resolution status, and
whether a post-incident review has been flagged.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 60 days", "the last 2 months", "May 2024",
     "since the outage"). Default: the last 60 days. Keep the user's
     natural phrasing for use in the ask input; convert to ISO dates
     separately for the search call.
   - [system_scope] — either "all" (default) or a specific system or
     team to focus on.
   - [system_clause] — derived. When [system_scope] is not "all", set
     to " for [system_scope]". When [system_scope] is "all", set to
     empty string.

2. Call search with:
   - query: incident outage down failure error degraded not working
     unavailable broken system issue alert
     (if [system_scope] is not "all", append the system or team name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all IT-related email threads from [time_range][system_clause]. Identify every incident, outage, system failure, and unresolved technical issue reported. For each incident determine: what system or service was affected, who reported it, when it was first reported, the scope of impact, the current resolution status based on the most recent email, who owns resolution, and whether a post-incident review or root cause analysis has been mentioned.
   - output_format:
   {
   "strict": true,
   "schema": {
   "type": "object",
   "description": "IT incident tracker across all reported system issues and outages",
   "additionalProperties": false,
   "properties": {
   "as_of": {
   "type": "string",
   "description": "ISO8601 date when this report was generated"
   },
   "incidents": {
   "type": "array",
   "description": "List of every IT incident found in email threads",
   "items": {
   "type": "object",
   "description": "A single IT incident with full status tracking",
   "additionalProperties": false,
   "properties": {
   "incident_title": {
   "type": "string",
   "description": "Brief title describing the incident"
   },
   "system_affected": {
   "type": "string",
   "description": "Name of the system, service, or infrastructure component affected"
   },
   "incident_type": {
   "type": "string",
   "description": "Category of incident",
   "enum": [
   "outage", "degraded_performance", "security_incident",
   "data_issue", "integration_failure", "hardware_failure",
   "software_bug", "network_issue", "authentication_issue", "other"
   ]
   },
   "reported_by": {
   "type": "string",
   "description": "Name or role of the person who first reported this incident"
   },
   "reported_on": {
   "type": "string",
   "description": "ISO8601 date when the incident was first reported in email"
   },
   "users_affected": {
   "type": "string",
   "description": "Description of who or how many users are affected, empty string if unknown"
   },
   "severity": {
   "type": "string",
   "description": "Severity of this incident based on scope and business impact",
   "enum": ["critical", "high", "medium", "low"]
   },
   "status": {
   "type": "string",
   "description": "Current resolution status of this incident",
   "enum": [
   "open", "investigating", "fix_in_progress", "fix_deployed",
   "monitoring", "resolved", "post_incident_review_pending", "unknown"
   ]
   },
   "owner": {
   "type": "string",
   "description": "Name or role of the person or team responsible for resolution"
   },
   "days_open": {
   "type": "number",
   "description": "Number of days this incident has been open"
   },
   "last_update_summary": {
   "type": "string",
   "description": "Summary of the most recent email update on this incident"
   },
   "post_incident_review_flagged": {
   "type": "boolean",
   "description": "Whether a post-incident review or root cause analysis has been mentioned"
   },
   "recommended_action": {
   "type": "string",
   "description": "Recommended next step to resolve or progress this incident"
   }
   },
   "required": [
   "incident_title", "system_affected", "incident_type", "reported_by",
   "reported_on", "users_affected", "severity", "status", "owner",
   "days_open", "last_update_summary", "post_incident_review_flagged",
   "recommended_action"
   ]
   }
   },
   "critical_open_count": {
   "type": "number",
   "description": "Number of critical severity incidents that are still open"
   },
   "post_review_pending_count": {
   "type": "number",
   "description": "Number of resolved incidents with a post-incident review still pending"
   },
   "summary": {
   "type": "string",
   "description": "One or two sentence summary of active incident landscape and most critical items"
   }
   },
   "required": [
   "as_of", "incidents", "critical_open_count",
   "post_review_pending_count", "summary"
   ]
   }
   }

4. Present critical open incidents first, then by days_open descending.
   Lead with critical_open count and post_review_pending count.

5. Ask: "Would you like me to draft an incident status update or post-
   incident review kickoff email for any of these?"