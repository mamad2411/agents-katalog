---
name: competitor-pricing-scan
description: Scan competitor pricing pages with web_extract, normalize plans into a like-for-like comparison table, and flag positioning gaps. Use when the user asks to "check competitor pricing", "how do we compare on price", "pricing scan", "what do rivals charge", "are we underpriced", or names competitors whose plans they want mapped. Don't use for deep research on one company as a sales prospect — that's lead-research-dossier.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Business Ops, Pricing, Competitive Intelligence, Research]
    related_skills: [lead-research-dossier, cold-outreach-sequencer, weekly-revenue-report]
    requires_toolsets: [web]
---

# Competitor Pricing Scan

Fetches live competitor pricing pages, forces every plan into one normalized table (same currency, same billing period, same feature axes), and calls out where the user's positioning has gaps or openings. Every number is sourced and dated — pricing pages change weekly, so a scan without dates is fiction.

## When to Use

- User wants to know what 2–6 named competitors charge and how plans compare.
- User is setting or revising their own pricing and needs the landscape first.
- User suspects they're under/overpriced and wants evidence.
- **Not for:** deep research on one company as a sales prospect — that's `lead-research-dossier`. Not for tracking your own revenue — `weekly-revenue-report`.

## Quick Reference

| Action | Command / Call |
|---|---|
| Find pricing page | web search: `"<competitor>" pricing` → prefer `/pricing` on the official domain |
| Extract plans | `web_extract` on the pricing URL — capture plan names, prices, billing period, seat/usage limits, key features |
| Hidden pricing | search `"<competitor>" pricing site:reddit.com` or review sites; label result "reported, unverified" |
| Normalize math | everything → per seat (or per unit) per month, billed annually, one currency |
| Gap analysis | compare axes: price floor, price ceiling, free tier, billing granularity, feature gating |

## Procedure

1. **Precheck** — confirm web tools are available; get from the user: the competitor list (2–6 names), the user's own current pricing (for the comparison row), and the normalization unit (per seat/month is the default). No competitor list? Ask — don't guess the market.
2. **Locate** — find each competitor's official pricing page. Verify it's the company's own domain, not a review-site summary. Record the URL and today's date per competitor.
3. **Extract** — `web_extract` each page. Pull: every plan name, price, billing period (monthly vs annual-billed-monthly — they differ), currency, unit (seat/usage/flat), free tier or trial, and the 3–5 headline features that gate each tier. "Contact sales" is a data point — record it as `custom`.
4. **Normalize** — convert everything to the agreed unit. Show your math for any conversion (annual → monthly: ÷12; currency conversions flagged with the rate used and marked approximate). Never mix a monthly-billed price against an annual-billed one without labeling both.
5. **Build the table** — one row per competitor plan plus the user's own plans, columns per the template. Missing data is `—` with a note, never a guessed number.
6. **Gap analysis** — answer at minimum: Where is the price floor and who owns it? Is there an uncontested tier (e.g., nobody serves the $20–50 mid-tier)? What does everyone gate that the user gives away free (or vice versa)? Who's moved recently (promo banners, "new" tags)?
7. **Deliver** — template below, with the sources block. Recommend a re-scan cadence (quarterly, or before any pricing decision).

## Output Template

```
# Pricing Scan — <market/segment> — <date>
Normalized to: <currency> per <unit> per month, billed <period>

| Company | Plan | Price (norm.) | Billing | Free tier | Key gates | Source (date) |
|---|---|---|---|---|---|---|
| **You** | ... | ... | ... | ... | ... | — |

## Positioning Gaps
1. <gap or opening — evidence — so-what for the user>
2. ...
3. ...

## Caveats
- <unverified numbers, currency assumptions, pages that blocked extraction>
Re-scan recommended: <cadence>
```

## Pitfalls

- **Comparing annual-billed against monthly-billed prices** — "$29/mo billed annually" vs "$29/mo" is a ~20% error hiding in plain sight. Recovery: capture the billing period for every price and normalize to one basis; when a page shows both, record both and use the annual-billed figure in the table with a footnote.
- **Pricing page blocked or JS-rendered** — `web_extract` returns nav chrome and no numbers. Recovery: try the page's `?plan=` variants, a web search for cached copies, or review-site data — and clearly mark those numbers "reported, unverified <date>".
- **Stale scan treated as current** — competitor repriced last month; your table says otherwise. Recovery: date every source in the table; refuse to merge numbers from a previous scan without re-fetching.
- **Feature names that don't map** — "unlimited projects" vs "workspaces" vs "boards" aren't the same axis. Recovery: define 4–6 comparison axes in the user's vocabulary first, then map each competitor's terms onto them, noting imperfect matches.

## Verification

- [ ] Every price traces to a source URL fetched today (or is labeled unverified)
- [ ] All prices normalized to one currency, unit, and billing basis — math shown
- [ ] User's own pricing appears as a row for direct comparison
- [ ] ≥3 gap findings, each with evidence and a so-what
- [ ] No guessed numbers — gaps in data are visibly marked `—`
