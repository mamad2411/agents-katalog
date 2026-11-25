---
name: agency-deliverables-tracker
description: Tracks every deliverable, deadline, and open item across marketing agency and freelancer relationships from email — what has been delivered, what is outstanding, what is overdue, and what feedback has been given. Use when a marketing team manages multiple external agencies or freelancers. Triggers on "agency deliverables", "what is the agency working on", "outstanding agency work", "freelancer deliverables", "agency status", "what do I owe the agency".
metadata:
  version: 1.0.0
---

# Agency Deliverables Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all agency and freelancer email threads to extract every deliverable
that was requested or committed to — tracking what has been received, what
is outstanding, what is overdue, and what feedback loops are still open.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last 3 months", "May 2024",
     "since the agency onboarded"). Default: the last 90 days. Keep
     the user's natural phrasing for use in the ask input; convert to
     ISO dates separately for the search call.
   - [agency_scope] — either "all" (default) or the name of a specific
     agency or freelancer to focus on.
   - [agency_clause] — derived. When [agency_scope] is not "all", set
     to " for [agency_scope]". When [agency_scope] is "all", set to
     empty string.

2. Call search with:
   - query: agency freelancer deliverable draft creative brief feedback
     revision due submit deadline deliver
     (if [agency_scope] is not "all", append the agency name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads from [time_range][agency_clause] involving marketing agencies, creative studios, and freelancers. For each agency or freelancer, extract every deliverable that was requested, scoped, or committed to. For each deliverable determine: what it is, when it was due, whether it has been delivered, whether feedback was given, and whether there are any outstanding revisions or open items in the feedback loop.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Agency deliverables tracker across all external marketing partners",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "agencies": {
           "type": "array",
           "description": "List of agencies and freelancers with their deliverable status",
           "items": {
             "type": "object",
             "description": "Deliverable status for a single agency or freelancer",
             "additionalProperties": false,
             "properties": {
               "agency_name": {
                 "type": "string",
                 "description": "Name of the agency or freelancer"
               },
               "agency_type": {
                 "type": "string",
                 "description": "Type of agency or external partner",
                 "enum": [
                   "creative_agency", "pr_agency", "digital_agency", "media_buyer",
                   "content_freelancer", "designer", "developer", "copywriter", "other"
                 ]
               },
               "deliverables": {
                 "type": "array",
                 "description": "List of deliverables from this agency",
                 "items": {
                   "type": "object",
                   "description": "A single deliverable with status",
                   "additionalProperties": false,
                   "properties": {
                     "deliverable": {
                       "type": "string",
                       "description": "Description of what was requested or committed"
                     },
                     "due_date": {
                       "type": "string",
                       "description": "ISO8601 due date, empty string if not specified"
                     },
                     "status": {
                       "type": "string",
                       "description": "Current status of this deliverable",
                       "enum": [
                         "not_started", "in_progress", "submitted_awaiting_review",
                         "feedback_given", "in_revision", "approved", "overdue", "unknown"
                       ]
                     },
                     "days_overdue": {
                       "type": "number",
                       "description": "Number of days past due date, 0 if not overdue"
                     },
                     "open_feedback_items": {
                       "type": "array",
                       "description": "Specific feedback points or revision requests still open",
                       "items": {
                         "type": "string",
                         "description": "A single open feedback item or revision request"
                       }
                     },
                     "blocker": {
                       "type": "string",
                       "description": "Anything blocking this deliverable from progressing, empty string if none"
                     }
                   },
                   "required": [
                     "deliverable", "due_date", "status", "days_overdue",
                     "open_feedback_items", "blocker"
                   ]
                 }
               },
               "we_owe_them": {
                 "type": "array",
                 "description": "Items the marketing team owes this agency to unblock their work",
                 "items": {
                   "type": "string",
                   "description": "A single item owed to the agency"
                 }
               }
             },
             "required": ["agency_name", "agency_type", "deliverables", "we_owe_them"]
           }
         },
         "overdue_count": {
           "type": "number",
           "description": "Total number of overdue deliverables across all agencies"
         },
         "we_owe_count": {
           "type": "number",
           "description": "Total number of items the team owes to agencies that are blocking work"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of overall agency deliverable status and most urgent items"
         }
       },
       "required": ["as_of", "agencies", "overdue_count", "we_owe_count", "summary"]
     }
   }

4. Present overdue deliverables and items we owe agencies first. Lead with
   overdue count and we_owe count.

5. Ask: "Would you like me to draft a status request or feedback email
   for any agency?"
