---
name: fyers-trading
description: >-
  Build trading strategies, automation bots, and backtesting scripts on the FYERS
  Trading API v3 (Indian markets — NSE/BSE/MCX). Use when the user wants to fetch
  market data, historical candles, quotes, market depth, or option chains; place,
  modify, or cancel orders (regular, GTT, smart orders); manage positions/holdings;
  stream live data over WebSocket; authenticate with FYERS OAuth; or backtest a
  strategy with FYERS historical data. Triggers: "fyers", "fyers api", "fyers bot",
  "fyers strategy", "fyers backtest", "place an order on fyers", "fyers option chain",
  "fyers historical data", "fyers websocket".
version: 1.0.0
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebFetch
---

# FYERS Trading API v3

Help developers build **strategies, automation, and backtesting** on the official
**FYERS Developer API v3** (`https://api-t1.fyers.in`). Generate working Python
(`fyers-apiv3` SDK) or raw-REST code, wire up OAuth correctly, and respect the
real-money safety rules below.

> **Scope note.** This skill targets the *public developer API* (`api-t1.fyers.in`
> + the `fyers-apiv3` SDK + WebSockets). It is **not** the FIA chat-assistant proxy
> (`fia.fyers.in`). Generate code freely; the "never write code / no orders" rules
> from FIA do **not** apply here.

## Safety rules (non-negotiable — real money)

1. **Secrets only via environment variables.** Never hardcode `app_id`, `secret_id`,
   `access_token`, or PIN in generated code or commit them. Read from env / `.env`.
2. **Dry-run by default.** Order-placing code must default to a `DRY_RUN=True` (or
   `--dry-run`) mode that logs the payload instead of sending it. Live placement
   requires an explicit, obvious opt-in flag the user sets themselves.
3. **Validate the symbol against the master before every order.** Never place,
   modify, or build an order from a hand-constructed symbol. Confirm it exists in the
   daily symbol master first (`scripts/fyers_symbols.py` / `validate_symbol()`), which
   also gives the lot size to check `qty` against. An unvalidated symbol fails live with
   code `-300`. `fyers_client.place_order()` enforces this by default.
4. **Confirm before going live.** Before running anything that places/modifies/
   cancels real orders, state plainly what it will do and have the user confirm.
5. **Respect rate limits:** 10 req/sec, 200 req/min, 100,000 req/day; order ops ≤10/sec
   (HTTP 429 → honor `Retry-After`). Breach the per-minute cap >3×/day → blocked all day.
6. **Use WebSocket for live ticks**, never a polling loop on `/quotes`.
7. **Tokens expire daily.** A 401 / code `-8`/`-15`/`-16`/`-17` means re-login, not retry.

> **Two-gate rule for going live (elaborates rule 2 and rule 4 — doesn't replace them).**
> Under the default conversational-execution mode, you (the agent) may run dry-run order
> code yourself and show the real logged payload in chat. But you may invoke a *live*
> order path yourself only when **both** gates hold: (a) the code/script itself requires
> an explicit opt-in the user set themselves (e.g. `--live`, `DRY_RUN=False` in the file/
> CLI — this must exist per rule 2, and you never set it on the user's behalf), **and**
> (b) you have plain-language typed confirmation from the user in chat for that specific
> action (per rule 4). Neither gate substitutes for the other — a flag without chat
> confirmation, or chat confirmation without the flag, is not enough to execute live.

## Default mode: conversational execution

**Default behavior for any FYERS strategy/data/order task: run scripts for real, in the
project folder, as you go — don't just generate code and hand it off.** Develop in small
increments: write/edit one small piece of the strategy → actually run it via Bash from the
project folder → show the real output in chat → let the user react/redirect → repeat. Never
dump a "finished" strategy in one shot without having executed each piece along the way.
This applies to auth setup (below), fetching data, computing signals, dry-run orders, and
backtests (see "Strategy deliverable convention"). Everything you run must be a real,
persistent file in the project folder (see that section) — never an inline/throwaway snippet.

**Opt-out:** if the user explicitly asks only for code, or says not to run anything (e.g.
"just give me the code", "don't run it"), fall back to generating files without executing —
similar to this skill's older behavior.

## Step 0 — Set up the environment (first time only)

If the user asks to "set up" the skill, or no project venv exists yet, create one and
install the strategy-code dependencies **before** anything else:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

If a package fails to install, don't stop — install the rest, retry the failing one
alone, and resolve it before moving on to strategy generation. Full detail, including
the default package list and what each is for: **`references/setup.md`**.

## Step 1 — Authenticate (do this first, conversationally)

Under the default conversational-execution mode, authenticate *with* the user in chat
rather than just pointing them at a script. Do this in the project folder:

1. **Check for a valid token yourself** by running it:
   ```bash
   python scripts/fyers_login.py --check   # prints OK if cached token is valid
   ```
2. **If missing/401 and `.env` doesn't exist yet**, scaffold it yourself: create `.env`
   in the project folder with the same keys as `.env.example` (`FYERS_APP_ID`,
   `FYERS_SECRET_ID`, `FYERS_REDIRECT_URI`, and `FYERS_PIN` only if the refresh-token flow
   is needed) present but with **blank values** — never write secret values into the file,
   and never ask the user to paste secret values into chat. Then ask the user to open
   `.env` themselves and fill in the values, and **wait for their explicit confirmation**
   (e.g. "done" / "filled in") before doing anything else. Do not guess and continue.
3. **Once confirmed, run the OAuth flow yourself**:
   ```bash
   python scripts/fyers_login.py           # opens auth URL, exchanges code, caches token
   ```
   Relay the printed auth URL to the user in chat, have them log in and copy back the
   `auth_code` (or full redirect URL), and complete the exchange in the same script run.
4. **Confirm success yourself** — run `python scripts/fyers_client.py profile` and report
   the real result in chat (don't assert it should work).

This caches the daily `access_token` to `~/.fyers/token.json`. The flow under the hood is:
`generate-authcode` → user logs in → `auth_code` → `appIdHash = SHA256("app_id:secret_id")`
→ `validate-authcode` → `access_token`. Full detail, including the standalone/manual path
for users who opt out of the conversational default: **`references/auth.md`**.

## Step 2 — Route the task

| User wants… | Load this reference | Use |
|---|---|---|
| Set up / install the skill, venv, dependencies | `references/setup.md` | — |
| Login / token / OAuth / refresh | `references/auth.md` | `scripts/fyers_login.py` |
| Quotes, depth, history, market status | `references/market-data.md` | `scripts/fyers_client.py` |
| Option chain, greeks, IV, PCR, expiry selection, ATM/ITM/OTM, max pain | `references/market-data.md` | `scripts/fyers_client.py` + `scripts/option_chain.py` |
| Place / modify / cancel / GTT / smart orders, positions | `references/orders.md` | `scripts/fyers_client.py` |
| Symbol strings (eq/fut/opt), look up a name → exact symbol, lot/tick/expiry | `references/symbols.md` | `scripts/fyers_symbols.py` |
| Live streaming (data / order / TBT sockets) | `references/websocket.md` | — |
| Backtest a strategy from historical candles | `references/backtesting.md` | `scripts/example_strategy.py` |
| Technical indicators (RSI, MACD, Bollinger, ATR, etc.) | `references/indicators.md` | `scripts/indicators.py` |
| Visualize / report a backtest's performance (tear sheet, Sharpe, drawdown, monthly returns) | `references/quantstats.md` | `scripts/quantstats_report.py` |
| Any endpoint path / payload / enum code | `references/endpoints.md` | — |
| Rate limits, error codes, retries | `references/rate-limits.md` | — |

Read references **on demand** — don't load all of them up front. `endpoints.md` is the
full path/field/enum-code catalog; the others are task-focused.

## Step 3 — Write, verify, report

- Prefer reusing `scripts/fyers_client.py` (loads the cached token, adds the
  `Authorization: app_id:access_token` header, and wraps the safety/rate-limit logic).
- After writing code, verify it imports/compiles (`python -m py_compile <file>`), and
  run data-only paths against the live API when a token exists. **Never** run live order
  code to "test" it — use dry-run.
- Get **enum codes exact** (order `type` 1/2/3/4, `side` 1/-1, `productType`, segment/
  exchange IDs). They're in `references/endpoints.md`; do not guess them.

## Strategy deliverable convention

When building a **strategy, bot, or automation** (anything beyond a one-off query),
deliver it as a **self-contained folder**, not a single script — and, per the default
conversational-execution mode above, build it *incrementally with real execution at each
step*, not as a one-shot file dump:

- Create a directory named for the strategy (e.g. `strategies/sma_crossover/`) and put
  **all** of its files inside — signal/entry logic, config, runner, `requirements.txt`
  if needed, `.env` (scaffolded per Step 1), and a short `README.md`. Never dump a
  multi-part strategy into one file. The venv, `.env`, and every module live in this one
  folder — all scripts are run FROM here, on these real files, for the rest of the
  conversation.
- Build it piece by piece: write/edit one small piece (e.g. the candle-fetch, then the
  signal, then the order stub) → run it for real via Bash from the strategy folder → show
  the actual output in chat → let the user redirect → move to the next piece. Do not write
  the whole strategy and then run it once at the end.
- After the strategy is written, produce a **Mermaid flow diagram** of the algorithm
  (data → signal → risk checks → order → logging) and save it in the folder (e.g.
  `flow.mmd` or embedded in the folder's `README.md`) so the user can review the logic
  at a glance. Show the diagram to the user.
- **Automatically backtest once the strategy is functional — don't wait to be asked.** As
  soon as the original strategy runs against real data, build and run a backtest yourself
  against FYERS historical candles (`references/backtesting.md`, `scripts/example_strategy.py`),
  in the strategy folder, and show the real metrics in chat (not a description of what it
  would show). This is the default flow, not an offer — proceed without a prompt. (Only skip
  if the user explicitly opted out of the agent running code, per "Default mode: conversational
  execution".) Put the backtest in the same strategy folder.
- **Then automatically generate a QuantStats tear sheet — also without being asked.** Right
  after the backtest produces a returns series (`df["strat_ret"]`), run
  `scripts/quantstats_report.py` on it (`html_report()` for the full HTML tear sheet, plus
  `key_metrics()` for the headline numbers in chat) so the user sees a professional view of
  their algo's performance — Sharpe/Sortino/drawdown/CAGR and the monthly-returns heatmap. Save
  the tear sheet in the strategy folder (e.g. `report.html`) and tell the user its path and the
  key metrics. Requires QuantStats installed (`references/quantstats.md`); if it isn't, say so
  and still report the backtest's own metrics. Mind the intraday→daily and "two win rates"
  gotchas documented in `references/quantstats.md`.
- **After a successful first backtest, offer Supercharge Mode.** Once the strategy has a
  working backtest with real metrics, offer to *optimize* it — hand off to the sibling
  **`fyers-supercharge`** skill, which convenes a multi-agent strategist council that debates
  improvements, generates optimized variants, backtests them, and searches for measurably better
  versions (keeping the original as the immutable baseline). Present it as: "Your strategy is
  ready. Unlock Supercharge Mode? Our AI team of professional strategists will analyze it,
  debate improvements, generate optimized variants, and recommend stronger alternatives." On
  "Yes", switch to `fyers-supercharge`. Requires that skill to be installed; it inherits all the
  safety rules above.
- Order dry-runs happen the same way — run the order code yourself in dry-run and show
  the real logged payload. Going live is gated (see the two-gate rule under the safety
  rules above). You can also proactively surface `scripts/trade_logger.py`'s `tail`/
  `summary` output in chat as the conversation progresses (e.g. after a dry-run or a live
  fill), not only when the user explicitly asks for the log.
- **Repeatability:** everything you write and run during the conversation must remain a
  real, standalone-runnable file in the strategy folder afterward (e.g.
  `python strategies/sma_crossover/run.py`) — the conversational execution is the
  *development loop*, not the only way to run the result.

## Scripts

- `scripts/fyers_login.py` — OAuth login + daily token cache (`--check`, `--print-token`).
- `scripts/fyers_client.py` — reusable REST client (profile/funds/holdings/positions/
  orders/quotes/history/optionchain) with dry-run order placement + 429 handling.
- `scripts/fyers_symbols.py` — download/cache the daily symbol master files and resolve a
  name → exact symbol (`search` / `info` / `refresh`); no token needed (public files).
- `scripts/helper.py` — token-free order utilities: lot/qty validation, price rounding to
  tick size, expiry date parsing, DTE, and `order_checks()` (all pre-order checks in one call).
- `scripts/option_chain.py` — token-free option chain helpers: `parse_chain()`, `atm_strike()`,
  `filter_expiry()`, `pcr()`, `straddle_cost()`, `max_pain()`; CLI: `demo`.
- `scripts/example_strategy.py` — end-to-end template: fetch candles → signal → **dry-run**
  order. Copy and adapt; flip to live only with explicit `--live`.
- `scripts/indicators.py` — TA-Lib wrappers for common indicators (SMA/EMA/WMA, Bollinger,
  ADX, RSI, MACD, Stochastic, CCI, momentum, ROC, OBV, A/D, ATR/NATR); lazy `talib` import;
  CLI: `demo`.
- `scripts/quantstats_report.py` — QuantStats wrappers to visualize/report a backtest's
  returns series: full HTML tear sheet, Sharpe/Sortino/drawdown/CAGR, monthly heatmap;
  intraday→daily resampling; lazy `quantstats` import; CLI: `demo`.
- `scripts/trade_logger.py` — append-only JSONL audit log (`~/.fyers/trades.jsonl`);
  called automatically by `fyers_client.place_order()` after every order attempt; exposes
  `log_order()`, `log_event()`, `tail(n)`, `summary()`; CLI: `tail [--n N]` / `summary`.
