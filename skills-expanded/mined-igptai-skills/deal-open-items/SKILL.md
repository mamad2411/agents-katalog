---
name: deal-open-items
description: Surfaces every unresolved commitment, pending decision, and unanswered question across active sales deal threads. Use when a salesperson wants to know what is still open in a deal, what was promised but not confirmed, or what is blocking progress. Triggers on "what's still open", "open items", "what do I owe them", "what's blocking this deal".
metadata:
  version: 1.0.0
---

# Deal Open Items

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Finds every unresolved commitment, unanswered question, and pending decision
buried in active sales email threads — things the salesperson promised to do,
questions from the prospect never answered, and decisions raised but never
confirmed.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last quarter", "May 2024",
     "since the discovery call"). Default: the last 90 days. Keep the
     user's natural phrasing for use in the ask input; convert to ISO
     dates separately for the search call.
   - [deal_scope] — either "all" (default) or the name of a specific
     deal, company, or contact to focus on.
   - [deal_clause] — derived. When [deal_scope] is not "all", set to
     " related to [deal_scope]". When [deal_scope] is "all", set to
     empty string.

2. Call search with:
   - query: open items commitments questions pending decision
     (if [deal_scope] is not "all", append the deal, company, or contact to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads from [time_range][deal_clause]. Extract every open item: any commitment made by either party with no confirmation of completion, any question asked that was never answered, and any decision raised but never resolved. For each item include who owns it, what was said, the date raised, and urgency.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Full open items report for a single sales deal",
       "additionalProperties": false,
       "properties": {
         "deal": {
           "type": "string",
           "description": "Name of the deal or company being analyzed"
         },
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "open_items": {
           "type": "array",
           "description": "List of every unresolved item found across email threads",
           "items": {
             "type": "object",
             "description": "A single unresolved commitment, question, or decision",
             "additionalProperties": false,
             "properties": {
               "type": {
                 "type": "string",
                 "description": "Category of the open item",
                 "enum": ["commitment", "unanswered_question", "pending_decision"]
               },
               "description": {
                 "type": "string",
                 "description": "Clear description of what is open and what was said"
               },
               "owned_by": {
                 "type": "string",
                 "description": "Which party is responsible for resolving this item",
                 "enum": ["us", "prospect", "unknown"]
               },
               "raised_on": {
                 "type": "string",
                 "description": "ISO8601 date when this item was first raised"
               },
               "status": {
                 "type": "string",
                 "description": "Whether the item is fully open or has had some partial response",
                 "enum": ["open", "partially_addressed"]
               },
               "urgency": {
                 "type": "string",
                 "description": "How urgently this item needs to be resolved to keep the deal moving",
                 "enum": ["high", "medium", "low"]
               }
             },
             "required": ["type", "description", "owned_by", "raised_on", "status", "urgency"]
           }
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of the overall open items situation for this deal"
         }
       },
       "required": ["deal", "as_of", "open_items", "summary"]
     }
   }

4. Present grouped by type: our commitments first, then prospect's, then
   pending decisions. Lead with total count and the most urgent item.

5. Ask: "Would you like me to draft follow-up emails for any of these?"

---

## If No Results Found

Tell the user: "No open items found for [deal name] in the last 90 days.
Tell me how far back to look and I will expand the search."
