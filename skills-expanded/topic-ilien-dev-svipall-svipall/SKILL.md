---
name: svipall
description: Reach any web page from this machine — fetch, crawl, search, extract, drive a page, get past an anti-bot wall or a captcha, watch a page for changes. Use for ANY web access, including when a built-in WebFetch or WebSearch would otherwise be the obvious choice, and whenever a page came back blocked, empty, truncated, or as a "checking your browser" screen. The shell and the MCP tools are the same server and both are documented here.
---

# Svipall

Local-first web scraping. Every request, every browser and every captcha stays on this machine —
no API keys, no third-party solving service, nothing sent anywhere.

**Use it for every web access.** Svipall climbs a tier ladder, remembers what worked per domain, and
labels what came back; a built-in fetch has no notion of a wall, and a challenge page is a `200`.
Claude Code's `WebFetch` hands that page to a small model, which summarises it like any other.

One server, two surfaces: `svipall …` from a shell, and the MCP tools an assistant calls. The shell
costs a fraction of the tokens; the tools are the same operations under other names, and the table
near the end of this file maps one to the other. Every command prints one JSON object to stdout,
with diagnostics on stderr, so `svipall ... | jq` works.

## Start here

```bash
svipall fetch https://example.com/article
```

`mode=auto` is the default and the right answer: Svipall climbs a ladder — plain HTTP, then a browser,
then a stealth browser, then a real one, then one that waits out a challenge — stopping at the first
tier that works, and remembering it for that domain. Do not pick a tier by hand.

Identity defaults to `auto`: learned emulated routes first, at most one native fallback last.
Native exposes real device characteristics; `config set auto_native_fallback=false` prohibits that
automatic fallback. Respect `cooldown_seconds_left` and `stopped_reason`; switching modes does not
reset the persistent visit limit (12 top-level attempts/60s/domain/exit, 15-minute cooldown by
default). Browser resources and page-triggered requests are additional traffic. No route or mode
guarantees anonymity or successful delivery. `status` shows the effective policy.

`svipall doctor` answers what this installation can actually do — which browser would run, which
captcha models are compiled in, whether the dashboard port is free — and names the command that
fixes anything that is wrong. Run it once before concluding a site is the problem.

## When a page comes back blocked

The result carries `blocked_reason`, `wall_kind`, `wall_vendor`, `widgets` and a `note` saying what
to do. Read it rather than retrying: a blind retry on a wall is how a domain earns a cooldown.
`wall_vendor` names the product guarding the domain by its own endpoint, and appears on a page that
arrived too — it says who is watching, not that anything was withheld.

- The note names a captcha widget → the MCP server's `solve_and_continue` solves it in place, or a
  person finishes it at the dashboard (`svipall status` prints the URL, and it works from a phone).
- A fingerprinting wall that never yields → route the domain through a proxy:
  `svipall route add shop.example --proxy socks5://… --country DE`, or a pool it moves through as
  exits get blocked: `--proxies A,B,C --countries DE,DE,NL`. Subdomains inherit. `svipall status`
  shows each exit's health and latency per domain; `svipall route check shop.example` tests them
  (liveness, latency, DNS-leak) with no third-party service — prefer `socks5h://` over `socks5://`,
  which resolves DNS on this machine.
- `blocked_reason: "address_budget"` → nothing was requested: this address has spent its standing
  with that host and is being rested. The result says how many seconds until it has not. Route the
  domain through a proxy, wait, or `web_status(clear_budget="shop.example")` if you mean to spend it
  anyway. `svipall status` shows what every address has spent where.
- `blocked_reason: "exit_down"` → the proxy itself did not answer, so the site was never asked.
  The exit is passed over for two minutes with its standing intact. With a pool, fetch once more
  and it leaves through another exit. With a single route, bring the proxy back first. A tunnel
  declared as `[[tunnels]]` in the config comes back by itself; `svipall status` shows it.
- A login wall → `web_login` once, by hand, and the profile keeps the cookies.

## Reading a page cheaply

| Want | Command |
|---|---|
| The prose | `svipall fetch URL` |
| Only what is relevant | `svipall fetch URL --query "shipping costs"` |
| Something to click | `svipall snapshot URL` — roles, names and refs. Measured: 12 tokens on a plain page, 1 600 on a dense one (the node list is capped at 200), against 8 700 for the same page's prose |
| The site's real API | `svipall capture URL` — the JSON the page itself fetched while loading |
| What a video says | `svipall video URL --lang es` — captions and chapters as one `[m:ss]` timeline, not the description; `--frames 8` adds keyframes where the picture changes, as PNG paths in the timeline; no captions and a media file means local speech recognition once `svipall models install` has run |
| A lot of pages | `svipall crawl URL --out pages.csv` — writes a file, returns a path and a count |
| A table, as rows | `svipall fetch URL --tables --out rows.csv` — typed rows with their columns, not a markdown grid |
| A listing, as rows | `svipall fetch URL --schema auto` — reads the page's own repeated structure, names the columns for what they hold, and returns the schema it worked out in `induced_schema`. Keep that and pass it as `--schema '{…}'` next time. A page with no clear record set returns neither rather than guessing |
| A document, not a page | `svipall fetch https://x/report.docx` — docx, xlsx, pptx, odt, epub, rtf, csv and pdf read as markdown, from the web or from `file://`. A PDF of scanned pages says so in `document.scanned`, and is read page by page, like an image, once `svipall models install` has run |
| A recording, not a page | `svipall fetch https://x/episode?id=3` — an audio or video file, known by its type, comes back as what it says once `svipall models install` has run; `media` says what it was. A podcast feed read with `svipall map` gives each episode's `enclosure` and published `transcript` |
| Markup you already have | `svipall fetch raw: --stdin < page.html`, or `svipall fetch file:///…/page.html` (under `~/.svipall/in` or `local_roots`) |

`svipall capture` is the one people forget. Most sites render from an endpoint their own JavaScript
called a moment earlier, and that response is smaller, already typed and far more stable than the
HTML built from it. An endpoint that took `page=1` will take `page=2`.

## Crawling

```bash
svipall crawl https://docs.example/ --pages 50 --query "authentication"
svipall crawl https://docs.example/ --dfs            # one branch to its end: a manual, a listing
svipall crawl https://docs.example/ --since-last     # only what the sitemap says has changed
svipall crawl https://a.example/ --out rows.jsonl    # to a file, not through the context
```

A crawl returns a `crawl_id`. If it is interrupted, pass that id back and it continues from where it
stopped rather than starting over.

## Finding things

```bash
svipall search "rust async runtime" --engine all   # every engine, merged by agreement
svipall map https://example.com                    # the site's URLs, a few hundred tokens
```

## Remembering across runs

```bash
svipall notes set shop/last_id 4820
svipall notes get shop/last_id
svipall watch add https://example.com/changelog --every 3600
svipall watch add https://shop.example/item --selector ".price"   # one region; survives a redesign
svipall watch check                                # what changed since last time
svipall log --summary                              # which domains are slow or blocked, and why
svipall solver export-corpus --out ./corpus       # every captcha seen + answer, for training your own models
svipall quality ask --count 20                    # put pages in front of a person at the dashboard to rate
svipall quality export-training --out set.jsonl   # those ratings plus what the log implies, as training data
svipall quality train --in set.jsonl --out ~/.svipall/models
svipall models status                             # embedded, installed, and whether this build can read one
svipall models install                            # the release's models archive into ~/.svipall/models/
```

`svipall log --summary` is worth a look when a site starts failing: a domain that is half blocked and
slow is a domain whose learned tier is wrong.

## The same operations, as MCP tools

| You want | Call |
|---|---|
| One page as clean Markdown (PDF and office documents too) | `web_fetch` — `query=` for one fact from a long page |
| A table or a listing as rows | `web_fetch` with `tables=true`, or `schema="auto"` |
| Several known pages | `web_fetch_many` |
| A site's URLs, before deciding what to fetch | `web_map` — a few hundred tokens |
| A whole site, or many pages of one | `web_crawl` (`out_file` for anything large; `schema` or `tables` for rows) |
| To search the web | `web_search` (no API key) |
| A site's own search box | `web_site_search` |
| The API behind a listing | `web_capture` — the JSON the page itself fetched; `page=2` beats following links |
| Something to click, type or scroll | `web_snapshot` first, then `web_act` with `ref` (one shot), or `browser_open` → `browser_do` … → `browser_close` when cookies must stay alive |
| What a video says: captions and chapters as one timeline | `web_video` — a watch page, a page that embeds a player, a `<video>` or a media file; `frames=8` for keyframes |
| A picture of a page | `web_screenshot` (`mobile` for a phone); a screenshot cannot be clicked |
| To get past a login or a gate by hand, once | `web_login` — the cookies are kept |
| To send a domain through a proxy | `web_route` |
| What changed since last time | `web_diff` once, `web_watch` on a schedule |
| To remember something across sessions | `web_notes` |
| Why a domain is slow or blocked | `web_log view=summary` |
| Current state, and resets | `web_status` |

A captcha named in `blocked_reason` goes to `solve_and_continue`; the `solve_*` tools return a bare
token bound to the session that produced it, for a form you post yourself. `web_status` reports the
dashboard URL for the challenges a person has to answer. **Human verification that needs a person:
stop and say so.** Do not loop.

## From another language

```bash
svipall serve --port 8788     # one endpoint per tool; the bearer key is printed once
curl -sH "Authorization: Bearer $KEY" -H 'content-type: application/json' \
     -d '{"url":"https://example.com","query":"pricing"}' localhost:8788/v1/fetch
```

Same objects as the CLI. A blocked page is a `200` carrying `blocked_reason`; only a bad request or
a broken installation is not.

## What a page says about itself

Every delivered page carries `quality`: `full` when there is nothing to report, otherwise `partial`
(cut off) or `thin` (a husk), with `quality_reasons` naming why. A page withheld behind a
subscription comes back as `wall_kind: paywall`, and a 200 that is really a missing page as
`softnotfound` — neither is content, and no tier fixes either. `optimization: high` appears only on
the far end of pages built for a ranking. `web_fetch_many` adds `corroboration`, which says how many
of the results are actually different documents rather than one story on five hostnames.

Links in the markdown are written the way the page wrote them: a link to the page's own site is a
path (`/wiki/Web_crawler`), to be joined to that response's `url`; a link to another host is
absolute. Measured across four real pages, that is 15% of the delivered text. `include_links`
returns every link absolute when a ready-to-fetch list is what is wanted.

A field that reports an *event* is there only when the event happened: `final_url` when a redirect
moved the page, `native_fallback` when a real-device attempt was made. `identity_used` is always
present — silence is not a way to say that nothing about this machine was exposed.

**None of it ever withholds a page.** They are labels: the odd, thin, heavily-optimised page that
happens to hold the answer is returned exactly like any other, and what to do about it is yours.

## Rules worth keeping

- **Never retry a blocked URL blindly.** Read `blocked_reason` and act on it.
- **Never set the tier by hand.** `auto` learns; a fixed tier is either slower or weaker.
- **Prefer `snapshot` to prose when the next step is a click**, and `capture` to parsing HTML.
- **Send bulk results to a file.** `--out` on `fetch` and `crawl` costs a path instead of the rows.
- **Credentials never go in a command.** Put them in `~/.svipall/secrets.env` and refer to them by
  name as `${SHOP_PASSWORD}`; the value is substituted on the way to the browser and never appears
  in the transcript.
