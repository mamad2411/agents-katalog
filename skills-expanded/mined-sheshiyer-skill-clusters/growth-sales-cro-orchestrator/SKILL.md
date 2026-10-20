---
name: growth-sales-cro-orchestrator
description: "Route a growth, sales, or conversion-rate-optimization task to the right skill among 24 specialists — page/form/popup/signup/onboarding/paywall CRO, A/B testing, analytics, pricing, paid ads, RevOps, churn, referrals, sales collateral, pitch decks, competitor/customer research, and app-store optimization. USE WHEN a user wants to lift conversions, grow revenue, or close more deals but hasn't named the specific funnel stage or lever."
cluster: growth-sales-cro
version: 1.0.0
---

# Growth-Sales-CRO Orchestrator

The single entry skill for moving a number — conversions, activation, revenue, retention,
closed deals. It locates the task on the **funnel stage × lever** map and delegates to one of
24 specialist spokes. The cross-cutting model every spoke shares — the funnel itself, the
**baseline → hypothesis → test → decide** measurement loop, and the rule that you optimize on
evidence rather than opinion — lives in `growth-sales-cro-core`; read it before proposing any
change you intend to call a "win", before designing a test, or before touching pricing.

## Routing map (intent → spoke)

**Measure first (shared substrate — almost always step zero)**
- Instrument events, GA4/GTM/Mixpanel/Segment, tracking plan, attribution → `analytics-tracking` *(if you can't see the metric, you can't move it)*
- Design the experiment that proves a change works → `ab-test-setup` *(hypothesis, variant, significance, runtime)*

**Convert (self-serve funnel — the heart of CRO)**
- A marketing page (home, landing, pricing, feature, blog) isn't converting → `page-cro`
- A non-signup form (lead, contact, demo, application, checkout) → `form-cro`
- A popup, modal, overlay, exit-intent, sticky bar → `popup-cro`
- A signup / registration / trial-start flow → `signup-flow-cro`
- Post-signup activation, first-run, time-to-value, "they sign up but don't stick" → `onboarding-cro`
- In-product upgrade screen, upsell, feature gate, free→paid → `paywall-upgrade-cro`

**Monetize (what & how you charge)**
- Pricing tiers, packaging, value metric, freemium, price increase → `pricing-strategy` *(public pricing; for the in-app upgrade moment use `paywall-upgrade-cro`)*

**Acquire (paid demand)**
- Google/Meta/LinkedIn/X campaigns, ROAS, CPA, targeting, retargeting, bidding → `paid-ads`

**Retain & expand (keep and grow the base)**
- Churn, cancel flow, save offers, dunning, win-back, retention → `churn-prevention`
- Referral / affiliate / ambassador / viral-loop programs → `referral-program`

**Sell (human-assisted path, runs parallel to self-serve)**
- Lead lifecycle, scoring, routing, MQL→SQL, marketing→sales handoff, CRM hygiene → `revops`
- Sales narratives, talking points, value framing from product docs → `sales`
- Sales collateral: decks, one-pagers, objection handling, demo scripts, battle-card content → `sales-enablement`
- Investor / fundraising pitch experience (scrollytelling deck artifact) → `pitchdeck-skill`
- Find and qualify target accounts/contacts for outbound → `lead-research-assistant`

**Research (cross-cutting evidence — feeds every lane)**
- Voice-of-customer: interviews, transcripts, reviews, JTBD, personas, "why they churn/convert" → `customer-research`
- Company brief: exec quotes, product strategy, org context for a target/partner → `company-research`
- Competitor comparison / "vs" / alternative pages (SEO + sales enablement) → `competitor-alternatives`
- Structured teardown of a rival's positioning, messaging, channel behavior → `competitor-teardown`

**App-store growth (mobile listing surface)**
- ASO: keywords, metadata, ranking, store listing optimization → `app-store-optimization`
- Store screenshots / preview gallery to platform spec → `app-store-screenshots`
- Codebase-driven, ASO-optimized generated screenshots → `aso-appstore-screenshots`

## Standard Operating Flow

1. **Locate the task** on the map: which funnel stage (acquire → convert → activate → monetize → retain → expand, or the parallel sell path) and which lever.
2. **Establish the metric first.** If the request implies a "win" but no baseline or instrumentation exists, route through `analytics-tracking` before changing anything, and through `ab-test-setup` if the change is worth proving. The model is in `growth-sales-cro-core`.
3. **Delegate to the spoke(s).** Multi-step asks fan out in funnel order — e.g. "more paying users" → `page-cro` (top) → `signup-flow-cro` → `onboarding-cro` → `paywall-upgrade-cro`, each gated by a measured hypothesis.
4. **Ground in evidence.** Conversion and messaging changes should cite `customer-research` (voice of customer) or competitor findings, not taste.
5. **Return**: chosen spoke(s), the single metric each change targets, the test plan (or why none), and the next action.

## Guardrails

See `growth-sales-cro-core`. In short: **one change, one metric, one hypothesis** — name the
number before you touch the funnel; don't call an untested change a "win"; respect statistical
significance and minimum runtime before declaring a winner; ground copy and offers in
voice-of-customer evidence, not opinion; never invent metrics, lift percentages, or competitor
claims. Pricing and paywall changes are revenue-affecting — state the assumption and the blast
radius before shipping.

## External companions (not in this cluster)

- `alex-hormozi-pitch` and `customer-sales-automation` ship as a separate **bundle** (an
  empty/agent-only package without a top-level `SKILL.md`), so they are archived outside this
  cluster. Reach for the bundle when you want Hormozi-style offer/pitch framing or the
  prebuilt sales-automation/support agents; this cluster's `sales`, `sales-enablement`, and
  `pitchdeck-skill` cover the same intents natively.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
