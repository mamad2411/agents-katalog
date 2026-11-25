---
name: meeting-prep-briefing
description: Before a sales call, surfaces everything iGPT knows about a contact from email history — past commitments, open items, sentiment, and what to prioritize. Use when preparing for a call or meeting. Triggers on "prep me for my call with", "meeting prep", "brief me on", "what do I know about [contact]", "get me ready for my meeting".
metadata:
  version: 1.0.0
---

# Meeting Prep Briefing

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Produces a structured pre-meeting brief by reading all email history with a
contact — their history, what was promised, what is open, their communication
style, and what to prioritize in the meeting.

---

## Workflow

1. Before calling any tool, collect these values from the user. Do not
   invent values they did not give.

   - [contact] — the name of the person the meeting is with. No default
     — must come from the user.
   - [company] — the company [contact] works at. No default — must come
     from the user.
   - [time_range] — what window of email history to pull from. The user
     may give this in any form ("last 12 months", "the last year",
     "May 2024", "since we first met"). Default: the last 12 months.
     Keep the user's natural phrasing for use in the ask input; convert
     to ISO dates separately for the search call.

2. Call search with:
   - query: [contact] [company]
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Produce a pre-meeting briefing for a sales call with [contact] at [company], drawing on email history from [time_range]. Cover: (1) relationship history and tone, (2) what was last discussed and current status, (3) any open commitments from either side, (4) concerns or objections raised historically, (5) what they care about most based on what they ask and say, (6) what to prioritize or be careful about in this meeting.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Structured pre-meeting briefing document for a sales call",
       "additionalProperties": false,
       "properties": {
         "contact": {
           "type": "string",
           "description": "Full name of the person the meeting is with"
         },
         "company": {
           "type": "string",
           "description": "Company the contact works for"
         },
         "relationship_summary": {
           "type": "string",
           "description": "Overview of the relationship history, how long you have been in contact, and the general tone of communication"
         },
         "last_interaction": {
           "type": "object",
           "description": "Details of the most recent email exchange with this contact",
           "additionalProperties": false,
           "properties": {
             "date": {
               "type": "string",
               "description": "ISO8601 date of the last interaction"
             },
             "topic": {
               "type": "string",
               "description": "What the last conversation was about"
             },
             "outcome": {
               "type": "string",
               "description": "How the last conversation ended or what was agreed"
             }
           },
           "required": ["date", "topic", "outcome"]
         },
         "open_commitments": {
           "type": "array",
           "description": "List of commitments made by either side that have not yet been confirmed as complete",
           "items": {
             "type": "object",
             "description": "A single open commitment from either party",
             "additionalProperties": false,
             "properties": {
               "description": {
                 "type": "string",
                 "description": "What was committed to"
               },
               "owned_by": {
                 "type": "string",
                 "description": "Which party made the commitment",
                 "enum": ["us", "them"]
               },
               "raised_on": {
                 "type": "string",
                 "description": "ISO8601 date when the commitment was made"
               }
             },
             "required": ["description", "owned_by", "raised_on"]
           }
         },
         "known_concerns": {
           "type": "array",
           "description": "Concerns, objections, or hesitations this contact has raised historically",
           "items": {
             "type": "string",
             "description": "A single concern or objection"
           }
         },
         "what_they_care_about": {
           "type": "array",
           "description": "Topics, outcomes, or values this contact consistently emphasizes in communication",
           "items": {
             "type": "string",
             "description": "A single priority or value this contact has expressed"
           }
         },
         "meeting_priorities": {
           "type": "array",
           "description": "Ordered list of what to focus on or accomplish in this meeting",
           "items": {
             "type": "string",
             "description": "A single meeting priority"
           }
         },
         "watch_out_for": {
           "type": "array",
           "description": "Things to be careful about or potential landmines in this meeting",
           "items": {
             "type": "string",
             "description": "A single risk or sensitivity to be aware of"
           }
         }
       },
       "required": ["contact", "company", "relationship_summary", "last_interaction",
         "open_commitments", "known_concerns", "what_they_care_about",
         "meeting_priorities", "watch_out_for"]
     }
   }

4. Present as a clean brief: relationship summary first, then priorities,
   then full detail sections.
