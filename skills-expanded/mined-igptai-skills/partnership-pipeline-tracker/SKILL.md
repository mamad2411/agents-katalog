---
name: partnership-pipeline-tracker
description: Tracks every active partnership conversation from email — where each discussion stands, what was agreed, what the next step is, and which conversations have stalled. Use when a marketing or BD team wants a full view of the partnership pipeline without manually reviewing every thread. Triggers on "partnership pipeline", "active partnership conversations", "partnership status", "where are partnership discussions", "BD pipeline", "which partnerships are progressing".
metadata:
  version: 1.0.0
---

# Partnership Pipeline Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all partnership and business development email threads to produce a
structured pipeline view — current stage of each conversation, last contact
date, open commitments, next steps, and which discussions have gone quiet
or stalled.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 6 months", "the last 90 days", "May 2024",
     "since BD kicked off"). Default: the last 6 months. Keep the
     user's natural phrasing for use in the ask input; convert to ISO
     dates separately for the search call.
   - [partnership_scope] — either "all" (default) or a specific
     partnership type or partner company to focus on.
   - [partnership_clause] — derived. When [partnership_scope] is not
     "all", set to " for [partnership_scope]". When [partnership_scope]
     is "all", set to empty string.

2. Call search with:
   - query: partnership collaboration co-marketing integration BD agreement
     joint launch announcement deal
     (if [partnership_scope] is not "all", append the partnership type or partner name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all partnership and business development email threads from [time_range][partnership_clause]. For each active partnership conversation identify: the partner company, the type of partnership being discussed, the current stage of the conversation, when contact was last made, what was last agreed or discussed, the next step required, who owns that next step, and any open commitments from either side.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Partnership pipeline report across all active BD conversations",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "partnerships": {
           "type": "array",
           "description": "List of every active partnership conversation in the pipeline",
           "items": {
             "type": "object",
             "description": "A single partnership conversation with current pipeline status",
             "additionalProperties": false,
             "properties": {
               "partner": {
                 "type": "string",
                 "description": "Name of the partner company or organization"
               },
               "partnership_type": {
                 "type": "string",
                 "description": "Category of partnership being discussed",
                 "enum": [
                   "co_marketing", "integration", "reseller", "referral",
                   "joint_venture", "content", "event", "technology", "other"
                 ]
               },
               "stage": {
                 "type": "string",
                 "description": "Current stage of this partnership conversation",
                 "enum": [
                   "initial_outreach", "exploratory_discussion", "alignment_meeting",
                   "proposal_shared", "negotiating_terms", "agreement_in_progress",
                   "active", "stalled", "declined", "unknown"
                 ]
               },
               "last_contact_date": {
                 "type": "string",
                 "description": "ISO8601 date of the most recent email exchange"
               },
               "days_since_contact": {
                 "type": "number",
                 "description": "Number of days since the last email exchange"
               },
               "last_exchange_summary": {
                 "type": "string",
                 "description": "Brief summary of what was discussed in the most recent exchange"
               },
               "open_commitments": {
                 "type": "array",
                 "description": "Commitments from either side that have not been confirmed as complete",
                 "items": {
                   "type": "object",
                   "description": "A single open commitment in this partnership",
                   "additionalProperties": false,
                   "properties": {
                     "commitment": {
                       "type": "string",
                       "description": "Description of the commitment made"
                     },
                     "owned_by": {
                       "type": "string",
                       "description": "Which side owns this commitment",
                       "enum": ["us", "partner", "unknown"]
                     }
                   },
                   "required": ["commitment", "owned_by"]
                 }
               },
               "next_step": {
                 "type": "string",
                 "description": "The next action required to move this partnership forward"
               },
               "next_step_owner": {
                 "type": "string",
                 "description": "Who owns the next step",
                 "enum": ["us", "partner", "both", "unknown"]
               },
               "potential_value": {
                 "type": "string",
                 "description": "Assessment of the strategic value of this partnership if it progresses",
                 "enum": ["high", "medium", "low", "unknown"]
               }
             },
             "required": [
               "partner", "partnership_type", "stage", "last_contact_date",
               "days_since_contact", "last_exchange_summary", "open_commitments",
               "next_step", "next_step_owner", "potential_value"
             ]
           }
         },
         "stalled_count": {
           "type": "number",
           "description": "Number of partnership conversations that have stalled"
         },
         "our_next_step_count": {
           "type": "number",
           "description": "Number of partnerships where the next step is ours to take"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of the partnership pipeline health and most urgent items"
         }
       },
       "required": [
         "as_of", "partnerships", "stalled_count", "our_next_step_count", "summary"
       ]
     }
   }

4. Present ordered by stage proximity to active, with stalled partnerships
   flagged. Lead with our_next_step count and stalled count.

5. Ask: "Would you like me to draft follow-up messages for any stalled or
   next-step-ours partnerships?"
