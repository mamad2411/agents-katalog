---
name: fundraising-thread-tracker
description: Tracks every active investor conversation in a fundraising process — where each conversation stands, what was said, what the next step is, and which leads have gone cold. Use when a founder is in an active fundraise and wants to manage their pipeline from email. Triggers on "fundraising pipeline", "investor conversations", "fundraise tracker", "which investors are warm", "fundraising status", "where is each investor in the process".
metadata:
  version: 1.0.0
---

# Fundraising Thread Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all investor outreach and fundraising email threads to produce a full
pipeline view — where each investor conversation stands, what was last said,
what the next step is, who has gone quiet, and which conversations are most
likely to convert.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 6 months", "the last 90 days", "May 2024",
     "since the round opened"). Default: the last 6 months. Keep the
     user's natural phrasing for use in the ask input; convert to ISO
     dates separately for the search call.
   - [investor_scope] — either "all" (default) or the name of a specific
     investor or fund to focus on.
   - [investor_clause] — derived. When [investor_scope] is not "all", set
     to " for investor [investor_scope]". When [investor_scope] is "all",
     set to empty string.

2. Call search with:
   - query: term sheet investment round deck meeting intro fund interest
     due diligence commit lead follow
     (if [investor_scope] is not "all", append the investor name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all fundraising and investor outreach email threads from [time_range][investor_clause]. For each investor or fund in the pipeline, determine: their current stage in the conversation, when contact was last made, what was last discussed, what the next step is and who owns it, their apparent level of interest based on email tone, and any signals suggesting they are moving toward a decision or pulling back.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Fundraising pipeline tracker across all active investor conversations",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this pipeline was generated"
         },
         "pipeline": {
           "type": "array",
           "description": "List of every investor in the current fundraising pipeline",
           "items": {
             "type": "object",
             "description": "A single investor conversation with current pipeline status",
             "additionalProperties": false,
             "properties": {
               "investor_name": {
                 "type": "string",
                 "description": "Name of the investor or fund"
               },
               "investor_type": {
                 "type": "string",
                 "description": "Type of investor",
                 "enum": [
                   "lead_vc", "tier_1_vc", "tier_2_vc", "angel",
                   "family_office", "strategic", "unknown"
                 ]
               },
               "stage": {
                 "type": "string",
                 "description": "Current stage of this investor conversation",
                 "enum": [
                   "initial_outreach", "intro_meeting_scheduled", "intro_meeting_done",
                   "follow_up_meeting", "due_diligence", "partner_meeting",
                   "term_sheet_discussion", "term_sheet_received", "closing",
                   "passed", "gone_quiet", "unknown"
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
               "interest_level": {
                 "type": "string",
                 "description": "Apparent level of investment interest based on email signals",
                 "enum": ["very_high", "high", "medium", "low", "unknown"]
               },
               "last_exchange_summary": {
                 "type": "string",
                 "description": "Brief summary of what was discussed in the most recent email exchange"
               },
               "next_step": {
                 "type": "string",
                 "description": "The next action required to move this conversation forward"
               },
               "next_step_owner": {
                 "type": "string",
                 "description": "Who owns the next step",
                 "enum": ["us", "investor", "both", "unknown"]
               },
               "key_concerns_raised": {
                 "type": "array",
                 "description": "Any concerns, objections, or questions this investor has raised",
                 "items": {
                   "type": "string",
                   "description": "A single concern or question raised by this investor"
                 }
               },
               "conversion_likelihood": {
                 "type": "string",
                 "description": "Estimated likelihood of this investor converting to a check",
                 "enum": ["high", "medium", "low", "unknown"]
               }
             },
             "required": [
               "investor_name", "investor_type", "stage", "last_contact_date",
               "days_since_contact", "interest_level", "last_exchange_summary",
               "next_step", "next_step_owner", "key_concerns_raised",
               "conversion_likelihood"
             ]
           }
         },
         "active_count": {
           "type": "number",
           "description": "Number of investors in active conversation"
         },
         "gone_quiet_count": {
           "type": "number",
           "description": "Number of investors who have gone quiet and need follow-up"
         },
         "high_conversion_count": {
           "type": "number",
           "description": "Number of investors with high conversion likelihood"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of the fundraising pipeline and most important next actions"
         }
       },
       "required": [
         "as_of", "pipeline", "active_count", "gone_quiet_count",
         "high_conversion_count", "summary"
       ]
     }
   }

4. Present ordered by conversion likelihood then by stage proximity to close.
   Lead with active count, high conversion count, and gone quiet count.

5. Ask: "Would you like me to draft follow-up messages for any investors
   who have gone quiet or where the next step is ours?"
