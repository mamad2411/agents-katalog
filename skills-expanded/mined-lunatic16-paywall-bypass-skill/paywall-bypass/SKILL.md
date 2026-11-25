---
name: paywall-bypass
description: Identify paywall types and generate bypass strategies for web scraping and content extraction. Covers 500+ news sites, major paywall providers (Piano, TinyPass, Poool, etc.), and extraction techniques (bot spoofing, AMP, JSON-LD, archive fetching).
version: 1.0.0
author: Extracted from Bypass Paywalls Clean (magnolia1234)
date: 2026-04-04
---

# Paywall Bypass Helper

Identify paywall provider types and generate bypass strategies for web scraping, content extraction, and research across 500+ news sites.

## Use this skill when

- The user asks to "bypass paywall", "extract article content", or "get full text" from a paywalled URL
- The user needs to scrape or research content from news sites with subscription walls
- The user asks what paywall technology a specific site uses
- The user needs to write scripts that handle paywalled content programmatically
- The user asks about cookie behavior that triggers or avoids paywalls

## Do not use this skill when

- The task involves cracking DRM, decrypting encrypted content, or circumventing hard encryption
- The user requests illegal access to credentials or personal data
- The target is a non-paywall access control (login-only portals, intranets)
- The user wants to distribute full paywalled content commercially

## How paywalls work

Paywalls generally work through one of these mechanisms:

1. **Metered paywalls** — track article views via cookies/localStorage; after N free articles, block access
2. **Hard paywalls** — content is loaded but hidden behind CSS/JS overlay; blocking the JS reveals text
3. **Server-side paywalls** — content is not sent to the browser; requires external fetching (archive, cache, bot UA)
4. **Hybrid paywalls** — combination of client-side blocking + server-side checks

## Paywall provider identification

To identify which paywall provider a site uses, inspect the page source for these signatures:

| Provider | Detection Script/Pattern | Sites Using |
|----------|------------------------|-------------|
| **Piano.io** | `.piano.io/`, `.piano.io/xbuilder/` | Foreign Policy, DN.no, Funke, Vocento, Berlingske |
| **TinyPass (Piano)** | `.tinypass.com/`, `js.tinypass.com` | Chicago Sun-Times, Fortune, Adweek, Corriere.it, Digiday |
| **Poool.fr** | `.poool.fr/` | Alternatives Economiques, Challenges, Elle.fr, Le Télégramme, GCF group |
| **Sophi.io** | `.sophi.io/` | Adweek, Automobilwoche, Business Insider, Crain Comm |
| **Evolok** | `.evolok.net/` | El País, Vocento group, Leaky Paywall |
| **Qiota** | `.qiota.com/` | AutoPlus.fr, Cosmopolitan.fr, Nice-Matin group, Rossel group |
| **Pelcro** | `js.pelcro.com/` | Domani, Foreign Affairs, Crain Comm |
| **Cxense** | `.cxense.com/` | Barron's, Business Insider JP, IPM group |
| **Blueconic** | `.blueconic.net/` | Bridge Tower Media |
| **Memberstack** | `[data-memberstack-app]` | Various SaaS-gated sites |
| **Steady** | `steadyhq.com/` | American Purpose, some Ghost sites |
| **Leaky Paywall** | `/leaky-paywall/` | WordPress sites with Leaky plugin |
| **Wallkit** | `wallkit.net` | WordPress subscription sites |
| **AMP Access** | `.ampproject.org/v0/amp-access-`, `.ampproject.org/v0/amp-subscriptions-` | Many sites with AMP versions |

For a complete list of patterns, see `references/paywall-patterns.md`.

## Bypass technique decision tree

### Step 1: Identify the paywall type

```
Check page source for:
  1. Scripts matching known paywall providers (table above)
  2. Cookie names (TDNotesRead, TID_ID, ra, blaize_session, etc.)
  3. AMP version availability (<link rel="amphtml">)
  4. JSON-LD article data (script[type="application/ld+json"])
  5. CSS class patterns (paywall, overlay, modal, gated)
```

### Step 2: Choose bypass technique

| Technique | When to use | How |
|-----------|-------------|-----|
| **Block paywall script** | Script-based paywall (TinyPass, Piano, Poool, etc.) | Block the script URL; content loads but paywall overlay doesn't trigger |
| **Clear cookies** | Metered paywall tracking views | Remove tracking cookies; localStorage.clear() + sessionStorage.clear() |
| **Bot UA spoofing** | Server serves full content to crawlers | Set `User-Agent` to Googlebot/Bingbot; add `Referer: https://www.google.com/` |
| **AMP page** | Site has AMP version with relaxed paywall | Navigate to AMP URL or unhide content blocked by `amp-access`/`amp-subscriptions` |
| **JSON-LD extraction** | Article body in structured data | Parse `script[type="application/ld+json"]` for `articleBody` key |
| **Archive fetch** | Server-side paywall, no client-side text | Fetch article from archive.is or Google cache |
| **Next.js data** | Sites using Next.js SSR | Extract from `script#__NEXT_DATA__` |
| **External link** | No bypass possible client-side | Generate link to archive.is or Google Search Tool for manual fetch |

### Step 3: Implement bypass

For each technique, see `references/content-extraction.md` for implementation details including code patterns, selectors, and fallback strategies.

## Cookie management per provider

Different paywall providers use different cookies to track access:

| Provider | Tracking Cookie(s) | Action |
|----------|-------------------|--------|
| Piano (general) | None specific | Block script, no cookie action needed |
| TinyPass (Piano) | `xbc` (HBR) | Drop specific cookie |
| DPG Media (NL) | `TID_ID` | Drop this cookie to reset meter |
| Haaretz Group | `ra` | Drop this cookie |
| Adweek/Zephr | `blaize_session` | Drop this cookie |
| Pitchfork | `pay_ent_msmp` | Drop this cookie |
| Business Standard | `userUid` | Drop this cookie |
| eNotes | `ENOTESID` | Drop this cookie |
| DN Media (no) | `AnonUserCookie` | Drop this cookie |

**Important**: Some sites require cookies to be *preserved* (e.g., authentication-based bypass). Check `references/cookie-rules.md` for per-site rules.

## Common media groups

Many news sites share paywall infrastructure. Identifying the media group simplifies bypass:

| Group | Key Sites | Paywall Type |
|-------|-----------|-------------|
| **News Corp Australia** | theaustralian.com.au, heraldsun.com.au, dailytelegraph.com.au | AMP subscriptions + hard paywall |
| **McClatchy (USA)** | bnd.com, miamiherald.com, sacbee.com, kansascity.com | Piano + Googlebot |
| **Gannett** | azcentral.com, freep.com, indystar.com | Googlebot UA |
| **Hearst (USA)** | houstonchronicle.com, sfchronicle.com, statesman.com | Custom script blocking |
| **Lee Enterprises** | townnews.com-based sites | TownNews/Leaky paywall |
| **Vocento (ES)** | abc.es, elmundo.es (not), larioja.com, ideal.es | Evolok + AMP access |
| **GEDI (IT)** | repubblica.it, lastampa.it, huffingtonpost.it | Piano + Googlebot |
| **DPG Media (NL)** | volkskrant.nl, trouw.nl, demorgen.be | Custom temptation.js |
| **Groupe Rossel (FR/BE)** | lavoixdunord.fr, lesoir.be, sudinfo.be | Qiota |
| **Funke (DE)** | abendblatt.de, morgenpost.de, waz.de | Piano |
| **Crain Comm (USA)** | adage.com, autonews.com, chicagobusiness.com | Pelcro + Sophi |
| **DN Media (NO)** | dn.no, rechargenews.com, upstreamonline.com | Custom + fetch from archive |
| **Conde Nast (USA)** | newyorker.com, vogue.com, wired.com, gq.com | Custom + script blocking |
| **Advance Local (USA)** | nj.com, mlive.com, cleveland.com, al.com | Sophi + DOMPurify |

## Implementation guidelines

### When writing a scraper/bypass script

1. **Always inspect first** — check page source for paywall scripts before attempting bypass
2. **Start with the least invasive technique** — cookie clear > script block > UA spoof > external fetch
3. **Handle JavaScript-rendered content** — many modern sites use React/Next.js; use Puppeteer/Playwright if needed
4. **Respect rate limits** — do not hammer servers with requests; add delays between fetches
5. **Use headless browsers for JS-rendered paywalls** — some paywalls only trigger after JS execution
6. **Validate output** — verify extracted text is complete, not truncated teaser content

### When analyzing a new/unlisted site

1. Check for AMP version: `<link rel="amphtml" href="...">`
2. Search for paywall scripts: `.piano.`, `.tinypass.`, `.poool.`, `.sophi.`, `.evolok.`, `.qiota.`
3. Check localStorage keys for meter tracking
4. Try Googlebot UA: `Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)`
5. Check for JSON-LD: `script[type="application/ld+json"]` with `articleBody`
6. Try archive.is as fallback

## References

- `references/paywall-patterns.md` — Complete regex patterns for all paywall providers
- `references/content-extraction.md` — JSON-LD, AMP, archive.is, Next.js extraction methods
- `references/cookie-rules.md` — Per-site cookie management rules

## Examples

- `examples/identify-paywall.md` — Walkthrough for detecting paywall type from HTML source
- `examples/bypass-strategy.md` — Step-by-step bypass recipe for a specific site
