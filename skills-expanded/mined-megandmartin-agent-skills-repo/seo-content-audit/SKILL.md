---
name: seo-content-audit
description: Audit a single web page for SEO — title/meta, heading structure, search-intent match, internal links — and deliver quick wins ranked by effort vs impact. Use when the user says "audit this page", "why doesn't this page rank", "SEO check", "review my landing page for search", or pastes a URL asking how to improve its traffic. Don't use for tearing down a competitor's product and pricing — that's competitor-teardown — or for monitoring topic trends weekly — that's trend-radar.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Research & Analysis, SEO, Content, Marketing]
    related_skills: [competitor-teardown, trend-radar]
    requires_toolsets: [web]
---

# SEO Content Audit

Audits one page against the fundamentals that actually move rankings for small sites: does the title/meta match a real search intent, is the heading structure coherent, does the content deliver what the searcher wanted, and is the page wired into the rest of the site? Output is a ranked quick-win list — effort vs impact — not a 40-point checklist dump. The standard: every finding cites what was actually fetched from the page, and no traffic or ranking numbers are ever invented.

## When to Use

- User gives a URL and wants to know why it under-performs in search or how to improve it.
- Pre-publish check on a new landing page or blog post.
- Comparing the user's page against the pages that currently rank for the target query.
- **Not for:** competitor product/pricing analysis (`competitor-teardown`); recurring topic monitoring (`trend-radar`).

## Quick Reference

| Action | Command / Call |
|---|---|
| Fetch page | `curl -sL -A "Mozilla/5.0" "$URL" -o /tmp/page.html` (or `web_extract` if curl is blocked) |
| Parse structure | python heredoc, step 3 — title, meta description, H1–H3 outline, link counts, word count |
| Intent check | search the target query; note what page types rank (guides? tools? product pages?) |
| Status/redirects | `curl -s -o /dev/null -w "%{http_code} %{url_effective}\n" -L "$URL"` |
| Internal links | from the parse: same-domain hrefs in body; orphan check = does anything link TO this page |

## Procedure

1. **Precheck** — confirm web access and get: the URL, the target query/intent ("what search should this page win?"), and site context (other pages that could link to it). No target query? Derive one from the title with the user's confirmation — auditing without a target is guesswork.
2. **Fetch** — `curl -sL -A "Mozilla/5.0" "$URL" -o /tmp/page.html` and record the final status code and URL. A redirect chain or non-200 is finding #1 before anything else.
3. **Parse structure** — expect title, meta, heading outline, and link/word counts:
   ```bash
   python3 - /tmp/page.html "$URL" <<'PY'
   import re, sys
   from urllib.parse import urlparse
   html = open(sys.argv[1], encoding='utf-8', errors='ignore').read()
   host = urlparse(sys.argv[2]).netloc
   g = lambda p: re.findall(p, html, re.I | re.S)
   title = g(r'<title[^>]*>(.*?)</title>')
   meta = g(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']')
   print("TITLE:", title[0].strip() if title else "MISSING", f"({len(title[0].strip()) if title else 0} chars)")
   print("META:", (meta[0][:160] if meta else "MISSING"))
   for lvl, txt in g(r'<h([1-3])[^>]*>(.*?)</h\1>'):
       print(f"H{lvl}: {re.sub('<[^>]+>', '', txt).strip()[:80]}")
   hrefs = g(r'href=["\'](.*?)["\']')
   internal = [h for h in hrefs if h.startswith('/') or host in h]
   print(f"links: {len(internal)} internal / {len(hrefs)-len(internal)} other")
   print("words:", len(re.sub(r'<script.*?</script>|<style.*?</style>|<[^>]+>', ' ', html, flags=re.S).split()))
   PY
   ```
4. **Intent match** — search the target query and note the top results' page *types* and angles. Compare: does the user's page match the intent the results reveal (how-to vs comparison vs product)? A perfectly optimized page against the wrong intent loses.
5. **Content and structure findings** — score against: exactly one H1 that contains the query's core concept; title 30–60 chars, front-loaded, distinct from H1 acceptable; meta 70–155 chars with a reason to click; logical H2/H3 outline that answers the intent's sub-questions; word count in the ballpark of what ranks (from step 4 — observed, not a magic number).
6. **Internal linking** — from the parse: does the body link to related pages, and (ask the user or check the site's hub pages) does anything link to this page? Orphan pages don't rank.
7. **Deliver** — rank every finding into the quick-wins table by effort (S/M/L) and impact (high/med/low), highest impact-per-effort first. Impact ratings are judgment — label them as such, never as predictions of specific traffic.

## Output Template

```
# SEO Audit — <url> — <date>
Target query: "<query>" | HTTP: <code> | Intent type observed in results: <type>

## Snapshot
Title (<n> chars): "<...>" | Meta (<n> chars): "<...>" | H1s: <n> | Words: <n>
Internal links out: <n> | Known links in: <n or "unknown — check">

## Findings
1. <finding — what the page shows vs what the intent needs — evidence from fetch/search>

## Quick wins (do in this order)
| # | Fix | Effort | Impact (judgment) | Why |
|---|---|---|---|---|

## Not worth doing now
- <common advice that doesn't apply here, and why>
```

## Pitfalls

- **JS-rendered page returns an empty shell** — curl gets 200 but the parse shows no headings and ~0 words. Recovery: retry with `web_extract` (renders more), and note that search engines may see the shell too — that itself becomes a high-impact finding.
- **Auditing against the wrong intent** — page optimized for "best X tools" when the user's page is a product page. Recovery: step 4 is mandatory before scoring; if intent mismatches, the #1 quick win is repositioning or retargeting the query, not tweaking metas.
- **Inventing traffic/ranking numbers** — "this fix will add 40% traffic". Recovery: impact column is explicitly labeled judgment; real numbers only if the user provides Search Console data, cited as such.
- **Checklist dumping** — 30 findings, no priorities, user does nothing. Recovery: cap quick wins at 7, ranked by impact-per-effort; everything else goes to "Not worth doing now" with a reason.
- **Regex parse misses exotic markup** — attributes ordered unusually, single quotes, uppercase tags. Recovery: the parse patterns are case-insensitive, but spot-check the raw HTML (`grep -io '<h1' /tmp/page.html | wc -l`) whenever a MISSING result looks implausible.

## Verification

- [ ] Findings reference actual fetched content (title/meta/headings quoted)
- [ ] Intent check performed against live results, page type recorded
- [ ] Quick wins ≤7, each with effort + impact + why
- [ ] No invented traffic, ranking, or volume numbers anywhere
- [ ] HTTP status and redirect chain reported
