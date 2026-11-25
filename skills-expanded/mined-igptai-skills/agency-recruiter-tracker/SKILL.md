---
name: agency-recruiter-tracker
description: Tracks every external agency recruiter and RPO relationship from email — what roles they are working, what candidates they have submitted, submission quality signals, fee arrangements, and which agencies are performing versus going quiet. Use when an in-house recruiting team manages external agency relationships and wants to hold them accountable. Triggers on "agency recruiter status", "external recruiter performance", "agency submissions", "RPO tracker", "which agencies are active", "recruiter agency pipeline".
metadata:
  version: 1.0.0
---

# Agency Recruiter Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all external agency recruiter email threads to produce a performance
view — which roles each agency is working, how many candidates they have
submitted, the quality signal for those submissions, whether they are
meeting agreed terms, fee arrangements referenced, and which agencies have
gone quiet or are underperforming.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last quarter", "May 2024",
     "since the new agency partnership"). Default: the last 90 days.
     Keep the user's natural phrasing for use in the ask input; convert
     to ISO dates separately for the search call.
   - [agency_scope] — either "all" (default) or the name of a specific
     external recruiting agency to focus on.
   - [agency_clause] — derived. When [agency_scope] is not "all", set
     to " for agency [agency_scope]". When [agency_scope] is "all", set
     to empty string.

2. Call search with:
   - query: agency recruiter submit candidate profile RPO retained
     contingency fee placement shortlist exclusive
     (if [agency_scope] is not "all", append the agency name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all external agency recruiter email threads from [time_range][agency_clause]. For each agency, identify: what roles they are working, how many candidates they have submitted, any quality signals about those submissions from hiring manager or recruiter reactions, the fee arrangement referenced, whether they are operating on a retained or contingency basis, whether they are meeting their commitments, and whether they have gone quiet on any roles.
   - output_format:
   {
   "strict": true,
   "schema": {
   "type": "object",
   "description": "External agency recruiter performance tracker",
   "additionalProperties": false,
   "properties": {
   "as_of": {
   "type": "string",
   "description": "ISO8601 date when this report was generated"
   },
   "agencies": {
   "type": "array",
   "description": "List of every external recruiting agency with performance tracking",
   "items": {
   "type": "object",
   "description": "Performance summary for a single external recruiting agency",
   "additionalProperties": false,
   "properties": {
   "agency_name": {
   "type": "string",
   "description": "Name of the recruiting agency or RPO"
   },
   "engagement_type": {
   "type": "string",
   "description": "Type of agency engagement",
   "enum": ["retained", "contingency", "rpo", "contract_staffing", "unknown"]
   },
   "roles_working": {
   "type": "array",
   "description": "List of roles this agency is currently working",
   "items": {
   "type": "string",
   "description": "A role title this agency is sourcing for"
   }
   },
   "candidates_submitted": {
   "type": "number",
   "description": "Total number of candidates submitted by this agency in the period"
   },
   "submission_quality_signal": {
   "type": "string",
   "description": "Overall quality signal for this agency's candidate submissions",
   "enum": ["strong", "mixed", "poor", "unknown"]
   },
   "candidates_advanced": {
   "type": "number",
   "description": "Number of submitted candidates who were advanced to interview, -1 if unknown"
   },
   "fee_arrangement": {
   "type": "string",
   "description": "Fee arrangement referenced in email, empty string if not found"
   },
   "last_contact_date": {
   "type": "string",
   "description": "ISO8601 date of the most recent email exchange"
   },
   "days_since_contact": {
   "type": "number",
   "description": "Number of days since the last email exchange"
   },
   "activity_status": {
   "type": "string",
   "description": "Overall activity level of this agency in the period",
   "enum": ["very_active", "active", "slowing", "gone_quiet", "unknown"]
   },
   "open_commitments": {
   "type": "array",
   "description": "Commitments this agency has made that are still outstanding",
   "items": {
   "type": "string",
   "description": "A single open commitment from this agency"
   }
   },
   "performance_rating": {
   "type": "string",
   "description": "Overall performance rating for this agency based on email signals",
   "enum": ["strong", "adequate", "underperforming", "unknown"]
   },
   "recommended_action": {
   "type": "string",
   "description": "Recommended action for managing this agency relationship"
   }
   },
   "required": [
   "agency_name", "engagement_type", "roles_working", "candidates_submitted",
   "submission_quality_signal", "candidates_advanced", "fee_arrangement",
   "last_contact_date", "days_since_contact", "activity_status",
   "open_commitments", "performance_rating", "recommended_action"
   ]
   }
   },
   "gone_quiet_count": {
   "type": "number",
   "description": "Number of agencies that have gone quiet on active roles"
   },
   "underperforming_count": {
   "type": "number",
   "description": "Number of agencies rated as underperforming"
   },
   "summary": {
   "type": "string",
   "description": "One or two sentence summary of external agency performance and most urgent actions"
   }
   },
   "required": [
   "as_of", "agencies", "gone_quiet_count", "underperforming_count", "summary"
   ]
   }
   }

4. Present underperforming and gone-quiet agencies first. Lead with
   gone_quiet count and underperforming count.

5. Ask: "Would you like me to draft a performance check-in or accountability
   email to any of these agencies?"