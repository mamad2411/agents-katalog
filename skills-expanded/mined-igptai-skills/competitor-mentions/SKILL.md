---
name: competitor-mentions
description: Extracts every mention of a competitor from prospect and customer email threads with context about how they were raised. Use when a salesperson wants to understand their competitive landscape from real conversations. Triggers on "competitor mentions", "who are they comparing us to", "competitive intelligence", "what are prospects saying about competitors".
metadata:
  version: 1.0.0
---

# Competitor Mentions

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Surfaces every time a competitor was mentioned in prospect or customer email
threads — who mentioned them, in what context, how favorably, and what concern
was behind the comparison. Turns scattered signals into a structured brief.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 180 days", "the last 6 months", "May 2024",
     "since the new competitor launched"). Default: the last 180 days.
     Keep the user's natural phrasing for use in the ask input; convert
     to ISO dates separately for the search call.
   - [account_scope] — either "all" (default) or the name of a specific
     account to focus on.
   - [competitor_scope] — either "all" (default) or the name of a
     specific competitor to focus on.
   - [scope_clause] — derived. Combine [account_scope] and
     [competitor_scope] into a single natural-language clause: when
     both are "all", set to empty string; when only account is
     specified, set to " for account [account_scope]"; when only
     competitor is specified, set to " mentioning competitor
     [competitor_scope]"; when both are specified, set to " for
     account [account_scope] mentioning competitor [competitor_scope]".

2. Call search with:
   - query: competitor alternative compared considering switching versus
     (if [account_scope] is not "all", append the account name to the query;
     if [competitor_scope] is not "all", append the competitor name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads from [time_range][scope_clause]. Find every mention of a competitor, alternative product, or comparison to another vendor. For each: identify the competitor named, who mentioned them, the context, whether the mention was favorable or unfavorable to us, and what concern was behind it.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Competitive intelligence report extracted from email threads",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "mentions": {
           "type": "array",
           "description": "List of every competitor mention found across email threads",
           "items": {
             "type": "object",
             "description": "A single competitor mention with full context",
             "additionalProperties": false,
             "properties": {
               "competitor": {
                 "type": "string",
                 "description": "Name of the competitor or alternative product mentioned"
               },
               "mentioned_by": {
                 "type": "string",
                 "description": "Name or role of the person who mentioned the competitor"
               },
               "account": {
                 "type": "string",
                 "description": "Company or deal where this mention occurred"
               },
               "date": {
                 "type": "string",
                 "description": "ISO8601 date when the mention occurred"
               },
               "context": {
                 "type": "string",
                 "description": "What was being discussed when the competitor was mentioned"
               },
               "sentiment": {
                 "type": "string",
                 "description": "Whether the mention suggested we are winning or losing this comparison",
                 "enum": ["favorable_to_us", "unfavorable_to_us", "neutral"]
               },
               "underlying_concern": {
                 "type": "string",
                 "description": "The real concern or question behind why this competitor was brought up"
               }
             },
             "required": ["competitor", "mentioned_by", "account", "date", "context", "sentiment", "underlying_concern"]
           }
         },
         "most_mentioned": {
           "type": "string",
           "description": "Name of the competitor mentioned most frequently across all threads"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of the competitive landscape from email history"
         }
       },
       "required": ["as_of", "mentions", "most_mentioned", "summary"]
     }
   }

4. Present grouped by competitor, ordered by frequency. Highlight the most
   mentioned competitor and the most common underlying concern.
