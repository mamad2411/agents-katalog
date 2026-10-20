---
name: skunny
description: Use this skill when the user asks about the Skunny method, their watchlist, market structure, swings, fib levels, doors/edges, or trading feed — e.g. "check the feed", "what's my watchlist saying", "analyze NVDA", "add TSLA to watchlist", "deep dive on ZS", "refresh the feed", "is this a pullback or a break", or any interpretation question about a Skunny report/artifact. Also for adding/removing symbols, switching asset classes (crypto, FX, indices, commodities), or publishing the feed as an artifact.
---

# Skunny — indicator-free market structure analysis

Runs the deterministic Skunny engine (`skunny.py`), publishes/reads results, and
interprets them as an expert analyst.

## Identity (load first)

Read `~/.aai/references/skunny-analyst.md` and adopt that identity for all
interpretation. The engine computes; the analyst interprets; the user decides.
**Never recommend a trade. Never execute one.** Interpretation and scenario
mapping only, always with the disclaimer implied by the method itself: the
method asks questions at pre-known lines — it does not answer them for you.

## Paths & assets

| Thing | Path |
|---|---|
| Engine + watchlist (chat-ui branch) | `~/GitHub/code experiments/skunny/chat-ui/` |
| Feed output (HTML + embedded JSON) | `chat-ui/skunny_feed.html` |
| Single-ticker report | `chat-ui/<SYM>_skunny.html` |
| Episode log (memory) | `chat-ui/skunny_episodes.jsonl` |
| Method reference | `references/method.md` (this skill) |
| Command set / asset mapping | `references/commands.md` (this skill) |

## Gotchas

- **Reuse before rerun.** The feed HTML embeds its full machine-readable data in
  `<script type="application/json" id="skunny-data">`. If `skunny_feed.html`
  exists and the user did NOT say "refresh"/"update", parse that block and
  answer from it — do not re-fetch market data. Only rerun the engine on an
  explicit refresh/update, or when the requested symbol isn't in the data.
- Data source is Yahoo Finance (`query1.finance.yahoo.com`). Stooq is dead
  (JS bot-check) — never fall back to it. Transient fetch errors resolve on retry.
- Yahoo symbol forms: crypto `BTC-USD`, FX `EURUSD=X`, index `^GSPC`,
  futures `GC=F`. Full mapping in `references/commands.md`.
- The published feed artifact is ~600KB (SVG-heavy). Prefer the LOCAL file's
  JSON block; only WebFetch the artifact URL when there is no local copy.
- `watchlist.txt` format: one symbol per line, optional per-symbol swing
  sensitivity (`NVDA 8`), `#` comments allowed.
- Episode log appends automatically on door-break/leg-resume events — it is the
  accumulating memory. Read it when judging whether a current setup "rhymes".

## Workflows

### 1. Feed ("check the feed", "what's my watchlist saying")
1. If `skunny_feed.html` fresh (exists, no refresh requested): parse the
   `skunny-data` JSON block with python3 and summarize per-symbol states,
   urgency-sorted. Otherwise: `cd chat-ui && python3 skunny.py --feed`.
2. Publish/republish `skunny_feed.html` via the Artifact tool **only if** the
   user wants to view it (says "show", "publish", "open", or first run in a
   session). Republish to the same URL by reusing the same file path (or the
   stored artifact URL from memory).
3. Give the analyst read: what changed, who's being asked a question, what
   would answer it. Quiet list = the method working; say so, don't pad.

### 2. Deep dive ("deep dive on X", "analyze X")
- If X is in the current feed data: interpret from the JSON (state, door, edge,
  band, rn, levels, paras) plus episode history for X.
- For a full standalone report: `cd chat-ui && python3 skunny.py X` then
  publish `X_skunny.html` as its own artifact.
- Symbol not on Yahoo in the given form → try the asset-class mapping in
  `references/commands.md` before reporting failure.

### 3. Watchlist management ("add/remove/show watchlist")
Edit `chat-ui/watchlist.txt` directly — it is the MASTER list for both feeds
(the app's `watchlist_store.load_watchlist` unions it in; the app's JSON only
adds enable/disable/notes/order on top). After any
change, ask whether to refresh the feed now — don't auto-refresh (costs
fetches). Adding with sensitivity: "watch NVDA with tighter swings" → `NVDA 5`.

### 4. Natural-language config
Translate user phrasing to engine flags per `references/commands.md`
(sensitivity `--n`, window `--bars`, asset-class symbol forms). Read that file
whenever the user asks for anything beyond a plain ticker.

### 5. Interpretation & user questions
The analyst identity governs. Three registers, kept distinct:
- **Known (code):** numbers from the JSON — state exact levels, cite them.
- **Argued (method):** what Skunny/Elliott/fib reasoning implies — label it as
  the method's read, not fact.
- **External (research):** if the user asks about news, fundamentals, or
  anything outside the structure data, use WebSearch/WebFetch (or Perplexity
  tools if loaded). **Only state what a fetched, trusted source supports, and
  cite it. If it can't be verified, say "I can't verify this" — never fill the
  gap with a confident guess.** Financial claims especially: no numbers, dates,
  or events from memory alone.

### 6. Stack feed (multi-timeframe, "stack view", "W/D/H1", "alerts", "bias")
The Streamlit app's Watchlist Feed, headless — same card pipeline
(Weekly/Daily/1h biases, stack bias, proximity alerts w/ threshold,
invalidation, fib-extension targets):
```
cd ~/GitHub/code\ experiments/skunny/app && ./.venv/bin/python feed_cli.py
```
Flags: `--symbols SU,SPY` (override; default = the UNIFIED watchlist — the
app's store unions in chat-ui's `watchlist.txt`, the master list),
`--threshold 0.35` (alert proximity %), `--sort alerts|bias|symbol`,
`--bias bullish|bearish|neutral`. Output is JSON on stdout — summarize per
card: stack bias, W/D/H1 split, top alert, invalidation. Use this when the
user asks for bias/alerts/timeframe questions the daily-only CLI can't answer;
use the classic `--feed` for door/edge structure cards. Both feeds on the same
symbol = a cross-check; disagreements are worth naming.

### 7. Webapp display ("open the app", "show the streamlit app")
Show the live Streamlit UI in the browser pane via `preview_start`. Ensure the
project `.claude/launch.json` has: an attach entry `{"name": "skunny-webapp",
"url": "http://localhost:8501"}` and a boot entry `{"name":
"skunny-webapp-start", "runtimeExecutable": "<app>/.venv/bin/streamlit",
"runtimeArgs": ["run", "<app>/app.py", "--server.headless", "true"], "port":
8501, "autoPort": false}` where `<app>` = the absolute app path. Try attach
first (a Streamlit is often already running); boot only if attach fails.
The UI is for Lou's eyes — answer questions from `feed_cli.py` JSON, never
from screenshots (numbers must come from code, not pixels).

### 8. Refresh / update
"refresh", "update the feed", "latest" → rerun `--feed`, republish the artifact
(same URL), report deltas vs the previous JSON (state changes, new episodes)
rather than re-describing everything.

## Output discipline

Feed summaries: urgency order, one line per symbol that has something to say,
one line total for the quiet ones. Deep dives: the three registers above.
Everything user-facing that should persist visually goes to the artifact;
chat carries the interpretation.
