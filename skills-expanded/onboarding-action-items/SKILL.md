---
name: onboarding-action-items
description: Extracts every outstanding action item from new employee onboarding email threads — setup tasks, access requests, paperwork, introductions, and training items that have not been confirmed complete. Use when an HR manager or people ops team wants to ensure new hires are not stuck waiting on internal actions. Triggers on "onboarding action items", "what's pending for new hires", "onboarding checklist gaps", "new employee setup", "what do we still need to do for new starters".
metadata:
  version: 1.0.0
---

# Onboarding Action Items

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans new employee onboarding email threads to extract every outstanding
action item — tasks the company or team must complete before or during the
employee's first days that have not yet been confirmed as done.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last 3 months", "May 2024",
     "since the new hire batch"). Default: the last 90 days. Keep the
     user's natural phrasing for use in the ask input; convert to ISO
     dates separately for the search call.
   - [employee_scope] — either "all" (default) or the name of a specific
     new hire to focus on.
   - [employee_clause] — derived. When [employee_scope] is not "all",
     set to " for new hire [employee_scope]". When [employee_scope] is
     "all", set to empty string.

2. Call search with:
   - query: new hire onboarding first day access equipment setup training
     welcome introduction paperwork
     (if [employee_scope] is not "all", append the employee name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all new employee onboarding email threads from [time_range][employee_clause]. For each new hire, identify every action item that is outstanding — system access not yet provisioned, equipment not yet delivered, paperwork not yet completed, introductions not yet made, training not yet scheduled, and any other onboarding task that was mentioned but not confirmed as done. Note who owns each action and how many days it has been pending.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Outstanding onboarding action items for new employees",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "new_hires": {
           "type": "array",
           "description": "List of new hires with their outstanding onboarding action items",
           "items": {
             "type": "object",
             "description": "A single new hire and their outstanding onboarding tasks",
             "additionalProperties": false,
             "properties": {
               "employee_name": {
                 "type": "string",
                 "description": "Full name of the new hire"
               },
               "role": {
                 "type": "string",
                 "description": "Job title or role of the new hire"
               },
               "start_date": {
                 "type": "string",
                 "description": "ISO8601 start date of the new hire, empty string if not confirmed"
               },
               "action_items": {
                 "type": "array",
                 "description": "List of outstanding onboarding tasks for this new hire",
                 "items": {
                   "type": "object",
                   "description": "A single outstanding onboarding action item",
                   "additionalProperties": false,
                   "properties": {
                     "task": {
                       "type": "string",
                       "description": "Clear description of the onboarding task that needs to be completed"
                     },
                     "task_type": {
                       "type": "string",
                       "description": "Category of onboarding task",
                       "enum": [
                         "system_access", "equipment", "paperwork", "introduction",
                         "training", "payroll_setup", "benefits_enrollment",
                         "workspace_setup", "policy_acknowledgment", "other"
                       ]
                     },
                     "owned_by": {
                       "type": "string",
                       "description": "Name, role, or team responsible for completing this task"
                     },
                     "days_pending": {
                       "type": "number",
                       "description": "Number of days this task has been outstanding"
                     },
                     "urgency": {
                       "type": "string",
                       "description": "How urgently this task needs to be completed relative to the start date",
                       "enum": ["critical", "high", "medium", "low"]
                     }
                   },
                   "required": [
                     "task", "task_type", "owned_by", "days_pending", "urgency"
                   ]
                 }
               },
               "overall_readiness": {
                 "type": "string",
                 "description": "Overall assessment of how ready this new hire's onboarding is",
                 "enum": ["ready", "mostly_ready", "gaps_present", "significant_gaps", "unknown"]
               }
             },
             "required": [
               "employee_name", "role", "start_date", "action_items", "overall_readiness"
             ]
           }
         },
         "critical_items_count": {
           "type": "number",
           "description": "Total number of critical urgency onboarding tasks outstanding across all new hires"
         },
         "systemic_gaps": {
           "type": "array",
           "description": "Task types that are consistently incomplete across multiple new hires, suggesting a process gap",
           "items": {
             "type": "string",
             "description": "A task type that is a recurring onboarding gap"
           }
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of onboarding readiness across new hires and critical gaps"
         }
       },
       "required": [
         "as_of", "new_hires", "critical_items_count", "systemic_gaps", "summary"
       ]
     }
   }

4. Present new hires with the most critical gaps first. Lead with critical
   item count and highlight any systemic gaps prominently.

5. Ask: "Would you like me to draft reminder emails to the teams responsible
   for any critical outstanding tasks?"
