---
name: scope-creep-detector
description: Detects scope creep signals across active consulting engagements — requests that go beyond the agreed statement of work, informal additions accepted without change orders, and patterns of expanding client expectations. Use when a consultant wants to identify where they are working outside scope and need to have a change order conversation. Triggers on "scope creep", "out of scope requests", "working outside the SOW", "scope expansion", "change order needed", "what's outside the original scope".
metadata:
  version: 1.0.0
---

# Scope Creep Detector

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Reads client engagement email threads to surface every instance where work
was requested or agreed to that appears to go beyond the original statement
of work — informal additions, expanded deliverables, extra meetings, and
requests accepted without a formal change order — and quantifies the pattern
by client.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last 3 months", "May 2024",
     "since the project kickoff"). Default: the last 90 days. Keep the
     user's natural phrasing for use in the ask input; convert to ISO
     dates separately for the search call.
   - [client_scope] — either "all" (default) or the name of a specific
     engagement to focus on.
   - [client_clause] — derived. When [client_scope] is not "all", set to
     " for client [client_scope]". When [client_scope] is "all", set to
     empty string.

2. Call search with:
   - query: also can you could you additionally while you're at it extra
     add on top of that quick favor one more thing
     (if [client_scope] is not "all", append the client name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all client engagement email threads from [time_range][client_clause]. Identify every instance of potential scope creep — requests for work not covered in the original agreement, additional deliverables accepted informally, expanded meeting or support time, and any pattern where the client's expectations appear to be growing beyond what was scoped and priced. For each instance note the client, what was requested, whether it was accepted, and whether a change order or repricing conversation is warranted.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Scope creep detection report across active consulting engagements",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "scope_creep_instances": {
           "type": "array",
           "description": "List of every potential scope creep instance found across client engagements",
           "items": {
             "type": "object",
             "description": "A single scope creep instance with context and recommendation",
             "additionalProperties": false,
             "properties": {
               "client": {
                 "type": "string",
                 "description": "Name of the client where scope creep was detected"
               },
               "description": {
                 "type": "string",
                 "description": "Clear description of what was requested or accepted beyond original scope"
               },
               "creep_type": {
                 "type": "string",
                 "description": "Category of scope creep",
                 "enum": [
                   "additional_deliverable", "expanded_deliverable", "extra_meeting",
                   "unscoped_support", "timeline_extension", "extra_stakeholder",
                   "informal_addition", "other"
                 ]
               },
               "date_requested": {
                 "type": "string",
                 "description": "ISO8601 date when the out-of-scope request was made"
               },
               "accepted": {
                 "type": "boolean",
                 "description": "Whether this out-of-scope request was accepted without a change order"
               },
               "change_order_raised": {
                 "type": "boolean",
                 "description": "Whether a change order or repricing conversation has been raised for this item"
               },
               "estimated_impact": {
                 "type": "string",
                 "description": "Assessment of the time or cost impact of this scope addition",
                 "enum": ["significant", "moderate", "minor", "unknown"]
               },
               "evidence": {
                 "type": "string",
                 "description": "Quote or paraphrase from email that surfaces this scope creep instance"
               },
               "recommended_action": {
                 "type": "string",
                 "description": "Recommended action — raise a change order, have a scope conversation, or document for the next renewal"
               }
             },
             "required": [
               "client", "description", "creep_type", "date_requested",
               "accepted", "change_order_raised", "estimated_impact",
               "evidence", "recommended_action"
             ]
           }
         },
         "by_client": {
           "type": "array",
           "description": "Summary of scope creep instances grouped by client",
           "items": {
             "type": "object",
             "description": "Scope creep summary for a single client",
             "additionalProperties": false,
             "properties": {
               "client": {
                 "type": "string",
                 "description": "Name of the client"
               },
               "instance_count": {
                 "type": "number",
                 "description": "Number of scope creep instances for this client"
               },
               "unaddressed_count": {
                 "type": "number",
                 "description": "Number of instances accepted without a change order"
               },
               "overall_severity": {
                 "type": "string",
                 "description": "Overall severity of scope creep for this client",
                 "enum": ["significant", "moderate", "minor", "none"]
               }
             },
             "required": ["client", "instance_count", "unaddressed_count", "overall_severity"]
           }
         },
         "total_unaddressed": {
           "type": "number",
           "description": "Total number of scope creep instances accepted without a change order"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of scope creep patterns and clients most at risk of under-billing"
         }
       },
       "required": [
         "as_of", "scope_creep_instances", "by_client", "total_unaddressed", "summary"
       ]
     }
   }

4. Present by client ordered by unaddressed count. Lead with total
   unaddressed instances and the client with the most significant scope
   creep pattern.

5. Ask: "Would you like me to draft a change order conversation email
   for any of these clients?"
