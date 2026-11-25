---
name: gtm-outbound-engine
description: Design and run a B2B outbound engine as five layers — orchestration (Claude Code as the single control plane), signal (hiring surges, tech adoption, funding, LinkedIn engagement), data (waterfall enrichment to verified email/phone/firmographics), action (email on proper inbox infrastructure or LinkedIn sequences) and system of record (one CRM everything writes back to) — executed as a 5-step pipeline inside Claude Code - pull and enrich, clean/dedupe/normalise, extract signals and score ICP, write 1:1 personalisation, push to sender. Maps each layer to the MCP connectors actually available in this account (Clay, Vibe Prospecting, OpenFunnel, HubSpot, Apollo-style providers) and ships a working lead-cleaning script. Use when building or auditing an outbound/GTM/RevOps stack, choosing enrichment or sequencing tools, or asked to "run outbound from Claude Code". Upstream of `outbound-campaign-brief` (campaign + approval gate) and `linkedin-signal-outreach`.
---

# GTM Outbound Engine

Sources (uploaded infographics):
- "The 5-layer GTM engine — from signal detection to a CRM record, fully automated with AI agents" (Cold IQ / Julien Lieben) — the layer model and 14-tool stack.
- "The All-in-One Outbound Pipeline — Everything you need to run high-converting outbound. Inside Claude Code." — the 5-step execution flow.
- "AI-Powered Lead Generation Machine — How I'd build a predictable B2B pipeline using AI" (Denis Panjuta) — a second, more granular 9-stage tool-stack map, see below. Same architecture (signal → data → outreach → CRM), different and largely non-overlapping tool names.
- "21 Things to Install in Claude to Build a Lead Generation System" (Denis Panjuta) — a Plugins/Skills/MCP breakdown of the same system, see the connector-status note below.
- "The Role of a GTM Engineer" (Matteo Fois / Kinetyca.com) — a Venn diagram naming Claude itself as the "GTM Engineer" sitting at the center of three overlapping tool categories, see below.

Both the first two are vendor marketing (Cold IQ sells a unified GTM API). The architecture is sound; "fully automated" is not — see Gates.

## A fourth tool map: Claude as "GTM Engineer" (Matteo Fois)

This source frames the same job differently — instead of a linear
pipeline, three overlapping engines with Claude at the center resolving
which one to route a task to:

| Engine | Job | Tools named in source | Overlap zone |
|---|---|---|---|
| Growth Engine | Demand generation, campaign automation | Bombora (already listed above), RB2B, GoExtrovert, Apify, Common Room | → *Signal Routing* (Growth ∩ Ops) |
| Ops Engine | CRM automation, pipeline management | Attio, n8n, Notion, Clay, Supabase | → *Signal Routing* (Growth ∩ Ops), *Pipeline Ops* (Ops ∩ Sales) |
| Sales Engine | AI prospecting, personalized outbound | Apollo, Prospeo, HeyReach, Sales Navigator, Smartlead | → *Warm Outreach* (Growth ∩ Sales), *Pipeline Ops* (Ops ∩ Sales) |

**[Certain]** these are the names on the graphic; **[Guessing]** on
pricing/current availability. New names not in the tool tables above:
**RB2B** (identifies anonymous website visitors by company/person — a
top-of-funnel signal source), **GoExtrovert**, **Apify** (web-scraping
platform, useful for building custom enrichment sources this account's
connectors don't cover), **Attio** (CRM, an alternative to the
HubSpot/Airtable system-of-record above), **Supabase** (already
documented as a dev-infra pick in `dev-repos-to-clone`, shown here in a
GTM-ops role instead), **HeyReach** (LinkedIn outreach automation),
**Smartlead** (already named in the 5-step pipeline's step 5 above).
Notion, Clay, Common Room, and Apollo are already connected/covered
above — this map doesn't change their status.

## Connector status for the "21 Things to Install" list

Of the 7 MCP servers that source names (Apollo, HubSpot, Clay, Common
Room, Notion, Slack, Zapier), **6 are already connected and available in
this Claude Code environment** — HubSpot, Clay, Common Room, Notion,
Slack, and Zapier all appear in this session's own MCP tool list, nothing
to install. Only **Apollo MCP** is not connected here; Apollo-style
enrichment in this account currently runs through Clay/Vibe Prospecting
instead (see the layer table above). The source's "Plugins" column
(Revenoid, BetterCallClaudeGrowth, "Claude Marketing," Octave) names
products not independently verified to a canonical repo/marketplace
listing — don't install any of those from name alone; Windsor.ai and
Apollo are real, established companies but their "plugin" packaging as
shown wasn't confirmed. The source's "Skills" column (`prospect`,
`enrich-lead`, `account-research`, `draft-outreach`, `call-prep`,
`lead-triage`, `cold-email`) is exactly this skill's 5-step pipeline
above broken into finer-grained stages — build against the pipeline
already documented here rather than creating seven redundant micro-skills
for the same jobs.

## The five layers (bottom-up = build order)

| # | Layer | Job | Tools named in source | Connected in this account |
|---|---|---|---|---|
| 1 | Orchestration | Reads API docs, wires the other four layers, retries through errors | Claude, OpenAI, Cold IQ | Claude Code (this session), `n8n-agent-builder` for scheduled runs |
| 2 | Signal | Detect hiring surges, tech adoption, funding rounds, LinkedIn engagement before competitors | PredictLeads, LimaData, GetLeads | OpenFunnel (`search-companies-by-tech-stack`, `deep-research`), HubSpot `search_intent_signals`, Clay |
| 3 | Data | Raw signals → verified emails, phones, firmographics via waterfall enrichment | Cold IQ, Apollo, Explorium, Prospeo, FullEnrich, GetLeads, LeadMagic | Clay (`add-contact-data-points`), Vibe Prospecting (`enrich-prospects`, `enrich-business`) |
| 4 | Action | Route contacts to the right channel: high-volume email on inbox infrastructure that lands, or LinkedIn sequences | Instantly, Hypertide, Expandi | None connected — export CSV (Vibe Prospecting `export-to-csv`) and import |
| 5 | System of record | Every signal, enrichment and reply writes back to one CRM | folk | HubSpot (`search_crm_objects`, `get_crm_objects`), Airtable |

The full 14-tool stack from the source: Cold IQ, Apollo, Explorium, PredictLeads, LimaData, Prospeo, FullEnrich, GetLeads, Openmart, Instantly, Expandi, Hypertide, LeadMagic, folk. **[Certain]** these are the names on the graphic; **[Guessing]** on current pricing/availability — verify each before buying.

## Alternate tool-stack map (9-stage pipeline, Denis Panjuta)

A second source graphic breaks the same signal → data → outreach → CRM
architecture into nine narrower stages with different named tools (some
overlap with the 14-tool list above — Apollo appears in both; most don't).
**[Certain]** these are the names on the graphic; **[Guessing]** on current
pricing/availability/whether each is still the best-in-category pick —
this is a snapshot of one creator's stack, not an endorsement:

| Stage | Job | Tools named in source |
|---|---|---|
| Traffic sources | Get discovered | LinkedIn, Instantly, Webflow (SEO), Google Ads, YouTube, Eventbrite, Discord |
| Lead capture | Collect leads | Phantombuster (LinkedIn followers), Leadfeeder (site visitors), Typeform (form fills), Shield (post engagers), Snov.io (email replies), beehiiv (newsletter subs) |
| Data enrichment | Get full context | Clay, Apollo.io, Clearbit, Lusha, Pipl, People Data Labs |
| AI research & insights | Understand prospects | ChatGPT, Claude, Perplexity, Gemini, Tavily, Exa |
| Lead scoring & prioritization | Find best opportunities | MadKudu, 6sense, Bombora, Zoho SalesIQ, Calixa, Regie.ai |
| Personalization engine | Create relevance at scale | Smartwriter.ai, Jasper, Tyle (dynamic images), ChatGPT (pain-point extraction), Lemlist AI (icebreakers), Clay (custom fields) |
| Outreach | Multi-channel AI outreach | Lemlist, Expandi, Aircall, Zoko (WhatsApp), Meta Ads (retargeting), Outplay |
| CRM & follow-up | Track, nurture, close | HubSpot, Salesforce, pipedrive, Make, Mixmax, ClickUp |
| Sales process | Human-run close | Qualified lead → discovery call → needs assessment → solution proposal → negotiation → closed won |

Reach for this map instead of the 14-tool stack above when the gap is
specifically in an earlier stage the first map doesn't break out (traffic
capture, AI-assisted personalization at the copy/image level, or a
specific CRM/automation choice) — otherwise the 5-layer model and its
Claude Code pipeline above is still the one to build against; this table
is a tool reference, not a second architecture to implement in parallel.

## The 5-step pipeline (inside Claude Code)

| Step | What happens | How here |
|---|---|---|
| 1. Pull data & waterfall enrichment | Query provider A; for every field still empty, try provider B, then C | Clay / Vibe Prospecting MCP; record which provider filled each field |
| 2. Clean, deduplicate, normalise | Standardise job titles, company domains, drop duplicates | `python3 scripts/clean_leads.py in.csv out.csv` (this skill) |
| 3. Extract signals & score ICP | Read live web/job/news signals; score against explicit ICP criteria | OpenFunnel / HubSpot intent / `WebFetch`; scoring rubric below |
| 4. Write 1:1 personalisation | Multi-touch sequence grounded in the account's real signal | Prompt below; drafts only |
| 5. Push to sender | Format clean records, push to Instantly / Smartlead / Outreach | CSV export + manual import until a sender connector exists |

## ICP scoring rubric (step 3)

Score 0–3 per criterion, weight, sum to 100. Define before you pull data, not after.

| Criterion | Weight | 0 | 3 |
|---|---|---|---|
| Firmographic fit (industry, size, region) | 30 | Outside | Exact match |
| Trigger signal in last 90 days (hire, funding, tech change) | 30 | None | Direct trigger for your offer |
| Role fit of contact (decision power) | 20 | No influence | Economic buyer |
| Reachability (verified email, deliverable domain) | 10 | Unverified | Verified |
| Negative signals (competitor customer, layoffs, lawsuit) | −10 | — | Present |

Tier A ≥ 75, B 55–74, below 55 not contacted.

## Gates (non-negotiable)

1. **Lawful basis before step 1** (EU/GDPR): B2B legitimate interest needs a documented balancing test, a source-of-data notice in the first email, and a working opt-out. Greece/EU ePrivacy rules on unsolicited email to individuals apply to named personal addresses. **[Likely]**
2. **Human approval before step 5.** Use `outbound-campaign-brief` for the approval gate and send cap.
3. **Deliverability before volume**: separate sending domains, SPF/DKIM/DMARC, warm-up, < 50 sends per inbox per day. **[Likely]**
4. **No invented personalisation**: every personal line must cite the signal it came from.

## Step 4 prompt

```
You write first-touch B2B emails for {{company}} selling {{offer}}.
Account: {{account_json}}  Signal: {{signal}} (source: {{signal_url}}, date: {{signal_date}})
Write 3 touches (day 0, 3, 8). Touch 1 ≤ 90 words: line 1 references the signal factually, line 2 connects it to one problem we solve, line 3 one proof point from {{proof_rows}}, CTA a single yes/no question.
Never invent facts not present in the account or signal. Output JSON: {"touches":[{"day","subject","body"}],"signal_cited":true}.
```

## Related
`outbound-campaign-brief`, `lead-scraper`, `linkedin-signal-outreach`, `outreach-execution`, `mcp-integration-scout` agent, `ai-automation-blueprints` (#02), `/outbound-pipeline`.
