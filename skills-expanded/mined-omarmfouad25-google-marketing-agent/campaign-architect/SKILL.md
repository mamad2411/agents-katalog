---
name: campaign-architect
description: Plan a Google Ads account structure and budget from the account's own data: campaign types, naming, budget split, bidding stages, goals and negative lists. Use when the user says "plan our campaigns", "restructure the account", "how should I split the budget", "new account structure", "Q4 plan for <brand>", or before building several campaigns at once.
---

# Campaign architect

Turn an account's real performance into a campaign plan: which campaigns, which type, which budget, which bidding
stage, which goal. The plan is a document; building it is the job of `search-launch` and `demand-gen-launch`.

## When to use

- A new quarter or a re-plan of an existing account.
- A new account that needs a structure before anything is built.
- "How much should each campaign get?" with more than one campaign involved.

## Inputs

Ask once, all together, for whatever the data can't answer:
- Tracks: which audiences are separate businesses (for example business buyers vs consumers).
- Focus lines: the products or services that must get protected budget.
- Markets and languages (the languages each landing page exists in).
- Monthly budget per track, and a target cost per lead if they have one.

## Steps

Call `account_profile` first (currency, writes, linked GA4).

1. **Baseline, last 30 and 90 days (read-only).** Don't plan from a blank sheet: the current account shows what to fix.
   If the account has no campaigns yet, run `tracking-audit` before building anything.
   GAQL has no `LAST_90_DAYS`: for 90 days use `segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'`.
   - `get_account_summary`, `get_campaign_performance`, `get_campaign_budgets`, `get_keyword_performance`, and the top
     search terms by cost with `run_gaql_query`.
   - Network split per campaign:
     `SELECT campaign.name, segments.ad_network_type, metrics.cost_micros, metrics.clicks FROM campaign WHERE segments.date DURING LAST_30_DAYS`.
     A "Search" campaign spending mostly outside Google Search is a Display campaign in disguise.
   - Spend outside the target areas: `geographic_view.location_type` and `user_location_view.targeting_location`
     (see the `ads-audit` skill for the queries).
   - What each campaign bids on: `campaign_conversion_goal` and `conversion_goal_campaign_config`.
   - Search demand: keywords with almost no impressions over weeks mean little search demand in those markets.
2. **Real leads.** If GA4 is linked, `ga4_custom_report` with `dimensions: ["landingPage", "eventName", "sessionDefaultChannelGroup"]` and
   `metrics: ["keyEvents", "sessions"]` for the same period. Cost per lead must be paid-only: use only the
   "Paid Search" rows for Search, and "Cross-network" / "Display" / "Paid Video" rows for Demand Gen. Work out cost per
   lead per line from Ads cost and those GA4 leads, not from Ads conversions alone.
3. **Measurement gate.** If campaigns don't bid on a working, audience-specific goal, stop and recommend the
   `tracking-audit` skill first. Bidding on broken measurement wastes the whole plan. `guide("measurement")`.
4. **Choose campaign types:**
   - Buyers search the product, category or brand → **Search**.
   - Little or no search demand (keywords barely serve) → **Demand Gen** to create demand, plus a small Search
     campaign on problem or benefit terms.
   - Own brand terms → a small separate Search campaign, so brand clicks don't flatter non-brand cost per lead.
   - Reaching decision-makers before they search → Demand Gen with a business audience, judged on engaged visits and
     leads.
5. **Structure rules:**
   - **One campaign = one budget = one goal = one audience.** Separate business and consumer campaigns, always.
   - Focus lines get their own campaign. Split a portfolio when one line's volume starves another.
   - No shared budgets. No Dynamic Search Ads.
   - Countries share a campaign at first; split one out only when its cost per lead differs by more than about 50%,
     or it needs a guaranteed budget.
   - Build in waves: core Search first, Demand Gen as soon as creative exists, awareness later.
6. **Naming convention** (pipe-delimited, fixed order, so the UI sorts and filters by it):
   `<Brand> | <B2B or B2C> | <Line> | <Search or DG> | <Markets> | <Period>`; ad groups `<Product> | <Theme> | <Language>`;
   lists `NEG | <Purpose>`; goals `<Audience> Leads`.
7. **Budget split:**
   - Per track first, then per campaign by strategic priority and expected lead value, not by last period's spend.
   - Brand protection gets the smallest share (around 5–10% of its track).
   - Each daily budget should be at least 1× the target cost per lead, ideally 2–3×. A campaign that can't buy about
     15–30 conversions a month should be merged or start on clicks.
   - Demand Gen needs more conversion volume to learn. If its budget can't buy about 30 conversions a month on its goal,
     launch it on MAXIMIZE_CLICKS (supported by `ads_create_demand_gen_campaign`) and judge it on engaged visits and
     leads.
   - Flag any campaign below that floor instead of silently accepting it.
8. **Bidding stage per campaign:**

   | Stage | Search | Demand Gen |
   |---|---|---|
   | Launch, little history | Maximize clicks with a CPC cap (about the line's historical average CPC) | Maximize conversions when the goal records and the budget allows; otherwise Maximize clicks |
   | Brand campaign | Manual CPC, low bid | — |
   | About 15–30 conversions in 30 days (review in week 3) | Switch from clicks to maximize conversions | Stay |
   | About 30+ conversions a month and a stable cost per lead for 2–4 weeks | Add a target CPA at the achieved level, never below | Same |

   No bidding, goal or audience changes in the first 1–2 weeks; one change per campaign per review. Bidding strategy
   changes are made in the Google Ads interface (Campaign → Settings → Bidding); no tool does it yet.
9. **Goals and negatives:**
   - One custom goal per audience, made of exactly that audience's lead actions. Page views stay secondary.
   - Shared negative lists by audience, phrase match:
     - `NEG | Global` on everything: jobs, courses, free, irrelevant industries, in every language.
     - `NEG | B2B - Consumer terms` on business campaigns: near me, reviews, at home…
     - `NEG | B2C - Trade terms` on consumer campaigns: supplier, wholesale, used, distributor…
     - Brand terms as negatives on non-brand campaigns.
   - Don't negate "price" for business buyers: they search "<product> price".
10. **Standard settings for every new campaign:**
    - Location: people in the location (presence).
    - Languages: every language the landing page exists in (Google infers the languages a user understands; target every language the landing page exists in).
    - Search: Google Search only (partners and Display expansion off).
    - Own budget, campaign-level custom goal, created paused.
    - In the interface: auto-apply recommendations off and automatically created assets off; Demand Gen final URL
      expansion off.
11. **Transition.** New campaigns run in parallel with the ones they replace for about 7 days, then the old ones are
    paused. Keep an old campaign running if it's the only source of a lead type the new structure doesn't cover yet.
12. **Optional foundations, after the user approves the plan:**
    - `ads_create_custom_goal` per audience; it needs `conversionActionIds` (get them with the `conversion_action`
      query in `tracking-audit`).
    - `ads_negative_list` to create the shared lists (attach them when the campaigns exist).

    Each one is a preview first, applied only after a yes.

## Output

One plan document (Markdown, or HTML if they want to share it):

```
# <Account> plan: <period>
## Diagnosis (what the baseline showed, with numbers)
## Campaign map
| Campaign (named) | Type | Audience | Markets | Languages | Daily budget | Bidding stage | Goal |
## Budget split (per track, per campaign, the floor check)
## Goals and negative lists
## Standard settings
## Transition and review plan (launch day, day 3, week 1, week 3, monthly)
## Build order → hand off to search-launch / demand-gen-launch
```

## Never

- Never create campaigns in this skill; hand each campaign row to `search-launch` or `demand-gen-launch`.
- Never propose shared budgets, Dynamic Search Ads, or one campaign that mixes business and consumer goals.
- Never size a daily budget below one target cost per lead without flagging it.
- Never quote industry averages as targets; plan from the account's own baseline (`guide("benchmarks")` only explains
  how to read numbers).
- If the profile is read-only (no write tools), the plan is still complete; tell the user that creating the goals and
  lists needs `npx google-marketing-agent accounts set <alias> writes true` and an MCP client restart.
