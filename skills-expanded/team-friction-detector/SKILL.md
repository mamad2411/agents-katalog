---
name: team-friction-detector
description: Detects interpersonal friction, team tension, communication breakdown, and morale signals buried in internal email threads. Use when an HR manager or people lead wants an early warning of team health issues before they escalate. Triggers on "team friction", "team tension", "interpersonal issues", "team morale", "communication problems", "team health signals", "people issues".
metadata:
  version: 1.0.0
---

# Team Friction Detector

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Reads internal email threads for signals of team friction — tension between
individuals, communication breakdowns, disengagement patterns, morale issues,
and escalating interpersonal concerns — and surfaces them as an early warning
for HR or people leadership.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give
     this in any form ("last 60 days", "the last 2 months", "May 2024",
     "since the reorg"). Default: the last 60 days. Keep the user's
     natural phrasing for use in the ask input; convert to ISO dates
     separately for the search call.
   - [team_scope] — either "all" (default) or a specific team or
     department to focus on.
   - [team_clause] — derived. When [team_scope] is not "all", set to
     " within [team_scope]". When [team_scope] is "all", set to empty
     string.

2. Call search with:
   - query: frustrated disagree concern unhappy unfair tension conflict
     miscommunication ignored excluded overwhelmed
     (if [team_scope] is not "all", append the team or department name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all internal email threads from [time_range][team_clause]. Identify any signals of team friction or people issues — tension between team members, communication breakdowns, language suggesting someone feels ignored or excluded, signs of disengagement or low morale, complaints about workload or fairness, and any escalating interpersonal conflict. For each signal note the type, who is involved, the evidence, and how serious it appears. Be sensitive — focus on patterns and signals, not personal judgments.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Team friction and people health early warning report",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "period_from": {
           "type": "string",
           "description": "ISO8601 start date of the period scanned"
         },
         "friction_signals": {
           "type": "array",
           "description": "List of team friction and people health signals found in email",
           "items": {
             "type": "object",
             "description": "A single friction signal with context and severity",
             "additionalProperties": false,
             "properties": {
               "signal_type": {
                 "type": "string",
                 "description": "Category of friction or people issue",
                 "enum": [
                   "interpersonal_tension", "communication_breakdown",
                   "exclusion_or_ignored", "morale_concern", "workload_complaint",
                   "fairness_concern", "disengagement_signal", "escalating_conflict",
                   "manager_relationship_strain", "other"
                 ]
               },
               "description": {
                 "type": "string",
                 "description": "Clear description of what the signal is and why it is a concern"
               },
               "people_involved": {
                 "type": "array",
                 "description": "Names or roles of people involved in this friction signal",
                 "items": {
                   "type": "string",
                   "description": "Name or role of a person involved"
                 }
               },
               "evidence": {
                 "type": "string",
                 "description": "Paraphrase of the email content that surfaces this signal, avoiding unnecessarily direct quotes"
               },
               "date": {
                 "type": "string",
                 "description": "ISO8601 date when this signal appeared"
               },
               "severity": {
                 "type": "string",
                 "description": "How serious this friction signal is and how urgently it needs attention",
                 "enum": ["critical", "high", "medium", "low"]
               },
               "recommended_action": {
                 "type": "string",
                 "description": "Recommended HR or management action to address this signal"
               }
             },
             "required": [
               "signal_type", "description", "people_involved", "evidence",
               "date", "severity", "recommended_action"
             ]
           }
         },
         "overall_team_health": {
           "type": "string",
           "description": "Overall assessment of team health based on signals found",
           "enum": ["healthy", "caution", "at_risk", "critical", "unknown"]
         },
         "critical_count": {
           "type": "number",
           "description": "Number of friction signals rated as critical severity"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of team health and primary areas of concern"
         }
       },
       "required": [
         "as_of", "period_from", "friction_signals",
         "overall_team_health", "critical_count", "summary"
       ]
     }
   }

4. Present critical signals first, then high, then medium. Lead with overall
   team health and critical count. Include a reminder that these are signals
   for awareness, not conclusions.

5. Tell the user: "These signals are for early awareness only. Please handle
   any follow-up with appropriate sensitivity and care."
