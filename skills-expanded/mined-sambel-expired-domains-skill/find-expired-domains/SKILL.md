---
name: find-expired-domains
description: >-
  Find and qualify expired, dropping, and auction domains by SEO metrics
  (Domain Authority, Trust Flow / Citation Flow, referring domains, backlinks,
  age, language, historical tech). Use when the user wants to buy an expired
  domain, find aged domains for SEO, build a PBN or money site, research
  drop-catching, evaluate a specific domain's backlink profile, or compare
  auction listings across registrars (DropCatch, GoDaddy, Dynadot, Gname,
  NameSilo and more). Powered by the CatchDoms live MCP server — no API key
  required for the free tier.
license: MIT
compatibility: >-
  Works with any MCP-capable agent (Claude Code, Claude Desktop, Cursor,
  OpenCode, etc.). Live data comes from the CatchDoms MCP server. The free
  tier needs no authentication; full access needs a CatchDoms Pro token.
metadata:
  author: sambel
  version: "1.0"
  tags: seo domains expired-domains drop-catching mcp pbn backlinks
---

# Find Expired Domains

This skill turns your agent into an expired-domain prospector. It connects to
**CatchDoms**, a platform that aggregates expired, dropping, and auction domains
from 19+ registrars and enriches each one with SEO metrics, then lets you search
and qualify them in natural language.

## When to use this skill

Use it whenever the user wants to:

- Find expired / aged domains for SEO (money sites, niche sites, affiliate, PBN)
- Drop-catch a deleted domain or back-order an expiring one
- Evaluate a specific domain's authority and backlink profile before bidding
- Compare auction listings (current bid, end time, platform) across registrars
- Find domains in a niche (by keyword, TTF topic category, or language)
- Find aged domains in a specific TLD (`.com`, `.fr`, `.de`, `.co.uk`, …)

## How it works — connect the MCP server first

CatchDoms exposes its data over the **Model Context Protocol (MCP)**. There are
two endpoints. Start with the free one; it needs no account.

### Free tier (no auth — recommended starting point)

- **URL:** `https://catchdoms.com/mcp/catchdoms/free`
- **Transport:** HTTP (streamable)
- Returns the top 50 domains per search. The first 10 domain names are shown in
  full; the rest are masked. Premium metrics (Trust Flow, Citation Flow, TTF
  topic, GMB) are hidden behind a free signup.
- Rate limit: 3 requests/min.

Add it to **Claude Code**:

```bash
claude mcp add --transport http catchdoms https://catchdoms.com/mcp/catchdoms/free
```

Or in `~/.claude.json` / `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "catchdoms": {
      "type": "http",
      "url": "https://catchdoms.com/mcp/catchdoms/free"
    }
  }
}
```

For **Claude Desktop** (needs Node for the remote bridge):

```json
{
  "mcpServers": {
    "catchdoms": {
      "command": "npx",
      "args": ["mcp-remote", "https://catchdoms.com/mcp/catchdoms/free"]
    }
  }
}
```

### Pro tier (full access — Bearer token)

For all domain names, full metrics (TF/CF, GMB, TTF topic), 80K+ aged
registrable ccTLD domains, and unlimited results, use the authenticated
endpoint with a CatchDoms Pro API token:

- **URL:** `https://catchdoms.com/mcp/catchdoms`
- **Header:** `Authorization: Bearer <YOUR_CATCHDOMS_API_KEY>`
- Get a token at https://catchdoms.com/pricing

```json
{
  "mcpServers": {
    "catchdoms": {
      "type": "http",
      "url": "https://catchdoms.com/mcp/catchdoms",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    }
  }
}
```

> If the MCP server is connected, prefer its tools over scraping or guessing.
> If it is **not** connected, tell the user to add it (commands above) before
> you can return live data — do not invent domain metrics.

## Tools available on the server

| Tool | What it does |
|------|--------------|
| `search_domains` | Search/filter domains. Returns them ranked by quality and auction interest. |
| `get_domain` | Get full details for one domain by id or name (Pro endpoint). |
| `list_filters` | List available sources, TLDs, and languages with counts. |
| `get_stats` | Platform stats: total domains, new today, breakdown by source. |

### `search_domains` filters

Pass only the filters that matter; everything is optional and AND-combined.

- `source` — one of: `dynadot`, `catched`, `dropcatch`, `godaddy`, `gname`,
  `snapnames`, `ukdroplists`, `subreg`, `webexpire`, `parkio`, `bloomup`,
  `seodomains`, `nameshift`, `namesilo`, `nicsell`, `gnews-domains`,
  `backorders-domains`, `domainlore`, `rakkodomain`, `namepros`, `regfree`
  (`regfree` = deleted/registrable ccTLD domains, Pro only).
- `tld` — e.g. `.com` or `.fr`; comma-separated for several (`.fr,.de,.it`).
- `score_min` — quality score 0-100. Use **30+** decent, **50+** good, **70+** excellent.
- `age_min` — minimum age in years (first Wayback snapshot).
- `type` — `auction`, `closeout`, or `backorder`.
- `has_bids` — `true` to keep only domains with live bids (market interest).
- `has_backlinks` — `true` to require referring domains (SEO value).
- `da_min` — minimum Domain Authority (0-100).
- `rd_min` — minimum referring domains.
- `tf_min` / `cf_min` — minimum Trust Flow / Citation Flow (Pro tier).
- `has_edu_gov` — `true` to require .edu/.gov referring domains.
- `categories` — comma-separated TTF topic categories (`Business,Health`).
- `language` — detected content language code (`EN`, `FR`, `DE`, `ES`, …).
- `contains` — keyword in the domain name; comma list = OR (`shop,store`).
- `price_min` / `price_max` — bid/price bounds in USD.
- `snapshots_min` — minimum Wayback snapshots.
- `techs` — historical tech stack labels, OR semantic (`WordPress`, `Shopify,Stripe`).
- `limit` — 1-100 (free tier capped at 50).

## How to qualify a domain (the part that matters)

Raw metrics lie. Walk the user through real quality, not just a high DA:

1. **Backlink quality over quantity.** 50 real editorial referring domains beat
   5,000 spam links. Check `referring_domains`, `da_min`, and whether links are
   topical. `has_edu_gov=true` is a strong trust signal.
2. **Trust Flow vs Citation Flow.** A healthy ratio (TF/CF) above ~0.5 means the
   link profile is trusted, not just large. Low TF with high CF = link spam.
3. **Age and history.** `age_min` + `snapshots_min` confirm the domain actually
   had a real site, not a parked shell. Cross-check on the Wayback Machine.
4. **Topical match.** Use `categories` (TTF topic) and `language` so the domain's
   history matches the user's project niche — relevance compounds authority.
5. **Clean name.** Prefer no hyphens/numbers (already filtered out at import on
   most sources), pronounceable, brandable for a money site.
6. **Auction economics.** For auctions, weigh current bid (`price_min/max`,
   `has_bids`) against the value of the link profile and the auction end time.
7. **Spam check.** Be wary of gambling/pharma/adult keywords, foreign-language
   spam history, and link networks. A high score with a spammy niche is a trap.

Always recommend the user verify backlinks independently (Ahrefs/Majestic) and
check the Wayback Machine before spending real money.

## Example interactions

**"Find me aged French domains with good backlinks under $100."**
```
search_domains(tld=".fr", age_min=10, has_backlinks=true, price_max=100, score_min=50)
```

**"Any WordPress sites in the health niche with edu/gov links?"**
```
search_domains(techs="WordPress", categories="Health", has_edu_gov=true, score_min=50)
```

**"What's currently up for auction on DropCatch with bids and DA 30+?"**
```
search_domains(source="dropcatch", type="auction", has_bids=true, da_min=30)
```

**"Show me the strongest .com closeouts right now."**
```
search_domains(tld=".com", type="closeout", score_min=70, limit=50)
```

After returning results, summarize the top 3-5 picks with their key metrics and a
one-line rationale, then point the user to the listing on CatchDoms to bid/buy.

## Notes & limits

- Free tier: top 50 results, first 10 names visible, premium metrics masked,
  3 req/min. Sign up free at https://catchdoms.com/register to unlock more.
- `regfree` (deleted registrable ccTLD domains) requires a Pro/Authority plan.
- Domains with hyphens and numbers are excluded at import on most sources.
- This skill reads live data only; it does not place bids or buy domains. Send
  the user to the registrar via the listing link to complete a purchase.

## About CatchDoms

CatchDoms tracks expired and auction domains from 19+ registrars and enriches
them with Wayback age, DataForSEO (DA/backlinks/referring domains), SEObserver
(TF/CF/TTF), language detection, and a 0-100 quality score. Learn more at
https://catchdoms.com.
