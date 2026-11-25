---
name: strategic-commitment-log
description: Extracts every strategic commitment, promise, and formal undertaking a founder or executive has made to investors, board members, partners, and key stakeholders — and tracks which are still open. Use when an executive wants to ensure they are delivering on everything they have promised. Triggers on "strategic commitments", "what have I promised", "commitments to investors", "board commitments", "what am I on the hook for strategically", "executive commitment log".
metadata:
  version: 1.0.0
---

# Strategic Commitment Log

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans email threads with investors, board members, key partners, and strategic
stakeholders to find every commitment the executive has made — targets promised,
milestones committed to, decisions pledged — and tracks which remain open and
which have been delivered on.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 18 months", "the last year", "May 2024",
     "since the Series A"). Default: the last 18 months. Keep the user's
     natural phrasing for use in the ask input; convert to ISO dates
     separately for the search call.
   - [stakeholder_scope] — either "all" (default) or the name of a
     specific stakeholder to focus on.
   - [stakeholder_clause] — derived. When [stakeholder_scope] is not
     "all", set to " for stakeholder [stakeholder_scope]". When
     [stakeholder_scope] is "all", set to empty string.

2. Call search with:
   - query: commit promise will deliver target milestone by end of quarter
     we will achieve plan board investor
     (if [stakeholder_scope] is not "all", append the stakeholder name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads from [time_range][stakeholder_clause] involving investors, board members, partners, and strategic stakeholders. Find every commitment, promise, or target the founder or executive made — things like revenue targets committed to, milestones pledged, strategic decisions promised, hires committed to, and formal undertakings made. For each determine whether there is evidence it was delivered or whether it remains open.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Strategic commitment log tracking executive promises to key stakeholders",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this log was generated"
         },
         "commitments": {
           "type": "array",
           "description": "List of every strategic commitment found in email",
           "items": {
             "type": "object",
             "description": "A single strategic commitment with delivery status",
             "additionalProperties": false,
             "properties": {
               "commitment": {
                 "type": "string",
                 "description": "Clear statement of what was committed to"
               },
               "committed_to": {
                 "type": "string",
                 "description": "Name or role of the stakeholder to whom this commitment was made"
               },
               "stakeholder_type": {
                 "type": "string",
                 "description": "Type of stakeholder this commitment was made to",
                 "enum": [
                   "investor", "board_member", "partner", "customer",
                   "regulator", "team", "public", "other"
                 ]
               },
               "commitment_type": {
                 "type": "string",
                 "description": "Category of commitment",
                 "enum": [
                   "financial_target", "product_milestone", "strategic_hire",
                   "partnership_goal", "operational_target", "legal_obligation",
                   "reporting_commitment", "other"
                 ]
               },
               "made_on": {
                 "type": "string",
                 "description": "ISO8601 date this commitment was made"
               },
               "target_date": {
                 "type": "string",
                 "description": "ISO8601 date by which this was committed to be delivered, empty string if open-ended"
               },
               "evidence": {
                 "type": "string",
                 "description": "Quote or paraphrase from email documenting this commitment"
               },
               "status": {
                 "type": "string",
                 "description": "Current delivery status of this commitment",
                 "enum": ["delivered", "on_track", "at_risk", "overdue", "open", "unknown"]
               },
               "risk_if_missed": {
                 "type": "string",
                 "description": "What is at stake if this commitment is not delivered",
                 "enum": ["critical", "high", "medium", "low"]
               }
             },
             "required": [
               "commitment", "committed_to", "stakeholder_type", "commitment_type",
               "made_on", "target_date", "evidence", "status", "risk_if_missed"
             ]
           }
         },
         "overdue_count": {
           "type": "number",
           "description": "Number of commitments that are overdue"
         },
         "at_risk_count": {
           "type": "number",
           "description": "Number of commitments that are at risk of not being delivered"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of the commitment landscape and most critical open items"
         }
       },
       "required": [
         "as_of", "commitments", "overdue_count", "at_risk_count", "summary"
       ]
     }
   }

4. Present overdue and at_risk commitments first, ordered by risk_if_missed.
   Lead with overdue count and the highest-stakes open item.

5. Ask: "Would you like me to draft a stakeholder update addressing any
   overdue or at-risk commitments?"
