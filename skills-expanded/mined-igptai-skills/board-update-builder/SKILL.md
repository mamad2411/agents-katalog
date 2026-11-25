---
name: board-update-builder
description: Builds a structured board update draft by extracting key business developments, commitments made, decisions taken, and important signals from executive email threads over a given period. Use when a founder or CEO needs to prepare a board update and wants to pull the raw material from email rather than starting from scratch. Triggers on "build my board update", "board update draft", "prepare board materials", "what should I tell the board", "board meeting prep".
metadata:
  version: 1.0.0
---

# Board Update Builder

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans executive email threads over a defined period to extract the key
developments, decisions, wins, risks, and open items that belong in a board
update — then structures them into a draft the founder or CEO can refine and
send.

---

## Workflow

1. Before calling any tool, collect this value from the user. Offer the
   default and let the user override it; do not invent a value they did
   not give.

   - [time_range] — what window of email to scan and cover in the update.
     The user may give this in any form ("last 30 days", "the last quarter",
     "May 2024", "since the last board meeting"). Default: the last 30
     days. Keep the user's natural phrasing for use in the ask input;
     convert to ISO dates separately for the search call.

2. Call search with:
   - query: revenue growth milestone decision risk investor customer
     strategic hire partnership launched
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all executive email threads from [time_range]. Extract everything that belongs in a board update: key business developments and milestones reached, significant decisions made, major wins with customers or partners, risks or challenges that emerged, strategic hires or team changes, financial signals mentioned, and any open items or asks the board needs to weigh in on. Structure this as raw material for a board update.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Structured board update draft built from executive email history",
       "additionalProperties": false,
       "properties": {
         "period_from": {
           "type": "string",
           "description": "ISO8601 start date of the period this update covers"
         },
         "period_to": {
           "type": "string",
           "description": "ISO8601 end date of the period this update covers"
         },
         "headline_summary": {
           "type": "string",
           "description": "Two to three sentence executive summary of the most important things that happened in the period"
         },
         "business_highlights": {
           "type": "array",
           "description": "Key wins, milestones, and positive developments worth reporting to the board",
           "items": {
             "type": "object",
             "description": "A single business highlight or win",
             "additionalProperties": false,
             "properties": {
               "headline": {
                 "type": "string",
                 "description": "One sentence description of the highlight"
               },
               "detail": {
                 "type": "string",
                 "description": "Supporting detail or context for this highlight"
               },
               "category": {
                 "type": "string",
                 "description": "Business area this highlight relates to",
                 "enum": [
                   "revenue", "customer", "product", "team", "partnership",
                   "fundraising", "operational", "strategic", "other"
                 ]
               }
             },
             "required": ["headline", "detail", "category"]
           }
         },
         "key_decisions": {
           "type": "array",
           "description": "Significant decisions made in the period that the board should be aware of",
           "items": {
             "type": "object",
             "description": "A single key decision made in the period",
             "additionalProperties": false,
             "properties": {
               "decision": {
                 "type": "string",
                 "description": "Clear statement of what was decided"
               },
               "rationale": {
                 "type": "string",
                 "description": "Brief rationale for the decision, empty string if not stated"
               },
               "date": {
                 "type": "string",
                 "description": "ISO8601 date the decision was made"
               }
             },
             "required": ["decision", "rationale", "date"]
           }
         },
         "risks_and_challenges": {
           "type": "array",
           "description": "Risks, challenges, and concerns that emerged in the period and should be disclosed to the board",
           "items": {
             "type": "object",
             "description": "A single risk or challenge",
             "additionalProperties": false,
             "properties": {
               "description": {
                 "type": "string",
                 "description": "Clear description of the risk or challenge"
               },
               "severity": {
                 "type": "string",
                 "description": "How serious this risk or challenge is",
                 "enum": ["critical", "high", "medium", "low"]
               },
               "mitigation": {
                 "type": "string",
                 "description": "What is being done to address this, empty string if not yet determined"
               }
             },
             "required": ["description", "severity", "mitigation"]
           }
         },
         "asks_for_board": {
           "type": "array",
           "description": "Specific items where board input, approval, or assistance is needed",
           "items": {
             "type": "object",
             "description": "A single ask or request directed at the board",
             "additionalProperties": false,
             "properties": {
               "ask": {
                 "type": "string",
                 "description": "Clear statement of what is being asked of the board"
               },
               "context": {
                 "type": "string",
                 "description": "Background context the board needs to respond to this ask"
               },
               "urgency": {
                 "type": "string",
                 "description": "How urgently a board response is needed",
                 "enum": ["this_meeting", "next_30_days", "low"]
               }
             },
             "required": ["ask", "context", "urgency"]
           }
         },
         "metrics_mentioned": {
           "type": "array",
           "description": "Any quantitative metrics or numbers referenced in email that belong in the board update",
           "items": {
             "type": "object",
             "description": "A single metric or number mentioned in email",
             "additionalProperties": false,
             "properties": {
               "metric": {
                 "type": "string",
                 "description": "Name of the metric"
               },
               "value": {
                 "type": "string",
                 "description": "The value or figure as mentioned in email"
               },
               "context": {
                 "type": "string",
                 "description": "Brief context about what this metric represents"
               }
             },
             "required": ["metric", "value", "context"]
           }
         },
         "summary": {
           "type": "string",
           "description": "One sentence note on how complete this draft is and what the CEO should add manually"
         }
       },
       "required": [
         "period_from", "period_to", "headline_summary", "business_highlights",
         "key_decisions", "risks_and_challenges", "asks_for_board",
         "metrics_mentioned", "summary"
       ]
     }
   }

4. Present headline summary first, then highlights, then decisions, then
   risks, then board asks. Lead with the headline summary and note any
   sections that appear thin and may need the CEO to add context.

5. Ask: "Would you like me to format this into a full board update email
   or slide outline?"
