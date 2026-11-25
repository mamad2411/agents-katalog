---
name: research-action-items
description: Extracts every outstanding action item from research team email threads — tasks assigned in lab meetings, follow-up analyses requested, methods to investigate, experiments to run, and administrative tasks not yet confirmed as complete. Use when a PI or research team lead wants a consolidated action list without relying on memory or meeting notes. Triggers on "research action items", "lab action items", "what's outstanding in the lab", "team tasks from email", "meeting follow-ups", "what did I agree to do".
metadata:
  version: 1.0.0
---

# Research Action Items

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans research team and lab email threads to extract every action item —
analyses to run, experiments to design, methods to investigate, papers
to review, administrative tasks to complete, and any other commitment made
in email that has not been confirmed as done — and returns them organized
by owner and urgency.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 30 days", "the last month", "May 2024",
     "since the lab meeting"). Default: the last 30 days. Keep the
     user's natural phrasing for use in the ask input; convert to ISO
     dates separately for the search call.
   - [project_scope] — either "all" (default) or the name of a specific
     project to focus on.
   - [project_clause] — derived. When [project_scope] is not "all", set
     to " for project [project_scope]". When [project_scope] is "all",
     set to empty string.

2. Call search with:
   - query: action item please run investigate try test follow up
     assigned to check analyse review write send complete by
     (if [project_scope] is not "all", append the project name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all research team email threads from [time_range][project_clause]. Extract every action item assigned to or accepted by a named team member — analyses to run, experiments to design, methods to investigate, code to write, papers to review, data to process, reports to draft, administrative tasks to complete, and any other commitment made in email. For each action item note who owns it, what it is, who assigned it, any deadline given, and whether there is any evidence of completion in subsequent emails.
   - output_format:
   {
   "strict": true,
   "schema": {
   "type": "object",
   "description": "Research team action item tracker from email threads",
   "additionalProperties": false,
   "properties": {
   "as_of": {
   "type": "string",
   "description": "ISO8601 date when this report was generated"
   },
   "action_items": {
   "type": "array",
   "description": "List of every outstanding research team action item",
   "items": {
   "type": "object",
   "description": "A single research team action item",
   "additionalProperties": false,
   "properties": {
   "assigned_to": {
   "type": "string",
   "description": "Name or role of the team member responsible for this action"
   },
   "task": {
   "type": "string",
   "description": "Clear description of the action item"
   },
   "task_type": {
   "type": "string",
   "description": "Category of research task",
   "enum": [
   "analysis", "experiment", "literature_review", "writing",
   "data_processing", "code_development", "review_or_feedback",
   "administrative", "meeting_or_presentation", "other"
   ]
   },
   "assigned_by": {
   "type": "string",
   "description": "Name or role of the person who assigned this task"
   },
   "project": {
   "type": "string",
   "description": "Research project this task relates to"
   },
   "assigned_on": {
   "type": "string",
   "description": "ISO8601 date when this task was assigned or accepted"
   },
   "due_by": {
   "type": "string",
   "description": "ISO8601 deadline if specified, empty string if not given"
   },
   "days_outstanding": {
   "type": "number",
   "description": "Number of days since this task was assigned with no completion evidence"
   },
   "status": {
   "type": "string",
   "description": "Current status based on email evidence",
   "enum": ["outstanding", "in_progress", "overdue", "completed", "unknown"]
   },
   "urgency": {
   "type": "string",
   "description": "Urgency of this action item relative to research milestones",
   "enum": ["high", "medium", "low"]
   },
   "blocking_other_work": {
   "type": "boolean",
   "description": "Whether this action item is explicitly blocking other team members or research steps"
   },
   "evidence": {
   "type": "string",
   "description": "Quote or paraphrase from email documenting this assignment"
   }
   },
   "required": [
   "assigned_to", "task", "task_type", "assigned_by", "project",
   "assigned_on", "due_by", "days_outstanding", "status",
   "urgency", "blocking_other_work", "evidence"
   ]
   }
   },
   "overdue_count": {
   "type": "number",
   "description": "Total number of overdue action items across the team"
   },
   "blocking_count": {
   "type": "number",
   "description": "Number of action items explicitly blocking other work"
   },
   "by_team_member": {
   "type": "array",
   "description": "Action item summary grouped by team member",
   "items": {
   "type": "object",
   "description": "Action item counts for a single team member",
   "additionalProperties": false,
   "properties": {
   "team_member": {
   "type": "string",
   "description": "Name or role of the team member"
   },
   "outstanding_count": {
   "type": "number",
   "description": "Number of outstanding action items for this team member"
   },
   "overdue_count": {
   "type": "number",
   "description": "Number of overdue action items for this team member"
   },
   "has_blocking_item": {
   "type": "boolean",
   "description": "Whether this team member has any items that are blocking other work"
   }
   },
   "required": [
   "team_member", "outstanding_count", "overdue_count", "has_blocking_item"
   ]
   }
   },
   "by_project": {
   "type": "array",
   "description": "Action item summary grouped by research project",
   "items": {
   "type": "object",
   "description": "Action item counts for a single project",
   "additionalProperties": false,
   "properties": {
   "project": {
   "type": "string",
   "description": "Name of the research project"
   },
   "outstanding_count": {
   "type": "number",
   "description": "Number of outstanding action items for this project"
   },
   "overdue_count": {
   "type": "number",
   "description": "Number of overdue action items for this project"
   }
   },
   "required": ["project", "outstanding_count", "overdue_count"]
   }
   },
   "summary": {
   "type": "string",
   "description": "One or two sentence summary of research team action item status and most urgent gaps"
   }
   },
   "required": [
   "as_of", "action_items", "overdue_count", "blocking_count",
   "by_team_member", "by_project", "summary"
   ]
   }
   }

4. Present blocking items first, then overdue items, then the rest grouped
   by team member ordered by outstanding count. Lead with blocking count
   and overdue count.

5. Ask: "Would you like me to draft a team action item summary email or
   individual follow-up messages for any team members who are behind?"