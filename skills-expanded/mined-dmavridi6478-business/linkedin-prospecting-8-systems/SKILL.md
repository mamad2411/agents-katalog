---
name: linkedin-prospecting-8-systems
description: Eight-system LinkedIn prospecting operating model for Claude — ICP & list building, enrichment & verification, content warm-up, connection & outreach, DM sequencing & replies, CRM & pipeline logging, reporting & diagnostics, handoff & scaling — plus the MCP connection map and a daily routing routine. Structure reconstructed from the table of contents of "The LinkedIn Prospecting Guide to Claude" (44 pages, 80 skills); the guide's prompts are gated, so the prompts here are original. Run via /linkedin-systems.
---

# LinkedIn Prospecting — 8 Systems

**Provenance (read first):** the source is a 44-page PDF advertised on a video ("comment SYSTEMS and I'll DM"). Only the cover and table of contents were visible, so this skill reproduces the *structure* (8 systems, MCP setup, daily routing) and supplies original working prompts. It does NOT claim to reproduce the guide's 80 skills. Nothing here was verified against the full document.

## Table of contents as shown (page numbers from the source)

MCP setup: 8 full connections (p3) · S1 ICP & list building (p6) · S2 Enrichment & verification (p10) · S3 Content warm-up (p14) · S4 Connection & outreach (p18) · S5 DM sequencing & replies (p22) · S6 CRM & pipeline logging (p26) · S7 Reporting & diagnostics (p30) · S8 Handoff & scaling (p34) · The exact prompts: daily routing (p38)

## MCP connection map (which connectors this account actually has)

| Need | Connector | Status in this account |
|---|---|---|
| Prospect/company search & enrichment | Clay, Vibe Prospecting, OpenFunnel | Connected |
| CRM logging | HubSpot | Connected |
| Content scheduling | Typefully (X/LinkedIn/Threads) | Connected |
| LinkedIn analytics/posting | Taplio MCP LinkedIn | Needs reconnect (authorise in claude.ai) |
| LinkedIn DM triage | Kondo | Not in the MCP registry — unavailable |
| Notes/tasks + Slack alerts | Notion, Slack | Connected |
| Meeting notes | Granola | Not installed — connect in claude.ai |
| Automation glue | Zapier, Composio | Connected |

## The 8 systems

1. **ICP & list building** — turn a one-line brief into ICP filters (title, seniority, industry, size, geo, trigger), build a list with real data (Clay / Vibe Prospecting), never fabricate leads. Output: list + inclusion/exclusion rules.
2. **Enrichment & verification** — add company facts, verify titles and domains, flag free-mail and duplicates (`gtm-outbound-engine/scripts/clean_leads.py`). Output: clean, scored list with a `verified/unverified` column.
3. **Content warm-up** — 3–5 posts/week from `linkedin-strategy` + `linkedin-virality-playbook` so prospects see the sender before the invite; comment on prospects' posts with substance.
4. **Connection & outreach** — connection notes ≤300 characters, referencing something real; no pitch in the invite. Daily cap stated up front; human approves every batch.
5. **DM sequencing & replies** — 3-touch sequence (value → relevance → soft ask), reply-handling library by intent (interested / not now / wrong person / objection). See `linkedin-dm-funnel`, `linkedin-dm-9-claude-workflows`.
6. **CRM & pipeline logging** — every conversation logged with stage, next step, date; tags for source = LinkedIn.
7. **Reporting & diagnostics** — weekly: invites sent, acceptance %, reply %, meetings booked, cost of time; diagnose the weakest ratio before changing copy.
8. **Handoff & scaling** — SOPs so a VA/SDR can run S1–S7; only scale a motion that converts at small volume (`sop-builder`).

## Daily routing (original)

1. Morning: pull new replies → classify intent → draft responses → human approves.
2. Midday: publish/schedule one post; 10 substantive comments.
3. Afternoon: next approved invite batch (within cap); log to CRM.
4. End of day: 5-line report to Slack/Notion.

## Rules and risk

- LinkedIn's terms restrict automated connection/DM activity; keep Claude in a drafting-and-planning role and send manually or through LinkedIn-permitted tools. GDPR applies to EU prospects — document lawful basis and honour opt-outs.
- Never send without human approval and a stated send cap (`outbound-campaign-brief` gate).
- No fabricated personalisation: if a fact cannot be sourced, omit it.
