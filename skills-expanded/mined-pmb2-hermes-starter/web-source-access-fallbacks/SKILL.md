---
name: web-source-access-fallbacks
description: >-
  Use when sweeps hit bot-blocked sources: fallback ladders.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [web-access, search, captcha, playwright, duckduckgo, bing, federal-register, cron, sweeps, fallbacks]
    triggers:
      - search blocked
      - captcha
      - duckduckgo
      - bing challenge
      - federal register api
      - bot-blocked
      - source unreachable
      - registry lookup
    related_skills: [hermes-legal-watchdog, cron-watchdog, recurring-status-checks, web-scraping-scrapling]
---

# Web Source Access Fallbacks

Reaching web sources (search engines, .gov registries, JSON APIs) from automated
cron sweeps when the obvious path is bot-blocked. Applies to the legal watchdog,
reputation monitor, C2C hunting, bizdev, and any other recurring sweep on this
Windows host.

## Core Principle

**Access is per-session and per-fingerprint.** `curl`, the CDP browser, and the
Playwright MCP browser each carry different TLS/HTTP fingerprints and bot-detection
state. A source blocked for one backend can be wide open for another — in the SAME
session, minutes apart. Never conclude "source X is unreachable" until every
backend has been tried, and never harden a single-session block into a durable rule.

## The Backend Ladder

1. **`terminal` curl to structured JSON APIs first** (e.g. Federal Register API).
   Fastest, most reliable, no browser needed. See FR pattern below.
2. **Playwright MCP browser** (`mcp__playwright_mcp__browser_navigate`) — independent
   backend, unaffected by Chrome profile locks and CDP WebSocket death. Most
   consistent general web path in cron sessions.
3. **CDP browser / built-in `browser_navigate`** — only when its backend is up
   (fails with "CDP WebSocket connect failed" when Chrome/CDP is down).
4. **`web_search` tool** — when present in the toolset (session-dependent).

## Engine Quirks (verified Aug 2026)

- **DDG Lite via Playwright works when curl→DDG is blocked.** curl to
  `lite.duckduckgo.com/lite/?q=...` returns HTTP 202 with no result links when
  challenged; the same URL via Playwright renders results with zero errors.
  This is the single most useful fallback — try it before Bing.
- **DDG HTML endpoint (`html.duckduckgo.com/html/?q=...`) via Playwright is even better than Lite when it works:** standard `.result` blocks with `a.result__a` (title) + `.result__snippet` (snippet) — the classic selectors that return empty on Lite work cleanly on HTML. Verified Aug 7-8 2026 across 7 name/entity queries, zero CAPTCHA, richer results. Compact per-query extraction via `browser_evaluate` (one line per result, no snapshot files, cron-safe):
  ```js
  () => Array.from(document.querySelectorAll('.result')).map(r => { const a = r.querySelector('a.result__a'); const s = r.querySelector('.result__snippet'); return (a ? a.innerText : '') + ' || ' + (a ? a.href : '') + ' || ' + (s ? s.innerText.slice(0, 180) : ''); }).join('\n---\n')
  ```
  **`site:` queries on DDG HTML return ZERO results for ASP.NET-backed registries** (e.g. `site:sos.wyo.gov "the company"` — verified Aug 7 2026) — the entity data isn't indexed, so emptiness is an index gap, not evidence of absence. Do not use `site:` as a registry-status fallback; use session_search baselines or a human browser.
- **CDP chrome-devtools-mcp reaches DDG HTML when curl is CAPTCHA-blocked** (verified Aug 10 2026): `mcp__chrome_devtools_mcp__new_page(url=...)` → `take_snapshot()` returned full `.result` blocks for name/entity queries while curl to DDG Lite got the bot challenge. The DDG-HTML-via-browser claim generalizes to ANY live browser backend (Playwright OR CDP-MCP), not just Playwright.
- **Reliable CDP-MCP multi-query read: reuse ONE tab.** `mcp__chrome_devtools_mcp__navigate_page(type="url", url=...)` on the selected tab, then `take_snapshot()` per query. **Do NOT use `mcp__chrome_devtools_mcp__evaluate_script` for async-fetch batch reads** — it died with "Protocol error (Runtime.callFunctionOn): Target closed" (page dies before the call runs) and "Failed to fetch" (cross-origin when the selected page is about:blank). The `browser_evaluate` extraction snippet above is Playwright-only; on the CDP-MCP backend, per-page navigation + snapshot is the working pattern.
- **CDP-MCP browser restarts mid-sweep:** the backend restarts without warning ("browser was restarted or reconnected" / page list suddenly shows `about:blank`); page IDs remap and most tabs are wiped, with an old tab (e.g. the WY SOS page from an earlier job) resurfacing as selected. After any restart marker, call `list_pages` and re-select before acting. `fill_form` then errors "No snapshot found for page N" until you `take_snapshot` on the current page — always snapshot immediately before filling.

- **Bing via Playwright can be challenge-gated** ("One last step — Please solve
  the challenge below to continue") in the same session DDG Lite works. Bing is
  NOT reliably open; treat DDG Lite as the primary browser search engine.
- **Parsing DDG Lite results via `browser_evaluate`:** the `.result` and
  `a.result-link` class selectors can return empty. Reliable extraction:
  read `document.body.innerText` from the index of the first `"1."` — titles,
  snippets, and cites appear as plain text lines; grab hrefs from `a` elements.
- **Mojeek via curl IS a viable general-search fallback** (send a desktop
  User-Agent) when DDG and Bing are both blocked — validated Aug 2026: returned
  parseable results for name/entity queries while DDG was CAPTCHA'd and Bing was
  challenge-gated. Parse patterns: links `grep -oP '<a class="ob" href="\K[^"]+'`,
  titles `grep -oP 'class="title"[^>]*>\K[^<]+'`. Caveats: shallow index (name
  queries can return unrelated hits — e.g. "Backus" matches a MN town, "the operator"
  maps to Saint the operator MN), rate-limits after ~3 rapid queries (space with
  `sleep 2`), `site:` operator unreliable — empty results are index gaps, not
  evidence of absence.
- **OpenCorporates / Bizapedia via curl** often return empty, JS-gated, or 403
  pages — do not rely on them for registry lookups; use the official registry
  via browser or fall back to session_search baselines.
- **Yandex via curl** returns HTML but no extractable result links/titles
  (JS-required page) — not a usable fallback (confirmed Aug 2026).

## ASP.NET WebForms POST (registry search pages)

Many .gov/registry search pages are ASP.NET WebForms (WY SOS, leepa.org, county
clerk portals). They CAN be driven with a scripted POST — no browser needed.

- **Field NAMES use `$`, not `_`.** Names render as
  `ctl00$BodyContentPlaceHolder$...$OwnerNameTextBox` ($ separators) even
  though element IDs use underscores. A POST using `_` names returns the form
  with ZERO results — indistinguishable from a clean "no records" answer.
  Always verify the POST landed by echoing a submitted value back from the
  response before trusting an empty result.
- **Big `__VIEWSTATE` breaks argv.** leepa.org's viewstate is ~44KB —
  `curl --data-urlencode "__VIEWSTATE=$VS"` dies with "Argument list too long"
  on Windows. Build the POST body inside a Python script (`urllib`), not on
  the command line.
- Extract `__VIEWSTATE` + `__VIEWSTATEGENERATOR` from the GET, POST them with
  the target fields + the submit button's value. No `__EVENTVALIDATION` on
  newer .NET versions.
- **Surname-first result cells.** Owner grids render "BACKUS JOHN A & JOANNE E"
  (surname first). A regex requiring text BEFORE the surname misses these —
  match any cell containing the surname: `>([^<>]{1,100}<TERM>[^<>]{0,40})<`
  case-insensitive.

## Federal Register API Pattern

- Query: `https://www.federalregister.gov/api/v1/articles.json?conditions%5b...%5d`
- **MSYS/Windows curl: encode `[]` as `%5b` / `%5d`** or curl exits 3 / silently
  returns empty.
- **Intermittent JSON errors:** a single query can return
  `JSONDecodeError: Expecting value` (empty/invalid body) while sibling queries
  succeed — and the SAME query succeeds on retry. **Retry once after `sleep 2-3`
  before fast-failing.** Do not abandon the whole sweep on one empty response.
- **Verify agency IDs** against `agencies.json` (flat list, NOT a dict with
  "results"). A wrong ID returns HTTP 200 with empty results — silently wrong.
- Deep document text: use the article's `full_text_xml_url` (bypasses the HTML
  page CAPTCHA). Parse with `python -c` piping (cron-safe; `execute_code` is
  blocked in cron context).
- Individual article JSON: `https://www.federalregister.gov/api/v1/articles/<FRDoc>.json`
  returns title, type, publication_date, comments_close_on, and abstract in ONE
  call — the quickest way to check a proposed rule's comment deadline (e.g. FAR
  Overhaul FR Doc 2026-12562 → comments closed 2026-07-23). Use before reaching
  for `full_text_xml_url`.

## Obfuscated DOM IDs on Gov Sites

Some state portals randomize element IDs per page load (WY SOS observed Aug 2026:
textbox id=`ans`, submit button id=`jar`; `MainContent_*` IDs do NOT exist).
Consequences and workarounds:

- Snapshot refs (e.g. `e72`) die on reload — "Ref e72 not found... Try capturing
  new snapshot."
- Discover live IDs via evaluate: `[...document.querySelectorAll('input')].map(i => i.id)`
- Drive the form via evaluate: set `.value`, dispatch `input` + `change` events,
  then `.click()` the submit button — one evaluate, no refs needed.
- **Visual CAPTCHAs can appear only AFTER a postback attempt** (clean form render
  → submit → hang → retry → CAPTCHA). Detect via `document.body.innerText`
  looking for "What code is in the image?" / "Your support ID is:" — the
  accessibility snapshot can miss the challenge overlay entirely.

## Baseline Recovery When a Registry Is Blocked

When the official registry is unreachable, do NOT report "unknown":

1. `session_search` prior sweep sessions for the last-confirmed status
   (e.g. query `"<entity>" <state> annual report filing status`, sort newest).
2. Report that baseline explicitly flagged as **"needs manual verification"**
   (e.g. "ACTIVE per Aug 1 run — verify via human browser").

## Pitfalls

| Issue | Response |
|-------|----------|
| A source was blocked last session | Re-try it — blocks are per-session/per-fingerprint, not permanent |
| One curl query empty | Retry once after 2-3s sleep before assuming the source is down |
| Snapshot refs fail after reload | Re-snapshot, or switch to evaluate-based driving |
| >2 failed attempts on one source | Fast-fail and move on — sweeps have turn budgets |
| `execute_code` blocked in cron | Use `python -c` with stdin piping for JSON parsing |
| MSYS curl `-o /tmp/file` "not found" on read-back | From a non-`/tmp` cwd, native curl.exe writes where bash can't read (path-translation mismatch) even though curl reports success. Fix: `cd /tmp && curl -o file ...` (relative path), then verify with `wc -c` |

See `references/engine-status-log.md` for dated per-engine observations.
