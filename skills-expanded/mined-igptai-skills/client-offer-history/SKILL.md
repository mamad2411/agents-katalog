---
name: client-offer-history
description: Reconstructs the complete offer history for a specific client from email — every offer made, at what price, on which property, what the outcome was, and what feedback was received. Use when an agent wants to brief a client on their offer history or prepare strategy for a new offer. Triggers on "client offer history", "what offers have we made", "offer history", "previous offers", "offer track record", "what happened with past offers".
metadata:
  version: 1.0.0
---

# Client Offer History

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Traces all offer activity for a specific client through email history —
properties offered on, prices submitted, outcomes, competing offer context,
seller feedback, and any patterns that could inform future offer strategy.

---

## Workflow

1. Before calling any tool, collect these values from the user. Do not
   invent values they did not give.

   - [client] — the name of the client whose offer history to reconstruct.
     No default — must come from the user.
   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 12 months", "the last year", "May 2024",
     "since they started searching"). Default: the last 12 months. Keep
     the user's natural phrasing for use in the ask input; convert to
     ISO dates separately for the search call.

2. Call search with:
   - query: offer submitted price [client] accepted rejected countered
     competing highest best
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads related to [client] from [time_range]. Reconstruct their complete offer history: every property they made an offer on, the offer price submitted, any counter-offers exchanged, the final outcome, the reason for rejection or acceptance if stated, any competing offer context mentioned, and what feedback was received from the seller or listing agent. Note any patterns that could inform future offer strategy for this client.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Complete offer history for a single real estate client",
       "additionalProperties": false,
       "properties": {
         "client_name": {
           "type": "string",
           "description": "Full name of the client"
         },
         "period_from": {
           "type": "string",
           "description": "ISO8601 start date of the period covered"
         },
         "period_to": {
           "type": "string",
           "description": "ISO8601 end date of the period covered"
         },
         "offers": {
           "type": "array",
           "description": "Chronological list of every offer made by this client",
           "items": {
             "type": "object",
             "description": "A single offer with full context and outcome",
             "additionalProperties": false,
             "properties": {
               "property": {
                 "type": "string",
                 "description": "Address or description of the property offered on"
               },
               "offer_date": {
                 "type": "string",
                 "description": "ISO8601 date the offer was submitted"
               },
               "offer_price": {
                 "type": "number",
                 "description": "Initial offer price submitted"
               },
               "currency": {
                 "type": "string",
                 "description": "Currency of the offer price"
               },
               "asking_price": {
                 "type": "number",
                 "description": "Listed asking price at time of offer, 0 if not found"
               },
               "counter_offers": {
                 "type": "array",
                 "description": "Any counter-offer exchanges that occurred",
                 "items": {
                   "type": "object",
                   "description": "A single counter-offer in the negotiation",
                   "additionalProperties": false,
                   "properties": {
                     "price": {
                       "type": "number",
                       "description": "Counter-offer price"
                     },
                     "from": {
                       "type": "string",
                       "description": "Which party made this counter-offer",
                       "enum": ["seller", "buyer", "unknown"]
                     },
                     "date": {
                       "type": "string",
                       "description": "ISO8601 date of this counter-offer"
                     }
                   },
                   "required": ["price", "from", "date"]
                 }
               },
               "outcome": {
                 "type": "string",
                 "description": "Final outcome of this offer",
                 "enum": [
                   "accepted", "rejected", "countered_accepted", "countered_rejected",
                   "withdrawn_by_buyer", "outbid", "expired", "unknown"
                 ]
               },
               "rejection_reason": {
                 "type": "string",
                 "description": "Reason given for rejection if stated, empty string if not mentioned"
               },
               "competing_offers_mentioned": {
                 "type": "boolean",
                 "description": "Whether competing offers were mentioned in the email thread"
               },
               "seller_feedback": {
                 "type": "string",
                 "description": "Any feedback from the seller or listing agent about this offer, empty string if none"
               }
             },
             "required": [
               "property", "offer_date", "offer_price", "currency", "asking_price",
               "counter_offers", "outcome", "rejection_reason",
               "competing_offers_mentioned", "seller_feedback"
             ]
           }
         },
         "total_offers": {
           "type": "number",
           "description": "Total number of offers made by this client in the period"
         },
         "success_rate": {
           "type": "number",
           "description": "Percentage of offers that resulted in an accepted outcome"
         },
         "strategy_insights": {
           "type": "array",
           "description": "Patterns and insights from the offer history that could inform future offer strategy",
           "items": {
             "type": "string",
             "description": "A single strategic insight derived from the offer history"
           }
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of the client's offer history and key patterns"
         }
       },
       "required": [
         "client_name", "period_from", "period_to", "offers",
         "total_offers", "success_rate", "strategy_insights", "summary"
       ]
     }
   }

4. Present offers in reverse chronological order. Lead with total offers,
   success rate, and the top strategy insight.

5. Ask: "Would you like me to draft an offer strategy brief for this
   client based on their history?"
