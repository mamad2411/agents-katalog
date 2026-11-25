---
name: web-indexation
description: "Use right after any deploy that adds or changes a public page, or when a new site or domain goes live, so Google, Bing, regional engines and AI search (ChatGPT Search, Perplexity, Copilot) discover it: \"index this\", \"reindex\", \"ping IndexNow\", \"Search Console\", \"just deployed\", \"sitemap changed\". Also one-time per-property setup and indexation status checks. Never clicks \"Request Indexing\" in Search Console, because that quota is per Google account. NOT for why an indexed page ranks poorly (`/founder-pipeline:seo-audit`, `/founder-pipeline:ai-seo`)."
---

# Indexation — get pages discovered by search engines and AI crawlers

Three submission channels. Two can be automated; the third cannot, and that asymmetry drives the whole design.

| Channel | Who does it | Why |
|---|---|---|
| **IndexNow** (Bing, Yandex, and regional engines that participate) | automatable | No quota. One bulk POST covers up to 10,000 URLs. |
| **Regional engine direct reindex** (where your market has one — see the worked example below) | automatable | Usually throttled, but not scarce. |
| **Google** Request Indexing | **a human, in a browser** | No API exists. URL Inspection is read-only; the Indexing API is officially limited to `JobPosting` and `BroadcastEvent`. |

Everything below works by hand with nothing but `curl`. That is the shipped default and it is sufficient.

### Optional: an indexation queue

At more than a handful of pages a week, hand-submission stops scaling and you will want a small queue
service in front of these channels. **This plugin does not ship one** — it is a dozen-line service on
whatever runtime you already use. If you build one, this is the shape that works:

- **State:** one row per `(url, channel)`, with a status of `pending` / `done` / `blocked`, and an
  `added` timestamp. A spreadsheet is a perfectly good backing store at this scale.
- **Row id:** hash the `channel|url` pair. This makes re-submission idempotent, which is what stops a
  queue accumulating a duplicate pile.
- **A re-open operation.** Idempotent ids are right for "don't queue the same page twice" and wrong
  for "this page changed, submit it again". You need an explicit way to clear the completion stamp
  and set a row back to `pending`. Do it through the service, not by hand-editing the store — hand
  edits are how a queue drifts out of date exactly when it matters.
- **Re-opening must not touch `added`.** Serve the human worklist oldest-first by `added`, and a
  re-opened row keeps its original position, so long-queued pages sort to the top. That is how you
  prioritise a section: re-open it, and it leads the worklist.
- **Resolve what you can without spending quota.** Before a URL reaches the human worklist, check it
  with Search Console's read-only URL Inspection. Pages that turn out to be indexed already resolve
  to `done` for free, and a re-opened section often costs zero manual quota.
- **HEAD-check every URL before pinging**, following redirects manually. IndexNow rate-limits domains
  that submit dead or redirecting URLs.
- **Batch against your runtime's subrequest budget** and drain repeatedly until the pending count
  stops falling.
- **Per-site config**, keyed on host: the Search Console property id, the IndexNow key with its
  `keyLocation` and `pathPrefix`, and the name of the regional-engine credential if you have one.
  Key on host, not path — locale subdirectories share their domain's entry.

Wherever the steps below say "enqueue", a queue is optional: if you don't run one, do the direct
submission in the same step and you have lost nothing but bookkeeping.

## Quick decision

- **New/changed page on an existing site** → "Every deploy" below.
- **Brand-new site/domain just went live** → "One-time per-property setup" first, then "Every deploy".
- **Debugging why a page isn't ranking** → check indexation status FIRST, before touching keywords or content — see "Diagnosing a ranking problem".

## Every deploy (new or materially-changed page)

**1. Collect every new/changed URL, including locale mirrors, and enqueue them if you run a queue.**

One entry per URL, carrying the URL, which site it belongs to, and a short free-text note saying what
changed. If you run no queue, this step is just the list you carry into steps 2 and 2b.

The failure mode worth designing for: **a URL that was submitted before must not be silently
re-submitted, and must be explicitly re-openable when the page genuinely changed.** Both halves
matter, and getting only the first half is how a queue quietly stops resubmitting updated pages. See
the queue shape above.

**2. Ping IndexNow directly — this is additive to any queue, not redundant.**

A queue runner hosted on a shared-IP serverless platform gets **429 from `api.indexnow.org` and
`www.bing.com/indexnow` on essentially every request**: it egresses from cloud IPs shared across that
platform's customers, and Microsoft rate-limits by source IP, so you pay for strangers' traffic.
Falling back to `yandex.com/indexnow` is a complete submission (all IndexNow participants share
submissions) but never gets an explicit Microsoft acceptance. The byte-identical payload gets **200
from a laptop on a residential connection.** So ping from your own machine too:

```bash
KEY=<this site's IndexNow key>
ENC=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1],safe=''))" "$URL")
curl -so /dev/null -w '%{http_code}\n' "https://api.indexnow.org/indexnow?url=$ENC&key=$KEY"
curl -so /dev/null -w '%{http_code}\n' "https://www.bing.com/indexnow?url=$ENC&key=$KEY"   # Bing-explicit
```

Because ChatGPT Search and Microsoft Copilot read the Bing index, this is the closest thing that
exists to "submitting a page to ChatGPT."

IndexNow keys are public by design — the protocol requires you to serve the key in plaintext at a
public URL — so they are configuration, not secrets. Store each one with its `keyLocation` and
`pathPrefix`. **A key only authorises URLs under its own directory.** If the only key you ever
published for a host sits at `/some-section/<key>.txt`, then nothing on that host outside
`/some-section/` can be pinged until you serve a root key. Publish at the root unless you have a
specific reason not to.

Bulk/whole-sitemap resubmission (up to 10,000 URLs per POST):

```bash
curl -s https://<domain>/sitemap-0.xml \
  | grep -oE '<loc>[^<]+</loc>' | sed -E 's,</?loc>,,g' | sort -u > urls.txt
jq -Rn --arg host "<domain>" --arg key "<KEY>" \
       --arg keyloc "https://<domain>/<KEY>.txt" \
       '{host:$host, key:$key, keyLocation:$keyloc, urlList:[inputs]}' urls.txt > indexnow.json
curl -s -w "%{http_code}\n" -X POST "https://api.indexnow.org/indexnow" \
     -H "Content-Type: application/json; charset=utf-8" --data @indexnow.json
```

Don't submit URLs that `noindex`/redirect/404 — IndexNow rate-limits domains that spam dead URLs. HEAD-check with redirects unfollowed before pinging, whether by hand or in a queue runner.

**2b. Regional-engine force-reindex, where your home market has one.**

Most markets are Google-only and this step is empty for them. Where a second engine holds real share,
it usually offers a direct reindex endpoint with far more generous limits than Google's.

*Worked example — Seznam, the Czech engine.* It is the clearest illustration of the shape, and of the
traps, so it is written out even if your market is elsewhere:

```bash
curl -s -X POST "https://reporter.seznam.cz/wm-api/web/document/reindex?key=$WMT_KEY&url=$ENC" \
     -H "accept: application/json"   # success = {"status":200}
```

Rate limits: 5/s, 100/min, 500/day — sleep ~0.7s between calls on a sweep. **The key is per verified
property and the key alone selects the site** — there is no domain parameter — so the wrong site's key
silently reindexes the wrong domain. That is the trap to carry to any engine with the same design:
sanity-check the key's scope before a sweep (here, `GET https://reporter.seznam.cz/wm-api/web?key=<KEY>`)
and confirm the returned URLs are the domain you meant. Hold one credential per verified property,
in your secrets store, named after the property so they cannot be confused. A domain with no verified
property on that engine simply has no path here — record it as blocked rather than retrying it.
Base URL `https://reporter.seznam.cz/wm-api`, docs at `reporter.seznam.cz/wm/web/dokumentace`.

**3. Google — never click "Request Indexing" directly.**

Google Search Console's manual quota is shared per Google **account**, not per property. A single
click on one property can return "Quota Exceeded" immediately because the account-wide daily budget
was already spent elsewhere. Every property under the same account draws from the same budget, so one
site clicking freely starves every other site you own. This is observed behaviour, and it is the
reason for the worklist discipline below.

So: step 1 records that the page needs a Google click, and that is your part done. The click itself is
served as a **worklist**, worked oldest-first by whoever runs the browser pass. They stop the moment
"Quota Exceeded" appears — retrying wastes the run — and mark the pages they got through as done.
Never bypass the worklist with a direct click "just this once": that is the exact behaviour the
worklist exists to prevent. If you run no queue, the worklist is a plain list you keep by hand; the
discipline is what matters, not the tooling.

**4. Confirm discoverability plumbing.**

- URL is present in the site's auto-generated sitemap.
- If it's a key/money page (not every blog post), add it to `llms.txt` / `llms-full.txt` — an agent-tooling surface (coding agents, MCP), not a search-citation lever. See `${CLAUDE_PLUGIN_ROOT}/skills/ai-seo-llms-builder/references/evidence.md`.
- `robots.txt` allows the new path for every bot that matters. Keep one canonical `robots.txt` template per site rather than re-deriving the bot list per page. In short: Tier 1 classic search + Tier 2 AI *retrieval* bots (`OAI-SearchBot`, `ChatGPT-User`, `Claude-SearchBot`, `Claude-User`, `PerplexityBot`, etc.) must be allowed — those are what actually produce citations. `CCBot` and the other Tier 3 *training* bots are allowed by default too. A blocked crawler means the page is invisible to that engine no matter what else you do.

**5. AI search engines have no submit button — you earn presence, not push it.**

There's no equivalent of Request Indexing for ChatGPT/Perplexity/Claude/AI Overviews. The levers, in order of impact: crawler-allow (above) → the Bing index via IndexNow (step 2), the strongest first-party-adjacent lever available, because the large majority of ChatGPT and Copilot citations match Bing's top organic results [operating assumption] → inbound citations (business-profile products, directories, guest mentions — real backlinks, not requests; register-once directory/registry presence is owned by **`/founder-pipeline:web-listings`**) → internal interlinking so the page isn't an orphan → `llms.txt` listing, last — it's agent-tooling, not a citation lever (`${CLAUDE_PLUGIN_ROOT}/skills/ai-seo-llms-builder/references/evidence.md`). Baseline-probe the target phrasing in ChatGPT/Perplexity/Claude the day it ships, log absence, recheck at 2 and 6 weeks — AI citation lags the crawl, don't panic on week 0.

## Territory notes — where a locale needs a different submission path

Before adding a locale, answer one question: **does this market have a second engine you can submit
to, or is it Google-only?** Most are Google-only. Getting this wrong costs a week of looking for a
registry that does not exist.

*Worked example — Poland.* Google runs the overwhelming majority of Polish search, and Poland is a
single-engine market with no equivalent of Seznam, Yandex or Naver. The names that appear on legacy
"Polish search engines" lists are portals, **not crawlers you can submit to** — they matter as
*content and link* sources, which is `/founder-pipeline:web-listings` territory, not this skill's. So
a `/pl/` locale needs exactly what every other locale needs and nothing extra:

1. the URLs submitted as usual (IndexNow covers Bing → and therefore ChatGPT Search and Copilot),
2. the direct IndexNow ping from your own machine, since a hosted runner's pings get 429'd,
3. `hreflang` for the locale + `x-default` wired both ways, and the locale URLs present in the sitemap,
4. the existing Search Console property — a locale **subdirectory** inherits the domain property, so
   **no new property, no new verification, no new IndexNow key** (the root key already authorises
   `/<locale>/*`).

Your per-site config needs no new entry for a subdirectory locale either. Adding one would be the
error — submission keys on host, not path.

The same logic covers the case where a regional engine exists but has no verified property for the
locale in question, or is a single-country engine being asked to cover a neighbouring one: those URLs
simply resolve through IndexNow and Google, and you record the regional channel as blocked rather
than retrying it.

**Intent check before you spend indexation effort on a locale** (this is why the note lives here):
a page indexed against a mismatched SERP still converts nothing. A head term can carry real volume in
a locale and still return an SERP from an adjacent industry — the same word meaning corporate
training in one market and secondary education in another — in which case ranking for it buys you
nothing. What tends to work instead in a market you have no foothold in is **role-definition**
content in the local language, where a single local blogger often holds #1 and foreign-language pages
survive only in the bottom half of page one. Translate the definitional cluster into those locales;
leave the service pages in your primary language. Check the actual SERP for each target term in each
locale before committing.

## One-time per-property setup (brand-new site/domain)

Do this once when a new domain launches, before the "every deploy" loop applies to it:

1. **Generate an IndexNow key** and host it at the site root:
   ```bash
   KEY=$(openssl rand -hex 16)
   printf '%s' "$KEY" > public/$KEY.txt   # served verbatim at the root by most static hosts
   ```
   Verify `https://<domain>/<KEY>.txt` returns the key. Commit it to the repo so future deploys keep ownership valid. Put it at the **root**, not in a subdirectory — a key only authorises its own directory and below.
2. **Bing Webmaster Tools** (`bing.com/webmasters`): verify the site (importing from Google Search Console is fastest) and manually submit the sitemap — the GSC import does **not** carry the sitemap over.
3. **Google Search Console**: verify the property, submit the sitemap, re-fetch `robots.txt` to confirm Google has the latest version.
4. **Your regional engine's webmaster tools, if your market has one.** *Worked example — Seznam
   Webmaster* (`reporter.seznam.cz/wm`): add the site → verify via meta-tag / DNS-TXT / file. Four
   traps here generalise to most regional engines:
   - **Verification is login-gated.** A browser-automation tab does NOT share your logged-in session,
     so this needs a real human login and cannot be scripted end-to-end.
   - **Meta-tag gotcha:** the verification `<meta>` must be in EVERY layout's `<head>`, including any
     separate landing-page layout, or root-URL verification fails.
   - **Register the ROOT domain, not a locale subpath** — the root covers all of that locale's pages
     via the sitemap.
   - **Sitemap discovery may be passive.** Seznam has no sitemap-submission endpoint at all; it
     auto-discovers via the `Sitemap:` line in `robots.txt`. Check before assuming a submit button.

   Subpath-on-someone-else's-root wrinkle: if the site lives at `<root>/app-name` under a hosted site
   builder you do not control, the crawler-authoritative `robots.txt` is the ROOT's — add your
   `Sitemap:` line there, and serve the verification file at the root path via a proxy route. Once
   verified, generate the property's API key from the engine's own console and store it in your
   secrets store.
5. **Register the domain in your per-site config** — if you run a queue, submission will reject an
   unknown host until you do, and nothing else in this skill applies to it:
   - The Search Console property id (the `sc-domain:` or `https://` resource id from the property picker).
   - The IndexNow `key`, `keyLocation` and `pathPrefix` from step 1.
   - A reference to the regional-engine credential from step 4, or none if no such property is verified.
   - Push the regional-engine credential into your runtime's secrets store, and keep a copy in your
     own environment under the same name for manual use.
   - For the read-only URL Inspection check: create a service account, and in Search Console →
     Settings → Users and permissions add it with **Full** access. There is no CLI equivalent; this
     step is manual, per property.

## Diagnosing a ranking problem

Before blaming keywords, content, or backlinks for a page that "isn't ranking," check whether it's even indexed. Money pages can sit unindexed for **weeks** on a new or cutover domain — this has directly explained a "why isn't this ranking" investigation before, where the page still reported "URL is not on Google" nine days after a domain cutover. Run Search Console URL Inspection on the page first. If it's not indexed, that's the whole answer — fix indexation (this skill), don't start tuning content.

## Definition of done (per deploy)

- [ ] Every new/changed URL (+ locale mirrors) submitted, and the response checked — either newly queued, or an already-queued result consciously accepted, or the Google entry explicitly re-opened
- [ ] IndexNow pinged directly as well (generic + Bing-explicit), since a hosted runner's pings get 429'd
- [ ] URL confirmed present in the sitemap
- [ ] Key pages added to `llms.txt`/`llms-full.txt`
- [ ] `robots.txt` confirmed not blocking AI/search crawlers on the new path
- [ ] Nobody clicked "Request Indexing" in Search Console outside the worklist
