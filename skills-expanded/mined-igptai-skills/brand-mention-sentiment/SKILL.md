---
name: brand-mention-sentiment
description: Finds every mention of the company brand in inbound email — from customers, partners, press, and external contacts — and analyzes the sentiment and context of each mention. Use when a marketing team wants to understand how their brand is being perceived based on what lands in their inbox. Triggers on "brand mentions", "how is our brand perceived", "brand sentiment", "what are people saying about us", "inbound brand feedback", "brand perception from email".
metadata:
  version: 1.0.0
---

# Brand Mention Sentiment

## Prerequisites
This skill needs the iGPT MCP at https://mcp.igpt.ai/.

If the MCP tools aren't available or return an auth error, tell the
user to install the iGPT plugin (`/plugin marketplace add igptai/skills`)
or add https://mcp.igpt.ai/ as a connector, then complete OAuth and say
"ready". Retry once after they confirm. Never invent tokens or OAuth URLs.
For deeper troubleshooting: https://raw.githubusercontent.com/igptai/skills/main/shared/mcp-guard.md

---

## What This Skill Does

Scans inbound email for every mention of the company brand — in customer
replies, partner messages, press inquiries, and external contact — and returns
a structured sentiment analysis showing how the brand is being described,
what associations are being made, and where perception appears strongest or
weakest.

---

## Workflow

1. Before calling any tool, collect these values from the user. Offer the
   defaults and let the user override them; do not invent values they did
   not give.

   - [time_range] — what window of email to scan. The user may give this
     in any form ("last 90 days", "the last 3 months", "May 2024",
     "since the rebrand"). Default: the last 90 days. Keep the user's
     natural phrasing for use in the ask input; convert to ISO dates
     separately for the search call.
   - [audience_scope] — either "all" (default) or a specific audience
     segment to focus on (e.g. "customers", "press", "prospects",
     "partners").
   - [audience_clause] — derived. When [audience_scope] is not "all",
     set to " from [audience_scope]". When [audience_scope] is "all",
     set to empty string.

2. Call search with:
   - query: your company brand product known reputation great love trust
     compared heard about recommend
     (if [audience_scope] is not "all", append the audience segment to the query)
   - date_from: ISO start date derived from [time_range]
   - date_to: ISO end date derived from [time_range] (or today if open-ended)

3. Call ask with:
   - input: Review all inbound email threads from [time_range][audience_clause]. Find every mention of our brand, company, or product from external senders — customers, partners, press, prospects, and others. For each mention note: who mentioned us, in what context, what was said, the sentiment, and what aspect of the brand was being referenced. Look for patterns in how different audience types perceive and describe the brand.
   - output_format:
   {
     "strict": true,
     "schema": {
       "type": "object",
       "description": "Brand mention sentiment analysis from inbound email threads",
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
         "mentions": {
           "type": "array",
           "description": "List of every brand mention found in inbound email",
           "items": {
             "type": "object",
             "description": "A single brand mention with sentiment and context",
             "additionalProperties": false,
             "properties": {
               "source_name": {
                 "type": "string",
                 "description": "Name or role of the person who mentioned the brand"
               },
               "source_type": {
                 "type": "string",
                 "description": "Category of the person mentioning the brand",
                 "enum": [
                   "customer", "prospect", "partner", "journalist",
                   "investor", "competitor", "other"
                 ]
               },
               "date": {
                 "type": "string",
                 "description": "ISO8601 date of the mention"
               },
               "mention_context": {
                 "type": "string",
                 "description": "What was being discussed when the brand was mentioned"
               },
               "what_was_said": {
                 "type": "string",
                 "description": "Paraphrase of what was said about the brand"
               },
               "sentiment": {
                 "type": "string",
                 "description": "Sentiment of this brand mention",
                 "enum": ["very_positive", "positive", "neutral", "negative", "very_negative"]
               },
               "brand_aspect": {
                 "type": "string",
                 "description": "Which aspect of the brand was being referenced",
                 "enum": [
                   "product_quality", "customer_service", "pricing", "reputation",
                   "team", "innovation", "reliability", "values", "other"
                 ]
               },
               "notable": {
                 "type": "boolean",
                 "description": "Whether this mention is particularly noteworthy as a data point for brand strategy"
               }
             },
             "required": [
               "source_name", "source_type", "date", "mention_context",
               "what_was_said", "sentiment", "brand_aspect", "notable"
             ]
           }
         },
         "sentiment_breakdown": {
           "type": "object",
           "description": "Count of mentions by sentiment category",
           "additionalProperties": false,
           "properties": {
             "very_positive": { "type": "number", "description": "Count of very positive mentions" },
             "positive": { "type": "number", "description": "Count of positive mentions" },
             "neutral": { "type": "number", "description": "Count of neutral mentions" },
             "negative": { "type": "number", "description": "Count of negative mentions" },
             "very_negative": { "type": "number", "description": "Count of very negative mentions" }
           },
           "required": ["very_positive", "positive", "neutral", "negative", "very_negative"]
         },
         "top_brand_aspects": {
           "type": "array",
           "description": "The brand aspects most frequently mentioned, ordered by frequency",
           "items": {
             "type": "object",
             "description": "A brand aspect with mention count and dominant sentiment",
             "additionalProperties": false,
             "properties": {
               "aspect": {
                 "type": "string",
                 "description": "The brand aspect"
               },
               "mention_count": {
                 "type": "number",
                 "description": "How many times this aspect was mentioned"
               },
               "dominant_sentiment": {
                 "type": "string",
                 "description": "The most common sentiment for this aspect",
                 "enum": ["positive", "neutral", "negative"]
               }
             },
             "required": ["aspect", "mention_count", "dominant_sentiment"]
           }
         },
         "summary": {
           "type": "string",
           "description": "One or two sentence summary of overall brand sentiment and key perception themes"
         }
       },
       "required": [
         "period_from", "period_to", "mentions", "sentiment_breakdown",
         "top_brand_aspects", "summary"
       ]
     }
   }

4. Lead with sentiment breakdown and top brand aspects. Present notable
   mentions prominently. Order all mentions by sentiment (negative first
   to ensure issues are visible).

5. Ask: "Would you like me to identify specific mentions worth responding
   to or amplifying?"
