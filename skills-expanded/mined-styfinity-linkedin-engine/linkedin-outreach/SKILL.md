---
name: linkedin-outreach
description: Find decision-makers by title and seniority, draft connection notes under 200 characters referencing something specific, and send via the connected CLI capped at 20 per day. Use when you want to start outbound connection requests to a defined ICP.
argument-hint: "[target title(s) + seniority + geography + how many]"
---

# LinkedIn Outreach

The hero outbound skill. Find the right decision-makers, write a short human connection note for each, and send only what the operator approves, inside the ban-safe daily cap.

## Inputs
- Target title(s), seniority, geography, and how many: $ARGUMENTS
- The brief (ICP, voice profile, offer, pains) loads automatically.

## Do this
1. Search for matching decision-makers, live via the connected MCP layer if it is wired, or from a pasted or seed list if not. State which source you used.
2. Filter the results to the brief's ICP. Drop anyone outside the title, seniority, or geography rules. Say who you cut and why.
3. For each person, draft a connection note UNDER 200 characters that references one real specific detail (a post they wrote, a recent role move, a shared context). Count the characters and show the count.
4. Present the whole queue as DRAFTS for approval. Nothing leaves yet.
5. On explicit approval, send through the CLI's send command. It hard-caps at 20 per day for new accounts and logs every send. If approval covers more than today's remaining 20, send what fits and hold the rest.

## Output
- The drafted queue: each row is target (name, role, company), the under-200-char note with its character count, and the real detail referenced.
- After approval: a send summary - sent count, remaining in today's 20, and what was held for tomorrow.
- For people who accept the request, hand the thread to /linkedin-reply-triager and run /linkedin-humanizer on any reply draft.

## Rules
- Nothing sends without the connected CLI/MCP layer AND explicit approval. Draft-first, always.
- The 20-per-day cap is a ban-safety guardrail for new accounts. Do not exceed it.
- Every note references one real, specific detail. No generic "I'd love to connect" or "great to connect with people in your space".
- No em-dashes. No exclamation marks. No fake familiarity.
- Real numbers are fine, but never name the person or company they came from.
