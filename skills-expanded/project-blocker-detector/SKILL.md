---
name: project-blocker-detector
description: Finds every blocker, dependency, and unresolved obstacle mentioned across project email threads — things that are explicitly or implicitly preventing progress. Use when a project manager or team lead wants to know what is blocking their projects. Triggers on "what's blocking the project", "project blockers", "what are the dependencies", "what's holding us up", "unresolved blockers", "project impediments".
metadata:
  version: 1.0.0
---

# Project Blocker Detector

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans project-related email threads to find every blocker, unresolved
dependency, waiting item, and impediment — whether explicitly stated or
implied by pattern — and returns them as a structured list ordered by impact.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 60 days", "the last 2 months", "May 2024",
     "since the sprint started"). Default: the last 60 days. Keep the
     user's natural phrasing for use in the ask input; convert to ISO
     dates separately for the search call.
   - [project_scope] — either "all" (default) or the name or topic of a
     specific project to focus on.
   - [project_clause] — derived. When [project_scope] is not "all", set
     to " related to [project_scope]". When [project_scope] is "all",
     set to empty string.

2. Call search with:
   - query: blocked waiting dependency pending blocker holding up can't proceed
     (if [project_scope] is not "all", append the project name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads from [time_range][project_clause]. Identify every blocker, unresolved dependency, and impediment — things explicitly described as blocking progress, items waiting on a specific person or team, unresolved decisions that are holding up work, and any pattern where work cannot proceed until something else happens. For each blocker note what it is, who owns resolving it, how long it has been outstanding, and its impact on the project.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Project blocker report identifying all impediments to progress",
       "additionalProperties": false,
       "properties": {
         "project": {
           "type": "string",
           "description": "Name or description of the project being analyzed"
         },
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "blockers": {
           "type": "array",
           "description": "List of every blocker or impediment found across project email threads",
           "items": {
             "type": "object",
             "description": "A single blocker or impediment with full context",
             "additionalProperties": false,
             "properties": {
               "description": {
                 "type": "string",
                 "description": "Clear description of what the blocker is and why it is preventing progress"
               },
               "blocker_type": {
                 "type": "string",
                 "description": "Category of blocker",
                 "enum": [
                   "waiting_on_person", "waiting_on_team", "unresolved_decision",
                   "missing_resource", "technical_dependency", "external_dependency",
                   "approval_required", "unclear_requirement", "other"
                 ]
               },
               "owned_by": {
                 "type": "string",
                 "description": "Name or role of the person or team responsible for resolving this blocker"
               },
               "raised_on": {
                 "type": "string",
                 "description": "ISO8601 date when this blocker first appeared in email"
               },
               "days_outstanding": {
                 "type": "number",
                 "description": "Number of days this blocker has been unresolved"
               },
               "impact": {
                 "type": "string",
                 "description": "How this blocker affects the project if left unresolved",
                 "enum": ["critical", "high", "medium", "low"]
               },
               "evidence": {
                 "type": "string",
                 "description": "Quote or paraphrase from email that surfaces this blocker"
               },
               "suggested_action": {
                 "type": "string",
                 "description": "Recommended next step to resolve or escalate this blocker"
               }
             },
             "required": [
               "description", "blocker_type", "owned_by", "raised_on",
               "days_outstanding", "impact", "evidence", "suggested_action"
             ]
           }
         },
         "critical_count": {
           "type": "number",
           "description": "Number of blockers with critical impact on the project"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of total blockers found and the most critical item"
         }
       },
       "required": ["project", "as_of", "blockers", "critical_count", "summary"]
     }
   }

4. Present ordered by impact then by days outstanding. Lead with critical
   count and the most impactful blocker.

5. Ask: "Would you like me to draft escalation emails for any of these
   blockers?"
