---
name: decision-log
description: Reconstructs a chronological log of every significant decision made across project email threads — what was decided, who decided it, when, and what alternatives were considered. Use when a project manager or team needs a decision audit trail or wants to understand how the project got to its current state. Triggers on "decision log", "what decisions were made", "decision history", "who decided", "decision audit trail", "log of project decisions".
metadata:
  version: 1.0.0
---

# Decision Log

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Traces all significant decisions made in project email threads and assembles
them into a chronological decision log — what was decided, by whom, when,
what alternatives were considered, and any conditions or caveats attached.

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
   - [project_scope] — either "all" (default) or the name or topic of a
     specific project to focus on.
   - [project_clause] — derived. When [project_scope] is not "all", set
     to " related to [project_scope]". When [project_scope] is "all",
     set to empty string.

2. Call search with:
   - query: decided agreed going with chosen approved decided on
     (if [project_scope] is not "all", append the project name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads from [time_range][project_clause]. Identify every significant decision that was made — explicit choices, direction changes, scope decisions, technical choices, vendor selections, and any other point where a clear direction was established. For each decision record: what was decided, who made the decision, when, what alternatives were considered if mentioned, and any conditions or caveats attached to the decision.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Chronological decision log for a project extracted from email history",
       "additionalProperties": false,
       "properties": {
         "project": {
           "type": "string",
           "description": "Name or description of the project"
         },
         "period_from": {
           "type": "string",
           "description": "ISO8601 start date of the period covered"
         },
         "period_to": {
           "type": "string",
           "description": "ISO8601 end date of the period covered"
         },
         "decisions": {
           "type": "array",
           "description": "Chronological list of every significant decision found in email",
           "items": {
             "type": "object",
             "description": "A single project decision with full context",
             "additionalProperties": false,
             "properties": {
               "decision": {
                 "type": "string",
                 "description": "Clear statement of what was decided"
               },
               "decision_type": {
                 "type": "string",
                 "description": "Category of decision",
                 "enum": [
                   "scope", "technical", "vendor_selection", "timeline",
                   "budget", "resource", "process", "direction_change", "other"
                 ]
               },
               "decided_by": {
                 "type": "string",
                 "description": "Name or role of the person who made or ratified this decision"
               },
               "date": {
                 "type": "string",
                 "description": "ISO8601 date the decision was made"
               },
               "alternatives_considered": {
                 "type": "array",
                 "description": "Other options that were discussed before this decision was made",
                 "items": {
                   "type": "string",
                   "description": "A single alternative that was considered"
                 }
               },
               "rationale": {
                 "type": "string",
                 "description": "The reason given for this decision if stated in email, empty string if not mentioned"
               },
               "conditions_or_caveats": {
                 "type": "string",
                 "description": "Any conditions, assumptions, or caveats attached to this decision, empty string if none"
               },
               "evidence": {
                 "type": "string",
                 "description": "Quote or paraphrase from email that documents this decision"
               }
             },
             "required": [
               "decision", "decision_type", "decided_by", "date",
               "alternatives_considered", "rationale", "conditions_or_caveats", "evidence"
             ]
           }
         },
         "total_decisions": {
           "type": "number",
           "description": "Total number of decisions logged"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of the decision history and any notable patterns"
         }
       },
       "required": [
         "project", "period_from", "period_to", "decisions",
         "total_decisions", "summary"
       ]
     }
   }

4. Present as a numbered chronological log. Lead with total count and a
   one-line summary of the decision landscape.

5. Ask: "Would you like me to export this as a formatted decision log
   document?"
