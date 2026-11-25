---
name: hiring-manager-alignment-checker
description: Detects misalignment between recruiters and hiring managers from email — conflicting signals on candidate requirements, changing goalposts, slow feedback, vague criteria, and communication gaps that are slowing down or derailing hiring. Use when a recruiter wants to identify where hiring manager friction is causing pipeline problems. Triggers on "hiring manager alignment", "changing requirements", "unclear criteria", "hiring manager feedback delays", "recruiter hiring manager misalignment", "what is the hiring manager looking for".
metadata:
  version: 1.0.0
---

# Hiring Manager Alignment Checker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Reads recruiting email threads to surface misalignment signals between
recruiters and hiring managers — shifting requirements, inconsistent feedback,
slow response patterns, unclear decision criteria, and cases where a hiring
manager's email behavior is creating friction in the hiring process.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last quarter", "May 2024",
     "since the role opened"). Default: the last 90 days. Keep the
     user's natural phrasing for use in the ask input; convert to ISO
     dates separately for the search call.
   - [scope] — either "all" (default) or the name of a specific hiring
     manager or role to focus on.
   - [scope_clause] — derived. When [scope] is not "all", set to " for
     [scope]". When [scope] is "all", set to empty string.

2. Call search with:
   - query: hiring manager criteria requirements changed actually looking
     feedback slow unclear expectations role specification
     (if [scope] is not "all", append the hiring manager or role to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all recruiting email threads from [time_range][scope_clause]. For each open role, identify any signals of misalignment between recruiter and hiring manager — changing or evolving candidate requirements, inconsistent feedback patterns, hiring managers who are slow to respond or provide feedback, unclear or shifting decision criteria, cases where candidates the recruiter advanced were rejected without clear reasoning, and any communication pattern suggesting the recruiter and hiring manager are not on the same page about what is needed.
   - output_format:
   {
   "strict": true,
   "schema": {
   "type": "object",
   "description": "Hiring manager alignment assessment across all active recruiting engagements",
   "additionalProperties": false,
   "properties": {
   "as_of": {
   "type": "string",
   "description": "ISO8601 date when this report was generated"
   },
   "alignment_assessments": {
   "type": "array",
   "description": "Alignment assessment for each open role where signals were found",
   "items": {
   "type": "object",
   "description": "Alignment assessment for a single role and hiring manager",
   "additionalProperties": false,
   "properties": {
   "role": {
   "type": "string",
   "description": "Name of the open role"
   },
   "hiring_manager": {
   "type": "string",
   "description": "Name or role of the hiring manager"
   },
   "alignment_score": {
   "type": "string",
   "description": "Overall alignment level between recruiter and hiring manager",
   "enum": ["well_aligned", "minor_gaps", "significant_gaps", "misaligned"]
   },
   "misalignment_signals": {
   "type": "array",
   "description": "Specific misalignment signals detected for this role",
   "items": {
   "type": "object",
   "description": "A single misalignment signal with evidence",
   "additionalProperties": false,
   "properties": {
   "signal_type": {
   "type": "string",
   "description": "Category of misalignment signal",
   "enum": [
   "changing_requirements", "slow_feedback", "inconsistent_feedback",
   "unclear_criteria", "unexplained_rejections", "communication_gap",
   "competing_priorities", "unrealistic_expectations", "other"
   ]
   },
   "description": {
   "type": "string",
   "description": "Clear description of the misalignment signal"
   },
   "evidence": {
   "type": "string",
   "description": "Quote or paraphrase from email that surfaces this signal"
   },
   "impact_on_hiring": {
   "type": "string",
   "description": "How this misalignment is affecting the hiring process",
   "enum": ["blocking", "slowing", "minor_friction", "unknown"]
   }
   },
   "required": ["signal_type", "description", "evidence", "impact_on_hiring"]
   }
   },
   "avg_feedback_days": {
   "type": "number",
   "description": "Average number of days this hiring manager takes to provide interview feedback, -1 if unknown"
   },
   "recommended_action": {
   "type": "string",
   "description": "Recommended action to improve alignment with this hiring manager"
   }
   },
   "required": [
   "role", "hiring_manager", "alignment_score", "misalignment_signals",
   "avg_feedback_days", "recommended_action"
   ]
   }
   },
   "misaligned_count": {
   "type": "number",
   "description": "Number of roles where significant misalignment was detected"
   },
   "slow_feedback_hms": {
   "type": "array",
   "description": "Hiring managers consistently providing slow feedback, ordered by average days",
   "items": {
   "type": "object",
   "description": "A hiring manager with slow feedback patterns",
   "additionalProperties": false,
   "properties": {
   "hiring_manager": {
   "type": "string",
   "description": "Name or role of the hiring manager"
   },
   "avg_feedback_days": {
   "type": "number",
   "description": "Average days to provide feedback"
   }
   },
   "required": ["hiring_manager", "avg_feedback_days"]
   }
   },
   "summary": {
   "type": "string",
   "description": "One or two sentence summary of alignment health across the recruiting function and most critical gaps"
   }
   },
   "required": [
   "as_of", "alignment_assessments", "misaligned_count",
   "slow_feedback_hms", "summary"
   ]
   }
   }

4. Present misaligned roles first, then roles with minor gaps, ordered by
   severity of misalignment signals. Lead with misaligned count and the
   hiring manager with the slowest feedback pattern.

5. Ask: "Would you like me to draft a recruiter-to-hiring-manager alignment
   conversation guide or a feedback reminder for any of these roles?"