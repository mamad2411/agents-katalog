---
name: client-feedback-collector
description: Collects and structures all client feedback received across consulting engagements — formal feedback, informal reactions, satisfaction signals, and criticism — so the consultant has a consolidated view of how each client perceives the work. Use when a consultant wants to understand their client satisfaction landscape. Triggers on "client feedback", "what are clients saying about the work", "satisfaction signals", "collect feedback", "how happy are my clients", "client reactions".
metadata:
  version: 1.0.0
---

# Client Feedback Collector

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all client engagement email threads for feedback signals — formal
feedback given, informal reactions to deliverables, satisfaction or
dissatisfaction language, praise, criticism, and any pattern suggesting
a client's perception of the engagement is shifting — and returns a
structured satisfaction view by client.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 6 months", "the last 90 days", "May 2024",
     "since the kickoff"). Default: the last 6 months. Keep the user's
     natural phrasing for use in the ask input; convert to ISO dates
     separately for the search call.
   - [client_scope] — either "all" (default) or the name of a specific
     client to focus on.
   - [client_clause] — derived. When [client_scope] is not "all", set to
     " for client [client_scope]". When [client_scope] is "all", set to
     empty string.

2. Call search with:
   - query: feedback great love excellent disappointed not what we expected
     impressed could be better well done thank you result
     (if [client_scope] is not "all", append the client name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all client engagement email threads from [time_range][client_clause]. For each client, collect every piece of feedback they have expressed — formal feedback on deliverables, informal reactions, expressions of satisfaction or dissatisfaction, praise for specific work, criticism or concerns raised, and any pattern suggesting how the client perceives the engagement overall. Note the sentiment, what specifically was referenced, and whether the feedback was actioned.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Client feedback collection across all active consulting engagements",
       "additionalProperties": false,
       "properties": {
         "period_from": {
           "type": "string",
           "description": "ISO8601 start date of the period covered"
         },
         "period_to": {
           "type": "string",
           "description": "ISO8601 end date of the period covered"
         },
         "clients": {
           "type": "array",
           "description": "List of clients with aggregated feedback",
           "items": {
             "type": "object",
             "description": "Feedback summary for a single client",
             "additionalProperties": false,
             "properties": {
               "client": {
                 "type": "string",
                 "description": "Name of the client"
               },
               "overall_satisfaction": {
                 "type": "string",
                 "description": "Overall satisfaction level inferred from email signals",
                 "enum": ["very_satisfied", "satisfied", "neutral", "dissatisfied", "very_dissatisfied", "unknown"]
               },
               "satisfaction_trend": {
                 "type": "string",
                 "description": "Whether client satisfaction appears to be improving or declining over the period",
                 "enum": ["improving", "stable", "declining", "unknown"]
               },
               "feedback_items": {
                 "type": "array",
                 "description": "Individual feedback points from this client",
                 "items": {
                   "type": "object",
                   "description": "A single feedback item from this client",
                   "additionalProperties": false,
                   "properties": {
                     "feedback": {
                       "type": "string",
                       "description": "The feedback as expressed or closely paraphrased"
                     },
                     "feedback_type": {
                       "type": "string",
                       "description": "Category of feedback",
                       "enum": [
                         "praise", "constructive_criticism", "complaint",
                         "suggestion", "satisfaction_signal", "concern", "other"
                       ]
                     },
                     "about": {
                       "type": "string",
                       "description": "What deliverable, aspect, or interaction this feedback relates to"
                     },
                     "sentiment": {
                       "type": "string",
                       "description": "Sentiment of this feedback item",
                       "enum": ["positive", "neutral", "negative"]
                     },
                     "date": {
                       "type": "string",
                       "description": "ISO8601 date this feedback was given"
                     },
                     "actioned": {
                       "type": "boolean",
                       "description": "Whether this feedback has been addressed or responded to"
                     }
                   },
                   "required": [
                     "feedback", "feedback_type", "about", "sentiment", "date", "actioned"
                   ]
                 }
               },
               "unactioned_concerns": {
                 "type": "array",
                 "description": "Negative feedback or concerns from this client that have not yet been addressed",
                 "items": {
                   "type": "string",
                   "description": "An unaddressed concern or piece of negative feedback"
                 }
               },
               "relationship_risk": {
                 "type": "string",
                 "description": "Risk level to the client relationship based on feedback patterns",
                 "enum": ["high", "medium", "low", "none"]
               }
             },
             "required": [
               "client", "overall_satisfaction", "satisfaction_trend",
               "feedback_items", "unactioned_concerns", "relationship_risk"
             ]
           }
         },
         "at_risk_count": {
           "type": "number",
           "description": "Number of clients with high relationship risk based on feedback"
         },
         "unactioned_concerns_count": {
           "type": "number",
           "description": "Total number of unactioned concerns across all clients"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of overall client satisfaction and most urgent concerns"
         }
       },
       "required": [
         "period_from", "period_to", "clients", "at_risk_count",
         "unactioned_concerns_count", "summary"
       ]
     }
   }

4. Present clients with high relationship risk and declining satisfaction
   first. Lead with at_risk count and unactioned concerns count.

5. Ask: "Would you like me to draft a client check-in or feedback response
   for any of these clients?"
