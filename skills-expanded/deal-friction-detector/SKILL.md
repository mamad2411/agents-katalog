---
name: deal-friction-detector
description: Detects objections, hesitations, pricing friction, and blockers buried in sales email threads. Use when a salesperson wants to understand why a deal is stalling or what concerns have been raised. Triggers on "why is this deal stuck", "what objections do they have", "deal friction", "what are they worried about", "why aren't they responding".
metadata:
  version: 1.0.0
---

# Deal Friction Detector

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Reads between the lines of sales email threads to surface friction signals:
hesitation language, pricing objections, competitor comparisons, approval
blockers, timeline pushback, and patterns suggesting the deal is at risk —
even when nothing was stated explicitly.

---

## Workflow

1. Before calling any tool, collect these values from the user. Do not
   invent values they did not give.

   - [deal] — the name of the deal or company to analyze. No default —
     must come from the user.
   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 60 days", "the last 2 months", "May 2024",
     "since the proposal was sent"). Default: the last 60 days. Keep
     the user's natural phrasing for use in the ask input; convert to
     ISO dates separately for the search call.

2. Call search with:
   - query: concern hesitation price timeline competitor approval budget [deal]
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Analyze all email threads related to [deal] from [time_range]. Identify every friction signal: explicit objections, hesitation language, discount requests, competitor mentions, response delays, approval language, budget concerns, or any signal this deal may be stalling. For each signal note the type, evidence from the email, who expressed it, severity, and a suggested response.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Friction analysis report for a single sales deal",
       "additionalProperties": false,
       "properties": {
         "deal": {
           "type": "string",
           "description": "Name of the deal or company being analyzed"
         },
         "overall_risk": {
           "type": "string",
           "description": "Overall risk assessment of the deal based on all friction signals found",
           "enum": ["high", "medium", "low", "unknown"]
         },
         "friction_signals": {
           "type": "array",
           "description": "List of every friction signal detected across email threads",
           "items": {
             "type": "object",
             "description": "A single friction signal detected in the email threads",
             "additionalProperties": false,
             "properties": {
               "type": {
                 "type": "string",
                 "description": "Category of friction signal",
                 "enum": [
                   "pricing_objection", "timeline_pushback", "competitor_comparison",
                   "approval_blocker", "budget_concern", "hesitation_language",
                   "silence_gap", "scope_concern", "other"
                 ]
               },
               "evidence": {
                 "type": "string",
                 "description": "Direct quote or close paraphrase from the email that surfaces this signal"
               },
               "from": {
                 "type": "string",
                 "description": "Name or role of the person who expressed this signal"
               },
               "date": {
                 "type": "string",
                 "description": "ISO8601 date when this signal appeared"
               },
               "severity": {
                 "type": "string",
                 "description": "How much this signal threatens the deal",
                 "enum": ["high", "medium", "low"]
               },
               "suggested_response": {
                 "type": "string",
                 "description": "Recommended action or message to address this friction signal"
               }
             },
             "required": ["type", "evidence", "from", "date", "severity", "suggested_response"]
           }
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of the deal's overall friction situation"
         }
       },
       "required": ["deal", "overall_risk", "friction_signals", "summary"]
     }
   }

4. Present overall risk level first, then signals ordered by severity.
   Include the suggested response for each signal.

5. Ask: "Would you like help crafting a response to address any of these?"
