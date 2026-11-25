---
name: interview-pipeline-tracker
description: Tracks the interview status of every active candidate across all open roles from email — what stage each candidate is in, what feedback has been collected, what feedback is still missing, and where the process has stalled. Use when a recruiter wants a full interview pipeline view without manually chasing every thread. Triggers on "interview pipeline", "candidate interview status", "where is each candidate", "missing interview feedback", "interview tracker", "who is still in process".
metadata:
  version: 1.0.0
---

# Interview Pipeline Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all recruiting email threads to extract the current interview stage
of every active candidate — what has been completed, what feedback has been
collected, what is outstanding, which interviewers have not submitted
feedback, and where the process has stalled waiting on a hiring manager
or interviewer.

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
   - [scope] — either "all" (default) or the name of a specific role or
     candidate to focus on.
   - [scope_clause] — derived. When [scope] is not "all", set to " for
     [scope]". When [scope] is "all", set to empty string.

2. Call search with:
   - query: interview feedback debrief candidate stage screen panel
     decision advance reject hiring manager
     (if [scope] is not "all", append the role or candidate name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all recruiting email threads from [time_range][scope_clause]. For every active candidate across all open roles, determine: their current interview stage, what interviews have been completed, what feedback has been received, which interviewers or hiring managers have not yet submitted feedback, what the next step is, who owns that next step, and whether the process has stalled for this candidate. Flag any candidate where feedback has been outstanding for more than 3 business days.
   - output_format:
   {
   "strict": true,
   "schema": {
   "type": "object",
   "description": "Interview pipeline tracker across all active candidates and open roles",
   "additionalProperties": false,
   "properties": {
   "as_of": {
   "type": "string",
   "description": "ISO8601 date when this report was generated"
   },
   "candidates": {
   "type": "array",
   "description": "List of every active candidate with their interview pipeline status",
   "items": {
   "type": "object",
   "description": "A single candidate with full interview pipeline tracking",
   "additionalProperties": false,
   "properties": {
   "candidate_name": {
   "type": "string",
   "description": "Full name of the candidate"
   },
   "role": {
   "type": "string",
   "description": "The role this candidate is interviewing for"
   },
   "current_stage": {
   "type": "string",
   "description": "Current stage of the interview process",
   "enum": [
   "recruiter_screen", "hiring_manager_screen", "technical_assessment",
   "first_round", "second_round", "panel_interview", "final_round",
   "debrief_pending", "offer_stage", "stalled", "unknown"
   ]
   },
   "interviews_completed": {
   "type": "array",
   "description": "List of interviews already completed for this candidate",
   "items": {
   "type": "string",
   "description": "Description of a completed interview round or screen"
   }
   },
   "feedback_received_from": {
   "type": "array",
   "description": "Names or roles of interviewers who have submitted feedback",
   "items": {
   "type": "string",
   "description": "Name or role of an interviewer who provided feedback"
   }
   },
   "feedback_outstanding_from": {
   "type": "array",
   "description": "Names or roles of interviewers whose feedback is still missing",
   "items": {
   "type": "string",
   "description": "Name or role of an interviewer who has not yet submitted feedback"
   }
   },
   "days_feedback_outstanding": {
   "type": "number",
   "description": "Number of days the oldest outstanding feedback has been pending, 0 if none outstanding"
   },
   "next_step": {
   "type": "string",
   "description": "The next action required to move this candidate forward"
   },
   "next_step_owner": {
   "type": "string",
   "description": "Who owns the next step",
   "enum": ["recruiter", "hiring_manager", "interviewer", "candidate", "unknown"]
   },
   "overall_sentiment": {
   "type": "string",
   "description": "Overall interviewer sentiment toward this candidate based on email signals",
   "enum": ["very_positive", "positive", "mixed", "negative", "unknown"]
   },
   "process_health": {
   "type": "string",
   "description": "Health of the interview process for this candidate",
   "enum": ["progressing", "stalled", "feedback_delayed", "at_risk_of_dropping", "unknown"]
   }
   },
   "required": [
   "candidate_name", "role", "current_stage", "interviews_completed",
   "feedback_received_from", "feedback_outstanding_from",
   "days_feedback_outstanding", "next_step", "next_step_owner",
   "overall_sentiment", "process_health"
   ]
   }
   },
   "feedback_overdue_count": {
   "type": "number",
   "description": "Number of candidates with interview feedback outstanding for more than 3 business days"
   },
   "stalled_count": {
   "type": "number",
   "description": "Number of candidates whose interview process has stalled"
   },
   "by_role": {
   "type": "array",
   "description": "Summary of pipeline health grouped by open role",
   "items": {
   "type": "object",
   "description": "Pipeline summary for a single open role",
   "additionalProperties": false,
   "properties": {
   "role": {
   "type": "string",
   "description": "Name of the open role"
   },
   "active_candidates": {
   "type": "number",
   "description": "Number of active candidates for this role"
   },
   "stalled_candidates": {
   "type": "number",
   "description": "Number of stalled candidates for this role"
   },
   "furthest_stage": {
   "type": "string",
   "description": "The most advanced stage any candidate for this role has reached"
   }
   },
   "required": ["role", "active_candidates", "stalled_candidates", "furthest_stage"]
   }
   },
   "summary": {
   "type": "string",
   "description": "One or two sentence summary of the overall interview pipeline health and most urgent items"
   }
   },
   "required": [
   "as_of", "candidates", "feedback_overdue_count", "stalled_count", "by_role", "summary"
   ]
   }
   }

4. Present candidates with stalled processes and overdue feedback first,
   ordered by days_feedback_outstanding. Lead with feedback_overdue count
   and stalled count.

5. Ask: "Would you like me to draft feedback reminder emails to any
   interviewers or hiring managers who are overdue?"