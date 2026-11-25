---
name: investor-relationship-tracker
description: Tracks the health and status of every investor relationship from email — last contact, open commitments, promises made, sentiment, and which investors have gone quiet. Use when a founder wants to manage investor relations proactively and ensure no relationship is neglected. Triggers on "investor relationships", "investor tracker", "which investors have I not spoken to", "investor outreach status", "manage investor relations", "investor pipeline".
metadata:
  version: 1.0.0
---

# Investor Relationship Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Reviews all investor-related email threads to produce a relationship health
map — last contact date, conversation tone, open commitments, any asks that
were made, and which relationships have gone quiet and need rekindling.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 12 months", "the last year", "May 2024",
     "since the last update"). Default: the last 12 months. Keep the
     user's natural phrasing for use in the ask input; convert to ISO
     dates separately for the search call.
   - [investor_scope] — either "all" (default) or the name of a specific
     investor to focus on.
   - [investor_clause] — derived. When [investor_scope] is not "all", set
     to " for investor [investor_scope]". When [investor_scope] is "all",
     set to empty string.

2. Call search with:
   - query: investor update portfolio company board check-in intro meeting
     committed interest follow up
     (if [investor_scope] is not "all", append the investor name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all investor-related email threads from [time_range][investor_clause]. For each investor identify: when you last had meaningful contact, the overall tone and sentiment of the relationship, any commitments or promises made by either side that remain open, any asks the investor made that were not fully addressed, and whether the relationship appears warm, cool, or stale based on email patterns.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Investor relationship health tracker across all investor contacts",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "investors": {
           "type": "array",
           "description": "List of every investor with relationship health assessment",
           "items": {
             "type": "object",
             "description": "Relationship status for a single investor",
             "additionalProperties": false,
             "properties": {
               "investor_name": {
                 "type": "string",
                 "description": "Name of the investor or investment firm"
               },
               "investor_type": {
                 "type": "string",
                 "description": "Type of investor",
                 "enum": [
                   "lead_vc", "participating_vc", "angel", "family_office",
                   "strategic", "prospective", "other"
                 ]
               },
               "last_contact_date": {
                 "type": "string",
                 "description": "ISO8601 date of the most recent meaningful email exchange"
               },
               "days_since_contact": {
                 "type": "number",
                 "description": "Number of days since last meaningful contact"
               },
               "relationship_health": {
                 "type": "string",
                 "description": "Overall health of this investor relationship based on email patterns",
                 "enum": ["strong", "warm", "neutral", "cooling", "stale", "unknown"]
               },
               "sentiment": {
                 "type": "string",
                 "description": "Overall tone of the most recent communications",
                 "enum": ["very_positive", "positive", "neutral", "negative", "unknown"]
               },
               "open_commitments": {
                 "type": "array",
                 "description": "Commitments made by either side that have not been confirmed as complete",
                 "items": {
                   "type": "object",
                   "description": "A single open commitment in this investor relationship",
                   "additionalProperties": false,
                   "properties": {
                     "commitment": {
                       "type": "string",
                       "description": "Description of the commitment made"
                     },
                     "made_by": {
                       "type": "string",
                       "description": "Who made this commitment",
                       "enum": ["us", "investor", "unknown"]
                     },
                     "date": {
                       "type": "string",
                       "description": "ISO8601 date the commitment was made"
                     }
                   },
                   "required": ["commitment", "made_by", "date"]
                 }
               },
               "unanswered_asks": {
                 "type": "array",
                 "description": "Questions or requests from this investor that have not been fully addressed",
                 "items": {
                   "type": "string",
                   "description": "A single unanswered ask from the investor"
                 }
               },
               "recommended_action": {
                 "type": "string",
                 "description": "Recommended next step to maintain or strengthen this relationship"
               }
             },
             "required": [
               "investor_name", "investor_type", "last_contact_date",
               "days_since_contact", "relationship_health", "sentiment",
               "open_commitments", "unanswered_asks", "recommended_action"
             ]
           }
         },
         "stale_count": {
           "type": "number",
           "description": "Number of investor relationships that have gone stale"
         },
         "open_commitments_count": {
           "type": "number",
           "description": "Total number of open commitments across all investor relationships"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of overall investor relationship health and most urgent actions"
         }
       },
       "required": [
         "as_of", "investors", "stale_count", "open_commitments_count", "summary"
       ]
     }
   }

4. Present investors ordered by relationship health (stale first), then by
   days since contact. Lead with stale count and any open commitments that
   are ours to fulfill.

5. Ask: "Would you like me to draft investor update emails for any stale
   or cooling relationships?"
