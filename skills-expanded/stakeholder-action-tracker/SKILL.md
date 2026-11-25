---
name: stakeholder-action-tracker
description: Tracks every action item assigned to or expected from specific stakeholders across project email threads — who owes what, by when, and what is overdue. Use when a project manager wants to hold stakeholders accountable or needs a view of who is behind on their commitments. Triggers on "stakeholder actions", "who owes what", "action items by person", "track stakeholder commitments", "who is behind", "assigned actions".
metadata:
  version: 1.0.0
---

# Stakeholder Action Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Extracts every action item, task assignment, and commitment assigned to named
stakeholders across project email threads — and tracks whether each has been
completed, is in progress, or is overdue.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 60 days", "the last 2 months", "May 2024",
     "since the kickoff"). Default: the last 60 days. Keep the user's
     natural phrasing for use in the ask input; convert to ISO dates
     separately for the search call.
   - [project_scope] — either "all" (default) or the name of a specific
     project to focus on.
   - [stakeholder_scope] — either "all" (default) or the name of a
     specific stakeholder to focus on.
   - [scope_clause] — derived. Combine [project_scope] and
     [stakeholder_scope] into a single natural-language clause: when
     both are "all", set to empty string; when only project is
     specified, set to " related to [project_scope]"; when only
     stakeholder is specified, set to " for stakeholder
     [stakeholder_scope]"; when both are specified, set to " related to
     [project_scope] for stakeholder [stakeholder_scope]".

2. Call search with:
   - query: action item assigned to do will send please provide by
     (if [project_scope] is not "all", append the project name to the query;
     if [stakeholder_scope] is not "all", append the stakeholder name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads from [time_range][scope_clause]. For every named stakeholder, extract every action item, task, or commitment that was explicitly or implicitly assigned to them. For each action item note: who it was assigned to, what the task is, who assigned it, when it was assigned, any deadline mentioned, and whether there is any evidence of completion in subsequent emails.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Stakeholder action item tracker for a project",
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
         "action_items": {
           "type": "array",
           "description": "List of every action item assigned to a stakeholder",
           "items": {
             "type": "object",
             "description": "A single action item with assignment and status details",
             "additionalProperties": false,
             "properties": {
               "assigned_to": {
                 "type": "string",
                 "description": "Name or role of the stakeholder responsible for this action"
               },
               "task": {
                 "type": "string",
                 "description": "Clear description of the action item or task"
               },
               "assigned_by": {
                 "type": "string",
                 "description": "Name or role of the person who assigned this action"
               },
               "assigned_on": {
                 "type": "string",
                 "description": "ISO8601 date when this action item was assigned"
               },
               "due_date": {
                 "type": "string",
                 "description": "ISO8601 deadline for this action item, empty string if not specified"
               },
               "days_outstanding": {
                 "type": "number",
                 "description": "Number of days since this action was assigned with no completion evidence"
               },
               "status": {
                 "type": "string",
                 "description": "Current completion status of this action item",
                 "enum": ["open", "in_progress", "completed", "overdue", "unknown"]
               },
               "priority": {
                 "type": "string",
                 "description": "Priority of this action item relative to other project needs",
                 "enum": ["high", "medium", "low"]
               },
               "evidence": {
                 "type": "string",
                 "description": "Quote or paraphrase from email that documents this assignment"
               }
             },
             "required": [
               "assigned_to", "task", "assigned_by", "assigned_on",
               "due_date", "days_outstanding", "status", "priority", "evidence"
             ]
           }
         },
         "overdue_count": {
           "type": "number",
           "description": "Total number of action items that are overdue"
         },
         "by_stakeholder": {
           "type": "array",
           "description": "Summary of open action item counts grouped by stakeholder",
           "items": {
             "type": "object",
             "description": "Action item count for a single stakeholder",
             "additionalProperties": false,
             "properties": {
               "stakeholder": {
                 "type": "string",
                 "description": "Name or role of the stakeholder"
               },
               "open_count": {
                 "type": "number",
                 "description": "Number of open or overdue action items for this stakeholder"
               },
               "overdue_count": {
                 "type": "number",
                 "description": "Number of overdue action items for this stakeholder"
               }
             },
             "required": ["stakeholder", "open_count", "overdue_count"]
           }
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of total actions, overdue count, and stakeholders most behind"
         }
       },
       "required": [
         "project", "as_of", "action_items", "overdue_count",
         "by_stakeholder", "summary"
       ]
     }
   }

4. Present grouped by stakeholder, with overdue items highlighted. Lead with
   overdue count and the stakeholder with the most outstanding items.

5. Ask: "Would you like me to draft a follow-up message to any stakeholders
   who are behind?"
