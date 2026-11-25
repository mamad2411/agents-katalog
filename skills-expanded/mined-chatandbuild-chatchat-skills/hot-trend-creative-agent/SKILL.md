---
id: hot-trend-creative-agent
name: hot-trend-creative-agent
description: "Produces natural-language creative recommendations and 2-3 video directions for the Hot Trend Creative Agent. Use when the user asks what creative direction may work now, what trends to use, how to refresh an active campaign, or how to restart an inactive advertiser based on advertiser status, historical creative signals, hot trends, or possible creative fatigue."
category: TikTok
---

# Hot Trend Creative Agent

Use this skill to turn advertiser context, historical creative signals, and hot trend inputs into a user-facing creative recommendation.

## What this skill is for

This skill is part of a competition project that is currently in a **mock-first / scaffold-first** stage.

At this stage, the priority is to keep the skill:

- structurally clear
- easy to review
- easy to evolve collaboratively
- aligned with the TikTok Agentic Hub skill standard
- grounded in mock MCP data without pretending every downstream integration is fully implemented

## What this skill should do

- Identify the advertiser situation from the available context
- Distinguish between `new_adv`, `active_existing_adv`, `inactive_existing_adv`, and `unknown`
- Use advertiser profile, campaign/history context, trend inputs, and top-product inputs as the reasoning basis
- Treat creative fatigue cautiously when the advertiser is active
- Mention relevant historical creative winners, current TikTok hot trends, or top products when they materially support the recommendation
- Degrade gracefully when data is partial, missing, conflicting, or unavailable
- Produce a natural-language recommendation with 2-3 concrete video directions

## What this skill must not do

- Do **not** fabricate trend data, campaign performance, historical assets, or fatigue conclusions
- Do **not** assume the fake MCP scaffold is already fully implemented
- Do **not** hard-code future real MCP names into the core skill logic unless the project explicitly adopts them later
- Do **not** collapse all advertiser scenarios into one generic flow
- Do **not** end in raw debug-style field dumps when a clear natural-language recommendation is possible

## Accepted inputs

Use this skill when the user or surrounding workflow provides some combination of:

- advertiser identity or advertiser context
- country / market information
- industry or product category
- campaign activity state
- creative fatigue signals or reporting cues
- product images or creative assets
- a request asking what ads to create now, what trends are relevant, how to refresh a tired campaign, or how to restart an inactive advertiser

If the user wants a trend-backed or advertiser-specific recommendation but key fields are missing, do **not** pretend the data was loaded. Ask for the smallest missing input first, such as:

- advertiser_id
- country
- industry / category
- whether the advertiser is currently active

## Default working mode

Unless the caller specifies otherwise, follow this mode:

1. Interpret the user goal and available business context.
2. Infer the advertiser segment from the available evidence.
3. If the advertiser appears active, evaluate fatigue cautiously.
4. Gather or simulate advertiser profile, campaign/history context, trend inputs, and top-product inputs through the current mock interface boundaries.
5. Choose the appropriate branch for `new_adv`, `active_existing_adv`, `inactive_existing_adv`, or `unknown`.
6. Produce a natural-language recommendation that explains the direction and then gives 2-3 video descriptions.

## Step-by-step workflow

### Step 1: Understand the request and the user's language

Determine whether the request is primarily about:

- what creative direction to launch now to follow the hot trends
- what trend signals may be relevant
- how to refresh an active campaign
- how to start/restart an inactive advertiser
- what to do when creative fatigue may be happening

Match the user's language by default:

- if the user writes in Chinese, answer in Chinese
- if the user writes in English, answer in English
- only mix languages when a product term or proper noun genuinely needs it

### Step 2: Classify the advertiser situation

Prefer these segment labels:

- `new_adv`
- `active_existing_adv`
- `inactive_existing_adv`
- `unknown`

Use the best available evidence. If the evidence is incomplete or conflicting, keep the uncertainty visible.

### Step 3: Handle fatigue carefully for active advertisers

For active advertisers:

- use fatigue-related inputs only when there is enough evidence
- do not assert fatigue when the inputs are insufficient
- if the condition cannot be confirmed, return a conditional recommendation instead of a definitive fatigue judgment
- if fatigue is likely, prefer a refresh recommendation grounded in top-performing historical creative patterns rather than a fully disconnected new concept

### Step 4: Use the current mock interface boundaries only when the needed inputs exist

When available, reason through these capability boundaries:

- `get_advertiser_profile`
- `get_active_advertiser_campaign_context`
- `get_inactive_advertiser_historical_assets`
- `get_hashtag_trends`
- `get_top_ads_trends`
- `get_top_music_trends`
- `get_top_products`

These are recommended mock interface boundaries, not a claim that all implementations are complete.

Important behavior:

- if the request depends on advertiser-specific or trend-specific data, first check whether the required inputs exist
- if `advertiser_id` is missing, do not act as if advertiser data was fetched
- if country or industry is missing, do not act as if trend data was fetched
- when the needed inputs are missing, ask a short clarifying question instead of inventing a generic “trend-backed” answer

### Step 5: Apply graceful degradation

If data is missing, partial, empty, timed out, or conflicting:

- do not fabricate missing facts
- reduce confidence appropriately
- surface missing context in plain language
- fall back to weaker but still useful guidance only when the user explicitly wants a general answer
- avoid citing historical videos, fatigue conclusions, or hot trends as confirmed if they are not actually available
- if the user asked for advertiser-specific guidance and key inputs are missing, prefer one short clarifying question over a generic answer

### Step 6: Produce the user-facing recommendation

The final response should read like a short recommendation a user can act on, not like an internal debug object or a long strategy memo.

Prefer this structure:

1. **Current situation**
   - briefly state the advertiser situation and the most suitable next move
2. **Recommended video directions**
   - provide 2-3 concrete video directions
3. **Why these directions**
   - explain the basis in very concise language

If information is missing, add only one short limitation sentence at the end. Do not expand into a long appendix.

### Step 7: Keep the internal structure implicit, not mechanical

Internally, the response can still be grounded in these concepts:

- `segment`
- `trigger_reason`
- `recommended_action`
- `video_descriptions`
- `missing_data`
- `confidence`
- `sources`

But do **not** print these field names, English labels, or debug-style sections unless the caller explicitly asks for a structured format.

## Report style guidance

### Overall tone

- Match the user's language: Chinese in, Chinese out; English in, English out
- Avoid mixing in another language unless it is a necessary product or industry term
- Avoid engineer-facing vocabulary such as field names, schema-like phrasing, or internal labels
- Keep the answer compact; in the normal case, the full response should feel easy to scan in under one minute

### Current situation

Briefly state the advertiser situation in the user's language.

Examples:

- You’re a new advertiser, so it makes more sense to test a few easy-to-validate short video angles first.
- You already have active campaigns, and the current creatives show fatigue signals, so a refresh is more suitable than a full reset.
- You’re in a restart phase, so it makes sense to combine past winning assets with current trend signals.

### Recommended video directions

For each direction, keep it short and practical. Prefer this format:

- direction title
- opening hook
- rough visual flow
- why it fits this advertiser now

Unless the user explicitly asks for more, keep each direction to a short paragraph or 3-4 short lines.

### Why these directions

When relevant, mention only the most decision-useful basis, such as:

- advertiser status
- historical top-performing videos or assets
- active campaign fatigue context
- hot hashtags
- top ad patterns
- top music
- top products

Do not list every signal mechanically. Summarize only the 2-4 strongest reasons.

