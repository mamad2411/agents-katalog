---
name: event-action-items
description: Extracts every outstanding action item, commitment, and follow-up task from event planning and post-event email threads — logistics not yet confirmed, vendor commitments outstanding, attendee follow-ups not sent, and sponsorship deliverables open. Use when a marketing team is managing a conference, webinar, or event and wants all open items in one place. Triggers on "event action items", "what's outstanding for the event", "event planning tasks", "post-event follow-ups", "event logistics gaps", "what do we still need to do for the event".
metadata:
  version: 1.0.0
---

# Event Action Items

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans event planning and post-event email threads to extract every outstanding
action item — pre-event logistics, vendor commitments, speaker confirmations,
sponsorship deliverables, attendee follow-ups, and post-event tasks — and
returns them organized by urgency and owner.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last 3 months", "May 2024",
     "since planning started"). Default: the last 90 days. Keep the
     user's natural phrasing for use in the ask input; convert to ISO
     dates separately for the search call.
   - [event_scope] — either "all" (default) or the name of a specific
     event to focus on.
   - [event_clause] — derived. When [event_scope] is not "all", set to
     " related to [event_scope]". When [event_scope] is "all", set to
     empty string.

2. Call search with:
   - query: event conference webinar summit logistics venue speaker sponsor
     attendee registration confirm follow-up
     (if [event_scope] is not "all", append the event name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads from [time_range][event_clause]. Extract every outstanding action item across all phases of the event: pre-event logistics not yet confirmed, vendor deliverables outstanding, speaker or panelist confirmations still needed, sponsorship commitments not yet fulfilled, attendee communications not yet sent, and post-event follow-up tasks. For each item note what it is, who owns it, when it is needed by, and how urgent it is relative to the event.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Event action item tracker across all phases of event planning and execution",
       "additionalProperties": false,
       "properties": {
         "event_name": {
           "type": "string",
           "description": "Name or description of the event"
         },
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "action_items": {
           "type": "array",
           "description": "List of every outstanding event action item",
           "items": {
             "type": "object",
             "description": "A single outstanding event action item",
             "additionalProperties": false,
             "properties": {
               "task": {
                 "type": "string",
                 "description": "Clear description of the action item"
               },
               "phase": {
                 "type": "string",
                 "description": "Which phase of the event this task belongs to",
                 "enum": [
                   "pre_event_logistics", "speaker_management", "vendor_management",
                   "sponsorship", "attendee_communications", "content_preparation",
                   "post_event_follow_up", "other"
                 ]
               },
               "owned_by": {
                 "type": "string",
                 "description": "Name, role, or company responsible for completing this task"
               },
               "due_by": {
                 "type": "string",
                 "description": "ISO8601 date by which this must be completed, empty string if not specified"
               },
               "days_until_due": {
                 "type": "number",
                 "description": "Number of days until this task is due, -1 if unknown"
               },
               "urgency": {
                 "type": "string",
                 "description": "How urgently this task needs attention relative to the event timeline",
                 "enum": ["critical", "high", "medium", "low"]
               },
               "we_are_waiting_on_external": {
                 "type": "boolean",
                 "description": "Whether this task is blocked waiting on an external party such as a vendor or speaker"
               },
               "notes": {
                 "type": "string",
                 "description": "Any context about this task from email, empty string if none"
               }
             },
             "required": [
               "task", "phase", "owned_by", "due_by", "days_until_due",
               "urgency", "we_are_waiting_on_external", "notes"
             ]
           }
         },
         "critical_count": {
           "type": "number",
           "description": "Number of action items rated as critical urgency"
         },
         "waiting_on_external_count": {
           "type": "number",
           "description": "Number of tasks currently blocked waiting on an external party"
         },
         "by_phase": {
           "type": "array",
           "description": "Summary of open action item counts grouped by event phase",
           "items": {
             "type": "object",
             "description": "Action item count for a single event phase",
             "additionalProperties": false,
             "properties": {
               "phase": {
                 "type": "string",
                 "description": "Name of the event phase"
               },
               "open_count": {
                 "type": "number",
                 "description": "Number of open action items in this phase"
               }
             },
             "required": ["phase", "open_count"]
           }
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of total open items, critical count, and most urgent gaps"
         }
       },
       "required": [
         "event_name", "as_of", "action_items", "critical_count",
         "waiting_on_external_count", "by_phase", "summary"
       ]
     }
   }

4. Present critical items first, then items waiting on external parties,
   then the rest grouped by phase. Lead with critical count and
   waiting_on_external count.

5. Ask: "Would you like me to draft chase emails for any vendors, speakers,
   or sponsors who have outstanding items?"
