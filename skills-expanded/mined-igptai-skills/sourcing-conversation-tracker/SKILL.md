---
name: sourcing-conversation-tracker
description: Tracks every outbound sourcing conversation from email — who has been reached out to, who has responded, who is warm, who has gone quiet, and which prospects are actively considering a role. Use when a recruiter wants a full view of their sourcing pipeline without checking every thread individually. Triggers on "sourcing pipeline", "outbound recruiting", "who have I reached out to", "sourcing tracker", "warm prospects", "which sourced candidates are active".
metadata:
  version: 1.0.0
---

# Sourcing Conversation Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans outbound recruiting email threads to map the full sourcing pipeline —
who was contacted, who responded, the current level of interest for each
prospect, what the next step is, and which warm conversations have gone
quiet and need a follow-up to stay alive.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 60 days", "the last 2 months", "May 2024",
     "since the sourcing campaign"). Default: the last 60 days. Keep
     the user's natural phrasing for use in the ask input; convert to
     ISO dates separately for the search call.
   - [role_scope] — either "all" (default) or the name of a specific
     role to focus on.
   - [role_clause] — derived. When [role_scope] is not "all", set to
     " for role [role_scope]". When [role_scope] is "all", set to empty
     string.

2. Call search with:
   - query: reaching out opportunity role open position interested connect
     explore background profile sourcing passive
     (if [role_scope] is not "all", append the role name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all outbound recruiting and sourcing email threads from [time_range][role_clause]. For every prospect that was contacted, determine: the role they were approached for, when they were first contacted, whether they responded, their apparent level of interest based on email tone, the current status of the conversation, the next step required, and whether a warm conversation has gone quiet and needs a follow-up.
   - output_format:
   {
   "strict": true,
   "schema": {
   "type": "object",
   "description": "Sourcing pipeline tracker across all outbound recruiting conversations",
   "additionalProperties": false,
   "properties": {
   "as_of": {
   "type": "string",
   "description": "ISO8601 date when this report was generated"
   },
   "prospects": {
   "type": "array",
   "description": "List of every sourced prospect with their current pipeline status",
   "items": {
   "type": "object",
   "description": "A single sourced prospect with interest and status tracking",
   "additionalProperties": false,
   "properties": {
   "prospect_name": {
   "type": "string",
   "description": "Full name of the sourced prospect"
   },
   "role": {
   "type": "string",
   "description": "The role this prospect was approached for"
   },
   "first_contacted": {
   "type": "string",
   "description": "ISO8601 date of the first outreach email"
   },
   "responded": {
   "type": "boolean",
   "description": "Whether the prospect responded to outreach"
   },
   "last_contact_date": {
   "type": "string",
   "description": "ISO8601 date of the most recent email exchange"
   },
   "days_since_contact": {
   "type": "number",
   "description": "Number of days since the last email exchange"
   },
   "interest_level": {
   "type": "string",
   "description": "Apparent level of interest in the opportunity based on email signals",
   "enum": ["very_interested", "interested", "open_but_passive", "not_interested", "no_response", "unknown"]
   },
   "status": {
   "type": "string",
   "description": "Current status of this sourcing conversation",
   "enum": [
   "active_conversation", "screen_scheduled", "moved_to_pipeline",
   "warm_gone_quiet", "declined", "not_responded", "unknown"
   ]
   },
   "next_step": {
   "type": "string",
   "description": "Recommended next action for this prospect"
   },
   "follow_up_urgency": {
   "type": "string",
   "description": "How urgently a follow-up is needed to keep this prospect warm",
   "enum": ["immediate", "this_week", "low", "not_needed"]
   },
   "notes": {
   "type": "string",
   "description": "Any notable context about this prospect from email, empty string if none"
   }
   },
   "required": [
   "prospect_name", "role", "first_contacted", "responded",
   "last_contact_date", "days_since_contact", "interest_level",
   "status", "next_step", "follow_up_urgency", "notes"
   ]
   }
   },
   "warm_gone_quiet_count": {
   "type": "number",
   "description": "Number of interested prospects who have gone quiet and need a follow-up"
   },
   "no_response_count": {
   "type": "number",
   "description": "Number of prospects who have not responded to any outreach"
   },
   "active_conversation_count": {
   "type": "number",
   "description": "Number of prospects in active conversation"
   },
   "summary": {
   "type": "string",
   "description": "One or two sentence summary of the sourcing pipeline health and most urgent follow-ups"
   }
   },
   "required": [
   "as_of", "prospects", "warm_gone_quiet_count",
   "no_response_count", "active_conversation_count", "summary"
   ]
   }
   }

4. Present warm-gone-quiet prospects first, ordered by days_since_contact
   descending. Lead with warm_gone_quiet count and active_conversation count.

5. Ask: "Would you like me to draft follow-up messages for any warm
   prospects who have gone quiet?"