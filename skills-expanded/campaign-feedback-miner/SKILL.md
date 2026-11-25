---
name: campaign-feedback-miner
description: Extracts feedback on marketing campaigns from email — reactions from internal stakeholders, partner responses, customer replies, and agency comments — and structures it by campaign and theme. Use when a marketing team wants to consolidate scattered feedback on active or recent campaigns. Triggers on "campaign feedback", "what are people saying about the campaign", "collect campaign reactions", "campaign response feedback", "stakeholder feedback on marketing", "what worked in the campaign".
metadata:
  version: 1.0.0
---

# Campaign Feedback Miner

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans email for feedback, reactions, and commentary on marketing campaigns
from all sources — internal team, external partners, customers, and agencies
— and returns it structured by campaign, sentiment, and feedback theme.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last 3 months", "May 2024",
     "since the spring campaign launched"). Default: the last 90 days.
     Keep the user's natural phrasing for use in the ask input; convert
     to ISO dates separately for the search call.
   - [campaign_scope] — either "all" (default) or the name of a specific
     campaign to focus on.
   - [campaign_clause] — derived. When [campaign_scope] is not "all",
     set to " for campaign [campaign_scope]". When [campaign_scope] is
     "all", set to empty string.

2. Call search with:
   - query: campaign feedback response reaction results worked didn't work
     messaging creative performance
     (if [campaign_scope] is not "all", append the campaign name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads from [time_range][campaign_clause] that reference marketing campaigns. For each campaign mentioned, extract every piece of feedback or reaction — from internal stakeholders, external partners, customers, or agencies. Note who gave the feedback, what their overall sentiment was, what specific aspects they commented on, and whether the feedback was actionable. Group by campaign and identify the most common themes.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Campaign feedback report mined from email threads",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "campaigns": {
           "type": "array",
           "description": "List of campaigns with aggregated feedback",
           "items": {
             "type": "object",
             "description": "Feedback summary for a single campaign",
             "additionalProperties": false,
             "properties": {
               "campaign_name": {
                 "type": "string",
                 "description": "Name or description of the campaign"
               },
               "overall_sentiment": {
                 "type": "string",
                 "description": "Overall sentiment of feedback received for this campaign",
                 "enum": ["very_positive", "positive", "mixed", "negative", "very_negative", "unknown"]
               },
               "feedback_items": {
                 "type": "array",
                 "description": "Individual pieces of feedback received for this campaign",
                 "items": {
                   "type": "object",
                   "description": "A single feedback item from a specific source",
                   "additionalProperties": false,
                   "properties": {
                     "source": {
                       "type": "string",
                       "description": "Name or role of the person who gave this feedback"
                     },
                     "source_type": {
                       "type": "string",
                       "description": "Category of feedback source",
                       "enum": [
                         "internal_stakeholder", "partner", "customer",
                         "agency", "executive", "other"
                       ]
                     },
                     "feedback": {
                       "type": "string",
                       "description": "The feedback or reaction as expressed or closely paraphrased"
                     },
                     "sentiment": {
                       "type": "string",
                       "description": "Sentiment of this specific feedback item",
                       "enum": ["positive", "negative", "neutral", "mixed"]
                     },
                     "aspect": {
                       "type": "string",
                       "description": "What aspect of the campaign this feedback addresses",
                       "enum": [
                         "messaging", "creative", "targeting", "timing",
                         "channel", "results", "budget", "process", "other"
                       ]
                     },
                     "actionable": {
                       "type": "boolean",
                       "description": "Whether this feedback contains a specific actionable suggestion"
                     },
                     "date": {
                       "type": "string",
                       "description": "ISO8601 date when this feedback was given"
                     }
                   },
                   "required": [
                     "source", "source_type", "feedback", "sentiment",
                     "aspect", "actionable", "date"
                   ]
                 }
               },
               "top_themes": {
                 "type": "array",
                 "description": "The most common feedback themes for this campaign",
                 "items": {
                   "type": "string",
                   "description": "A recurring feedback theme"
                 }
               },
               "actionable_items": {
                 "type": "array",
                 "description": "Specific actionable improvements suggested across all feedback for this campaign",
                 "items": {
                   "type": "string",
                   "description": "A single actionable improvement or suggestion"
                 }
               }
             },
             "required": [
               "campaign_name", "overall_sentiment", "feedback_items",
               "top_themes", "actionable_items"
             ]
           }
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of overall campaign feedback and top themes across all campaigns"
         }
       },
       "required": ["as_of", "campaigns", "summary"]
     }
   }

4. Present by campaign, with overall sentiment leading each section.
   Highlight actionable items prominently. Lead with the summary.

5. Ask: "Would you like me to compile these into a campaign retrospective
   document?"
