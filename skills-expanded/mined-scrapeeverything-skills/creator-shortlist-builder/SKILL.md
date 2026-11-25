---
name: creator-shortlist-builder
description: Build a ranked shortlist of creators for an influencer campaign using the Scrape Everything API. Discovers candidates from YouTube channel and video search, Instagram reels search, Pinterest search, TikTok sounds and seed accounts, screens them on follower tier, engagement rate, views, cadence and topic fit, and outputs a scored table with links and the next step for each. Use when the user asks to find influencers or creators for a niche, build an outreach or partner list, find YouTubers or TikTokers like a given creator, or source micro-influencers for a campaign.
---

# Creator shortlist builder

From a campaign brief to a ranked, evidence-backed list of 10-20 public creators to contact.

## Inputs

- **Brief**: niche/topic keywords, product, target audience (language, region), campaign format.
- **Platforms**: any of YouTube, Instagram, TikTok, Pinterest, Twitch.
- **Follower tier**: nano (1k-10k), micro (10k-100k), mid (100k-500k), macro (500k-1M), mega (1M+). Default micro + mid.
- **Seeds** (optional): creators the user already likes, used to find similar ones.
- **Budget**: max credits (default 60) and shortlist size (default 15).

## Credit estimate

| Stage | Calls | Credits |
| --- | --- | ---: |
| Discover | `youtube.search` (type channel, then type video) per keyword | 1 each |
| Discover | `instagram.reels_search` per keyword (10 reels with owners) | 3 each |
| Discover | `pinterest.search` per keyword (pinners) | 2 each |
| Discover | `tiktok.music` on a niche sound (authors of top videos) | 2 each |
| Screen | profile call per candidate (`youtube.profile`, `instagram.profile`, `tiktok.profile`, `pinterest.profile`, `twitch.channel`) | 1 each |
| Score | posts call for the top ~15 (`youtube.videos` 1, `instagram.photos` 2, `tiktok.posts` 1) | 1-2 each |

Typical: 3 keywords x 2 platforms discovery (~10) + 30 screens (30) + 15 scores (~20) = **~60 credits**. Show the plan and confirm before spending more than the budget.

## How to call the API

Use the `scrapeeverything-api` skill if installed (MCP tools such as `youtube_search`, `instagram_reels_search`, `instagram_profile`, the `scrapeeverything` CLI, or `node <skills-dir>/scrapeeverything-api/scripts/se.mjs youtube.search query="home espresso" type=channel limit=20`). Otherwise `POST https://api.scrapeeverything.com/v1/<platform>/<action>` with a JSON body and `Authorization: Bearer $SCRAPEEVERYTHING_API_KEY`. Use `"cache_days": 7` on all calls.

## Method

1. **Keywords**: expand the brief into 3-5 search phrases (product category, problem solved, audience identity, in the target language).
2. **Discover** candidates (collect handle + platform + the evidence where you found them):
   - YouTube: `youtube.search` with `type: channel` gives `subscriber_count` and `handle` directly; `type: video` with `sort: popularity` surfaces creators whose videos rank for the topic.
   - Instagram: `instagram.reels_search` (`date_posted: last-month`) gives `owner_username` of reels about the keyword.
   - Pinterest: `pinterest.search` gives `pinner_username`.
   - TikTok: `tiktok.music` on a sound popular in the niche lists `videos[].author_username`; seeds' videos can also point to related creators.
   - Seeds: pull the seed's profile and posts to learn its keywords, then search with those.
3. **Deduplicate** and drop brands, media publishers and aggregator pages unless the user wants them.
4. **Screen** with one profile call each: keep only those in the follower tier, public, active (has recent posts), language/region match where visible (`region` on TikTok, bio language).
5. **Score** the remaining top ~15 with a posts call and these weights (state them in the report and let the user change them):
   - Engagement quality 35% (median ER or views/followers vs tier norm)
   - Topic fit 25% (share of recent posts on the niche, from captions/titles)
   - Consistency 15% (posts per week, no long gaps)
   - Audience match 15% (language, region, format)
   - Brand safety 10% (no red flags in recent captions)
6. **Rank** and give each a one-line rationale and a suggested next step (vet fully with the influencer-vetting skill, contact, or monitor).

## Output template

```markdown
# Creator shortlist: {campaign}
_Date: {YYYY-MM-DD} · Platforms: {list} · Tier: {tier} · Candidates found / screened / scored: {a}/{b}/{c} · Credits used: {n}_

## Scoring weights
Engagement 35 · Topic fit 25 · Consistency 15 · Audience 15 · Safety 10

## Shortlist
| Rank | Creator | Platform | Followers | Median ER / views | Posts/wk | Topic fit | Score | Why | Next step |
| ---: | --- | --- | ---: | ---: | ---: | --- | ---: | --- | --- |
| 1 | [@handle](profile link) | YouTube | 84k | 6.1% views/subs | 1.5 | 9/10 | 86 | ... | Full vet |

## Near misses
| Creator | Reason excluded |
| --- | --- |

## Discovery sources
- "{keyword}" on {platform}: {n} candidates

## Next steps
- Run influencer-vetting on the top 5 before outreach.
- Find business contact details only through each creator's public "contact" or business email field and platform tools, with consent-based outreach.
```

## Guardrails

- Only public creator accounts acting in a professional capacity; skip accounts that look like private individuals or minors.
- Do not scrape or compile personal contact data (phone numbers, home addresses, personal emails). Point to the creator's own published business channels instead.
- Rank on observable public metrics, and state the weights; do not infer sensitive attributes (ethnicity, health, religion, sexuality).
- Keep within the credit budget; stop discovery once you have about 2x the requested shortlist size.
