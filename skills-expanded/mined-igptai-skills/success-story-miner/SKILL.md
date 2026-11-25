---
name: success-story-miner
description: Finds customer success moments buried in email — expressions of satisfaction, positive outcomes, results achieved, and moments where customers praised the product or team. Use when a CSM wants to identify case study candidates, gather testimonial material, or find proof points. Triggers on "success stories", "customer wins", "find testimonials", "positive feedback", "case study candidates", "customer proof points".
metadata:
  version: 1.0.0
---

# Success Story Miner

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans all customer email threads for moments of genuine satisfaction —
customers sharing positive results, expressing appreciation, reporting
outcomes achieved, and making statements that could be used as testimonials
or case study material.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 12 months", "the last year", "May 2024",
     "since launch"). Default: the last 12 months. Keep the user's
     natural phrasing for use in the ask input; convert to ISO dates
     separately for the search call.
   - [account_scope] — either "all" (default) or the name of a specific
     customer account to focus on.
   - [account_clause] — derived. When [account_scope] is not "all", set
     to " for account [account_scope]". When [account_scope] is "all",
     set to empty string.

2. Call search with:
   - query: thank you great results love excellent working well impressed
     achieved solved helped outcome success
     (if [account_scope] is not "all", append the account name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all customer email threads from [time_range][account_clause]. Find every moment where a customer expressed genuine satisfaction, reported a positive outcome or result, praised the product or team, or said something that could be used as a testimonial or case study quote. For each success moment note the customer, what they said, the context of the win, and the potential value as a proof point or case study.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Customer success story and testimonial report mined from email history",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "success_moments": {
           "type": "array",
           "description": "List of every customer success moment found in email",
           "items": {
             "type": "object",
             "description": "A single customer success moment with testimonial potential",
             "additionalProperties": false,
             "properties": {
               "customer": {
                 "type": "string",
                 "description": "Name of the customer company"
               },
               "contact": {
                 "type": "string",
                 "description": "Name or role of the customer contact who expressed this success"
               },
               "date": {
                 "type": "string",
                 "description": "ISO8601 date when this success moment appeared in email"
               },
               "success_type": {
                 "type": "string",
                 "description": "Category of success moment",
                 "enum": [
                   "quantified_result", "problem_solved", "team_praise",
                   "product_praise", "recommendation_offer", "renewal_enthusiasm",
                   "expansion_interest", "general_satisfaction"
                 ]
               },
               "quote_or_summary": {
                 "type": "string",
                 "description": "Direct quote or close paraphrase of what the customer said"
               },
               "business_context": {
                 "type": "string",
                 "description": "Brief description of the business situation that led to this success"
               },
               "testimonial_potential": {
                 "type": "string",
                 "description": "How strong this moment is as testimonial or case study material",
                 "enum": ["excellent", "good", "moderate", "low"]
               },
               "case_study_angle": {
                 "type": "string",
                 "description": "The story angle this success moment could support in a case study"
               }
             },
             "required": [
               "customer", "contact", "date", "success_type", "quote_or_summary",
               "business_context", "testimonial_potential", "case_study_angle"
             ]
           }
         },
         "excellent_count": {
           "type": "number",
           "description": "Number of success moments rated as excellent testimonial material"
         },
         "top_candidates": {
           "type": "array",
           "description": "The top three customers most suitable for case study or testimonial outreach",
           "items": {
             "type": "string",
             "description": "Name of a customer who is a strong case study candidate"
           }
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of success moments found and top case study candidates"
         }
       },
       "required": [
         "as_of", "success_moments", "excellent_count", "top_candidates", "summary"
       ]
     }
   }

4. Present excellent and good testimonial moments first, ordered by potential.
   Lead with top candidates and excellent count.

5. Ask: "Would you like me to draft a case study request or testimonial ask
   for any of these customers?"
