---
name: crisis-signal-detector
description: Scans executive email threads for early warning signals of an emerging crisis — reputational, financial, legal, operational, or personnel — before it becomes public or unmanageable. Use when a founder or CEO wants a proactive scan for anything that could escalate into a serious problem. Triggers on "crisis signals", "early warning", "what could blow up", "emerging problems", "reputational risk", "executive risk scan".
metadata:
  version: 1.0.0
---

# Crisis Signal Detector

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Reads executive email threads for signals that something significant could
be developing — legal threats, financial pressure, key person flight risk,
customer concentration risk, reputational exposure, regulatory attention,
or any pattern that experienced executives recognize as a precursor to
a crisis.

---

## Workflow

1. Before calling any tool, collect this value from the user. Offer the
   default and let the user override it; do not invent a value they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 60 days", "the last 2 months", "May 2024",
     "since the incident"). Default: the last 60 days. Keep the user's
     natural phrasing for use in the ask input; convert to ISO dates
     separately for the search call.

2. Call search with:
   - query: urgent legal threat concern escalate serious risk exposure
     confidential sensitive regulatory pressure resignation departure
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all executive email threads from [time_range]. Identify any early warning signals of an emerging crisis — legal threats or disputes being raised, financial pressure signals, key person flight risk, reputational exposure, regulatory inquiries or attention, customer concentration risk, major operational failures, and any language or situation that suggests something serious could be developing. For each signal note the type, evidence, who is involved, and urgency.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Executive crisis early warning scan across email threads",
       "additionalProperties": false,
       "properties": {
         "period_from": {
           "type": "string",
           "description": "ISO8601 start date of the period scanned"
         },
         "period_to": {
           "type": "string",
           "description": "ISO8601 end date of the period scanned"
         },
         "signals": {
           "type": "array",
           "description": "List of every crisis signal detected in executive email threads",
           "items": {
             "type": "object",
             "description": "A single crisis signal with full context and urgency assessment",
             "additionalProperties": false,
             "properties": {
               "crisis_type": {
                 "type": "string",
                 "description": "Category of potential crisis",
                 "enum": [
                   "legal_threat", "financial_pressure", "key_person_flight_risk",
                   "reputational_exposure", "regulatory_attention",
                   "customer_concentration_risk", "operational_failure",
                   "personnel_crisis", "security_incident", "other"
                 ]
               },
               "description": {
                 "type": "string",
                 "description": "Clear description of what the signal is and why it could develop into a crisis"
               },
               "evidence": {
                 "type": "string",
                 "description": "Quote or paraphrase from email that surfaces this signal"
               },
               "parties_involved": {
                 "type": "array",
                 "description": "Names or roles of people involved in or affected by this signal",
                 "items": {
                   "type": "string",
                   "description": "Name or role of a party involved"
                 }
               },
               "date": {
                 "type": "string",
                 "description": "ISO8601 date when this signal first appeared"
               },
               "severity": {
                 "type": "string",
                 "description": "Potential severity if this signal develops into a full crisis",
                 "enum": ["critical", "high", "medium", "low"]
               },
               "time_sensitivity": {
                 "type": "string",
                 "description": "How quickly action is needed to prevent escalation",
                 "enum": ["immediate", "this_week", "this_month", "monitor"]
               },
               "recommended_action": {
                 "type": "string",
                 "description": "Recommended immediate action to address or monitor this signal"
               }
             },
             "required": [
               "crisis_type", "description", "evidence", "parties_involved",
               "date", "severity", "time_sensitivity", "recommended_action"
             ]
           }
         },
         "critical_count": {
           "type": "number",
           "description": "Number of signals rated as critical severity"
         },
         "immediate_action_count": {
           "type": "number",
           "description": "Number of signals requiring immediate action"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of the overall risk picture and most urgent items"
         }
       },
       "required": [
         "period_from", "period_to", "signals", "critical_count",
         "immediate_action_count", "summary"
       ]
     }
   }

4. Present signals ordered by time_sensitivity then severity. Lead with
   critical count and immediate action count. Treat this report with
   appropriate sensitivity.

5. Tell the user: "For any legal, regulatory, or personnel signals, please
   consult appropriate counsel or advisors before taking action."
