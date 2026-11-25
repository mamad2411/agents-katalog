---
name: website-launch-impact-report
description: "Build a client-facing before/after report answering whether a website relaunch or migration helped or hurt — SEO, conversions, and UX, pre-launch vs post-launch. Use when a site was relaunched, redesigned, or migrated to new URLs and someone asks 'did the new site help or hurt', 'new-site impact', 'before/after website report', or 'launch impact report for <client>'. Not for routine monthly SEO reporting or a report unconnected to a launch/migration event."
---

# Website Launch Impact Report

A before/after report anchored on a launch date: did the new site help or hurt? You compare a pre-launch window against an equal-length post-launch window across three lenses — **SEO** (Search Console), **conversions** (analytics + call tracking), and **UX** — and you split every lens by page type (money/service pages vs. blog), because a relaunch almost always moves those two groups in opposite directions.

A capable agent already knows the obvious moves: match window lengths, split branded vs. non-branded queries, confirm old URLs 301 to new ones and new ones are indexed, isolate organic from other channels, lead with a verdict and keep tables in an appendix, and recommend a 60/90-day re-check. **Do all that.** This skill exists for what a capable agent still gets wrong by default: **which comparison to headline** (next), and **five data-integrity traps** that quietly wreck the numbers.

## Headline the comparison that isn't seasonal

For anything with seasonal demand — home services, retail, travel, tax — a plain before/after around the launch **conflates the launch with the season**. Launch in spring, measure into summer, and a pest-control site shows a big "lift" that is mostly rising demand, not the new site.

Lead with **year-over-year, per page-group**: this year's post-launch window vs. the *same calendar window last year*. That cancels the season out and is the truest measure of the launch's effect on the pages that matter — the commercial/"money" pages. Keep the before/after too (the daily chart shows launch *timing*), but label it seasonally-influenced and never let it headline a seasonal group.

> Real case: a service-area group showed **+78% impressions** before/after; **year-over-year it was +9%** — most of the "launch lift" was just the season. Clicks held up YoY (+37%), so the honest headline was "up year-over-year," with the before/after flagged as mostly seasonal.

**Corollary — when you can't run year-over-year, check which season the post-launch window lands in; off-season cuts the other way.** With no year-ago data you must lead with before/after, so look at where the post window sits on the demand calendar. A launch heading *into* the off-season (a fall launch measured through winter, against a spring/summer "before") puts the launch's numbers on the *low* side of the season — the before/after now **understates** the launch, the mirror image of the spring-launch inflation above. The signature is impressions and average position climbing while clicks barely move: that is a seasonal headwind, not a weak launch. Say plainly that clicks are seasonally suppressed and will follow when demand returns, and treat the before/after as a floor. Don't default to "rankings just need time to mature" when the calendar is the simpler explanation — check the season first.

**Corollary — YoY totals must compare equal-coverage spans; the retention horizon silently truncates the last-year side.** Search Console keeps ~16 months. Request "this full measured span vs. the same span last year" and the last-year daily series can silently *start months late* — then summing both sides compares unequal windows and overstates growth. This flipped a real shipped headline from **"+38% YoY" to −3.8%** (last year covered 134 days of a requested 241), and overstated two more reports by 40–90 points. The same truncation corrupts anything derived from the series: a per-day legend rate divided by `len(daily)` inflates last year, and a chart plotted by day-index draws the last-year line across only part of the x-axis. **The tell is `len(last_daily) << len(this_daily)` — check the row counts of the two daily series, never trust the requested date range.** Fix by restricting *both* years to the calendar span both actually cover, stating that span in the copy, and deriving the chart and per-day rates from the matched arrays:

```python
def yoy_like_for_like(gsc_yoy):
    last_daily, this_daily = gsc_yoy["last"]["daily"], gsc_yoy["this"]["daily"]
    if not last_daily:
        return None                      # no-YoY variant: render nothing, don't fake it
    cov0, cov1 = last_daily[0]["date"], last_daily[-1]["date"]   # what last year actually covers
    t0, t1 = plus_one_year(cov0), plus_one_year(cov1)            # (guard Feb 29)
    this_m = [r for r in this_daily if t0 <= r["date"] <= t1]    # same calendar span this year
    # totals, delta %, spans, and the chart all come from last_daily + this_m — nothing else
```

This generalizes to any source with finite history (GA4, call tracking, Ahrefs): any period-over-period total must be computed over the *intersection* of the two periods' actual coverage.

**Corollary — split by intent, and don't over-weight content pages.** Informational blog traffic is being eroded industry-wide (AI overviews absorbing informational clicks), so a blog-clicks decline is usually a category trend, not a launch failure. Report it as context, mark it low-priority, and put the commercial pages front and center.

**Corollary — a group's average position is query-mix-sensitive; judge rankings on the queries present in both windows.** When a relaunch expands visibility, the group's impression-weighted average position moves for reasons that have nothing to do with rankings: new pages and new queries enter the average at deep positions and drag it down, or a rewritten section earns hundreds of new well-ranking queries and pulls it up. Both directions shipped as wrong stories in draft: one site's money pages "fell from 21 to 32" (the matched pages actually included the two that improved most — the drop was new inventory entering low), and another's blog "improved 32 → 13" while its position on the queries it already ranked for had actually slipped. Never explain a group-average move by guessing ("new-page dilution") — compute the split and read it:

- **Same-query position**: impression-weighted average position restricted to the queries that appear in **both** windows. This is the honest "did rankings actually move" number — headline this one.
- **New-query footprint**: the count of queries appearing only in the post window, with their own average position. This is the expansion story — report it separately ("appears for 833 searches it never ranked for before, at ~position 16"), never blended into the rankings verdict.
- If same-query position worsened, say so plainly (post-migration re-settling is common in the first weeks — flag it and commit to the 90-day re-check); if it held while the raw average fell, the "decline" is arithmetic, not rankings.

## The five things that go wrong

### 1. The last few days of Search Console data are incomplete — and will flip your verdict
Search Console backfills for roughly **3–4 days**: the most recent days under-report and revise *upward* later. If your post-launch window ends on "yesterday," you are comparing a complete pre-launch window against a post-launch window whose tail is missing data — understating post-launch and manufacturing a false decline.

- **Probe the latest fully-settled date** before fixing the window. Query the daily series and end the post window on the last day that isn't still climbing — don't assume a fixed lag, and don't just use today minus N.
- **Label the read.** If the window necessarily includes still-settling days, say so in the report: "conservative floor, will rise" vs. "settled picture." Then **re-pull and redeploy ~4+ days after the post window closes** — that later pull is the real story, not the first one.
- This is not the same as the 60/90-day ranking-maturity re-check. This is days, not weeks, and it's about *data completeness*, not *ranking re-settling*. You need both.
- **The shorter the post window, the more this bites.** Those 3–4 settling days are noise in a three-month window but 15–20% of a three-week one — and "we just relaunched, how's it doing?" (asked days in) is both the most common request and the most fragile. Widen the window if you can; if you can't, mark the whole report preliminary and commit in writing to the re-pull.

> Real case: a first-day read showed non-branded impressions **down ~9%**; a re-pull two days later, once Search Console settled, showed them **up ~17%**. The sign flipped. Never treat the first pull as final.

### 2. If URLs changed, matching pages by their new path silently misfiles every old page
When a relaunch changes slugs (e.g. `/miami-fl-pest-control/` → `/service-areas/miami-pest-control/`, or blog posts dropping a dated segment), grouping or comparing pages by their **post-launch** path dumps every **pre-launch** URL into "other." The visible symptom is a fake finding like "service-area pages went from 6 to 1,400" — the pages existed all along under old slugs; only the classifier was wrong. It also breaks per-page matched-pair comparison (every migrated page looks brand-new).

**First discover the real money-page path — don't assume `/service-areas/`.** Dump the top-level path segments pre- and post-launch to see where the commercial pages actually live (clients have used `/locations/`, `/service-area/` singular, `/pest-control/…`); build the classifier around the *real* path or it files every money page into "other." Then build a **slug-stable page key** that maps a page to the *same* identity before and after the move, and make your group classifier recognize **both** the old and new slug forms. Match pages by that key, not by raw URL.

```python
# One shared classifier, used everywhere you group or compare pages.
# group_of(url) -> which reporting group ("service_areas" / "blog" / "other"),
#                  recognizing BOTH old root-level slugs and new /service-areas/ ones.
# page_key(url) -> a slug-stable identity so a page that changed URL at launch
#                  keeps ONE key (old and new map together), enabling matched pairs.
#
#   /service-areas/miami-pest-control/  and  /miami-fl-pest-control/  -> "sa:miami-pest-control"
#   /blog/2024/november/foo/            and  /blog/foo/               -> "blog:foo"
#
# Normalize cosmetic launch-time cleanups too, or you get false negatives:
# strip trailing/leading hyphens, and strip a prefix like /services/ if
# top-level pages moved under it. Getting this normalization right is what
# turns a false "78% of blog pages lost" into the true retention number.
```

Once pages are keyed, add the redirect + indexation audit the obvious checklist already calls for — but now it's per-matched-page (did *this* page's equity survive?), which is the question the client actually has.

**Refinements that materially change the redirect audit:**
- **Partial migrations.** Often only some page-types change slugs — the money pages move, the blog keeps its URLs. A page that kept its slug and still returns 200 is **unchanged (healthy)**, not an "old URL still live (duplicate)." Only call it a duplicate when the slug was *supposed* to change but the old URL still serves 200. Getting this wrong turned a genuinely clean migration into a false "12% clean" alarm (really ~86%).
- **Strip URL fragments before classifying.** Search Console reports in-page jump links (`/blog/foo/#section-2`) as separate "pages"; they resolve to the same page and are never a real slug change or duplicate. Strip `#…` or they flood the "problems" list with non-issues.
- **Watch for content duplication at migration.** A relaunch can silently republish pages at duplicate URLs (e.g. every post re-created at a `…-2` slug). Detect and surface it — two live copies of one article split its search signals and need consolidating.
- **A WAF can 403 your crawler and fake a total collapse.** The audit fetches live URLs; some sites block non-browser User-Agents and return 403 to a default crawler UA, which would mark **every** page "broken." Spot-test one live URL with your crawler during recon — if it 403s, send a real-browser User-Agent (+ `Accept` headers) and re-test before trusting any redirect verdict. (Also always read the broken-URL breakdown *by page group* before writing the verdict — the 404s may be all blog or all money pages, which changes the story.)
- **Follow redirect *chains* to the final destination — single-hop "clean %" lies when redirects chain.** A relaunch whose redirect rules were authored on a staging host emits two-hop chains (old URL → `something.mystagingwebsite.com/…` → live prod URL). A crawler that checks only the first hop reports a terrifying ~2% "clean" when nearly all the equity actually reaches a live 200 page. Follow every redirect to its final status and report **the share of pre-launch impressions that reach a live page**, not just single-hop-clean%. Detect staging-host intermediates explicitly and surface them as a "collapse the chain to one hop" fix — it's also a fragility risk: if the staging host disappears, every chained URL 404s at once.
- **A 429 is rate-limiting, not a 404.** Crawling hundreds of URLs fast gets you throttled; bucket 429s (and timeouts) separately from real 404s, and re-verify that any high-impression URL landing in "broken" actually returns 404 before you put it in the report.
- **Don't label `broken + redirect_home` as "404s".** A URL 301-ing to the homepage lands on a 200 — it loses equity, but it is not a 404, and lumping the two under one "N URLs are broken (404)" figure makes the report contradict its own category table (two shipped reports said "19 404s" and "6 404s" when the true 404 counts were 14 and 5). Report the two failure modes separately, or label the combined tile "misrouted," never "404."
- **Weight broken URLs by impressions, and check whether any is a GBP/ads destination.** "Only 5 URLs broke" sounded like a clean migration until the impression-weighted view showed those 5 carried **~11% of all audited pre-launch impressions** — almost all from one URL that a Google Business Profile links to (a UTM-tagged locations page). Always compute and report the *impression share* of the broken bucket, not just the URL count, and scan broken URLs for UTM parameters (`gbp`, ads campaigns): a broken marketing-destination URL is a live lead leak, not just an SEO cleanup.
- **Cap the crawl to what matters.** Old sites carry enormous thin long tails (one had ~30,000 URLs); crawling all of them is slow and buys nothing. Cap the redirect crawl to the top-N URLs by impressions and **log the coverage %** so a reader knows the tail wasn't audited — never silently truncate.
- **Reworded slugs (not just restructured) keep matched-pair retention low no matter how good your key is.** A dated `/blog/2024/…/foo-bar/` that became `/blog/complete-guide-to-foo/` can't be matched deterministically. Don't headline a low blog matched-pair number in that case — it's a *matching* gap, not lost equity. Judge the blog on its clicks and average position before/after instead.

### 3. Tracking changes at launch — it fools UX metrics *and* conversions
A relaunch re-tags the site, and new tags don't behave like the old ones. This shows up in two places.

**UX metrics.** The dangerous one jumps the moment the new site goes live and jumps **identically across every device** — engagement rate doubling, pages-per-session doubling at the exact cutover, same on mobile and desktop. That's a tagging/config change, not users suddenly loving the site. Gate **every** UX metric with a **cutover step-test**: a sustained, instant, cross-device level-shift at the launch date is excluded from the verdict and *shown as evidence of the tagging change*; a metric that moves gradually is a real change you can trust. **Run the test per-metric and per-client — never hardcode which metric is the artifact.** Which one steps varies run to run: engagement rate was the artifact for one client and trustworthy for the next, while average engaged time flipped the opposite way — and some launches step on *nothing* (all three metrics clean → say so and give the section a clean bill of health). Read the actual gate output and frame the UX section (and any UX KPI tile) around whichever metrics passed; don't reach for a default. If load-speed data (Core Web Vitals) isn't available, say you couldn't measure it — don't proxy it with a tainted metric.

**Conversions, same root cause.** A conversion event breaks (a website "click-to-call" tag that drops ~90% overnight — a tag change, not a real call collapse), a form event gets replaced by a new one, or a whole new tracking system appears at launch. Before trusting any conversion delta:
- **Pick one source of truth and one *continuous* signal across the launch.** If calls run through a call-tracking system (CallRail, CallTrackingMetrics, …), trust *its* inbound-call counts over a website click event. Sum multiple events when one conversion spans several (e.g. first-time + repeat calls). Note the same call system can surface *inside* analytics as GA4 events (`first_time_/repeat_phone_call`) — use those if they run continuously across the launch.
- **No continuous call signal? Don't manufacture one.** If analytics carries no continuous phone-call event across the launch and forms are the money metric, report forms honestly and render calls as a **note-only** card ("tracked outside analytics, not comparable here") — don't reach for a separate call-tracking pull or link to a call dashboard just to fill the gap. Match the report to the signal you actually have continuously.
- **Show the broken/replaced events as excluded artifacts**, not as results — the same "show the step, exclude it from the verdict" move as the UX gate.
- **Report conversions site-wide, not per landing-page group, for call/form businesses.** The visitor lands on a service page but calls or submits from the homepage/contact page, so per-page attribution dumps conversions into "other" and understates the money pages. Tradeoff to state plainly: site-wide conversions can't be split money-pages-vs-blog, so when the client asks specifically whether the service pages convert, lean on their SEO clicks/impressions as the page-group signal and say conversions are proven only in aggregate.

### 4. Write the client copy with zero internal-context hedging
The client never saw your analysis history, your earlier draft, or the classification bug you fixed. Phrases that reference that history read as confusing non-sequiturs. Ban them:

- ❌ "Now that we know these pages existed before…" / "these pages already existed" / "not old pages mistaken for new ones" / "contrary to what it first looked like"
- ✅ State the fact plainly: "At launch these pages moved from old URLs to the new structure, and impressions held roughly steady."

If a sentence only makes sense to someone who watched you correct a mistake, delete the framing and keep the fact.

**And never hardcode a claim the data should make.** Every number *and every judgment adjective* in the at-a-glance summary matrix must be interpolated from the computed verdicts — an audit found **four** live reports whose summary matrix contradicted their own body sections because the conversions row was fork boilerplate ("calls aren't comparable here" on a client whose calls were the strongest metric in the report; "no pre-baseline" on forms that had one). The same failure mode hits prose adjectives: "engaged time actually rose" shipped on a client whose engaged time *fell* 13%, because the sentence was hand-written and only the numbers around it were interpolated. Derive the claim from the data (`status_from_pct(...)`, f-string the direction word), or put an `assert` next to judgment prose so a re-pull that no longer supports the claim fails loudly instead of shipping a contradiction.

### 5. Report the gaps honestly instead of hiding or dressing them up
- **No pre-launch baseline?** An event that only started firing at launch (a new form-submit event) has no "before." Report it as "new, no baseline" — never as `0 → N` growth, which fakes an infinite lift. The stronger version: if the **analytics property itself** was created at launch, then *neither* conversions nor UX has a before — the whole property starts at the cutover. Report both post-only and say so; don't manufacture a before/after out of a baseline that doesn't exist.
- **Small volumes?** Single- and low-double-digit counts are "directional only, not statistically robust." Label them so; don't build a headline on ten phone clicks.
- **Pre-existing trend?** If organic was already declining (or rising) year-over-year before the launch, show that as context and say plainly the launch didn't cause it — don't let the launch take blame or credit for a trend that predates it.

## Reparameterize for each client
The report is the same shape every time; these knobs change. Establish all of them before pulling data:

| Knob | Notes |
|---|---|
| Seasonal demand? | Almost always yes for home services. → headline **year-over-year per page-group**; treat before/after as seasonally-influenced (see "Headline the comparison that isn't seasonal"). |
| Search Console property | **Probe the account's property list first — don't guess the form.** Domain (`sc-domain:…`) vs. URL-prefix (`https://…/`) changes the query and which www/protocol variants are covered. If **both** a URL-prefix and a domain property exist, prefer the **domain** property: a relaunch can shift host/protocol handling so a `https://www.…/` prefix property silently **undercounts** post-launch URLs (one client's www-prefix showed under half the domain property's post-launch clicks). |
| Analytics property ID | Or none. Analytics uses a **different auth scope/token than Search Console** — don't assume one credential covers both. Discover the property programmatically from the analytics account (its account summaries) rather than guessing; **multiple or empty properties may exist** under one account, so probe sessions pre/post on each candidate and pick the one with continuous data across the launch. |
| Brand-term regex | Splits branded from non-branded. Mind spelling variants (e.g. "defense" vs. "defence") — and **scan the actual query report for brand misspellings before trusting the split**: sort queries by clicks and read the top ~25 for anything brand-shaped. One client's two most-clicked "non-branded" queries were misspellings of the brand name (51 clicks of brand intent — more than every genuinely non-branded query combined), which silently inflated the non-branded read until the regex was widened to catch them. |
| Launch/cutover date | Threaded through every window and every sentence of copy. **Verify it against a second source** — not one spreadsheet cell; a wrong date silently truncates a window or makes a viable client look data-blocked. It also tends to live in more than one place in your tooling (e.g. a separate chart-marker constant as well as the window math); when you fork a prior build, grep for **every** copy of the date and update them together. |
| Window length + refresh cadence | Equal pre/post lengths; plan the ~4-day-later re-pull (gotcha #1) and the 60/90-day re-check. For a launch **6–15 months old**, cap the pre-window so it stays within Search Console's ~16-month horizon — otherwise the "before" silently truncates and inflates the before/after. The horizon also bites the **last-year side of the sitewide YoY** — and it eventually bites *every* client as the calendar advances, so use the equal-coverage-span YoY (corollary above) even when today's pull looks complete. |
| Did URLs migrate? | If yes → you need the slug-stable page key (gotcha #2) and the redirect/indexation audit. Note whether *all* page-types moved or only some (partial migration). If no → skip both. |
| Conversion tracking system | Which system owns conversions — CallRail, CallTrackingMetrics, GA4 events, a form tool? Map the money events (calls, forms) and **check whether tracking changed at launch** — events die/appear/break (gotcha #3). For CallRail specifically, confirm the dynamic-number swap survived the launch; a broken swap target silently misattributes calls. Report call/form conversions site-wide. |
| Geo/state filter? | Some clients scope analytics to operating states; others don't — check account-manager notes, prior audits, or the analytics property config to decide. |

## Deliverable
One **self-contained single-file HTML** page — all CSS/JS/images inline, no CDN or external fonts, charts as inline SVG (not a JS chart library). It has to render years from now with nothing to fetch.

**Make it responsive and verify it on a phone before shipping.** Clients open these on phones, and a forked desktop template routinely overflows horizontally. Three CSS traps recur in card/grid report layouts: (1) grid/flex children default to `min-width:auto` and refuse to shrink — add `min-width:0` to them so cards can narrow; (2) an inline `grid-template-columns` on a KPI row overrides your media query — collapse it to one column at narrow widths with `!important` so it beats the inline style; (3) `white-space:nowrap` verdict/label chips force card width — let them wrap at narrow widths. Wide data tables may intentionally scroll inside a horizontal-scroll container (a design choice, not a bug). **Always measure `documentElement.scrollWidth` against the viewport at ≤390px (and 320px) and confirm zero overflow before you deploy.**

Structure it as a **plain-language story first**: did it work → by how much → where the leads come from → what's next. Push methodology, matched-pair tables, and caveats into a collapsible "for those who want the detail" section at the bottom. If you use reveal-on-scroll animations, add a no-JS / ~3-second failsafe that shows all content — a client must never land on a blank section.

Three rendering details that have each shipped broken:
- **Extracting "the first sentence" with `split(". ")` truncates on abbreviations** — a matrix takeaway rendered as *"At launch these money pages moved from old URLs (e.g."* because "e.g. " contains period-space. Use `re.split(r"\.\s+(?=[A-Z])", detail)[0]` (split only before a capital) or hand-write the takeaway.
- **Truncated tables must say so.** If a "redirect issues" table shows the top 40 of 260 problems, the heading must read "260 total — top 40 by traffic shown," not just "260" over 40 rows.
- **When you fork, verify the fork actually contains the mobile CSS fixes** — measure `scrollWidth`, don't assume. One report shipped (and was even recorded as fixed) while missing all three responsive rules and overflowing 507px at a 390px viewport.

Deploy the file to the client's static host and purge the CDN/reverse-proxy cache, then verify a cache MISS on the bare URL (a 200 alone doesn't prove freshness — a proxy will serve stale). Exact host, credentials, and purge command are environment-specific — keep them in your project's own instructions (e.g. your repo's CLAUDE.md or deploy script), not here.

## This template is still converging
This pattern has been built many times, and the reused-vs-bespoke boundary is now clear. **Reusable across runs** (only top-of-file constants change): the Search Console pull, the analytics pull, the migration crawl/classify, and the chart rendering. **Bespoke every run**: the slug-aware page classifier (`group_of`/`page_key`), the conversion-event map, and all client-facing prose. It's deliberately **not** yet frozen into one config-driven codebase — each run still teaches an edge (a new property form, a WAF block, a novel migration shape, a different UX-gate outcome).

**Keep the offline stages deterministic — byte-identical rebuild is your audit tool.** The merge/render steps (`build_data` → `build_html`) must stay pure functions of the pulled JSON artifacts: re-running them must reproduce `data.json` and `index.html` byte-for-byte. That property is what lets you later prove a shipped report was never hand-edited and that every rendered number traces to data — a full-batch audit of 11 live reports leaned on exactly this. Three things silently break it or hide problems until a re-pull:
- **Sort ties resolve by hash-seed order.** Sorting a `set(pre) | set(post)` union by `(-delta, -post_clicks)` and cutting at top-20 leaves ties ordered by Python's randomized string hashing — every audited client had ties at the cutoff, so re-running the pull reshuffles which rows appear in client-facing tables. Append the page/query string as a final sort key on **every** sort that feeds a truncated list.
- **Cache the raw API pulls**, the way the redirect crawl should already cache its raw results (`migration_raw.json` + a `REUSE_CRAWL` flag). Dump raw Search Console / analytics rows to `gsc_raw.json` / `ga_raw.json` with the probed latest date, and support `REUSE_RAW=1` so the aggregate JSONs can be regenerated offline — otherwise the pull stage can never be re-run or audited without fresh (different) data.
- **Pin the window for re-pulls.** The window derives from "latest reported date," i.e. from when you run. Support a `LATEST=YYYY-MM-DD` override so a deliberate re-pull can reproduce the shipped windows.

When you build one, fork the most complete existing internal instance rather than starting fresh — then **grep the fork for the previous client's hardcoded numbers and names and purge them before you build.** Prior-run figures get baked into KPI tiles and prose and will silently ship as the new client's numbers (a hardcoded "159 pages / was ~11" carried across two clients before it was caught). Note what you reused unchanged vs. what you had to build custom. Once the edges stop surprising you, extract a config-driven template; until then, favor copying the latest instance and reparameterizing over rebuilding.

---

> Maintained by [Pesty Marketing](https://pestymarketing.com) · Browse the [full skill catalog](https://pestymarketing.com/agent-skills/).
