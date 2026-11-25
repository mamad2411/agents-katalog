---
name: testing-cauce-serve
description: How to spin up isolated `cauce serve` instances for e2e testing — config/env conventions, replay-engine fault injection, port/dir layout, and UI/API check tactics. Includes SPA-era (post-FX-06) UI testing notes.
---

# Testing `cauce serve` end-to-end

## Spawn conventions

- Binary: `cargo build -p cauce-cli` → `target/debug/cauce`. Run from the **workspace root**
  so the replay engine's default `fixtures_root = engines/fixtures` resolves.
- Per-instance env: `CAUCE_DATA_DIR` (SQLite store), `CAUCE_CONFIG_DIR` (holds `config.toml`),
  `CAUCE_LOG=info`. Give each instance its own pair of dirs — a settings save writes
  `$CAUCE_CONFIG_DIR/config.toml` and would clobber a shared file.
- Start: `CAUCE_DATA_DIR=… CAUCE_CONFIG_DIR=… cauce serve --bind 127.0.0.1 --port <fixed>`.
  The e2e harness uses `--port 0` + parses `addr:` from stderr; for browser testing prefer a
  fixed port. `/health` answers 200 when up (≈1–2 s).
  **`--bind` takes a HOST only** — `--bind 127.0.0.1:4490` exits 1 with
  `"failed to lookup address information: Name or service not known"` (a DNS lookup, not a
  SocketAddr parse). Serve logs go to `$CAUCE_DATA_DIR/logs/cauce.<date>.jsonl`, NOT
  stdout — an "exit 1, empty log" launch failure is diagnosable there.
  rust-embed debug builds serve `assets/spa` FROM DISK — a committed SPA rebuild needs no
  cargo rebuild, just restart serve (verify with `curl /app/index.html | grep index-`).
- **Backgrounding**: `setsid env … ./cauce serve … &` from a one-shot exec can get reaped
  when the command's process tree exits. For a serve that must outlive the command, run it
  in a persistent TTY shell or with `nohup … & disown` in a reused `shell_id` session.

## Engine config

- `config.toml` `[[engines]]` entries default `enabled = true`. Builtins `replay`
  (enabled=false) and `ddgs` (exec, **tier 2**, enabled=true) always exist; a file entry
  with the same id wins.
- `CAUCE_ENGINES=id1,id2` pins the enabled set to exactly those ids — use it to isolate
  test engines and suppress builtin ddgs, which would otherwise join the tier-2 hedge set.
- Engine ids must match `[A-Za-z0-9._-]+` (hyphens OK, e.g. `replay-t2`).
- `tier = 2` in an `[[engines]]` entry defers that engine to the W3-01 hedge wave.
- Replay kind honours entry `id`/`tier`, so `[[engines]] id="replay" kind="replay"` plus
  `[[engines]] id="replay-t2" kind="replay" tier=2` runs two replay instances.

## Fault injection is SHARED env — design around it

`CAUCE_REPLAY_LATENCY_MS`, `CAUCE_REPLAY_EMPTY`, `CAUCE_REPLAY_FAIL_EVERY`,
`CAUCE_REPLAY_BLOCKED`, `CAUCE_REPLAY_PAGE_LIMIT` apply to **all** replay instances in the
process — you cannot give tier-1 and tier-2 different latencies from env. Multiple
`cauce serve` processes with different env is the workaround.

- `CAUCE_REPLAY_EMPTY=1` → instant `no_results` answers (good for the `reason="few"` early
  hedge fire).
- `CAUCE_REPLAY_LATENCY_MS=N` → every replay call sleeps N ms (good for the `reason="slow"`
  floor fire; with shared latency the t2 batch always lands ~hedge_point ms after t1's, so
  a "t2 answers first" ordering cannot be produced at serve level).
- Hedge knobs: `search.min_results`, `search.hedge_floor_ms`, `search.hedge_ceiling_ms` in
  config or `CAUCE_SEARCH_*` env (env also greys the /app/settings input + shows a "set by …"
  hint). Defaults: min_results=5, floor=300, ceiling=1500, deadline=3000.
- The tier-1 latency histogram (P90 hedge point) is **in-memory**: restart resets it → the
  first uncached search hedges at the floor; afterwards P90≈latency → hedge point clamps to
  the ceiling when latency > ceiling. A late-fired t2 whose remaining deadline < latency
  gets clipped (`failed: timeout`, `deadline_hit:true`); enough clips open its breaker and
  the hedge then reports `engines_skipped` instead of `hedged` — that is intended fire-time
  gating, not a bug. A `commit_config` fan-out rebuild (see `/app/settings` hot-apply) also
  resets the histogram.
- `CAUCE_SEARCH_HEDGE_FLOOR_MS > CAUCE_SEARCH_HEDGE_CEILING_MS` panics `Duration::clamp`
  per request (502 "in-flight search task vanished") — no validation exists (bug).

## SPA-era UI surface (post-FX-06)

- The Svelte 5 SPA at `/app` is the only UI. Routes: `/app` home, `/app/search`,
  `/app/answer`, `/app/history`, `/app/dashboard`, `/app/archive`, `/app/admin?tab=…`,
  `/app/settings`. Legacy `/`, `/search`, `/answer` 308 to their `/app` twins (query
  preserved); `/history`, `/dashboard`, `/archive`, `/settings` intentionally 404 — only
  the three canonical entry points redirect.
- Residual server-rendered pages that are NOT the SPA: `/answer/{id}` (persisted answer
  log — a completed ask navigates there so reloads don't re-run the loop), `/trace/{id}`
  (audit deep-links), `/opensearch.xml`, `/favicon.ico`.
- SPA asset regression to keep checking: `/app/assets/index-<hash>.js` must answer
  `text/javascript` (a `text/html` answer bricks the whole SPA — #276).
- Nav (0.9.0): logo + Search/Answer/History left, theme toggle + waffle menu right; below 700px the waffle is a full-screen sheet. Operator entries (Engines/Cache/Audit) only show with `adminSurface`.
- The displayed result count reads `engines_used[].result_count` (engine-reported) while
  rendered rows are post-merge-collapse — a "10 results" header over 9 rows is the merge's
  `collapse_same_host_after`, not a missing row bug. Cached-path renders show the
  post-collapse count.
- Ask flow: `step` frames → `Searching:` step chips, `delta` → answer text, `sources` →
  a `Sources (N)` chip per turn that opens the sources panel/drawer, `done` → status + confidence + model chip + related links; an
  ungrounded answer renders "cites no sources — it may be ungrounded" and is NOT cached.
- Click → archive: `<article>` links are `target="_blank"`; the click fires `POST /api/click`
  (clicks row) + `POST /api/pages` (archive index). Replay URLs are fabricated paths on real
  hosts → upstream 404 → nothing stored; the archive staying at 0 pages is correct.

## Threads e2e (0.9.0, `/api/threads`)

- `POST /api/answer` with `thread_id` upserts the thread and returns `done.thread_id`; omit it and nothing persists. `GET /api/threads` (newest first), `GET /api/threads/{id}`, `DELETE /api/threads/{id}`.
- Owner isolation: local mode owner is `local`; in public mode a second bearer token must get `404` on the first token's thread id. Check this, it is the whole point of the owner column.
- SPA URL is `/app/answer?thread=<id>`. Reload must show the full transcript; kill the server read (or use a fresh owner) to see the localStorage fallback. History at `/app/history` lists threads in a `Conversations` section.
- History cap: 21+ turns returns `400 bad_request`; the UI warns at 15 and shows a specific error.
- Landing preview: the landing is a build-time flag (`VITE_CAUCE_LANDING=1`). `pnpm build:spa` writes into the committed `assets/spa` (`emptyOutDir`), so build the landing with an `--outDir` outside the repo or `git checkout -- crates/cauce-server/assets/spa` afterwards, otherwise the artifact-freshness check fails. The out-of-repo recipe has not been run end to end.

## Check tactics

- API: `GET /api/search?q=…` → `meta.hedged`, `meta.hedge_at_ms`, `meta.engines_used`,
  `meta.engines_skipped`, `meta.source` (`"network"` vs `{cache:{…}}`), `meta.deadline_hit`.
- SSE: `GET /api/search/stream?q=…` → `event: results` per engine completion then terminal
  `event: meta`; streamed searches populate the cache too.
- Metrics: `GET /metrics` → `cauce_hedge_total{reason="slow"|"few"}` (unlabeled `0` before
  the first fire), `cauce_engine_breaker_state{engine}` (0 closed / 1 half-open / 2 open).
- Browser URL-bar navigation to `/api/search?q=…` returns **HTML** (Accept negotiation),
  not JSON. To show raw JSON in the page for a recording, use devtools console:
  `fetch('/api/search?q=…').then(r=>r.json()).then(j=>{document.body.innerHTML='<pre>'+JSON.stringify(j.meta,null,2)+'</pre>'})`.
- `/app/settings` form PUTs to `/api/config`; hot keys (`search.*`, `admission.*`,
  `cache.*`, `merge.*`, `health.*`, `ai.*`, `archive.*`, `ui.*`, `engines.*` incl. `tier`,
  `server.public_url`) apply on save; `server.host`/`server.port`/`auth.*`/`logs.*` report
  `requires_restart`. The save-status line reads `saved HH:MM` or
  `saved HH:MM — restart needed: <paths>`. JSON (non-form) PUTs get `applied`,
  `requires_restart`, `effective_after_restart`.
- Proving a hot engine-tier change in one process: `/app/admin?tab=engines` renders the
  **live pipeline's** effective tier — a row flipping `t1`→`t2` is the rebuild evidence.
  `meta.hedged` only goes `true` when the t=0 wave is non-empty AND a deferred engine
  exists AND `merge.map.len() < min_results` at the hedge point: replay returns 10 results
  ≥ default `min_results=5`, so the hedge self-cancels — seed `search.min_results` high
  (e.g. `100`) to see `hedged:true`. With the whole live set at tier 2,
  `promote_deferred` runs it at t=0 instead (waves.rs) and `hedged` stays `false` —
  correct, not a bug.
- Shell kills: never `pkill -f "port 4479"` — the pattern also matches your own wrapping
  shell command and kills it (same for `pkill -f stub.py` etc). Kill by PID from
  `ss -ltnp | grep :PORT`.

## AI provider e2e (`/app/answer`, `[ai]`)

- **Devin session secrets inject `CAUCE_AI_*` env vars into every shell**
  (`CAUCE_AI_BASE_URL`, `CAUCE_AI_API_KEY`, `CAUCE_AI_MODEL`, `CAUCE_AI_ENABLED`), and env
  overrides beat `config.toml`. A serve launched without explicit values silently talks to
  the secret base_url. Always set all four (plus `CAUCE_AI_PROTOCOL`) explicitly on the
  serve command — or keep them if a live-provider run is intended.
- Protocol: `[ai] protocol = "openai"` (default, `POST {base}/chat/completions` + Bearer)
  or `"anthropic"` (`POST {base}/v1/messages`, `x-api-key` + `anthropic-version: 2023-06-01`
  headers, no Bearer). `CAUCE_AI_PROTOCOL` env overrides. Unknown values fail `Config::load`
  → `cauce serve: invalid config: unknown variant …` + exit 2 (server never binds).
- Stub the provider instead of real egress: a ~100-line Python `http.server` replaying
  `crates/cauce-core/fixtures/ai/<proto>/sse_*.raw` bodies (`text/event-stream`) in call
  order works; add `GET /v1/models` → `models.json` and a `/log` endpoint so the request
  log (method, headers, fixture index) can be opened in the browser as evidence. Count
  POSTs separately for fixture ordering — any GET probe otherwise shifts the order.
- Search side of the answer loop: pin `CAUCE_ENGINES=replay` and point cassettes at
  `CAUCE_REPLAY_FIXTURES_DIR=<repo>/evals/ai/cassettes CAUCE_REPLAY_CASSETTE_ENGINE=replay`
  (files are `<dir>/<engine>/<sha8(normalized query)>.json`; the eval tokyo-weather pair
  covers the two fixture queries in `sse_toolcall*.raw`).
- Since #232 the cache gate is deterministic groundedness (≥1 source, every prose
  sentence carries an in-range `[n]`, no out-of-range cites) — the verbalized
  `confidence` score is display-only. An ungrounded answer is NOT cached, so repeat
  runs stay clean.
- Two answer modes share `/api/answer`: the tool loop sends a `"tools"` array; the SERP
  **Assist** card POSTs `{q, context_results}` with NO tools key. Assist reuses the answer
  cache keyed by query, so a second Assist click on the same query may serve instantly —
  use a fresh query per click.

### Live provider runs (real OpenRouter egress)

- `openrouter/free` (the pseudo-model) routes to whatever free upstream is healthy —
  observed `poolside/laguna-s-2.1:free` converging to a grounded answer with real source
  cards. Free-tier may still loop to max iterations, 429, or time out — a clean in-page
  error frame is acceptable evidence for provider-free environments.
- **Synthetic replay results make models keep searching.** Seed cassettes for the queries
  the model actually sends (watch the `step` frames' `query` fields on a first live run).
- **Cached answers are deterministic chip-state proof.** A grounded done writes an
  `answers` row; reloading the same `?q=` replays `done{cached:true}` with no provider
  call. The cache key includes the model.
- If the model wraps the metadata tail in a ```` ```json ```` fence, `parse_final_answer`
  strips the fence; an unrecoverable tail is dropped, never leaked (#232/#217).
- Multi-turn: follow-up probes must use a pronoun/referent (`who created it…`) so a missing
  `history` is visually obvious.

### Loop-guard / budget evidence lives in logs

- `cauce_agent::observer` events: `{"message":"tool call short-circuited","reason":
  "duplicate query"|"search budget exhausted","tool":"search_web"}`.
- Span counting recipe (jsonl, by record kind — substring grep overcounts):

      python3 -c "import json,collections
      opens=collections.Counter()
      for l in open('$LOG'):
          r=json.loads(l); sp=r.get('span') or {}
          if r.get('kind')=='span_open': opens[sp.get('name')]+=1
      print(opens)"

  Provider calls = `ai_http` opens; real searches = `pipeline.search` opens; guard hits =
  `kind:event` records with `fields.reason` = `"search budget exhausted"`/`"duplicate query"`.
- `CAUCE_AI_MAX_SEARCHES=2` run → 2 `pipeline.search` spans, N−2 `search budget
  exhausted` events; `Searching:` chip count > executed searches is the one-glance tell.
- `ai.provider_budget_s`: save `1`, then a provider call that sleeps >1 s → SSE
  `event: error` `"provider request timed out"` on the FIRST call.
- Log filename varies per instance: glob both `cauce-*.jsonl` and `cauce.*.jsonl` under
  `$CAUCE_DATA_DIR/logs/`.

## BYOK / free_daily_answers e2e (PUB-03)

### Attributing a non-loopback client IP on a single box

`free_daily_answers` (and the rate limiter) exempt **loopback peers** and consult
`client_key` (CF-Connecting-IP → leftmost XFF → ConnectInfo peer) only for non-loopback
peers. Browser traffic from the test box therefore never counts. The working recipe:

- `rate_limit.trust_proxy_headers = true` — consulted by the budget check
  **independently** of whether the governor bucket is enabled; set
  `rate_limit.enabled = false` so page loads don't throttle.
- A ~60-line Python proxy (`http.server` + `http.client`, streaming `resp.read1` so SSE
  passes) that listens on 127.0.0.1:PORT, injects `x-forwarded-for: <TEST-NET-3 ip>`, and
  dials cauce via the box's **non-loopback** interface IP (`hostname -I`, e.g.
  172.16.x.x). The socket peer is what `is_loopback()` sees — a proxy that dials
  127.0.0.1 defeats the test.
- Cauce must bind 0.0.0.0 (legal once `server.public_instance = true`), and the proxy
  must send **`Host: 127.0.0.1:<port>`** — HostGuard 403s any non-loopback host name
  even on a public instance.
- A second proxy port with a different XFF gives the "different IP has its own bucket"
  adversarial check.

### Config knobs are FILE-ONLY

`allow_user_keys`, `allow_user_base_url`, `free_daily_answers` have no `CAUCE_*` env
override — they must come from `$CAUCE_CONFIG_DIR/config.toml`. `ai.*` is hot-appliable
through `PUT /api/config` (admin bearer), which is handy for flipping
`allow_user_base_url` mid-test to show the disabled input state. Injected session
`CAUCE_AI_*` secrets still override the file for base_url/api_key/model/enabled/protocol
— set all five explicitly.

### Provider stub evidence

The answer loop POSTs `{merged.base_url}/chat/completions`. A stub that logs
`authorization` + `model` per POST and serves `/log` makes the BYOK proof
browser-viewable: `Bearer sk-user…` + caller model proves override propagation, and
`authorization: null` on a `base_url`-only override proves the admin key was blanked,
not leaked.

### States worth asserting

- `/app/settings` for a non-admin public user shows ONLY the BYOK fieldset (config form
  is `isAdmin`-gated; `page.refresh()` skipped).
- `allow_user_base_url=false` → base_url input `disabled` + placeholder "not allowed by
  this instance"; other inputs stay enabled.
- Both flags off → settings nav link hidden AND `/app/settings` renders the "Operator
  surface" admin-token gate.
- A stale saved `base_url` is dropped client-side when the gate is off
  (`byokWire(flags)` sends only what the instance advertises) — answers keep working,
  not 403s.


## Durable answer_log + /answer/{id} e2e (#254)

- **Per-run fixture dispatch**: detect `"role":"tool"` in the POST body — a run's
  second+ provider call carries tool results back, so first call → `sse_toolcall.raw`,
  later calls → answer fixture. Dispatch on a query-marker substring in the body
  (e.g. `"grounded probe" in body`) to choose between a cacheable and a
  non-cacheable answer fixture per question.
- **Authoring a metadata tail**: append a final SSE delta whose content is
  `\n\n{"confidence": 8, "related_questions": ["q1","q2"]}` — `parse_final_answer`
  scans the tail for the last `{` that parses to an object with `confidence`.
  That drives the confidence chip + related-question links on both the live and
  stored renders.
- **A `cached` answer_log row needs a grounded (fully-cited) answer**: every prose
  sentence must carry an in-range `[n]` cite AND ≥1 source — a single-sentence
  fixture like `"Tokyo is 22°C [1]."` + tail caches; the stock `sse_answer.raw`
  does NOT (uncited "Source:" line). Second identical `?q=` → cached replay
  (zero provider calls) that still mints a FRESH answer_log row with
  `status='cached'` → the stored render shows the `cached` chip.
- **No-re-run proof for the session-ID URL fix**: every live run costs exactly
  2 stub POSTs (toolcall + answer). Reload/back/forward on `/answer/{id}` must
  leave the stub request count and `answer_log` count unchanged — serve a stub
  `GET /log` page and screenshot it as evidence.
- **`GET /api/answer-log/{id}` has no HTML arm** — browser URL-bar GET renders
  the raw JSON row (good for on-video evidence). `GET /answer/{id}` of a
  deleted/unknown id → `{"error":{"code":"not_found"}}` JSON, not an HTML page.
  `DELETE /api/answer-log/{id}` is audited (`answer_log.delete`).
- **Model field quirk**: fresh rows store the provider RESPONSE's `model`
  (fixture model name, e.g. `liquid/lfm-2.5-2.6b:free`), while `cached` rows
  store the configured `CAUCE_AI_MODEL` — chips on `/answer/{id}` differ between
  a fresh run and its cached replay. Cosmetic, not a bug.
- **`/history` stats line is origin-agnostic**: "N total" counts all rows even
  under the default `origin=user` filter (e.g. "7 total" with an empty feed).
  Cosmetic inconsistency observed on the pre-SPA page; recheck on `/app/history`.

## Archive / click-beacon e2e (`/api/pages`)

- `archive.index_on_click` defaults true; `CAUCE_ARCHIVE_INDEX_ON_CLICK=false` disables the
  `POST /api/pages` arm on result clicks — `POST /api/click` still writes `clicks` rows
  (easy negative test).
- The archive `Fetcher` has an **egress guard** (#189): private/reserved targets refused
  with 4xx before any connect, on every redirect hop. Loopback targets need
  `CAUCE_ARCHIVE_ALLOW_PRIVATE=true`. Schemes: http/https only.
- For a deterministic click → `pages` row, serve `crates/cauce-core/tests/fixtures/archive/`
  on loopback (`python3 -m http.server 8123 --bind 127.0.0.1 --directory
  crates/cauce-core/tests/fixtures/archive`) and hand-author a cassette whose result URLs
  point at it (`<dir>/replay/<sha8(normalized query)>.json`, Cassette schema — every field
  incl. `published:null` and `score` required; sha8 = first 8 hex of sha256(
  `" ".join(q.split()).lower()`)).
- `sqlite3` CLI is NOT installed — use `python3 -c "import sqlite3; ..."` against
  `$CAUCE_DATA_DIR/cauce.db` (`SELECT url,title,length(markdown),byte_len FROM pages`;
  `clicks` for the click beacon). `put_page` upserts.
- HTTP surface: `POST /api/pages {"url"}` → 201 `PageRow`; `GET /api/pages/{pct-enc-url}` →
  200 or not_found envelope; bad scheme → 403 `url_blocked`.

## /app/settings admin form e2e (formisch + Bits UI)

- **Sign-in:** `/app/settings` is `admin_or_byok` — non-admins see only the BYOK
  fieldset when BYOK flags are on. For the admin form, sign in via the GateBlock
  on `/app/admin` ("Operator surface" → paste the `[auth].admin_tokens` value →
  "save token"), then navigate to `/app/settings`. Token lives in localStorage
  `cauce:admin-token`.
- **Env > file precedence:** every `CAUCE_*` env on the serve command overrides
  config.toml; Devin boxes inject `CAUCE_AI_*` into shells — set all five
  explicitly or `[ai]` file edits silently lose. Unchecking `aiEnabled` + Save
  writes `enabled = false` to the file but `GET /api/config` still reports
  `true`. Verify writes via `cat config.toml`, not effective config.
- **Persistence proof:** `PUT /api/config` rewrites the whole file — `sha256sum`
  before/after proves a blocked submit wrote nothing; a real save is a diff of
  urlencoded dotted names → real TOML keys.
- **Wire paths:** formisch emits names like `deadlineMs`, `engines.0.tier`.
  UiSelect maps `""` ↔ `__none__` in DOM only — `field.input` keeps the real
  `""`, so the file gets `tier = 3` never a `"__none__"` literal.
- **Bits wrappers:** UiCheckbox = `<button>` + hidden input inside an implicit
  `<label>` (clicking label text toggles). UiSelect portals its listbox — items
  render at the bottom of the DOM dump, outside `<main>`; the trigger's
  `aria-expanded` flips when open.
- **Devtools docked right shrinks the page ~340px** — recompute click
  coordinates after opening devtools, or clicks land in the panel.
- **Known degradations (pre-existing):** builtin engine rows not declared in
  config.toml render editable but don't persist; "applies after restart" lists
  keys that were submitted, even unchanged ones.

## Browser-testing gotchas (Chrome for Testing on this box)

- **Omnibox inline autocomplete hijacks typed URLs** to history suggestions — after typing
  a URL press `Delete` (strips the selected suggestion tail) before Enter, or the literal
  path never gets requested. This silently broke `/` and `/app/` probes during testing.
- **Min window width ~500 CSS px** — the WM/Chrome won't resize narrower. For ~390px mobile
  checks use DevTools device toolbar (F12 → phone icon → set width 390); verify
  `document.documentElement.scrollWidth <= innerWidth` for no horizontal overflow.
- **Console/pageerror sweep via CDP**: the box's Chrome runs with
  `--remote-debugging-port=29229`. Connect to the page target's ws URL from
  `GET :29229/json` with `suppress_origin=True` (websocket-client), enable `Runtime` +
  `Log`, `Page.navigate` through every surface, collect `Log.entryAdded`
  (level≥warning) + `Runtime.exceptionThrown`. Plain `browser_console` does NOT return
  accumulated page logs — CDP is the reliable path.
- Favicon `.ico` 404s from `icons.duckduckgo.com` are third-party rate-limit flake
  (same URLs 200 on retry), not app errors — exclude them when judging "0 console errors".
- `GET /opensearch.xml` downloads as a file in Chrome (Save dialog) rather than rendering —
  the dialog itself is the "it answers" evidence.

## CDP mobile emulation + console sweep (no devtools GUI)

Chrome here runs `--remote-debugging-port=29229`; plain `browser_console` returns
nothing for the SPA. Node v24's built-in `WebSocket` talks CDP directly — no deps.
Helper scripts live at `~/e2e/bin/cdp.js <ws-url> '<cmds-json>'` and
`~/e2e/bin/cdp_log.js <ws-url>` (enables Log+Runtime+Page, reloads, prints console
errors/warnings/exceptions). Get the page WS URL from `GET :29229/json`.

- ~390px without the device toolbar: `Emulation.setDeviceMetricsOverride`
  (390x720, dsf 2, mobile:true), then drive with the normal computer tool.
  `Emulation.clearDeviceMetricsOverride` does NOT restore — set explicit
  desktop metrics (e.g. 1280x700 dsf 1 mobile:false) to go back.
  h-overflow check: `innerWidth+'|'+document.documentElement.scrollWidth`.
- **Capturing transient toasts (sonner)**: short-lived toasts are easy to miss between
  screenshots. Inject once via CDP `Runtime.evaluate`:
  `window.__toastLog=[];new MutationObserver(()=>{const s=document.querySelector('section[aria-label^="Notifications"]');window.__toastLog.push(new Date().toISOString().slice(11,19)+" :: "+(s?s.innerText.replace(/\n+/g," | "):"NONE"))}).observe(document.body,{childList:true,subtree:true,characterData:true});`
  then evaluate `JSON.stringify(window.__toastLog)` for timestamped evidence of every
  toast mount/update/dismiss.
- `playwright-core` + `chromium.connectOverCDP('http://localhost:29229')` also
  works — use `waitUntil:'domcontentloaded'` (networkidle can hang on long-poll).

## Public-mode capability caveat

On `public_instance`, `serverHistory`/`sharedStats` are off: `/app/dashboard`
renders only the instance card (no days segment) and `/app/history` reads
browser-local IndexedDB history — seed it by running real omnibox searches.

## Confirm-dialog adversarial checks

The app-level `UiConfirmHost` is a FIFO (`ui/confirm.ts`). PR #291 testing found
Escape wedging the queue — worth re-checking on every dialog change:
- queue two confirms (a JS `el.click()` dispatches even while the modal is up —
  real pointer clicks are correctly blocked by `body pointer-events:none` +
  `pointer-events:auto` overlay), then Escape-settle the first: the second
  request's dialog MUST appear. If not, the host wedged.
- exercise cancel AND confirm on row delete + bulk delete separately, then any
  other confirm — latches can survive an episode.
- `body pointer-events:none` does NOT stop synthetic `.click()` dispatch —
  that's how you queue adversarial confirms, not a defect.
