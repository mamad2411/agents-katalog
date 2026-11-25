---
name: risk-radar
description: Surfaces project risks — timeline slippage signals, resource concerns, scope creep warnings, dependency risks, and stakeholder concerns — buried in project email threads. Use when a project manager wants an early warning scan of risks before they become problems. Triggers on "project risks", "risk radar", "what could go wrong", "early warning signs", "risk scan", "project risk assessment".
metadata:
  version: 1.0.0
---

# Risk Radar

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Reads between the lines of project email threads to detect early warning
signals — slippage language, resource pressure, scope creep, stakeholder
concerns, and dependency risks — before they escalate into actual project
failures.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 60 days", "the last 2 months", "May 2024",
     "since the last steering meeting"). Default: the last 60 days.
     Keep the user's natural phrasing for use in the ask input; convert
     to ISO dates separately for the search call.
   - [project_scope] — either "all" (default) or the name or topic of a
     specific project to focus on.
   - [project_clause] — derived. When [project_scope] is not "all", set
     to " related to [project_scope]". When [project_scope] is "all",
     set to empty string.

2. Call search with:
   - query: concern risk delay slipping scope change resource pressure worried
     (if [project_scope] is not "all", append the project name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Analyze all email threads from [time_range][project_clause]. Identify every risk signal — language suggesting timelines are slipping, resource pressure or availability concerns, scope additions not formally agreed, dependency risks, stakeholder dissatisfaction, budget pressure, and any pattern suggesting the project is at risk of missing its goals. For each risk note the type, the evidence, who raised it, and how serious it appears.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Project risk radar report identifying early warning signals from email",
       "additionalProperties": false,
       "properties": {
         "project": {
           "type": "string",
           "description": "Name or description of the project being analyzed"
         },
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "overall_health": {
           "type": "string",
           "description": "Overall project health assessment based on risk signals found",
           "enum": ["critical", "at_risk", "caution", "healthy", "unknown"]
         },
         "risks": {
           "type": "array",
           "description": "List of every risk signal detected across project email threads",
           "items": {
             "type": "object",
             "description": "A single project risk signal with full context",
             "additionalProperties": false,
             "properties": {
               "risk_type": {
                 "type": "string",
                 "description": "Category of risk",
                 "enum": [
                   "timeline_slippage", "scope_creep", "resource_pressure",
                   "dependency_risk", "stakeholder_concern", "budget_pressure",
                   "quality_concern", "communication_breakdown", "other"
                 ]
               },
               "description": {
                 "type": "string",
                 "description": "Clear description of what the risk is and how it could affect the project"
               },
               "evidence": {
                 "type": "string",
                 "description": "Quote or paraphrase from email that surfaces this risk signal"
               },
               "raised_by": {
                 "type": "string",
                 "description": "Name or role of the person whose email surfaced this risk"
               },
               "date": {
                 "type": "string",
                 "description": "ISO8601 date when this risk signal appeared"
               },
               "severity": {
                 "type": "string",
                 "description": "How much this risk threatens the project if unaddressed",
                 "enum": ["critical", "high", "medium", "low"]
               },
               "likelihood": {
                 "type": "string",
                 "description": "How likely this risk is to materialize based on email signals",
                 "enum": ["high", "medium", "low", "unknown"]
               },
               "recommended_action": {
                 "type": "string",
                 "description": "Recommended step to mitigate or monitor this risk"
               }
             },
             "required": [
               "risk_type", "description", "evidence", "raised_by",
               "date", "severity", "likelihood", "recommended_action"
             ]
           }
         },
         "critical_count": {
           "type": "number",
           "description": "Number of risks rated as critical severity"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of overall project health and top risks"
         }
       },
       "required": [
         "project", "as_of", "overall_health", "risks", "critical_count", "summary"
       ]
     }
   }

4. Present overall health status first, then risks ordered by severity then
   likelihood. Lead with critical count and the top risk.

5. Ask: "Would you like me to draft a risk update for stakeholders?"
