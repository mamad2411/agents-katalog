---
name: commission-agreement-tracker
description: Finds every commission agreement, referral fee arrangement, and co-brokerage split referenced in email — tracking the agreed rates, parties involved, conditions, and whether payment has been confirmed. Use when an agent or broker wants to ensure all commission arrangements are documented and no payments are missed. Triggers on "commission agreements", "referral fees", "co-brokerage splits", "commission tracker", "who do I owe a referral fee", "commission arrangements".
metadata:
  version: 1.0.0
---

# Commission Agreement Tracker

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans email for every commission arrangement, referral fee agreement, and
co-brokerage split — extracting the agreed rate, the parties involved, the
conditions, the associated transaction, and whether payment has been confirmed
or is still outstanding.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 12 months", "the last year", "May 2024",
     "since the brokerage merged"). Default: the last 12 months. Keep
     the user's natural phrasing for use in the ask input; convert to
     ISO dates separately for the search call.
   - [scope] — either "all" (default) or the name of a specific
     transaction, property, or party to focus on.
   - [scope_clause] — derived. When [scope] is not "all", set to " for
     [scope]". When [scope] is "all", set to empty string.

2. Call search with:
   - query: commission referral fee split co-brokerage percentage agreed
     paid owed closing proceeds
     (if [scope] is not "all", append the transaction or party name to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all email threads from [time_range][scope_clause] referencing commission agreements, referral fees, and co-brokerage splits. For each arrangement identify: the parties involved, the type of arrangement, the agreed rate or amount, any conditions attached, the associated property or transaction, and whether payment has been confirmed in email or whether it remains outstanding.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Commission agreement and referral fee tracker",
       "additionalProperties": false,
       "properties": {
         "as_of": {
           "type": "string",
           "description": "ISO8601 date when this report was generated"
         },
         "agreements": {
           "type": "array",
           "description": "List of every commission arrangement found in email",
           "items": {
             "type": "object",
             "description": "A single commission or referral fee arrangement",
             "additionalProperties": false,
             "properties": {
               "agreement_type": {
                 "type": "string",
                 "description": "Type of commission or fee arrangement",
                 "enum": [
                   "standard_commission", "referral_fee", "co_brokerage_split",
                   "reduced_commission", "flat_fee", "performance_bonus", "other"
                 ]
               },
               "counterparty": {
                 "type": "string",
                 "description": "Name of the other agent, broker, or party in this arrangement"
               },
               "property": {
                 "type": "string",
                 "description": "Property or transaction this arrangement is tied to"
               },
               "agreed_rate_or_amount": {
                 "type": "string",
                 "description": "The agreed commission rate as a percentage or flat amount as stated in email"
               },
               "conditions": {
                 "type": "string",
                 "description": "Any conditions attached to this arrangement, empty string if none"
               },
               "agreed_on": {
                 "type": "string",
                 "description": "ISO8601 date this arrangement was agreed, empty string if unclear"
               },
               "expected_closing_date": {
                 "type": "string",
                 "description": "ISO8601 expected closing date when payment would be due, empty string if unknown"
               },
               "payment_status": {
                 "type": "string",
                 "description": "Current payment status based on email evidence",
                 "enum": ["paid", "outstanding", "pending_closing", "disputed", "unknown"]
               },
               "payment_confirmed_date": {
                 "type": "string",
                 "description": "ISO8601 date payment was confirmed in email, empty string if not yet paid"
               },
               "estimated_amount": {
                 "type": "number",
                 "description": "Estimated commission amount in local currency based on agreed rate and property price, 0 if cannot be calculated"
               },
               "currency": {
                 "type": "string",
                 "description": "Currency of the estimated amount"
               },
               "notes": {
                 "type": "string",
                 "description": "Any additional context about this arrangement from email"
               }
             },
             "required": [
               "agreement_type", "counterparty", "property",
               "agreed_rate_or_amount", "conditions", "agreed_on",
               "expected_closing_date", "payment_status", "payment_confirmed_date",
               "estimated_amount", "currency", "notes"
             ]
           }
         },
         "outstanding_count": {
           "type": "number",
           "description": "Number of commission arrangements where payment is outstanding"
         },
         "total_outstanding_estimated": {
           "type": "number",
           "description": "Total estimated value of all outstanding commission payments"
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of commission arrangements and outstanding payments"
         }
       },
       "required": [
         "as_of", "agreements", "outstanding_count",
         "total_outstanding_estimated", "summary"
       ]
     }
   }

4. Present outstanding and pending_closing arrangements first, ordered by
   expected closing date. Lead with outstanding count and total outstanding
   estimated value.

5. Ask: "Would you like me to draft a commission confirmation or follow-up
   message for any outstanding arrangements?"
