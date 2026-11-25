---
name: competitor-teardown
description: Structured teardown of one competitor product — positioning, pricing, onboarding, and exploitable gaps — with every claim linked to a fetched source. Use when the user says "tear down <competitor>", "how does X position/onboard/charge", "deep dive on this competitor", or names a rival product they want dissected. Don't use for sizing the whole market — that's market-sizing-tam — or for ongoing weekly scanning of a space — that's trend-radar.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Research & Analysis, Competitive Intelligence, Product Strategy]
    related_skills: [market-sizing-tam, trend-radar, seo-content-audit]
    requires_toolsets: [web]
---

# Competitor Teardown

Produces a one-product teardown across four lenses — positioning, pricing, onboarding, gaps — where every factual claim carries a source URL fetched during this run. The standard: observed beats reported beats inferred, each claim is labeled which of the three it is, and the deliverable ends with what the user should do about it, not just what the competitor does.

## When to Use

- User names one competitor (or 2–3, run sequentially) and wants to understand how they win.
- Before a positioning, pricing, or onboarding decision: "what does X do here?"
- Investor/accelerator prep: "who else does this and how are you different?"
- **Not for:** market size math (`market-sizing-tam`); recurring signal monitoring (`trend-radar`); auditing a page's SEO (`seo-content-audit`).

## Quick Reference

| Action | Command / Call |
|---|---|
| Homepage positioning | `web_extract` on the root domain — capture hero headline, subhead, social proof, CTA verb |
| Pricing | `web_extract` on `/pricing` — plans, prices, billing basis, gated features, free tier |
| Onboarding (observed) | `web_extract` signup page + docs "getting started"; note steps, required fields, time-to-value claims |
| Onboarding (reported) | search `"<competitor>" onboarding OR "getting started" review` — G2, Reddit, YouTube walkthroughs |
| Sentiment & gaps | search `"<competitor>" site:reddit.com` and `"<competitor>" alternatives` — recurring complaints |
| Recent moves | search `"<competitor>" changelog OR "what's new"` — last 90 days |

## Procedure

1. **Precheck** — confirm web tools are available. Get from the user: the competitor name + URL, the user's own one-line positioning (needed for the gap analysis), and which lens matters most right now. No user positioning? Ask — a teardown without a "compared to what" produces trivia.
2. **Positioning** — extract the homepage. Record verbatim: hero headline, subhead, the customer named ("for teams who..."), proof elements (logos, counts, testimonials), and primary CTA verb. Then write the implied positioning in one sentence: *for <who>, X is the <category> that <differentiator>*. Label it `inferred` — it's your read, not their words.
3. **Pricing** — extract `/pricing`. Capture every plan: name, price, billing basis (monthly vs annual-billed — they differ), unit, free tier/trial, and the 3–5 features gating each step up. "Contact sales" is data — record as `custom`. Note the plan the page visually pushes; that's their target customer telling on itself.
4. **Onboarding** — extract the signup page and getting-started docs: steps to first value, required fields, credit-card-required?, self-serve vs sales-gated. Supplement with reviews and walkthroughs for the parts behind the signup wall — label those `reported`, with source.
5. **Gaps** — search reviews, Reddit, and "<competitor> alternatives" pages for recurring complaints (≥2 independent sources before it counts). Cross-reference with what the user does well. A gap is only exploitable if customers complain about it AND the user can credibly serve it.
6. **Deliver** — fill the template. Every claim row cites its URL and access date, and carries `observed` / `reported` / `inferred`. End with three moves for the user, each tied to a specific finding.

## Output Template

```
# Teardown — <competitor> — <date>
Their positioning (inferred): For <who>, <X> is the <category> that <differentiator>.

## Positioning        | evidence: <url> (<date>)
- Headline (verbatim): "<...>" | Named customer: <...> | Proof: <...>

## Pricing            | evidence: <url> (<date>)
| Plan | Price | Billing | Key gates |
|---|---|---|---|
Pushed plan: <which and why that matters>

## Onboarding
- Steps to first value: <n> — <list> [observed: <url>]
- Friction / walls: <...> [reported: <url>]

## Exploitable gaps
1. <gap> — complained about at <url1>, <url2> — user can win here because <...> (confidence: high/med/low)
2. ...

## Your three moves
1. <specific action> — because <finding #>
```

## Pitfalls

- **Marketing copy read as ground truth** — "loved by 10,000 teams" is a claim, not a fact. Recovery: label homepage numbers `reported (their claim)`; only independently verifiable facts (prices on the page, steps you observed) get `observed`.
- **Pricing page JS-blocked or extraction returns nav chrome** — no numbers come back. Recovery: try the Wayback Machine (`web.archive.org/web/2026/<url>`) or review-site pricing data; mark all such numbers `reported, unverified <date>` and never present them as current.
- **Gap analysis without the user's own position** — you list competitor weaknesses the user can't exploit either. Recovery: step 1 requires the user's positioning; every gap must pass "customers complain AND user can serve it".
- **One angry Reddit thread becomes 'users hate X'** — a single source inflated into a pattern. Recovery: gaps need ≥2 independent sources; one source gets reported as "single mention, unconfirmed".
- **Stale teardown reused** — pricing and positioning change monthly. Recovery: date every source; if asked to reuse a teardown older than 60 days, re-fetch pricing and homepage before answering.

## Verification

- [ ] Every factual claim has a source URL fetched this run, with access date
- [ ] Every claim labeled observed / reported / inferred
- [ ] Pricing table states billing basis for every price
- [ ] Each gap has ≥2 independent sources and a confidence label
- [ ] "Your three moves" each trace to a specific numbered finding
