---
name: business-content-orchestrator
description: "Route a business-content task to the right skill among 10 specialists — voice profiling, long-form articles, multi-platform content systems, SEO, market/competitor research, launch campaigns, investor decks/memos, investor outreach, lead intelligence, and social-graph ranking. USE WHEN a user is writing, marketing, fundraising, or doing outbound for a product or company but hasn't named the specific concern."
cluster: business-content
version: 1.0.0
---

# Business-Content Orchestrator

The single entry skill for go-to-market writing and outbound. It locates the task on the
**lane × audience** map and delegates to one of 10 specialist spokes. The cross-cutting model
every spoke shares — the source-derived **Voice Profile**, the research/signal substrate, and
the channel contract that keeps a message native to its surface — lives in
`business-content-core`; read it before drafting anything reputation-, launch-, or
fundraising-sensitive.

## Routing map (intent → spoke)

**Establish the voice & evidence (shared substrate — almost always first)**
- Reusable style from real source material → `brand-voice` *(produces the `VOICE PROFILE` every other lane consumes)*
- Market sizing, competitor scans, fund/diligence research → `market-research` *(produces the evidence other lanes cite)*

**Publish (own channels)**
- Long-form: articles, guides, tutorials, newsletter issues → `article-writing`
- Platform-native systems: X / LinkedIn / TikTok / YouTube threads, scripts, calendars, repurposing → `content-engine`
- Search visibility: technical SEO, on-page, schema, Core Web Vitals, keyword mapping → `seo`

**Market (the launch)**
- Multi-channel launch as one orchestrated campaign (positioning → landing copy → email → ads → social → video scripts) → `marketing-campaign` *(itself an orchestration layer; it pulls `brand-voice`, `content-engine`, and `seo`)*

**Fund (investor-facing)**
- Decks, one-pagers, memos, models, accelerator apps that must stay mutually consistent → `investor-materials`
- Cold emails, warm-intro blurbs, follow-ups, update emails to angels/VCs/accelerators → `investor-outreach`

**Reach (outbound & network)**
- Full find → score → warm-path → enrich → draft pipeline for high-value contacts → `lead-intelligence`
- The standalone graph-ranking engine (bridge math, decay tuning, network-gap analysis) → `social-graph-ranker` *(the model `lead-intelligence` runs internally; break it out when the user wants the ranking itself)*

## Folded spokes

Additional specialists folded into this cluster. They cover **narrative craft** (long-form
storytelling, fiction technique) and **internal/HR-facing writing** — adjacent to the
go-to-market lanes above and sharing the same voice-first, evidence-backed discipline. Route to
one when the named concern appears; load it on demand exactly like the spokes above.

- Curated quote/aphorism library — theme matching, add/research/search, newsletter variety → `aphorisms` *(reach for the opener/closer quote when drafting a newsletter or article)*
- Layered fiction system (Storr science + rhetorical figures) — story bibles, character arcs, chapters, prose → `writestory`
- Autonomous multi-agent novel pipeline (Writer→Validator→Auditor→Reviser CLI, review gates) → `inkos-multi-agent-novel-writing` *(book-length production at scale; distinct from `writestory`'s single-author craft loop)*
- Seven-step novel methodology guide — how to organize a novel project end-to-end → `novel-writer-workflow-guide`
- Natural dialogue technique — character-consistent, subtext-driven conversation that reveals character and advances plot → `natural-dialogue-techniques` *(pair with `writestory`/`novel-writer-workflow-guide` when drafting dialogue scenes)*
- Internal communications — 3P updates, leadership/company newsletters, FAQs, incident & status reports in standard company formats → `internal-comms`

## Picked-up spokes

Recently absorbed specialists (from antigravity-awesome-skills). They sit on the **build / launch /
measure** side of the same product story the GTM lanes serve — *what* you're shipping, *how* it
becomes a business, and *whether it works* — so the orchestrator can route product-/SaaS-shaped
asks, not just writing-shaped ones. Load each on demand exactly like the spokes above.

- Production LLM product engineering — RAG, prompt engineering at scale, structured-output validation, latency/streaming UX, cost control → `ai-product` *(reach for it when "the product itself is AI" and must hold up in production)*
- AI-API-wrapper business — defensibility, usage metering, rate limiting, model selection, output quality for a paid wrapper tool → `ai-wrapper-product` *(the business/moat angle on top of `ai-product`'s build angle)*
- Indie micro-SaaS launch playbook — validation → MVP → pricing → launch → sustainable revenue for solo/small founders → `micro-saas-launcher` *(bootstrapped GTM; pairs with `marketing-campaign` for the launch beat)*
- Notion-template (digital-product) business — design-to-sell, Gumroad/Lemon Squeezy, marketplaces, support systems → `notion-template-business` *(productizing templates into recurring revenue)*
- Senior PM toolkit — 30+ frameworks (RICE/JTBD/Kano/North Star), PRD/roadmap templates, 32 SaaS metrics with formulas → `product-manager` *(structured product analysis: PRDs, roadmaps, prioritization, metrics — feeds positioning into the publish/fund lanes)*
- Segment CDP engineering — Analytics.js, server-side tracking, Protocols tracking plans, identity resolution, governance → `segment-cdp` *(the measurement substrate behind launches; route here when "instrument the product / capture clean event data" comes up)*

## Standard Operating Flow

1. Locate the task: which lane (publish / market / fund / reach) and which audience (public, investor, prospect).
2. If the output is voice-sensitive, **run `brand-voice` first** and reuse its `VOICE PROFILE` — never re-derive style per draft or default to generic AI copy. If it makes a business claim, ground it via `market-research`. (Model in `business-content-core`.)
3. Delegate to the spoke(s). Multi-step asks fan out in lane order — e.g. "launch this" → `brand-voice` → `marketing-campaign` (which pulls `content-engine` + `seo`); "raise a round" → `investor-materials` → `investor-outreach`; "find and reach buyers" → `social-graph-ranker` → `lead-intelligence`.
4. Return: chosen spoke(s), the voice/evidence inputs they consumed, the target channel(s), and the next action (draft, deck, sequence, or outreach list).

## Guardrails

See `business-content-core`. In short: **voice-first, evidence-backed, channel-native** — one
`VOICE PROFILE` flows everywhere instead of per-draft mimicry; every business claim traces to a
real source, not invention; each message is shaped for its surface (the same copy reused across
email, LinkedIn, and X is a tell). Never auto-send outbound — draft and let the user approve.
The cluster's value is content that reads like a specific person with receipts; don't quietly
let it collapse into platform slop.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
