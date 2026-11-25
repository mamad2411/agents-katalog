---
name: policy-question-miner
description: Finds every HR policy question, benefits inquiry, and employee request buried in email — questions that were asked, answered, unanswered, or repeatedly asked by multiple people. Use when HR wants to understand what employees are confused about or to build an FAQ from real questions. Triggers on "policy questions from employees", "what are employees asking about", "HR FAQ", "benefits questions", "policy confusion", "common employee questions".
metadata:
  version: 1.0.0
---

# Policy Question Miner

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans email threads for HR policy questions, benefits inquiries, and employee
requests — identifying what employees are confused about, what questions are
being asked repeatedly, and what unanswered questions need a response. Output
can be used directly to build or improve an HR FAQ.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 6 months", "the last 90 days", "May 2024",
     "since the policy update"). Default: the last 6 months. Keep the
     user's natural phrasing for use in the ask input; convert to ISO
     dates separately for the search call.
   - [policy_scope] — either "all" (default) or a specific policy area
     to focus on (e.g. "benefits", "leave", "expense reimbursement").
   - [policy_clause] — derived. When [policy_scope] is not "all", set
     to " focused on [policy_scope]". When [policy_scope] is "all",
     set to empty string.

2. Call search with:
   - query: policy question benefits vacation leave parental sick pay
     expense reimbursement how do I what is the process
     (if [policy_scope] is not "all", append the policy area to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads from [time_range][policy_clause] that involve HR policy questions, benefits inquiries, or employee requests for process guidance. For each question identify: what was asked, who asked it, when, what policy area it relates to, whether it was answered, and whether the same or similar question has been asked by multiple people. Identify any questions that were never answered.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "HR policy question analysis mined from employee email threads",
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
         "questions": {
           "type": "array",
           "description": "List of every HR policy question found in email",
           "items": {
             "type": "object",
             "description": "A single policy question with context and status",
             "additionalProperties": false,
             "properties": {
               "question": {
                 "type": "string",
                 "description": "The policy question as asked or closely paraphrased"
               },
               "policy_area": {
                 "type": "string",
                 "description": "The HR policy area this question relates to",
                 "enum": [
                   "vacation_and_leave", "parental_leave", "sick_leave",
                   "compensation", "benefits", "expense_reimbursement",
                   "remote_work", "performance_review", "onboarding",
                   "offboarding", "code_of_conduct", "other"
                 ]
               },
               "asked_by": {
                 "type": "string",
                 "description": "Name or role of the employee who asked this question"
               },
               "date_asked": {
                 "type": "string",
                 "description": "ISO8601 date when this question was first asked"
               },
               "times_asked": {
                 "type": "number",
                 "description": "Number of times this or a very similar question was asked across all employees"
               },
               "answered": {
                 "type": "boolean",
                 "description": "Whether this question received a clear answer in email"
               },
               "answer_summary": {
                 "type": "string",
                 "description": "Brief summary of the answer given, empty string if not answered"
               },
               "faq_candidate": {
                 "type": "boolean",
                 "description": "Whether this question is a good candidate for inclusion in an HR FAQ based on frequency or importance"
               }
             },
             "required": [
               "question", "policy_area", "asked_by", "date_asked",
               "times_asked", "answered", "answer_summary", "faq_candidate"
             ]
           }
         },
         "unanswered_count": {
           "type": "number",
           "description": "Total number of policy questions that were never answered"
         },
         "top_policy_areas": {
           "type": "array",
           "description": "The policy areas with the most questions, ordered by frequency",
           "items": {
             "type": "object",
             "description": "A policy area and its question count",
             "additionalProperties": false,
             "properties": {
               "policy_area": {
                 "type": "string",
                 "description": "Name of the policy area"
               },
               "question_count": {
                 "type": "number",
                 "description": "Number of questions asked about this policy area"
               }
             },
             "required": ["policy_area", "question_count"]
           }
         },
         "faq_candidates_count": {
           "type": "number",
           "description": "Number of questions identified as strong FAQ candidates"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of policy question patterns and top areas of confusion"
         }
       },
       "required": [
         "period_from", "period_to", "questions", "unanswered_count",
         "top_policy_areas", "faq_candidates_count", "summary"
       ]
     }
   }

4. Present unanswered questions first, then FAQ candidates ordered by times
   asked. Lead with unanswered count and the top policy area by question
   volume.

5. Ask: "Would you like me to draft FAQ answers for the most frequently
   asked questions?"
