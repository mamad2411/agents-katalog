---
name: milestone-status-extractor
description: Extracts the current status of every project milestone mentioned in email — what has been completed, what is in progress, what is at risk, and what is overdue. Use when a project manager needs a milestone status view from email without updating a project management tool manually. Triggers on "milestone status", "project milestones", "what milestones are complete", "milestone progress", "what's on track", "milestone report".
metadata:
  version: 1.0.0
---

# Milestone Status Extractor

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Finds every project milestone referenced in email threads, determines its
current status based on the most recent email evidence, and returns a
structured milestone tracker showing what is on track, at risk, or overdue.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last 3 months", "May 2024",
     "since the kickoff"). Default: the last 90 days. Keep the user's
     natural phrasing for use in the ask input; convert to ISO dates
     separately for the search call.
   - [project_scope] — either "all" (default) or the name of a specific
     project to focus on.
   - [project_clause] — derived. When [project_scope] is not "all", set
     to " related to [project_scope]". When [project_scope] is "all",
     set to empty string.

2. Call search with:
   - query: milestone deadline phase complete delivered launch release
     (if [project_scope] is not "all", append the project name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads from [time_range][project_clause]. Identify every project milestone, phase, or major deliverable mentioned. For each milestone determine: the milestone name, the target date if mentioned, the current status based on the most recent email evidence, and whether it is on track, at risk, or already delayed. Note who reported on this milestone and when.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Project milestone status report extracted from email threads",
       "additionalProperties": false,
       "properties": {
         "project": {
           "type": "string",
           "description": "Name or description of the project"
         },
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "milestones": {
           "type": "array",
           "description": "List of every project milestone found in email with current status",
           "items": {
             "type": "object",
             "description": "A single project milestone with its current status and evidence",
             "additionalProperties": false,
             "properties": {
               "milestone_name": {
                 "type": "string",
                 "description": "Name or description of this milestone or deliverable"
               },
               "target_date": {
                 "type": "string",
                 "description": "ISO8601 target completion date, empty string if not mentioned"
               },
               "status": {
                 "type": "string",
                 "description": "Current status of this milestone based on most recent email evidence",
                 "enum": [
                   "completed", "on_track", "at_risk", "delayed",
                   "blocked", "not_started", "unknown"
                 ]
               },
               "percent_complete": {
                 "type": "number",
                 "description": "Estimated percentage complete based on email language, -1 if cannot be determined"
               },
               "last_reported_by": {
                 "type": "string",
                 "description": "Name or role of the person who most recently reported on this milestone"
               },
               "last_reported_on": {
                 "type": "string",
                 "description": "ISO8601 date of the most recent status update for this milestone"
               },
               "status_summary": {
                 "type": "string",
                 "description": "Brief summary of the current situation for this milestone based on email"
               },
               "risks_or_blockers": {
                 "type": "string",
                 "description": "Any risks or blockers affecting this milestone, empty string if none"
               }
             },
             "required": [
               "milestone_name", "target_date", "status", "percent_complete",
               "last_reported_by", "last_reported_on", "status_summary",
               "risks_or_blockers"
             ]
           }
         },
         "completed_count": {
           "type": "number",
           "description": "Number of milestones with completed status"
         },
         "at_risk_count": {
           "type": "number",
           "description": "Number of milestones with at_risk or delayed status"
         },
         "overall_project_status": {
           "type": "string",
           "description": "Overall project health based on the milestone picture",
           "enum": ["on_track", "at_risk", "delayed", "critical", "unknown"]
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of milestone progress and overall project status"
         }
       },
       "required": [
         "project", "as_of", "milestones", "completed_count",
         "at_risk_count", "overall_project_status", "summary"
       ]
     }
   }

4. Present overall project status first, then milestones grouped by status:
   at_risk and delayed first, then on_track, then completed. Lead with the
   at_risk count.

5. Ask: "Would you like me to draft a milestone status update for
   stakeholders?"
