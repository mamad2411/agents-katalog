---
name: grant-deadline-tracker
description: Tracks every grant application, funding deadline, and submission requirement referenced in email — surfacing what is due, who is responsible for each section, what is still outstanding, and which deadlines are at risk. Use when a researcher or research administrator wants to ensure no grant deadline is missed. Triggers on "grant deadlines", "funding deadlines", "grant submissions", "what grants are due", "grant application status", "research funding deadlines".
metadata:
  version: 1.0.0
---

# Grant Deadline Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans email for every grant opportunity, funding call, and application
deadline — extracting submission dates, funder requirements, team section
assignments, internal review deadlines, and any outstanding items that
could put a submission at risk.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 12 months", "the last year", "May 2024",
     "since the funding cycle opened"). Default: the last 12 months.
     Keep the user's natural phrasing for use in the ask input; convert
     to ISO dates separately for the search call.
   - [scope] — either "all" (default) or the name of a specific funder,
     program, or project to focus on.
   - [scope_clause] — derived. When [scope] is not "all", set to " for
     [scope]". When [scope] is "all", set to empty string.

2. Call search with:
   - query: grant funding deadline submission LOI letter of intent RFP
     proposal funder award call application due stage
     (if [scope] is not "all", append the funder, program, or project to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads from [time_range][scope_clause] related to grant applications, funding opportunities, and research proposals. For each grant identify: the funder, the program or call name, the submission deadline, any internal review or draft deadlines referenced, the principal investigator and key team members, sections or components assigned to specific people, what is still outstanding, and whether the application is on track based on email activity and progress signals.
   - output_format:
   {
   "strict": true,
   "schema": {
   "type": "object",
   "description": "Grant application and funding deadline tracker from research email threads",
   "additionalProperties": false,
   "properties": {
   "as_of": {
   "type": "string",
   "description": "ISO8601 date when this report was generated"
   },
   "grants": {
   "type": "array",
   "description": "List of every grant application with deadline and status tracking",
   "items": {
   "type": "object",
   "description": "A single grant application with full deadline and progress tracking",
   "additionalProperties": false,
   "properties": {
   "grant_name": {
   "type": "string",
   "description": "Name or description of the grant or funding call"
   },
   "funder": {
   "type": "string",
   "description": "Name of the funding agency or organization"
   },
   "principal_investigator": {
   "type": "string",
   "description": "Name or role of the lead investigator for this application"
   },
   "submission_deadline": {
   "type": "string",
   "description": "ISO8601 date of the external submission deadline, empty string if unknown"
   },
   "days_until_deadline": {
   "type": "number",
   "description": "Number of days until the submission deadline, -1 if unknown"
   },
   "internal_review_deadline": {
   "type": "string",
   "description": "ISO8601 date of the internal review or draft deadline if referenced, empty string if not mentioned"
   },
   "application_status": {
   "type": "string",
   "description": "Current status of this grant application",
   "enum": [
   "not_started", "in_preparation", "internal_review",
   "submitted", "under_review_by_funder", "awarded",
   "rejected", "resubmission_planned", "unknown"
   ]
   },
   "outstanding_sections": {
   "type": "array",
   "description": "Sections or components of the application still not drafted or submitted",
   "items": {
   "type": "object",
   "description": "A single outstanding grant section",
   "additionalProperties": false,
   "properties": {
   "section": {
   "type": "string",
   "description": "Name of the outstanding section or component"
   },
   "assigned_to": {
   "type": "string",
   "description": "Name or role responsible for this section"
   },
   "due_by": {
   "type": "string",
   "description": "ISO8601 internal due date for this section, empty string if not specified"
   }
   },
   "required": ["section", "assigned_to", "due_by"]
   }
   },
   "risk_level": {
   "type": "string",
   "description": "Risk of missing this deadline based on progress signals",
   "enum": ["on_track", "at_risk", "critical", "unknown"]
   },
   "estimated_award_value": {
   "type": "string",
   "description": "Estimated grant value if mentioned in email, empty string if not found"
   },
   "recommended_action": {
   "type": "string",
   "description": "Recommended immediate action to keep this application on track"
   }
   },
   "required": [
   "grant_name", "funder", "principal_investigator",
   "submission_deadline", "days_until_deadline",
   "internal_review_deadline", "application_status",
   "outstanding_sections", "risk_level",
   "estimated_award_value", "recommended_action"
   ]
   }
   },
   "critical_count": {
   "type": "number",
   "description": "Number of grant applications at critical risk of missing the deadline"
   },
   "due_within_30_days": {
   "type": "number",
   "description": "Number of grant deadlines within the next 30 days"
   },
   "summary": {
   "type": "string",
   "description": "One or two sentence summary of the grant pipeline and most urgent deadlines"
   }
   },
   "required": [
   "as_of", "grants", "critical_count", "due_within_30_days", "summary"
   ]
   }
   }

4. Present critical and at-risk grants first, ordered by days_until_deadline.
   Lead with critical count and due_within_30_days.

5. Ask: "Would you like me to draft a grant preparation timeline or chase
   emails for any outstanding sections?"