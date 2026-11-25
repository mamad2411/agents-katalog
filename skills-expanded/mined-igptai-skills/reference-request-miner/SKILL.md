---
name: reference-request-miner
description: Finds every request for references, testimonials, case studies, and introductions buried in prospecting and client email threads — requests made by prospects, offers made by happy clients, and opportunities to ask for a reference that have not yet been actioned. Use when a consultant wants to build their reference network or respond to reference requests. Triggers on "reference requests", "who has offered to be a reference", "testimonial requests", "case study opportunities", "intro requests", "who can I use as a reference".
metadata:
  version: 1.0.0
---

# Reference Request Miner

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans email for every reference-related signal — prospects asking for
references, satisfied clients who have offered to vouch, opportunities
to request a testimonial that were never followed up on, and introduction
requests that could open new doors — and returns them as a structured
action list.

---

## Workflow

1. Before calling any tool, collect this value from the user. Offer the
   default and let the user override it; do not invent a value they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 12 months", "the last year", "May 2024",
     "since launch"). Default: the last 12 months. Keep the user's
     natural phrasing for use in the ask input; convert to ISO dates
     separately for the search call.

2. Call search with:
   - query: reference testimonial case study introduction recommend speak
     to vouch happy to connect intro referral
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads from [time_range]. Find every reference-related signal: prospects who asked to speak with a reference client, existing clients who volunteered to be a reference or offered to make introductions, situations where a client was clearly happy enough to be a strong reference candidate but was never asked, and any introduction requests made that were not followed through on. For each signal note who is involved, what was said, and what action is recommended.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Reference request and testimonial opportunity report mined from email",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "signals": {
           "type": "array",
           "description": "List of every reference-related signal found in email",
           "items": {
             "type": "object",
             "description": "A single reference or testimonial signal with context and action",
             "additionalProperties": false,
             "properties": {
               "signal_type": {
                 "type": "string",
                 "description": "Category of reference-related signal",
                 "enum": [
                   "prospect_requested_reference", "client_offered_reference",
                   "client_offered_introduction", "testimonial_opportunity",
                   "case_study_opportunity", "introduction_request_pending",
                   "reference_check_completed", "other"
                 ]
               },
               "person_involved": {
                 "type": "string",
                 "description": "Name of the client or prospect involved in this signal"
               },
               "company": {
                 "type": "string",
                 "description": "Company this person is associated with"
               },
               "date": {
                 "type": "string",
                 "description": "ISO8601 date when this signal appeared in email"
               },
               "context": {
                 "type": "string",
                 "description": "Brief description of the situation and what was said"
               },
               "actioned": {
                 "type": "boolean",
                 "description": "Whether this signal has already been followed up on"
               },
               "opportunity_strength": {
                 "type": "string",
                 "description": "How strong this reference or testimonial opportunity is",
                 "enum": ["excellent", "good", "moderate", "low"]
               },
               "recommended_action": {
                 "type": "string",
                 "description": "Specific recommended action to take on this signal"
               }
             },
             "required": [
               "signal_type", "person_involved", "company", "date",
               "context", "actioned", "opportunity_strength", "recommended_action"
             ]
           }
         },
         "unactioned_count": {
           "type": "number",
           "description": "Number of reference or testimonial signals that have not yet been acted on"
         },
         "excellent_opportunities": {
           "type": "array",
           "description": "Names of clients who represent the strongest unactioned reference or testimonial opportunities",
           "items": {
             "type": "string",
             "description": "Name of a client who is an excellent reference opportunity"
           }
         },
         "pending_reference_requests": {
           "type": "array",
           "description": "Prospects who have specifically asked for a reference and are still waiting",
           "items": {
             "type": "string",
             "description": "Name of a prospect waiting for a reference"
           }
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of reference opportunities and any urgent pending requests"
         }
       },
       "required": [
         "as_of", "signals", "unactioned_count",
         "excellent_opportunities", "pending_reference_requests", "summary"
       ]
     }
   }

4. Present pending reference requests first — prospects waiting on a
   reference are time-sensitive. Then present excellent unactioned
   opportunities. Lead with pending_reference_requests count and
   unactioned count.

5. Ask: "Would you like me to draft a reference request email to any
   of the excellent opportunity clients, or match a reference to a
   waiting prospect?"
