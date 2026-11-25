---
name: pe-deal-sourcing
version: 1.0.0
description: Build a private-equity origination strategy and proprietary deal pipeline — set the thesis, pick the channel mix, size the funnel, and produce a target list with an outreach and tracking plan.
author: matrixx0070
tags: [deal-sourcing, origination, deal-pipeline, thesis-driven, proprietary-deals, funnel-math, private-equity]
capabilities: []
---

## When to use

Use this when a fund needs to fill the top of its funnel — when it is standing up an origination motion, entering a new sector or geography, or has capital to deploy and too few quality opportunities in flight. Reach for it to decide *where* deals should come from, *what* the fund is hunting for, and *how many* touches are needed to close the number of platforms the fund promised its LPs. The output is an origination plan: a stated thesis, a channel mix with owners, funnel math tied to the deployment target, and a ranked target list with an outreach cadence and CRM-tracking structure.

**Not for:** deciding go/no-go on a single opportunity already in hand (use pe-deal-screening — sourcing fills the funnel, screening judges one item in it); building the diligence workstream once a deal is under LOI (use pe-dd-checklist); preparing management-meeting question sets (use pe-dd-meeting-prep); writing the IC memo for a deal you want to pursue (use pe-ic-memo); modeling returns for a target (use pe-returns-analysis); analyzing a target's unit economics (use pe-unit-economics); assessing a target's AI maturity and AI-driven value (use pe-ai-readiness); building the post-close value-creation plan (use pe-value-creation-plan); or tracking portfolio-company KPIs after close (use pe-portfolio-monitoring).

## Method

1. State the origination posture. Decide the balance between **thesis-driven** origination (you define a sector/sub-sector view first, then hunt targets that fit) and **opportunistic** origination (you react to what intermediaries bring). **Decision:** if the fund has a differentiated angle or operating expertise in a space, weight thesis-driven; if it is a generalist or early in a fund's life needing volume, weight opportunistic — most funds run a blend, but the split determines where effort goes.
2. Write the thesis (if thesis-driven). Name the sub-sector, the tailwind (regulation, consolidation, technology shift, demographic), the target profile (revenue band, EBITDA band, business model, ownership type), and *why this fund wins this deal* (angle: operating partners, add-on platform, sector reputation, speed/certainty).
3. Set the channel mix across three lanes: **intermediated** (investment banks, brokers, auction processes — high volume, low proprietary edge, competitive pricing), **proprietary/relationship** (direct owner outreach, executive networks, prior management teams — lower volume, better pricing, higher conversion), and **thematic/mapped** (systematic market-mapping of every company fitting the thesis, then patient cultivation). **Decision:** allocate origination hours by expected yield, not by comfort — auctions are easy to fill but win rates are low and multiples are bid up; proprietary is hard but is where returns are made.
4. Size the funnel backward from the deployment target. Start from platforms-to-close per year, apply stage conversion rates, and solve for required top-of-funnel volume (see Reference for the math). This tells you whether the channel mix can physically produce the required deal count.
5. Build the target list. For thematic origination, map the universe: every company matching the profile, with owner, size, ownership status, and a proprietary-signal flag (aging owner, no succession, sponsor-backed nearing hold-period end, carve-out candidate). Rank by fit × winnability × reachability.
6. Design the outreach cadence and ownership. Assign each target/relationship to an owner, set a touch rhythm (quarterly for cultivation targets, event-driven for signals), and define the CRM fields and stage gates so nothing goes cold.
7. Instrument the funnel. Track conversion at every stage so the mix can be re-weighted next quarter toward the channels actually producing closes — origination is a measured, iterated motion, not a one-time list.

## Example

A lower-mid-market fund with $400M and a 5-year deployment period targets ~$300M into 6 platforms over 3 years, i.e. 2 platforms/year. Its thesis: consolidation of owner-operated HVAC and plumbing services businesses ($3–8M EBITDA) riding the aging-owner succession wave, with the fund's edge being a buy-and-build playbook and a bench of vetted operating CEOs. Working backward with typical conversion — 2 closes need ~4 LOIs, ~13 IC-stage looks, ~40 management meetings, ~130 screened deals, ~650 sourced opportunities per year. The team judges that intermediated flow alone (auctions for these micro-cap targets are thin and pricey) cannot supply 650 quality looks, so it commits 60% of origination hours to a thematic map of ~900 regional owner-operated targets, cultivating the ~200 with owners over 60 and no clear successor via quarterly direct outreach, and 40% to broker relationships for opportunistic tuck-ins. First-year result: 610 sourced, 3 LOIs, 2 closes — funnel math held, and proprietary deals closed at ~1.5x turns cheaper than the one auction deal they lost on price.

## Pitfalls

- **Confusing volume with pipeline.** A CRM full of auction teasers is not a pipeline if win rates are near zero. Measure *qualified, winnable* opportunities, not raw deal count — 650 teasers you can't win is worse than 40 proprietary conversations you can.
- **A thesis too broad to act on.** "We invest in healthcare" is not a thesis; it produces no target list and no proprietary edge. The thesis must be narrow enough to name specific companies and explain why you win them.
- **Letting proprietary relationships go cold.** Proprietary origination is a multi-year cultivation game; a single meeting then silence yields nothing. Without an owned cadence and CRM stage gates, relationship deals quietly die and the fund defaults back to expensive auctions.
- **Ignoring winnability.** Sourcing beautiful targets you have no angle to win burns time. Score reachability and win probability alongside fit, and concentrate on deals where the fund's edge actually converts.
- **Never re-weighting the mix.** Channel yields drift; the auction market heats and cools, a thematic vein gets picked over. Funds that don't instrument stage conversion keep pouring hours into channels that stopped producing.

## Output format

```
# Origination Plan — <fund> — <sector/thesis> — <date> — v<n>

## Thesis
Sub-sector: <...>   Tailwind: <...>
Target profile: revenue <band> | EBITDA <band> | model <...> | ownership <...>
Why we win: <angle>

## Deployment target → funnel math
Platforms/yr: <n>   Avg equity/deal: <$>   Required top-of-funnel: <n>/yr
| Stage | Conversion | Volume needed |
| Sourced → Screened | <%> | <n> |
| Screened → Mgmt meeting | <%> | <n> |
| Mgmt meeting → IC look | <%> | <n> |
| IC look → LOI | <%> | <n> |
| LOI → Close | <%> | <n> |

## Channel mix
| Channel | Type (intermediated/proprietary/thematic) | Effort % | Expected yield | Owner |

## Target list
| Target | Owner status | Rev/EBITDA | Fit (1-5) | Winnability (1-5) | Signal | Assigned to | Stage | Next touch |

## Cadence & tracking
- <target/relationship> — <cadence> — <owner> — <CRM stage gate>

## Review
Re-weight channels quarterly on actual stage-conversion data.
```

## Reference

Origination is the front of the private-equity value chain: no proprietary, well-priced flow, no returns. The material below reflects how funds actually run sourcing.

### Thesis-driven vs opportunistic origination

| | **Thesis-driven** | **Opportunistic** |
|--|--|--|
| Starting point | A sector/sub-sector view formed first | Whatever comes across the desk |
| Deal supply | Self-generated via mapping and outreach | Intermediary-fed |
| Pricing | Often better (proprietary, less competition) | Market-clearing (auctions bid up) |
| Win rate | Higher where the fund has an angle | Lower (competing on price) |
| Effort profile | High upfront (map + cultivate), compounding | Low upfront, reactive |
| Best for | Specialists, buy-and-build, differentiated funds | Generalists, volume needs, filling gaps |

Most funds blend the two. The strategic question is the *split*: a fund with genuine sector edge should overweight thesis-driven because that is where mispriced, winnable deals live; a generalist or a fund early in its investment period needing to show deployment often leans opportunistic for volume, accepting thinner returns.

### Channel mix — the three origination lanes

| Channel | Mechanism | Volume | Proprietary edge | Typical win rate | Pricing |
|---------|-----------|--------|------------------|------------------|---------|
| **Intermediated** | Sell-side banks, brokers, auctions, teasers/CIMs | High | Low (everyone sees it) | Low (5–15%) | Competitive, bid up |
| **Proprietary / relationship** | Direct owner outreach, executive & advisor networks, repeat management teams | Low–medium | High | High (30–50%+) | Favorable |
| **Thematic / mapped** | Systematic market map of the whole universe, patient cultivation of best-fit targets | Medium (over time) | Highest | Highest on cultivated targets | Best |

A healthy lower/mid-market origination motion skews effort toward proprietary and thematic, using intermediated flow for coverage and tuck-ins. Auction-only sourcing is the hallmark of an undifferentiated fund and shows up later as compressed entry-multiple discipline and weak returns.

### Funnel math — sizing origination from the deployment target

Work **backward** from what the fund committed to deploy:

```
Platforms to close per year = Target deployment / Avg equity per platform / Investment period (yrs)
Top-of-funnel needed = Closes ÷ (c1 × c2 × c3 × c4 × c5)
```

where c1…c5 are the stage-to-stage conversion rates. Illustrative mid-market conversions (calibrate to your own history):

| Stage transition | Typical conversion |
|------------------|--------------------|
| Sourced → Screened (passes quick screen) | ~20% |
| Screened → Management meeting | ~30% |
| Management meeting → Serious IC-stage look | ~30% |
| IC-stage look → LOI submitted | ~30% |
| LOI → Closed deal | ~50% |

Compounded, roughly **300–350 sourced opportunities produce one close**. So a fund needing 2 closes/year needs ~600–700 sourced looks/year. If the chosen channel mix cannot physically generate that qualified volume, either the mix is wrong or the deployment target is unrealistic — this is the single most useful diagnostic the math provides.

### Proprietary-signal flags (what to map for in thematic sourcing)

- **Succession gap** — owner over ~60, no family or management successor identified.
- **Sponsor hold-period end** — company backed by another fund approaching year 4–6 of its hold (likely to come to market).
- **Carve-out candidate** — a non-core division of a larger corporate.
- **Distress / covenant pressure** — capital need creating a motivated seller.
- **Consolidation fragment** — sub-scale player in a fragmenting market ripe for roll-up.

### CRM stages and hygiene

A minimum origination CRM tracks: Target → Contacted → Meeting held → NDA/info exchange → IOI/LOI → Diligence → Close, with an owner, last-touch date, and next-action for every live target. The discipline that matters is the **cadence**: cultivation targets get a scheduled recurring touch, signal-driven targets get event triggers, and stage-conversion rates are reviewed quarterly to re-weight where origination hours go.
