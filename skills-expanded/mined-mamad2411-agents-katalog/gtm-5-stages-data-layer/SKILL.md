---
name: gtm-5-stages-data-layer
description: Use when the user wants to diagnose GTM (go-to-market) maturity by how their outbound/prospecting DATA LAYER is sourced and maintained, not just what motion or channel they run — manual spreadsheets, a rotting purchased list, a hand-cleaned enrichment waterfall, a verified/scheduled source, or a live-queried agent source. Trigger phrases include "why is our list quality bad", "what stage of GTM maturity are we at", "our bounce rate is high", or "/gtm-5-stages-data-layer". Distinct from this repo's gtm-strategy skill (7 building blocks + 7 motions) — this one is specifically about the data layer underneath outbound, not motion selection.
---

# 5 Stages of GTM — The Data Layer That Decides Who Climbs It

Source: arrel.ai infographic (Nicholas De La Guardia), "5 Stages of GTM: The
Ladder, and the Data Layer That Decides Who Climbs It." The core claim: teams
usually diagnose GTM problems as a channel or motion problem, when the actual
blocker is almost always the data layer underneath — the list itself.

## The ladder

| Stage | How it runs | Data layer |
|---|---|---|
| **1. Founder-led** | One channel, warm outbound, everything manual | **Manual** — your own network and a spreadsheet |
| **2. Foundational** | First CRM, first sequencer | **Rotting** — a list someone bought or exported once, rotting the day it lands |
| **3. Multi-channel** | Email, LinkedIn and calling feed each other | **Hand-cleaned** — an enrichment waterfall stitched from 3-4 sources, cleaned by hand every month |
| **4. Orchestrated** | Signals decide who gets worked first | **Verified** — one verified source, refreshed on a schedule, job changes caught before a sequence fires |
| **5. AI-native** | Agents build the list, qualify it, and hand it to the sequencer | **Live** — the same verified source, queried live from the agent instead of exported |

**Most teams stall at Stage 2** — the list underneath never got fixed, so
every motion layered on top (multi-channel, orchestration) inherits the same
rot.

## Why this matters (the cited result)

One client (B2B SaaS, ~40 people, two SDRs) moved only the data layer — same
domains, same copy, same reps:

| | Before | After |
|---|---|---|
| Bounce rate | 17% | <5% |
| Meetings/month | 8 | 15 |

The fix was the data (a verified source refreshed every 7 days, queried live
as an MCP), not a new tool, new copy, or more reps.

## How to use this

1. Diagnose which stage the user's team is actually at — ask how the
   prospecting list is sourced and how often it's refreshed, not what
   channels or tools they use. Channel sophistication (Stage 3) built on a
   rotting list (Stage 2 data layer) still underperforms.
2. If stuck at Stage 2 (rotting list, high bounce rate, "we bought a list
   once"), the highest-leverage fix is the data layer itself — a verified,
   scheduled-refresh source — before recommending more channels, more
   sequences, or more reps.
3. Stage 5 (AI-native, live-queried) is the ceiling, not a prerequisite —
   don't recommend it to a team that hasn't fixed Stage 2 yet.

## Related

`gtm-strategy` (the 7 building blocks + 7 motions framework — motion
selection, not the data layer under outbound specifically), `gtm-outbound-engine`,
`gtm-api-stack`, `gtm-stack-20person-b2b`, `client-research-web`.
