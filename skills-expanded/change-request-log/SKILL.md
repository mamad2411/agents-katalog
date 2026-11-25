---
name: change-request-log
description: Extracts every IT change request from email — system upgrades, configuration changes, infrastructure modifications, deployment requests, and policy updates — tracking approval status, implementation status, and any changes that went ahead without proper approval. Use when an IT manager wants a change management log derived from email. Triggers on "change requests", "IT changes", "what system changes are pending", "change management log", "infrastructure changes", "deployment requests".
metadata:
  version: 1.0.0
---

# Change Request Log

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all IT email threads for change requests — system upgrades, configuration
changes, infrastructure modifications, deployment approvals, and policy
updates — and tracks each through the approval and implementation lifecycle,
flagging any that bypassed the approval process or remain in limbo.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 60 days", "the last 2 months", "May 2024",
     "since the freeze ended"). Default: the last 60 days. Keep the
     user's natural phrasing for use in the ask input; convert to ISO
     dates separately for the search call.
   - [system_scope] — either "all" (default) or a specific system to
     focus on.
   - [system_clause] — derived. When [system_scope] is not "all", set
     to " for [system_scope]". When [system_scope] is "all", set to
     empty string.

2. Call search with:
   - query: change request upgrade deploy configuration modify infrastructure
     approval CAB release rollout update patch
     (if [system_scope] is not "all", append the system name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all IT email threads from [time_range][system_clause]. Identify every change request — system upgrades, configuration changes, infrastructure modifications, deployment requests, policy updates, and any other formal or informal IT change. For each change note: what was requested, who requested it, what system it affects, when it was requested, whether approval was obtained, whether the change has been implemented, and whether any change appears to have been made without following the proper approval process.
   - output_format:
   {
   "strict": true,
   "schema": {
   "type": "object",
   "description": "IT change request log extracted from email threads",
   "additionalProperties": false,
   "properties": {
   "as_of": {
   "type": "string",
   "description": "ISO8601 date when this log was generated"
   },
   "change_requests": {
   "type": "array",
   "description": "List of every IT change request found in email",
   "items": {
   "type": "object",
   "description": "A single IT change request with approval and implementation tracking",
   "additionalProperties": false,
   "properties": {
   "change_title": {
   "type": "string",
   "description": "Brief title describing the change"
   },
   "change_type": {
   "type": "string",
   "description": "Category of IT change",
   "enum": [
   "system_upgrade", "configuration_change", "infrastructure_modification",
   "deployment", "security_patch", "policy_update", "integration_change",
   "access_policy_change", "hardware_change", "other"
   ]
   },
   "system_affected": {
   "type": "string",
   "description": "The system or infrastructure component this change affects"
   },
   "requested_by": {
   "type": "string",
   "description": "Name or role of the person requesting this change"
   },
   "requested_on": {
   "type": "string",
   "description": "ISO8601 date the change was requested"
   },
   "risk_level": {
   "type": "string",
   "description": "Risk level of this change to system stability or security",
   "enum": ["high", "medium", "low", "unknown"]
   },
   "approval_status": {
   "type": "string",
   "description": "Whether this change has been formally approved",
   "enum": [
   "approved", "pending_approval", "denied",
   "implemented_without_approval", "unknown"
   ]
   },
   "approved_by": {
   "type": "string",
   "description": "Name or role of the approver, empty string if not yet approved"
   },
   "implementation_status": {
   "type": "string",
   "description": "Current implementation status of this change",
   "enum": [
   "not_started", "scheduled", "in_progress",
   "implemented", "rolled_back", "on_hold", "unknown"
   ]
   },
   "scheduled_date": {
   "type": "string",
   "description": "ISO8601 date the change is scheduled for, empty string if not scheduled"
   },
   "bypass_flag": {
   "type": "boolean",
   "description": "Whether this change appears to have been implemented without proper approval"
   },
   "notes": {
   "type": "string",
   "description": "Any additional context about this change from email, empty string if none"
   }
   },
   "required": [
   "change_title", "change_type", "system_affected", "requested_by",
   "requested_on", "risk_level", "approval_status", "approved_by",
   "implementation_status", "scheduled_date", "bypass_flag", "notes"
   ]
   }
   },
   "pending_approval_count": {
   "type": "number",
   "description": "Number of change requests awaiting approval"
   },
   "bypass_count": {
   "type": "number",
   "description": "Number of changes that appear to have been implemented without proper approval"
   },
   "high_risk_pending_count": {
   "type": "number",
   "description": "Number of high-risk changes still awaiting approval or implementation"
   },
   "summary": {
   "type": "string",
   "description": "One or two sentence summary of the change request backlog and any compliance concerns"
   }
   },
   "required": [
   "as_of", "change_requests", "pending_approval_count",
   "bypass_count", "high_risk_pending_count", "summary"
   ]
   }
   }

4. Present bypass-flagged changes and high-risk pending approvals first.
   Lead with bypass count and high_risk_pending count. Flag any unapproved
   high-risk changes as requiring immediate attention.

5. Ask: "Would you like me to draft an approval request or change
   communication for any of these items?"