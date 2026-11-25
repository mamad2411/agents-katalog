---
name: client-deliverable-tracker
description: Tracks every deliverable committed to across active consulting engagements — what has been delivered, what is outstanding, what is overdue, and what feedback is still open. Use when a consultant or agency wants a full view of all client deliverable commitments without manually reviewing every thread. Triggers on "client deliverables", "what have I promised to deliver", "outstanding deliverables", "what is due to clients", "deliverable tracker", "what am I behind on".
metadata:
  version: 1.0.0
---

# Client Deliverable Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all client engagement email threads to extract every deliverable
committed to — reports, presentations, audits, workshops, strategies,
implementations — and tracks whether each has been submitted, is in progress,
is awaiting feedback, or is overdue.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last 3 months", "May 2024",
     "between Jan 1 and Mar 15", "since the kickoff"). Default: the last
     90 days. Keep the user's natural phrasing for use in the ask input;
     convert to ISO dates separately for the search call.
   - [client_scope] — either "all" (default) or the name of a specific
     client / engagement to focus on.
   - [client_clause] — derived. When [client_scope] is not "all", set to
     " for client [client_scope]". When [client_scope] is "all", set to
     empty string.

2. Call search with:
   - query: deliverable submit deliver due send report presentation
     workshop audit strategy draft review
     (if [client_scope] is not "all", append the client name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if the
     range is open-ended)

3. Call ask with:
   - input: Review all client engagement email threads from [time_range][client_clause]. For each active client, extract every deliverable that was committed to or requested — reports, presentations, strategies, audits, workshops, recommendations, and any other work product promised. For each deliverable determine: the client, what was committed, when it was due, whether it has been submitted, any feedback received, whether there are outstanding revisions, and whether anything is overdue.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Client deliverable tracker across all active consulting engagements",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "deliverables": {
           "type": "array",
           "description": "List of every deliverable committed to across all active engagements",
           "items": {
             "type": "object",
             "description": "A single client deliverable with status and context",
             "additionalProperties": false,
             "properties": {
               "client": {
                 "type": "string",
                 "description": "Name of the client company or engagement"
               },
               "deliverable": {
                 "type": "string",
                 "description": "Clear description of what was committed to be delivered"
               },
               "deliverable_type": {
                 "type": "string",
                 "description": "Category of deliverable",
                 "enum": [
                   "report", "presentation", "strategy", "audit", "workshop",
                   "implementation", "recommendation", "analysis", "training",
                   "code", "design", "other"
                 ]
               },
               "committed_on": {
                 "type": "string",
                 "description": "ISO8601 date the deliverable was committed to"
               },
               "due_date": {
                 "type": "string",
                 "description": "ISO8601 date the deliverable is or was due, empty string if not specified"
               },
               "status": {
                 "type": "string",
                 "description": "Current status of this deliverable",
                 "enum": [
                   "not_started", "in_progress", "submitted_awaiting_feedback",
                   "feedback_received", "in_revision", "approved", "overdue", "unknown"
                 ]
               },
               "days_overdue": {
                 "type": "number",
                 "description": "Number of days past the due date, 0 if not overdue"
               },
               "open_feedback_items": {
                 "type": "array",
                 "description": "Specific feedback points or revision requests from the client still unaddressed",
                 "items": {
                   "type": "string",
                   "description": "A single open feedback item or revision request"
                 }
               },
               "blocker": {
                 "type": "string",
                 "description": "Anything blocking this deliverable from progressing, empty string if none"
               },
               "we_are_waiting_on_client": {
                 "type": "boolean",
                 "description": "Whether progress is currently blocked waiting on input or approval from the client"
               }
             },
             "required": [
               "client", "deliverable", "deliverable_type", "committed_on",
               "due_date", "status", "days_overdue", "open_feedback_items",
               "blocker", "we_are_waiting_on_client"
             ]
           }
         },
         "overdue_count": {
           "type": "number",
           "description": "Total number of overdue deliverables across all clients"
         },
         "waiting_on_client_count": {
           "type": "number",
           "description": "Number of deliverables currently blocked waiting on client input"
         },
         "by_client": {
           "type": "array",
           "description": "Summary of deliverable status grouped by client",
           "items": {
             "type": "object",
             "description": "Deliverable status summary for a single client",
             "additionalProperties": false,
             "properties": {
               "client": {
                 "type": "string",
                 "description": "Name of the client"
               },
               "total_deliverables": {
                 "type": "number",
                 "description": "Total number of deliverables for this client"
               },
               "overdue_count": {
                 "type": "number",
                 "description": "Number of overdue deliverables for this client"
               },
               "in_progress_count": {
                 "type": "number",
                 "description": "Number of deliverables currently in progress for this client"
               }
             },
             "required": ["client", "total_deliverables", "overdue_count", "in_progress_count"]
           }
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of overall deliverable status and most urgent items"
         }
       },
       "required": [
         "as_of", "deliverables", "overdue_count",
         "waiting_on_client_count", "by_client", "summary"
       ]
     }
   }

4. Present overdue deliverables first, then items waiting on client input,
   then in-progress items. Lead with overdue count and waiting_on_client
   count.

5. Ask: "Would you like me to draft a status update or delivery email
   for any of these clients?"
