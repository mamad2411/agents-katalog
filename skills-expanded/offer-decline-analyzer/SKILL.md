---
name: offer-decline-analyzer
description: Analyzes every offer decline referenced in email — what reasons were given, what counter-offers were made, compensation signals, competing offers mentioned, and patterns across declines that could improve offer strategy. Use when a recruiter or hiring manager wants to understand why offers are being declined and what could be done differently. Triggers on "offer declines", "why are candidates declining", "declined offer analysis", "offer rejection reasons", "improve offer acceptance rate", "what are we losing candidates to".
metadata:
  version: 1.0.0
---

# Offer Decline Analyzer

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans email for every offer that was declined, extracts the reasons given or
implied, identifies patterns across declines — compensation gaps, competing
offers, role concerns, location issues, timing — and returns actionable
insights for improving offer strategy and acceptance rates.

---

## Workflow

1. Before calling any tool, collect this value from the user. Offer the
   default and let the user override it; do not invent a value they did
   not give.

   - [time_range] — what window of email to analyze. The user may give
     this in any form ("last 12 months", "the last year", "May 2024",
     "since the new comp band"). Default: the last 12 months. Keep
     the user's natural phrasing for use in the ask input; convert to
     ISO dates separately for the search call.

2. Call search with:
   - query: declined offer unfortunately decided another opportunity
     compensation competing going with accepted elsewhere counter
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all recruiting email threads from [time_range]. Find every instance where a candidate declined an offer or withdrew from the process after receiving an offer. For each decline note: the candidate, the role, the reason given or implied, whether a counter-offer was made, any competing offer that was mentioned, compensation signals, and any other factor that contributed to the decline. Then identify patterns across all declines.
   - output_format:
   {
   "strict": true,
   "schema": {
   "type": "object",
   "description": "Offer decline analysis report identifying patterns and actionable insights",
   "additionalProperties": false,
   "properties": {
   "period_from": {
   "type": "string",
   "description": "ISO8601 start date of the period analyzed"
   },
   "period_to": {
   "type": "string",
   "description": "ISO8601 end date of the period analyzed"
   },
   "declines": {
   "type": "array",
   "description": "List of every offer decline found in email",
   "items": {
   "type": "object",
   "description": "A single offer decline with full context and reasons",
   "additionalProperties": false,
   "properties": {
   "candidate_name": {
   "type": "string",
   "description": "Full name of the candidate who declined"
   },
   "role": {
   "type": "string",
   "description": "The role the offer was made for"
   },
   "decline_date": {
   "type": "string",
   "description": "ISO8601 date the decline was communicated"
   },
   "primary_reason": {
   "type": "string",
   "description": "The primary reason given or most strongly implied for declining",
   "enum": [
   "compensation_too_low", "accepted_competing_offer",
   "role_concerns", "location_or_remote_policy", "company_concerns",
   "timing_not_right", "counter_offer_accepted", "personal_reasons",
   "culture_fit_concerns", "career_growth_concerns", "unknown"
   ]
   },
   "secondary_reasons": {
   "type": "array",
   "description": "Any additional contributing reasons mentioned",
   "items": {
   "type": "string",
   "description": "A secondary contributing reason for declining"
   }
   },
   "competing_offer_mentioned": {
   "type": "boolean",
   "description": "Whether a competing offer was mentioned as a factor"
   },
   "competing_company": {
   "type": "string",
   "description": "Name of the competing company if mentioned, empty string if not"
   },
   "compensation_gap_signal": {
   "type": "string",
   "description": "Any signal about a compensation gap, empty string if not mentioned"
   },
   "counter_offer_made": {
   "type": "boolean",
   "description": "Whether a counter-offer was made in response to the decline"
   },
   "counter_offer_outcome": {
   "type": "string",
   "description": "What happened after the counter-offer was made, empty string if no counter was made",
   "enum": ["accepted", "still_declined", "not_applicable", "unknown"]
   },
   "salvageable": {
   "type": "boolean",
   "description": "Whether this decline appears salvageable based on the reasons given"
   }
   },
   "required": [
   "candidate_name", "role", "decline_date", "primary_reason",
   "secondary_reasons", "competing_offer_mentioned", "competing_company",
   "compensation_gap_signal", "counter_offer_made",
   "counter_offer_outcome", "salvageable"
   ]
   }
   },
   "decline_count": {
   "type": "number",
   "description": "Total number of offer declines in the period"
   },
   "top_decline_reasons": {
   "type": "array",
   "description": "The most common decline reasons ranked by frequency",
   "items": {
   "type": "object",
   "description": "A decline reason with frequency count",
   "additionalProperties": false,
   "properties": {
   "reason": {
   "type": "string",
   "description": "The decline reason category"
   },
   "count": {
   "type": "number",
   "description": "Number of declines citing this reason"
   }
   },
   "required": ["reason", "count"]
   }
   },
   "most_common_competitor": {
   "type": "string",
   "description": "The company mentioned most often as the competing offer destination, empty string if not determinable"
   },
   "strategic_insights": {
   "type": "array",
   "description": "Actionable insights from the decline pattern analysis",
   "items": {
   "type": "string",
   "description": "A single strategic insight or recommendation to improve offer acceptance rates"
   }
   },
   "summary": {
   "type": "string",
   "description": "Two to three sentence summary of decline patterns and top recommendations"
   }
   },
   "required": [
   "period_from", "period_to", "declines", "decline_count",
   "top_decline_reasons", "most_common_competitor",
   "strategic_insights", "summary"
   ]
   }
   }

4. Present summary and strategic insights first, then top decline reasons,
   then the individual decline log. Lead with the most actionable insight
   and the most common decline reason.

5. Ask: "Would you like me to draft revised offer messaging or a counter-
   offer strategy based on these patterns?"