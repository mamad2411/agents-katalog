---
name: past-solutions-matcher
description: Given a prospect's current problem, finds similar problems solved for past customers — surfacing proof points and solution patterns from email history. Use when a salesperson wants to reference a similar win in a sales conversation. Triggers on "have we solved this before", "similar customer problem", "find me a reference", "past solutions", "who else had this problem".
metadata:
  version: 1.0.0
---

# Past Solutions Matcher

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Takes a description of a prospect's current problem and searches email history
for past customers who had the same or a similar problem — what the solution
was, what the outcome was, and any customer language expressing results.

---

## Workflow

1. Before calling any tool, collect these values from the user. Do not
   invent values they did not give.

   - [problem] — a clear 1-2 sentence description of the problem or
     challenge the current prospect is facing. No default — must come
     from the user. Ask a follow-up question if their first description
     is too vague to search on.
   - [time_range] — what window of email history to search. The user
     may give this in any form ("last 2 years", "the last 24 months",
     "May 2024 onward", "since I joined"). Default: the last 2 years.
     Keep the user's natural phrasing for use in the ask input; convert
     to ISO dates separately for the search call.

2. Call search with:
   - query: solved success result outcome [problem]
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Search all email history from [time_range] for customers who faced a similar problem to this: [problem]. For each match identify: the customer company, their specific problem, the solution applied, the outcome or result mentioned in email, and any customer quotes expressing satisfaction or results.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Past solutions report matching a current prospect problem to historical customer wins",
       "additionalProperties": false,
       "properties": {
         "prospect_problem": {
           "type": "string",
           "description": "The problem description provided by the salesperson for the current prospect"
         },
         "matches": {
           "type": "array",
           "description": "List of past customers whose problems closely match the prospect's current situation",
           "items": {
             "type": "object",
             "description": "A single past customer match with solution and outcome details",
             "additionalProperties": false,
             "properties": {
               "customer": {
                 "type": "string",
                 "description": "Name of the past customer company"
               },
               "their_problem": {
                 "type": "string",
                 "description": "Description of the problem this past customer faced"
               },
               "solution_applied": {
                 "type": "string",
                 "description": "What solution was implemented or proposed to solve their problem"
               },
               "outcome": {
                 "type": "string",
                 "description": "The result or outcome as mentioned in email threads"
               },
               "customer_quote": {
                 "type": "string",
                 "description": "A direct or paraphrased quote from the customer expressing satisfaction or results, empty string if none found"
               },
               "relevance": {
                 "type": "string",
                 "description": "How closely this past situation matches the current prospect's problem",
                 "enum": ["high", "medium", "low"]
               }
             },
             "required": ["customer", "their_problem", "solution_applied", "outcome", "customer_quote", "relevance"]
           }
         },
         "recommended_reference": {
           "type": "string",
           "description": "Name of the single best past customer to reference in the current sales conversation and why"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of what was found and the strongest proof point available"
         }
       },
       "required": ["prospect_problem", "matches", "recommended_reference", "summary"]
     }
   }

4. Present ordered by relevance. Lead with the recommended reference and
   a one-line pitch for why it is the strongest match.

5. Ask: "Would you like me to draft a message referencing this customer story?"
