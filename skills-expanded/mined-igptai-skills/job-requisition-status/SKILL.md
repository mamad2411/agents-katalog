---
name: job-requisition-status
description: Tracks the current status of every open job requisition from email — whether approval has been obtained, which roles are actively being sourced, where each requisition is in the hiring funnel, and which reqs have stalled without activity. Use when a recruiting manager wants a full requisition health view across the team. Triggers on "job requisition status", "open reqs", "req status", "which roles are approved", "hiring funnel by requisition", "req activity".
metadata:
  version: 1.0.0
---

# Job Requisition Status

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans recruiting and HR email threads to produce a requisition-level view
of every open role — approval status, whether sourcing has begun, pipeline
depth, hiring manager engagement, and any reqs that appear to have stalled
or gone cold without explanation.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last quarter", "May 2024",
     "since the headcount approval"). Default: the last 90 days. Keep
     the user's natural phrasing for use in the ask input; convert to
     ISO dates separately for the search call.
   - [scope] — either "all" (default) or the name of a specific
     department or hiring manager to focus on.
   - [scope_clause] — derived. When [scope] is not "all", set to " for
     [scope]". When [scope] is "all", set to empty string.

2. Call search with:
   - query: requisition req approved headcount role open position sourcing
     backfill new hire approved pipeline JD job description
     (if [scope] is not "all", append the department or hiring manager to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all recruiting and HR email threads from [time_range][scope_clause]. For every job requisition mentioned, determine: the role title, department, hiring manager, approval status, whether a job description has been finalized, whether active sourcing has begun, the depth of the current candidate pipeline, the most recent activity on this req, and whether the req appears to have stalled or is progressing normally.
   - output_format:
   {
   "strict": true,
   "schema": {
   "type": "object",
   "description": "Job requisition status tracker across all open roles",
   "additionalProperties": false,
   "properties": {
   "as_of": {
   "type": "string",
   "description": "ISO8601 date when this report was generated"
   },
   "requisitions": {
   "type": "array",
   "description": "List of every job requisition with current status",
   "items": {
   "type": "object",
   "description": "A single job requisition with full status tracking",
   "additionalProperties": false,
   "properties": {
   "role_title": {
   "type": "string",
   "description": "Title of the open role"
   },
   "department": {
   "type": "string",
   "description": "Department this role sits in, empty string if not mentioned"
   },
   "hiring_manager": {
   "type": "string",
   "description": "Name of the hiring manager for this role"
   },
   "req_type": {
   "type": "string",
   "description": "Whether this is a new position or a backfill",
   "enum": ["new_headcount", "backfill", "unknown"]
   },
   "approval_status": {
   "type": "string",
   "description": "Whether headcount approval has been obtained",
   "enum": ["approved", "pending_approval", "conditionally_approved", "unknown"]
   },
   "jd_status": {
   "type": "string",
   "description": "Status of the job description",
   "enum": ["finalized", "in_draft", "not_started", "unknown"]
   },
   "sourcing_status": {
   "type": "string",
   "description": "Whether active sourcing has begun for this req",
   "enum": ["actively_sourcing", "sourcing_not_started", "on_hold", "unknown"]
   },
   "pipeline_depth": {
   "type": "string",
   "description": "Assessment of how many active candidates are in the pipeline for this role",
   "enum": ["strong", "adequate", "thin", "empty", "unknown"]
   },
   "last_activity_date": {
   "type": "string",
   "description": "ISO8601 date of the most recent email activity on this req"
   },
   "days_since_activity": {
   "type": "number",
   "description": "Number of days since the last email activity on this req"
   },
   "req_health": {
   "type": "string",
   "description": "Overall health of this requisition based on activity and pipeline signals",
   "enum": ["on_track", "needs_attention", "stalled", "at_risk", "unknown"]
   },
   "blockers": {
   "type": "array",
   "description": "Any blockers preventing this req from progressing",
   "items": {
   "type": "string",
   "description": "A single blocker for this requisition"
   }
   },
   "recommended_action": {
   "type": "string",
   "description": "Recommended next step to unblock or accelerate this requisition"
   }
   },
   "required": [
   "role_title", "department", "hiring_manager", "req_type",
   "approval_status", "jd_status", "sourcing_status", "pipeline_depth",
   "last_activity_date", "days_since_activity", "req_health",
   "blockers", "recommended_action"
   ]
   }
   },
   "stalled_count": {
   "type": "number",
   "description": "Number of requisitions that have stalled or gone cold"
   },
   "thin_pipeline_count": {
   "type": "number",
   "description": "Number of approved reqs with a thin or empty candidate pipeline"
   },
   "pending_approval_count": {
   "type": "number",
   "description": "Number of reqs still awaiting headcount approval"
   },
   "summary": {
   "type": "string",
   "description": "One or two sentence summary of requisition portfolio health and most urgent items"
   }
   },
   "required": [
   "as_of", "requisitions", "stalled_count",
   "thin_pipeline_count", "pending_approval_count", "summary"
   ]
   }
   }

4. Present stalled and at_risk reqs first, then reqs with thin pipelines,
   then pending approvals. Lead with stalled count, thin pipeline count,
   and pending approval count.

5. Ask: "Would you like me to draft a recruiting kickoff email or sourcing
   plan for any stalled or thin-pipeline reqs?"