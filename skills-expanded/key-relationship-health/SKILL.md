---
name: key-relationship-health
description: Monitors the health of the executive's most important relationships — key customers, partners, advisors, and senior hires — based on email engagement patterns, sentiment, and open items. Use when a founder or CEO wants a relationship health dashboard across their most strategically important contacts. Triggers on "relationship health", "key relationships", "who have I neglected", "relationship dashboard", "strategic contacts status", "important relationships going cold".
metadata:
  version: 1.0.0
---

# Key Relationship Health

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Reviews email engagement patterns with the executive's most important
relationships — customers, partners, advisors, and senior hires — to surface
which are strong, which are cooling, which have gone quiet, and what open
items exist in each.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last 3 months", "May 2024",
     "since the offsite"). Default: the last 90 days. Keep the user's
     natural phrasing for use in the ask input; convert to ISO dates
     separately for the search call.
   - [category_scope] — either "all" (default) or a specific category
     of relationship to focus on (e.g. "key customers", "advisors",
     "strategic partners").
   - [category_clause] — derived. When [category_scope] is not "all", set
     to " across [category_scope]". When [category_scope] is "all", set
     to empty string.

2. Call search with:
   - query: partner advisor customer key account strategic relationship
     introduction meeting check-in
     (if [category_scope] is not "all", append the category name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads from [time_range][category_clause] involving key customers, strategic partners, advisors, and senior external contacts. For each relationship assess: when contact was last made, the overall tone and engagement level, any open items or unresolved commitments, whether the relationship appears to be strengthening or cooling, and what action would be recommended to maintain or improve it.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Key relationship health dashboard for executive contacts",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this dashboard was generated"
         },
         "relationships": {
           "type": "array",
           "description": "List of key relationships with health assessments",
           "items": {
             "type": "object",
             "description": "Health assessment for a single key relationship",
             "additionalProperties": false,
             "properties": {
               "contact_name": {
                 "type": "string",
                 "description": "Name of the key contact"
               },
               "organization": {
                 "type": "string",
                 "description": "Company or organization this contact is associated with"
               },
               "relationship_type": {
                 "type": "string",
                 "description": "Category of this key relationship",
                 "enum": [
                   "key_customer", "strategic_partner", "advisor", "board_member",
                   "senior_hire", "press_or_analyst", "government_or_regulator", "other"
                 ]
               },
               "last_contact_date": {
                 "type": "string",
                 "description": "ISO8601 date of the most recent meaningful email exchange"
               },
               "days_since_contact": {
                 "type": "number",
                 "description": "Number of days since the last meaningful exchange"
               },
               "health": {
                 "type": "string",
                 "description": "Overall health of this relationship based on email engagement",
                 "enum": ["strong", "warm", "neutral", "cooling", "stale", "unknown"]
               },
               "engagement_trend": {
                 "type": "string",
                 "description": "Whether this relationship's engagement is improving or declining",
                 "enum": ["improving", "stable", "declining", "unknown"]
               },
               "open_items": {
                 "type": "array",
                 "description": "Unresolved commitments, questions, or actions in this relationship",
                 "items": {
                   "type": "string",
                   "description": "A single open item in this relationship"
                 }
               },
               "last_conversation_summary": {
                 "type": "string",
                 "description": "Brief summary of what the most recent email exchange was about"
               },
               "recommended_action": {
                 "type": "string",
                 "description": "Recommended action to maintain or strengthen this relationship"
               }
             },
             "required": [
               "contact_name", "organization", "relationship_type",
               "last_contact_date", "days_since_contact", "health",
               "engagement_trend", "open_items", "last_conversation_summary",
               "recommended_action"
             ]
           }
         },
         "stale_count": {
           "type": "number",
           "description": "Number of key relationships that have gone stale"
         },
         "cooling_count": {
           "type": "number",
           "description": "Number of key relationships that are cooling"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of overall relationship portfolio health"
         }
       },
       "required": [
         "as_of", "relationships", "stale_count", "cooling_count", "summary"
       ]
     }
   }

4. Present stale and cooling relationships first, ordered by days since
   contact. Lead with stale and cooling counts.

5. Ask: "Would you like me to draft reconnection messages for any stale
   or cooling relationships?"
