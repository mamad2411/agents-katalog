---
name: press-coverage-tracker
description: Finds every mention of press coverage, journalist outreach, media pickup, and PR activity referenced in email — tracking what got covered, what pitches are outstanding, and what journalists are engaged. Use when a marketing or PR team wants a coverage and outreach status view from email. Triggers on "press coverage", "media coverage", "PR status", "journalist outreach", "what press have we got", "media pipeline".
metadata:
  version: 1.0.0
---

# Press Coverage Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans email threads for all press and media activity — coverage that landed,
pitches sent, journalist conversations, pending follow-ups, and any media
opportunities that were mentioned but not yet pursued — and returns a
structured PR status view.

---

## Workflow

1. Before calling any tool, collect this value from the user. Offer the
   default and let the user override it; do not invent a value they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last 3 months", "May 2024",
     "since the launch announcement"). Default: the last 90 days. Keep
     the user's natural phrasing for use in the ask input; convert to
     ISO dates separately for the search call.

2. Call search with:
   - query: press journalist media coverage article story pitch publication
     interview reporter feature outlet
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads from [time_range] related to press, media, and PR activity. Extract: every piece of coverage that landed or was confirmed, every journalist or publication that was pitched or engaged, the current status of each media relationship, any outstanding pitches awaiting a response, interviews scheduled or completed, and any media opportunities mentioned that have not yet been actioned.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Press coverage and PR activity tracker from email",
       "additionalProperties": false,
       "properties": {
         "period_from": {
           "type": "string",
           "description": "ISO8601 start date of the period tracked"
         },
         "period_to": {
           "type": "string",
           "description": "ISO8601 end date of the period tracked"
         },
         "coverage": {
           "type": "array",
           "description": "List of press coverage that landed or was confirmed in the period",
           "items": {
             "type": "object",
             "description": "A single piece of confirmed press coverage",
             "additionalProperties": false,
             "properties": {
               "publication": {
                 "type": "string",
                 "description": "Name of the publication or outlet"
               },
               "journalist": {
                 "type": "string",
                 "description": "Name of the journalist, empty string if not mentioned"
               },
               "coverage_type": {
                 "type": "string",
                 "description": "Type of coverage",
                 "enum": [
                   "feature_article", "news_mention", "interview", "podcast",
                   "review", "opinion_piece", "product_launch", "other"
                 ]
               },
               "topic": {
                 "type": "string",
                 "description": "What the coverage was about"
               },
               "date": {
                 "type": "string",
                 "description": "ISO8601 date the coverage appeared or was confirmed"
               },
               "sentiment": {
                 "type": "string",
                 "description": "Overall tone of the coverage",
                 "enum": ["positive", "neutral", "negative", "unknown"]
               }
             },
             "required": [
               "publication", "journalist", "coverage_type",
               "topic", "date", "sentiment"
             ]
           }
         },
         "active_outreach": {
           "type": "array",
           "description": "Journalist and media relationships currently being cultivated or pitched",
           "items": {
             "type": "object",
             "description": "A single active journalist or media outreach thread",
             "additionalProperties": false,
             "properties": {
               "journalist": {
                 "type": "string",
                 "description": "Name of the journalist or media contact"
               },
               "publication": {
                 "type": "string",
                 "description": "Publication or outlet they write for"
               },
               "status": {
                 "type": "string",
                 "description": "Current status of this outreach",
                 "enum": [
                   "pitched_awaiting_response", "in_conversation", "interview_scheduled",
                   "article_in_progress", "declined", "gone_quiet", "unknown"
                 ]
               },
               "pitch_topic": {
                 "type": "string",
                 "description": "What was pitched or discussed with this journalist"
               },
               "last_contact_date": {
                 "type": "string",
                 "description": "ISO8601 date of the most recent email exchange"
               },
               "days_since_contact": {
                 "type": "number",
                 "description": "Number of days since last contact"
               },
               "next_step": {
                 "type": "string",
                 "description": "Recommended next action for this media relationship"
               }
             },
             "required": [
               "journalist", "publication", "status", "pitch_topic",
               "last_contact_date", "days_since_contact", "next_step"
             ]
           }
         },
         "coverage_count": {
           "type": "number",
           "description": "Total number of confirmed coverage pieces in the period"
         },
         "pending_responses_count": {
           "type": "number",
           "description": "Number of pitches awaiting a response from journalists"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of press coverage landed and active outreach pipeline"
         }
       },
       "required": [
         "period_from", "period_to", "coverage", "active_outreach",
         "coverage_count", "pending_responses_count", "summary"
       ]
     }
   }

4. Present confirmed coverage first, then active outreach ordered by status.
   Lead with coverage count and pending responses count.

5. Ask: "Would you like me to draft follow-up messages for any outstanding
   pitches or gone-quiet journalists?"
