---
name: windsor
description: Pull marketing/analytics data from 325+ sources for analysis. Use whenever the user mentions Facebook Ads, Google Ads, LinkedIn, TikTok, GA4, Shopify, Salesforce, HubSpot, marketing campaigns, ad spend, attribution, channel ROI, conversion funnels, customer acquisition cost, or any cross-platform marketing intelligence question. Activates on phrases like "how is my Facebook campaign doing", "pull GA4 data", "compare ad spend across channels", "give me advice on optimizing X campaign", or any "I have data in [marketing tool]" framing. Free tier: 600 req/min, 10k/day.
---

# Windsor.ai — Marketing Intelligence via Data Pipeline

Windsor connects 325+ data sources (every major marketing/analytics platform) to 19 destinations including Claude. This plugin wraps the Windsor API as slash commands + pre-built marketing analysis prompts so Claude can pull fresh data and produce real recommendations instead of generic advice.

The mantra (from Windsor's own welcome video):

> *Windsor helps you to get data from more than 325 different data sources into 19 different destinations… your data pipeline to bring data from all the data sources in your organization into the destination of choice.*

We are the LLM destination. The plugin is what makes that destination useful inside Claude.

## When to invoke

- User asks any marketing-performance question naming a platform (Facebook Ads, Google Ads, LinkedIn, TikTok, GA4, etc.)
- User wants cross-channel attribution or ROI comparison
- User asks for campaign optimization advice ("how should I optimize my X campaign")
- User has data in Shopify, Salesforce, HubSpot and wants Claude to reason over it
- Anyone says "pull data from [marketing platform]" or "give me a report on [campaign]"

## Slash commands

### Discovery
| Command | Action |
|---------|--------|
| `/windsor connectors` | List all 325+ available connectors (paged) |
| `/windsor accounts` | List the user's currently-connected data source accounts |
| `/windsor fields <connector>` | Discover available fields for a specific connector (e.g., `/windsor fields facebook`) |

### Data pull
| Command | Action |
|---------|--------|
| `/windsor pull <connector> [--fields=...] [--from=...] [--to=...]` | Pull fresh data from a connector. Default: last 30 days, all default fields. Returns JSON. |
| `/windsor preview <connector>` | Show a 10-row preview of data without committing to a full pull |
| `/windsor compare <connectors...> --metric=<m>` | Cross-channel comparison on a single metric (e.g., `/windsor compare facebook,googleads,linkedin --metric=cpa`) |

### Pre-built analyses
| Command | Action |
|---------|--------|
| `/windsor optimize-campaign <connector> <campaign-name>` | Pull fresh campaign data + run optimization analysis. Returns: top wasteful spend, undersaturated audiences, recommended budget shifts, creative refresh signals |
| `/windsor channel-roi [period]` | Cross-channel ROI report for the period (default last 30 days). Ranks channels by efficiency. |
| `/windsor attribution <conversion-event>` | Multi-touch attribution analysis for a conversion event |
| `/windsor budget-shift <from-channel> <to-channel> <amount>` | Simulate the impact of moving budget between channels based on historical performance |
| `/windsor creative-fatigue <connector>` | Identify ad creatives that are losing performance over time |

## API surface (under the hood)

This plugin wraps the Windsor REST API (`https://connectors.windsor.ai`):

- Auth: API key as query param (`?api_key=...`)
- Default response format: JSON
- Rate limits: 600 req/min, 10k req/day (free tier)
- Refresh intervals: 60 min (Standard/Plus), 15 min (Professional/Enterprise)

Key endpoints used:
- `GET /list_connectors` — connector discovery
- `GET /{connector}/fields` — field discovery for a connector
- `GET /{connector}` — pull data
- `GET /onboard.windsor.ai/api/common/ds-accounts` — list connected accounts

## Pre-built analysis prompts

These are the templates the plugin loads into the LLM when an analysis slash command runs. Each one is tuned to produce actionable, evidence-bound recommendations rather than generic marketing advice.

### Campaign optimization template

```
You are reviewing live performance data from {connector} for campaign "{campaign}".

DATA (fresh, pulled {timestamp}):
{data}

Produce a campaign optimization report with these sections:

1. Top wasteful spend — line items / audiences / placements that are
   spending without converting. Cite the specific row + amount.
2. Undersaturated wins — line items / audiences with high efficiency
   that are budget-capped. Cite the specific row + recommended budget lift.
3. Creative refresh signals — ad creatives showing fatigue (declining
   CTR / rising CPC). List the top 3 to pause or refresh.
4. Recommended budget reallocation — concrete dollar shifts, not
   percentages. "Move $X/day from line A to line B."
5. One-line summary — what's the highest-ROI single change to make this week.

Cite data row IDs / line item IDs in every recommendation. No generic advice.
```

### Channel ROI template

```
You are comparing marketing channel performance for the period {period}.

DATA (fresh, pulled {timestamp}):
{cross_channel_data}

Produce a ranked report:

1. Channel ranking by ROI (revenue / spend), descending
2. Channel ranking by CPA, ascending
3. Channels that are over-funded (low ROI, high spend) — name budget
   to consider cutting
4. Channels that are under-funded (high ROI, low spend) — name budget
   to consider lifting
5. Cross-channel notes — anything that suggests one channel is feeding
   another (e.g., upper-funnel display correlating with branded search)
6. Recommended monthly budget reallocation — concrete dollar shifts

Always include the underlying numbers. No "consider doing X" without "because the data says Y."
```

(Additional templates for `/windsor attribution`, `/windsor budget-shift`, `/windsor creative-fatigue` follow the same shape — fresh data + tight structure + cite-the-rows.)

## What makes this skill differentiating

A generic "marketing GPT" gives you generic advice. A Windsor-powered Claude gives you advice grounded in **fresh data pulled at request time** with **specific row references** in the recommendations. That's the difference between "consider improving your CTR" and "pause line item 89432, it's spent $1,247 this week with 0 conversions."

For Max-tier users, this skill is gifted — it's how their Claude becomes a marketing analyst that knows their actual numbers.

## Configuration check

If `WINDSOR_API_KEY` is unset, the skill returns:

> *"Windsor is not configured. Get a free API key at windsor.ai (no credit card required for the free tier — 600 req/min, 10k/day). Then set WINDSOR_API_KEY in your env. Once set, run `/windsor accounts` to see what's connected."*

If the key is set but no accounts are connected, the skill prompts the user to connect data sources at windsor.ai/onboard before running pulls.

## Free tier hard rules

- Don't exceed 600 req/min — the plugin batches and rate-limits internally
- Don't exceed 10k req/day — the plugin caches results for the configured refresh interval and refuses to re-pull within that window unless `--force` is passed
- Default refresh interval: 60 minutes (Standard/Plus tier)
- Cache responses keyed by `{connector}:{fields}:{from}:{to}` so identical pulls don't burn quota
