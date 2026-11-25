---
name: access-request-tracker
description: Tracks every IT access request, permission change, and account provisioning item from email — what has been requested, by whom, whether it has been approved and fulfilled, and what is still pending. Use when an IT manager wants to clear the access request backlog or audit who has been granted what. Triggers on "access requests", "pending access", "who has requested access", "access provisioning", "permission requests", "account setup requests".
metadata:
  version: 1.0.0
---

# Access Request Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all IT and HR-related email threads for every access request,
permission change, and account provisioning item — extracting who requested
what, whether approval was obtained, whether IT has fulfilled the request,
and what is still sitting in the queue unactioned.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 60 days", "the last 2 months", "May 2024",
     "since the audit"). Default: the last 60 days. Keep the user's
     natural phrasing for use in the ask input; convert to ISO dates
     separately for the search call.
   - [system_scope] — either "all" (default) or a specific system, team,
     or resource to focus on.
   - [system_clause] — derived. When [system_scope] is not "all", set
     to " for [system_scope]". When [system_scope] is "all", set to
     empty string.

2. Call search with:
   - query: access request permission grant account setup provisioning
     approve credentials login system role
     (if [system_scope] is not "all", append the system or team name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads from [time_range][system_clause] involving IT access requests, permission changes, and account provisioning. For each request identify: who requested access, what system or resource they need access to, what level of access was requested, whether a manager or approver gave approval, whether IT has fulfilled the request, and whether the request is still pending or has gone unactioned.
   - output_format:
   {
   "strict": true,
   "schema": {
   "type": "object",
   "description": "IT access request tracker across all pending and recent provisioning requests",
   "additionalProperties": false,
   "properties": {
   "as_of": {
   "type": "string",
   "description": "ISO8601 date when this report was generated"
   },
   "requests": {
   "type": "array",
   "description": "List of every access or provisioning request found in email",
   "items": {
   "type": "object",
   "description": "A single access request with approval and fulfillment status",
   "additionalProperties": false,
   "properties": {
   "requester": {
   "type": "string",
   "description": "Name of the person requesting access"
   },
   "system_or_resource": {
   "type": "string",
   "description": "The system, application, or resource access was requested for"
   },
   "access_type": {
   "type": "string",
   "description": "Type of access or change requested",
   "enum": [
   "new_account", "role_change", "elevated_permissions",
   "read_access", "write_access", "admin_access",
   "vpn_access", "offboarding_removal", "other"
   ]
   },
   "requested_on": {
   "type": "string",
   "description": "ISO8601 date the request was made"
   },
   "approval_status": {
   "type": "string",
   "description": "Whether the request has been approved by the appropriate manager",
   "enum": ["approved", "pending_approval", "denied", "unknown"]
   },
   "approved_by": {
   "type": "string",
   "description": "Name or role of the approver, empty string if not yet approved"
   },
   "fulfillment_status": {
   "type": "string",
   "description": "Whether IT has fulfilled this request",
   "enum": ["fulfilled", "in_progress", "pending", "blocked", "unknown"]
   },
   "days_pending": {
   "type": "number",
   "description": "Number of days this request has been waiting for approval or fulfillment"
   },
   "urgency": {
   "type": "string",
   "description": "How urgently this access request needs to be fulfilled",
   "enum": ["high", "medium", "low"]
   },
   "blocker": {
   "type": "string",
   "description": "Anything blocking this request from being fulfilled, empty string if none"
   }
   },
   "required": [
   "requester", "system_or_resource", "access_type", "requested_on",
   "approval_status", "approved_by", "fulfillment_status",
   "days_pending", "urgency", "blocker"
   ]
   }
   },
   "pending_approval_count": {
   "type": "number",
   "description": "Number of requests still waiting for manager approval"
   },
   "pending_fulfillment_count": {
   "type": "number",
   "description": "Number of approved requests not yet fulfilled by IT"
   },
   "overdue_count": {
   "type": "number",
   "description": "Number of requests that have been pending for more than 5 business days"
   },
   "summary": {
   "type": "string",
   "description": "One or two sentence summary of access request backlog and most urgent items"
   }
   },
   "required": [
   "as_of", "requests", "pending_approval_count",
   "pending_fulfillment_count", "overdue_count", "summary"
   ]
   }
   }

4. Present approved-but-unfulfilled requests first, then pending-approval
   requests, ordered by days_pending descending. Lead with pending_fulfillment
   count and overdue count.

5. Ask: "Would you like me to draft a fulfillment reminder or approval
   chase for any outstanding requests?"