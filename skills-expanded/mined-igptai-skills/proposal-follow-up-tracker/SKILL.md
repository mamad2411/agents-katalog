---
name: proposal-follow-up-tracker
description: Tracks every outstanding proposal sent to prospective clients — where each stands, how long it has been outstanding, whether feedback has been received, and which proposals have gone quiet. Use when a consultant wants a full view of their proposal pipeline and knows exactly who to follow up with. Triggers on "proposal follow-up", "outstanding proposals", "proposals waiting for a response", "proposal pipeline", "which proposals are pending", "proposal tracker".
metadata:
  version: 1.0.0
---

# Proposal Follow-Up Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all proposal-related email threads to find every proposal that was
sent and tracks its current status — awaiting response, under review, in
negotiation, accepted, declined, or gone quiet — so the consultant always
knows who to follow up with and when.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 6 months", "the last 90 days", "May 2024",
     "since the trade show"). Default: the last 6 months. Keep the user's
     natural phrasing for use in the ask input; convert to ISO dates
     separately for the search call.
   - [prospect_scope] — either "all" (default) or the name of a specific
     prospect to focus on.
   - [prospect_clause] — derived. When [prospect_scope] is not "all",
     set to " for prospect [prospect_scope]". When [prospect_scope] is
     "all", set to empty string.

2. Call search with:
   - query: proposal quote estimate scope of work SOW sent reviewing
     consider budget timeline decision
     (if [prospect_scope] is not "all", append the prospect name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads from [time_range][prospect_clause] related to consulting proposals, quotes, and scopes of work sent to prospective clients. For each proposal identify: the prospect, what the proposal covered, the date it was sent, the current status based on the most recent email, any feedback or questions received, the apparent level of interest, and whether this proposal has gone quiet and needs a follow-up.
   - output_format:
   {
   "strict": true,
   "schema": {
   "type": "object",
   "description": "Proposal pipeline tracker across all outstanding consulting proposals",
   "additionalProperties": false,
   "properties": {
   "as_of": {
   "type": "string",
   "description": "ISO8601 date when this report was generated"
   },
   "proposals": {
   "type": "array",
   "description": "List of every proposal with its current pipeline status",
   "items": {
   "type": "object",
   "description": "A single proposal with full pipeline context",
   "additionalProperties": false,
   "properties": {
   "prospect": {
   "type": "string",
   "description": "Name of the prospective client the proposal was sent to"
   },
   "proposal_description": {
   "type": "string",
   "description": "Brief description of what the proposal covered"
   },
   "sent_date": {
   "type": "string",
   "description": "ISO8601 date the proposal was sent"
   },
   "proposed_value": {
   "type": "string",
   "description": "The proposed fee or budget as stated in email, empty string if not found"
   },
   "status": {
   "type": "string",
   "description": "Current status of this proposal",
   "enum": [
   "sent_awaiting_response", "under_review", "questions_raised",
   "in_negotiation", "verbally_accepted", "formally_accepted",
   "declined", "gone_quiet", "on_hold", "unknown"
   ]
   },
   "days_outstanding": {
   "type": "number",
   "description": "Number of days since the proposal was sent with no final decision"
   },
   "last_contact_date": {
   "type": "string",
   "description": "ISO8601 date of the most recent email exchange about this proposal"
   },
   "interest_level": {
   "type": "string",
   "description": "Apparent level of interest based on email signals",
   "enum": ["high", "medium", "low", "unknown"]
   },
   "open_questions": {
   "type": "array",
   "description": "Questions or concerns the prospect has raised that have not been fully addressed",
   "items": {
   "type": "string",
   "description": "A single open question or concern from the prospect"
   }
   },
   "conversion_likelihood": {
   "type": "string",
   "description": "Estimated likelihood this proposal converts to an engagement",
   "enum": ["high", "medium", "low", "unknown"]
   },
   "recommended_action": {
   "type": "string",
   "description": "Recommended next step for this proposal"
   }
   },
   "required": [
   "prospect", "proposal_description", "sent_date", "proposed_value",
   "status", "days_outstanding", "last_contact_date", "interest_level",
   "open_questions", "conversion_likelihood", "recommended_action"
   ]
   }
   },
   "pending_count": {
   "type": "number",
   "description": "Number of proposals awaiting a decision"
   },
   "gone_quiet_count": {
   "type": "number",
   "description": "Number of proposals where the prospect has gone quiet"
   },
   "high_conversion_count": {
   "type": "number",
   "description": "Number of proposals with high conversion likelihood"
   },
   "summary": {
   "type": "string",
   "description": "One or two sentence summary of the proposal pipeline and most urgent follow-ups"
   }
   },
   "required": [
   "as_of", "proposals", "pending_count",
   "gone_quiet_count", "high_conversion_count", "summary"
   ]
   }
   }

4. Present proposals ordered by conversion likelihood then by days
   outstanding. Flag gone_quiet proposals prominently. Lead with pending
   count, gone_quiet count, and high conversion count.

5. Ask: "Would you like me to draft follow-up emails for any outstanding
   or gone-quiet proposals?"