---
name: burp-recon
description: >
  Triage and investigate Burp Suite proxy traffic through the Burp MCP server, and manage
  TLS pass-through to silence tracker/analytics noise. Use this whenever the user asks you to
  look at captured traffic, proxy/HTTP history, find bugs in recorded requests, trace a
  login/auth flow, follow what happened after a request, locate where a token/cookie/parameter
  appears, OR quiet down a noisy Burp history by excluding third-party trackers from interception.
  Teaches the flat-table → pick-id → drill-in → follow-sequence workflow (never dump the whole
  history) plus the find-noise → TLS-pass-through loop.
---

# Burp Recon - the LLM-friendly way to read proxy traffic + kill noise

Real engagements hold 3,000-4,000+ proxy entries, most of them analytics/static-asset noise.
This extension adds a purpose-built toolset so an LLM can triage that volume cheaply, drill into
exactly what matters, and cut the noise at the source - without ever blowing the response-size cap
or truncating a cookie.

## ⭐ The tools this extension adds (use these - they are the point)

| Tool | What it's for | Why it beats the raw tools |
|---|---|---|
| **`get_proxy_http_history_summary`** | The PRIMARY view: a flat, ungrouped table (`id \| method \| host \| path \| status \| len \| mime`), newest-first, send order preserved. | One compact row per request instead of full bodies. Range-chunked, budget-capped - never truncates mid-data. |
| **`get_proxy_http_entry`** | Full request+response for ONE entry by its Burp `id`. | Headers/cookies **never** truncated; big bodies capped + resumable; `contextBefore/After` shows the surrounding sequence. |
| **`search_proxy_http_history`** | Regex/term search → matching rows **+ a snippet** around each hit. | Finds where a token/header lives without dumping full bodies. |
| **`get_proxy_http_history_stats`** | Aggregate shape-check: counts per host / method / status-class / mime-class + id range. | ~1-3 KB for any history size. Instantly reveals the noisy hosts. |
| **`get_proxy_websocket_history_summary`** | Lightweight WebSocket message summaries (direction, size, preview). Requires `count` AND `offset`. | Scan WS traffic without pulling 100 KB payloads. |
| **`get_proxy_tls_passthrough`** | Read Burp's TLS pass-through config (rules + flags). | See exactly which hosts are excluded from interception. |
| **`set_proxy_tls_passthrough`** | Add/remove TLS pass-through host rules, toggle flags. | Silence tracker noise at the source; reads back from Burp to confirm. |

> Avoid `get_proxy_http_history` / `_regex` for browsing - they return full raw entries at high
> token cost. They're only for when you truly need every raw byte of a small, filtered set.

---

## Part 1 - Reading history (the recon loop)

**Mental model:** scan a flat table → pick an `id` → drill in → follow the send sequence.

### 1. `get_proxy_http_history_summary` - START HERE
Returns `META {…}` + one row per request. The `id` column is Burp's real `#` and the handle for
every drill-down.

- **Browse big histories in chunks:** META gives `total`, `idRange`, `returnedIds`, `hasMore`.
  Page down with `toId` (e.g. `toId=<lowest id seen - 1>`). The last chunk ends with
  `--- END OF HISTORY ---`.
- **Only-new-traffic poll:** after seeing up to id N, call `fromId=N+1` to fetch just the new
  requests - you already hold everything ≤ N.
- **Filters (you decide relevance - no scope filter):** `hosts`, `methods`, `statusCodes`,
  `statusMin`/`statusMax`, `pathContains`, `hasNotes`, `hideNoise` (drops js/css/images/fonts),
  `dedupe` (collapse identical endpoints, adds `xN`). `pathMaxChars` caps long paths;
  `oldestFirst:true` reads a flow forwards; `format:"json"` for structured rows.
- **Bounds handled:** over-shooting `toId` clamps (`clampedToId`); a past-the-end `fromId` returns
  a clear "Highest id is N" message.

### 2. `get_proxy_http_entry` - drill into one id
Full request+response. **Headers are never truncated**; bodies cap at `maxBodyBytes` (default 50000)
and resume via `bodyOffset`. `include` = `all | request | response | request_headers |
response_headers` (use `*_headers` when you only need cookies/auth). `contextBefore`/`contextAfter`
return the neighbouring rows - the request sequence around this entry.

### 3. `search_proxy_http_history` - find by content
`regex` or `term` across raw requests+responses → rows + a short snippet. Never full bodies.
Filters: `hosts`, `methods`, `hideNoise`, `caseSensitive`.

### 4. `get_proxy_http_history_stats` - optional shape-check
Aggregates only. Great first call on a huge history to see the host/method/status/mime breakdown
and the id range before pulling rows.

### Recon recipes
- **Triage a capture:** `…_stats` → `…_summary` (newest 100) → page down with `toId` → note ids.
- **Trace login/auth:** `…_summary` `hosts=[target]` `methods=["POST"]` → find login id →
  `…_entry id=<login> contextAfter=5` to see token usage right after.
- **Follow after request N:** `…_entry id=N contextAfter=10`.
- **Where is a token/cookie set:** `search term="Set-Cookie"` or `regex="Authorization: Bearer"`.

---

## Part 2 - Killing noise with TLS pass-through

Burp logs every third-party tracker (doubleclick, facebook, nr-data, demdex, analytics.google, …),
drowning the real target. **TLS pass-through** tells Burp to forward those hosts' encrypted traffic
**without intercepting/decrypting it** - so they never hit the history at all.

### The find-noise → exclude loop
1. **Find the noise:** `get_proxy_http_history_stats` → look at `byHost`. The hosts with high
   counts that aren't the target are your noise (e.g. `bam.nr-data.net`, `ad.doubleclick.net`).
2. **Read current rules:** `get_proxy_tls_passthrough`.
3. **Add exclusions:** `set_proxy_tls_passthrough` with `addHosts` = host **regexes**
   (e.g. `.*\.doubleclick\.net`, `.*\.nr-data\.net`). It reads back from Burp and reports the actual
   stored count.
4. **Verify config:** `get_proxy_tls_passthrough` shows the rules.

### `set_proxy_tls_passthrough` params
- `addHosts` / `removeHosts` - host regexes (matched against the CONNECT host)
- `replaceAllRules` - set the whole list at once
- `applyToOutOfScopeItems` / `autoAddOnNegotiationFailure` - the two flags
- **No `port`/`protocol` params** - you supply only the host regex; the tool builds each rule with
  `port:"443"`/`protocol:"any"` for you.
- Unspecified fields are left unchanged. Requires **"Enable tools that can edit your config"** in
  the Burp MCP tab.

### Schema fact (learned the hard way - don't deviate)
Each Burp `ssl_pass_through` rule needs **four** keys, all required, or Burp silently drops it:
`{"enabled":true,"host":"<regex>","port":"443","protocol":"any"}`. `port` is a **string**, not an
int. The tool builds this for you - but if you ever hand-write rules via `set_project_options`, use
exactly this shape.

### ⚠️ Critical runtime caveat - pass-through only affects NEW connections
A rule takes effect when a **new TLS connection is negotiated**. Any tracker connection the browser
already had open keeps being intercepted (and logged) until it closes. So:
- **Adding a rule does not retroactively un-log an open connection.** Seeing a host still appear
  right after adding its rule is expected if the connection predates the rule.
- **To verify:** fully close the browser (kill existing tunnels) or use a fresh Incognito window,
  reopen, browse, then check `get_proxy_http_history_summary fromId=<baseline+1>` - the excluded
  hosts should now be **absent**.
- Always record the current max `id` as a baseline BEFORE the verification browse.

---

## Guardrails
- Default to summaries; fetch full bodies only for specific ids.
- Headers/cookies come back whole - for a huge body, raise `maxBodyBytes` or page with `bodyOffset`.
- History/search tools are read-only. `set_proxy_tls_passthrough` modifies config and is gated by
  the Burp "Enable config editing" toggle - confirm intent before changing pass-through rules, and
  remember it changes what Burp will/won't decrypt.
- If a tool returns "access denied by Burp Suite", tell the user to approve history access (or
  enable config editing) in the Burp MCP tab.
- Trust read-backs, not echoes: `set_proxy_tls_passthrough` reports Burp's **actual** stored state
  and warns on a count mismatch - if it warns, the rules didn't all apply.

---

## Resources (load on demand)
This file is the overview. For depth, read the matching file under `references/`:

- **`references/tool-reference.md`** - every parameter of all 7 tools, output anatomy, paging
  patterns, and the per-tool gotchas. Read this when you need exact param behavior.
- **`references/playbooks.md`** - step-by-step recipes (triage a capture, trace an auth flow, find
  where a token lives, hunt reflected input, kill tracker noise, poll for new traffic, and more).
- **`references/cheatsheet.md`** - one-page quick lookup: the loop, params at a glance, one-liners.
- **`references/vuln-cheatsheets.md`** - external payload/technique links per bug class (XSS, SQLi,
  SSRF, SSTI, RCE, IDOR, XXE, CSRF, JWT, CORS, and more) plus a recon angle for surfacing each one
  from captured traffic with the 7 tools.
- **`references/search-recipes.md`** - copy/paste `regex`/`term` patterns for
  `search_proxy_http_history`: auth/session, secrets and keys, error leakage, injection candidate
  params, PII, and tech fingerprinting.
- **`references/noise-hosts.md`** - ready to paste tracker/analytics host regexes for
  `set_proxy_tls_passthrough`, grouped by category, with a common starter bundle.
