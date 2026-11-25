---
name: follow-up-radar
description: Finds emails waiting for a reply, threads that went quiet, and questions never answered across all active sales conversations. Use when a salesperson wants to know who they owe a response to or what has been dropped. Triggers on "who do I need to follow up with", "what have I dropped", "stale threads", "who is waiting on me", "follow-up radar".
metadata:
  version: 1.0.0
---

# Follow-Up Radar

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all active sales email threads to find conversations waiting for a reply,
threads that have gone quiet past an acceptable window, and questions from
prospects that were never answered.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 60 days", "the last 2 months", "May 2024",
     "since I returned from leave"). Default: the last 60 days. Keep
     the user's natural phrasing for use in the ask input; convert to
     ISO dates separately for the search call.
   - [silence_days] — the number of business days of silence after which
     a thread should be flagged. Default: 5 business days when waiting
     on us; 7 business days when waiting on the prospect.

2. Call search with:
   - query: waiting reply no response follow up outstanding
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all sales email threads from [time_range]. Identify every thread where: (1) a prospect sent the last email and we have not replied in more than [silence_days] business days, (2) we sent an email with no reply in more than [silence_days] business days, or (3) a question was asked that was never answered. For each note who is involved, what the last message was, how many days since it was sent, and suggested urgency.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Follow-up radar report across all active sales conversations",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "follow_ups": {
           "type": "array",
           "description": "List of every conversation requiring a follow-up action",
           "items": {
             "type": "object",
             "description": "A single conversation that needs follow-up attention",
             "additionalProperties": false,
             "properties": {
               "type": {
                 "type": "string",
                 "description": "Who is waiting and why this follow-up is needed",
                 "enum": ["they_are_waiting", "we_are_waiting", "unanswered_question"]
               },
               "contact": {
                 "type": "string",
                 "description": "Name of the prospect or customer contact"
               },
               "account": {
                 "type": "string",
                 "description": "Company or deal name associated with this thread"
               },
               "last_message_summary": {
                 "type": "string",
                 "description": "Brief summary of what the last message said or asked"
               },
               "days_since_last_message": {
                 "type": "number",
                 "description": "Number of calendar days since the last message in this thread"
               },
               "urgency": {
                 "type": "string",
                 "description": "How urgently this follow-up needs to happen to protect the relationship or deal",
                 "enum": ["high", "medium", "low"]
               },
               "suggested_action": {
                 "type": "string",
                 "description": "Specific recommended action to take for this follow-up"
               }
             },
             "required": ["type", "contact", "account", "last_message_summary", "days_since_last_message", "urgency", "suggested_action"]
           }
         },
         "total_overdue": {
           "type": "number",
           "description": "Total count of conversations requiring immediate follow-up"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of the overall follow-up situation"
         }
       },
       "required": ["as_of", "follow_ups", "total_overdue", "summary"]
     }
   }

4. Present ordered by urgency then by days overdue. Lead with total count.
5. Offer to draft follow-up messages for any item.
