---
name: pricing-negotiation-history
description: Reconstructs the complete pricing negotiation history with a specific vendor from email — every price discussed, concession made, discount offered, and counter-proposal exchanged — so procurement can enter the next negotiation fully informed. Triggers on "pricing negotiation history", "what prices have we discussed", "negotiation history with vendor", "what discounts did we get", "previous pricing conversations", "vendor pricing history".
metadata:
  version: 1.0.0
---

# Pricing Negotiation History

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Traces all pricing conversations with a specific vendor through email history —
every price point discussed, discount or concession offered, counter-proposal
made, final price agreed, and any commitments around future pricing — to build
a complete negotiation dossier for the next pricing conversation.

---

## Workflow

1. Before calling any tool, collect these values from the user. Do not
   invent values they did not give.

   - [vendor] — the vendor to reconstruct pricing history for. No default
     — must come from the user.
   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 24 months", "the last 2 years", "May 2024",
     "since the master agreement"). Default: the last 24 months. Keep
     the user's natural phrasing for use in the ask input; convert to
     ISO dates separately for the search call.

2. Call search with:
   - query: price quote discount offer negotiate reduce concession proposal
     rate per unit cost [vendor]
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads with [vendor] from [time_range]. Reconstruct the complete pricing negotiation history: every price quoted, discount or concession offered by either side, counter-proposals made, final prices agreed, volume commitments tied to pricing, any pricing commitments made about future rates, and any language suggesting pricing flexibility or firmness. Note patterns that could inform the next negotiation.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Complete pricing negotiation history with a single vendor",
       "additionalProperties": false,
       "properties": {
         "vendor": {
           "type": "string",
           "description": "Name of the vendor whose pricing history is being traced"
         },
         "period_from": {
           "type": "string",
           "description": "ISO8601 start date of the period covered"
         },
         "period_to": {
           "type": "string",
           "description": "ISO8601 end date of the period covered"
         },
         "negotiation_events": {
           "type": "array",
           "description": "Chronological list of every pricing negotiation event found in email",
           "items": {
             "type": "object",
             "description": "A single pricing event or negotiation step",
             "additionalProperties": false,
             "properties": {
               "date": {
                 "type": "string",
                 "description": "ISO8601 date of this negotiation event"
               },
               "event_type": {
                 "type": "string",
                 "description": "Category of negotiation event",
                 "enum": [
                   "initial_quote", "counter_proposal", "discount_offered",
                   "discount_requested", "concession_made", "price_agreed",
                   "price_increase_notice", "volume_commitment", "future_pricing_commitment",
                   "price_hold_agreed", "other"
                 ]
               },
               "description": {
                 "type": "string",
                 "description": "Clear description of what happened in this negotiation event"
               },
               "price_or_rate": {
                 "type": "string",
                 "description": "The price, rate, or discount discussed in this event as stated in email, empty string if not specific"
               },
               "initiated_by": {
                 "type": "string",
                 "description": "Which party initiated this negotiation step",
                 "enum": ["us", "vendor", "unknown"]
               },
               "outcome": {
                 "type": "string",
                 "description": "The outcome or result of this negotiation step, empty string if no immediate outcome"
               },
               "evidence": {
                 "type": "string",
                 "description": "Quote or paraphrase from email documenting this event"
               }
             },
             "required": [
               "date", "event_type", "description", "price_or_rate",
               "initiated_by", "outcome", "evidence"
             ]
           }
         },
         "current_agreed_pricing": {
           "type": "string",
           "description": "The most recent agreed pricing arrangement based on email history, empty string if not determinable"
         },
         "total_savings_achieved": {
           "type": "string",
           "description": "Total savings or discounts achieved through negotiation as referenced in email, empty string if not quantified"
         },
         "vendor_flexibility_signals": {
           "type": "array",
           "description": "Signals from email suggesting areas where the vendor has shown pricing flexibility",
           "items": {
             "type": "string",
             "description": "A single flexibility signal observed in the vendor's negotiation behavior"
           }
         },
         "vendor_firm_positions": {
           "type": "array",
           "description": "Signals from email suggesting areas where the vendor has held firm on pricing",
           "items": {
             "type": "string",
             "description": "A position the vendor has consistently held firm on"
           }
         },
         "negotiation_insights": {
           "type": "array",
           "description": "Strategic insights from the pricing history that could inform the next negotiation",
           "items": {
             "type": "string",
             "description": "A single negotiation insight or recommendation"
           }
         },
         "summary": {
           "type": "string",
           "description": "Two to three sentence summary of the pricing relationship history and key negotiation leverage points"
         }
       },
       "required": [
         "vendor", "period_from", "period_to", "negotiation_events",
         "current_agreed_pricing", "total_savings_achieved",
         "vendor_flexibility_signals", "vendor_firm_positions",
         "negotiation_insights", "summary"
       ]
     }
   }

4. Present the summary and current agreed pricing first, then negotiation
   insights, then the chronological event history. Lead with the top
   negotiation insight and any upcoming repricing opportunity.

5. Ask: "Would you like me to draft a negotiation opening email or prepare
   a pricing counter-proposal based on this history?"
