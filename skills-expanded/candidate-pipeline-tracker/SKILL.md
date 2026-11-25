---
name: candidate-pipeline-tracker
description: Extracts the current status of every active candidate across open roles from hiring-related email threads — where each candidate is in the process, what the next step is, and what is stalling. Use when an HR manager or recruiter wants a full pipeline view without manually checking every thread. Triggers on "candidate pipeline", "where are candidates", "hiring pipeline status", "who is in process", "active candidates", "pipeline overview".
metadata:
  version: 1.0.0
---

# Candidate Pipeline Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all hiring-related email threads to extract the current stage of every
active candidate across all open roles — interview status, outstanding
feedback, next scheduled steps, and any candidates who have gone quiet or
are stalling in the process.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last 3 months", "May 2024",
     "since the requisition opened"). Default: the last 90 days. Keep
     the user's natural phrasing for use in the ask input; convert to
     ISO dates separately for the search call.
   - [role_scope] — either "all" (default) or the name of a specific
     open role to focus on.
   - [role_clause] — derived. When [role_scope] is not "all", set to
     " for role [role_scope]". When [role_scope] is "all", set to empty
     string.

2. Call search with:
   - query: candidate interview application role hiring resume screening
     feedback offer pipeline
     (if [role_scope] is not "all", append the role name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all hiring-related email threads from [time_range][role_clause]. For each active candidate across all open roles, determine: the role they are being considered for, their current stage in the hiring process, the most recent action taken, the next step required, who owns that next step, and whether there are any delays or gaps in the process for this candidate.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Active candidate pipeline report across all open roles",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "candidates": {
           "type": "array",
           "description": "List of every active candidate currently in the hiring pipeline",
           "items": {
             "type": "object",
             "description": "A single active candidate with their current pipeline status",
             "additionalProperties": false,
             "properties": {
               "candidate_name": {
                 "type": "string",
                 "description": "Full name of the candidate"
               },
               "role": {
                 "type": "string",
                 "description": "The role or position this candidate is being considered for"
               },
               "current_stage": {
                 "type": "string",
                 "description": "Current stage of the hiring process for this candidate",
                 "enum": [
                   "application_review", "phone_screen", "first_interview",
                   "technical_assessment", "panel_interview", "final_interview",
                   "reference_check", "offer_stage", "negotiation", "stalled", "unknown"
                 ]
               },
               "last_action": {
                 "type": "string",
                 "description": "Most recent action taken in this candidate's process"
               },
               "last_action_date": {
                 "type": "string",
                 "description": "ISO8601 date of the most recent action"
               },
               "next_step": {
                 "type": "string",
                 "description": "The next action required to move this candidate forward"
               },
               "next_step_owner": {
                 "type": "string",
                 "description": "Name or role of the person responsible for the next step"
               },
               "days_in_current_stage": {
                 "type": "number",
                 "description": "Number of days this candidate has been in their current stage"
               },
               "status": {
                 "type": "string",
                 "description": "Overall process health for this candidate",
                 "enum": ["progressing", "stalled", "delayed", "at_risk_of_dropping", "unknown"]
               },
               "notes": {
                 "type": "string",
                 "description": "Any notable context about this candidate from email, empty string if none"
               }
             },
             "required": [
               "candidate_name", "role", "current_stage", "last_action",
               "last_action_date", "next_step", "next_step_owner",
               "days_in_current_stage", "status", "notes"
             ]
           }
         },
         "by_role": {
           "type": "array",
           "description": "Summary of candidate counts grouped by open role",
           "items": {
             "type": "object",
             "description": "Candidate count summary for a single open role",
             "additionalProperties": false,
             "properties": {
               "role": {
                 "type": "string",
                 "description": "Name of the open role"
               },
               "active_candidates": {
                 "type": "number",
                 "description": "Number of active candidates for this role"
               },
               "stalled_candidates": {
                 "type": "number",
                 "description": "Number of candidates who are stalled in the process for this role"
               }
             },
             "required": ["role", "active_candidates", "stalled_candidates"]
           }
         },
         "stalled_count": {
           "type": "number",
           "description": "Total number of candidates whose process has stalled"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of the overall pipeline health and any urgent items"
         }
       },
       "required": ["as_of", "candidates", "by_role", "stalled_count", "summary"]
     }
   }

4. Present grouped by role, with stalled candidates highlighted. Lead with
   total active count, stalled count, and any candidates at risk of dropping.

5. Ask: "Would you like me to draft follow-up emails for any stalled
   candidates?"
