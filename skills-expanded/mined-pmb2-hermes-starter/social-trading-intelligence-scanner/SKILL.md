---
name: social-trading-intelligence-scanner
description: "Use when building Reddit/YouTube trading scanners."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [trading, options, reddit, youtube, scanner, cron, discord, wsb, stock-sniffer]
    triggers:
      - stock sniffer
      - wallstreetbets scan
      - trading intelligence scanner
      - swing options sniffer
      - reddit youtube trading report
      - stonk sniffer
      - multi-scan trading cron
    related_skills:
      - a betting-pipeline skill
      - discord-report-format
      - youtube
      - web-scraping-scrapling
      - finance-intelligence-agent
---

# Social Trading Intelligence Scanner

Class-level playbook for **research-only** multi-source trading intelligence pipelines (not auto-trading bots). Canonical production instance: private `pmb2/stock-sniffer`.

## When to use

- User wants recurring scans of **Reddit** (WSB + options/swing subs) and/or **YouTube trader channels**
- Need **morning pre-bell + intraday pulses + evening wrap** into Discord
- Building a **deterministic Python CLI** whose stdout is the cron delivery body
- Extracting tickers from social prose/transcripts without drowning in noise

Do **not** use for sports betting (→ `a betting-pipeline skill`) or SEC/EDGAR quant pipelines (→ `finance-intelligence-agent`).

## Non-negotiables

1. **Research aggregation only** — no order routing, no personalized financial advice as execution guidance
2. **CLI stdout = Discord body** — Hermes cron final message must be exactly CLI stdout; empty actionable set → exact `[SILENT]`
3. **Private repo + docs first** when user asks to plan/document — architecture, plan, sources, ops, report format
4. **Config-driven sources** (`sources.yaml`) + **schedule intent** (`schedule.yaml`) separate from code
5. Pin `requests==2.33.0` on the operator's host if coexisting with Hermes

## Canonical layout (Phase 5)

```
repo/
├── laws.md                    # BINDING hard rules (bankroll, size, spreads, IV, theta)
├── AGENTS.md                  # binding instructions for all agents
├── README.md
├── pyproject.toml
├── .env.example
├── configs/
│   ├── sources.yaml           # 6 sources + 10 module configs
│   ├── schedule.yaml          # cron intent
│   ├── bankroll.yaml          # risk caps + sandbox bankroll
│   └── alerts.yaml            # threshold-based alert rules
├── docs/                      # system docs (how it works)
│   ├── architecture.md
│   ├── plan.md
│   ├── sources.md
│   ├── operations.md
│   ├── report-format.md
│   └── risk-model.md
├── knowledge/                 # living trading mind (how we think)
│   ├── policy/                # law changelog, risk policy, validation framework
│   ├── strategy/playbooks/    # named setups (entry/invalidation/risk)
│   ├── strategy/frameworks/   # entry-invalidation, correlation-clusters
│   ├── lessons/               # durable postmortems
│   ├── notes/                 # evergreen research
│   ├── journal/               # dated session notes
│   └── templates/             # copy-paste templates
├── src/<pkg>/
│   ├── cli.py                 # scan, risk, backtest, pnl, gaps, econ, accuracy, paper, correlation, sources, status, recs, act, close, live, ledger, calls, moves, trigger-watch
│   ├── pipeline.py            # run_scan() — all sources + modules wired
│   ├── scoring.py             # build_signals(), reddit_highlights()
│   ├── tickers.py             # extract_tickers() with noise blocklist
│   ├── report.py              # format_discord() with extra_blocks
│   ├── storage.py             # SQLite ledger (runs, signals, raw_items)
│   ├── models.py              # Signal, RawItem, ScanResult, RiskCard, SourceKind
│   ├── config.py              # load_bankroll(), load_sources(), load_schedule()
│   ├── risk.py                # build_risk_card(), attach_risk_cards(), resolve_bankroll()
│   ├── sentiment.py           # sentiment_on_item(), adjust_signal_bias()
│   ├── options_chain.py       # enrich_signals_with_chains()
│   ├── backtest.py            # run_backtest(), signal_to_noise()
│   ├── gap_scanner.py         # scan_gaps(), cross_reference_gaps()
│   ├── alerts.py              # check_alerts(), load_alerts()
│   ├── economic_calendar.py   # get_upcoming_events(), econ_risk_flag()
│   ├── signal_accuracy.py     # compute_accuracy()
│   ├── pnl_journal.py         # format_pnl_discord()
│   ├── paper_trading.py       # get_paper_account(), format_paper_discord()
│   ├── correlation.py         # detect_cluster_risk(), compute_live_correlation()
│   ├── weekly_scoring.py      # score_by_dte(), adjust_signal_scores()
│   ├── recommendation.py      # generate_recommendation(), format_recommendation_discord()
│   ├── rec_ledger.py           # save_recommendation(), mark_acted(), mark_closed(), ledger_summary()
│   ├── live_tracker.py         # fetch_live_status(), format_live_discord()
│   ├── gateway_plugin.py      # route_message(), COMMANDS
│   ├── bot.py                 # stdin/stdout JSON bot interface
│   ├── llm.py                 # optional LLM transcript distillation
│   ├── marketdata.py          # yfinance enrich_signals(), get_quote(), earnings_proximity()
│   └── sources/
│       ├── __init__.py        # 6 source adapters
│       ├── reddit.py
│       ├── youtube.py
│       ├── stocktwits.py
│       ├── rss.py
│       ├── unusual_flow.py    # Phase 5
│       └── competitors.py     # Phase 5
├── tests/
│   ├── test_risk.py
│   ├── test_sentiment.py
│   ├── test_backtest.py
│   ├── test_options_chain.py
│   ├── test_bot.py
│   ├── test_pnl.py
│   ├── test_phase5.py         # gaps, alerts, econ, correlation, weekly, paper, gateway, accuracy, competitor
│   └── ...
├── scripts/
└── data/                      # gitignored SQLite ledger

## Multi-scan cadence (ET, Mon–Fri)

| Window | Cron | Mode |
|--------|------|------|
| Pre-bell | `30 8 * * 1-5` | `morning` (Suggested Moves format) |
| Midmorning | `30 10 * * 1-5` | `intraday` |
| Midday | `30 12 * * 1-5` | `intraday` |
| Power hour | `15 15 * * 1-5` | `intraday` |
| Evening wrap | `30 17 * * 1-5` | `evening` |
| **Trigger watch** | `*/15 9-16 * * 1-5` | `trigger-watch` (no_agent=True, script) |

Hermes job settings: main scans use `deliver: origin`, `enabled_toolsets: ["terminal","file"]`, `workdir:` repo path. Trigger watch uses `no_agent: true` with `script: trigger_watch.sh` — runs `python -m stocksniffer.cli trigger-watch` and delivers stdout verbatim (prints `[SILENT]` when no triggers, suppressing delivery).

Support: `references/hermes-cron-stdout-contract.md`

## Source adapters (6 sources, 2 added Phase 5)

### Reddit
1. Prefer **PRAW** when Reddit client id/secret exist
2. Else public JSON multi-host: `www.reddit.com` → `old.reddit.com` → `api.reddit.com`
3. Browser-like User-Agent; ~0.6s delay between public calls
4. `www` often **403 Blocked** from agent IPs — fallbacks mandatory

Support: `references/reddit-public-json-fallbacks.md`

### YouTube
1. Resolve real `channel_id` (UC…) via `yt-dlp ytsearchN:` when handle URLs 404
2. Channel RSS: `https://www.youtube.com/feeds/videos.xml?channel_id=UC...`
3. Transcripts via `youtube-transcript-api` (v2 instance API)
4. Search: `yt-dlp ytsearchN:query --flat-playlist --dump-single-json` (`entries` array)
5. Challenge bonus keywords: `30 day`, `small account`, `challenge day`

Support: `references/youtube-channel-ids.md`

### Unusual Options Flow (Phase 5)
1. Free tier: yfinance option chains → detect volume/OI spikes on top tickers
2. `detect_volume_spikes(symbols)` → list of `{ticker, side, strike, volume, open_interest, expiration, last_price}`
3. `fetch_flow_items(config, candidate_tickers)` → `(list[RawItem], list[str])` for pipeline
4. Source kind: `"unusual_flow"` — must be in models.SourceKind Literal
5. Config: `sources.yaml` → `unusual_flow.enabled + watchlist + oi_spike_threshold + vol_spike_threshold`

### Competitor Tracker (Phase 5)
1. StockTwits watchers: curated list of high-signal traders (traderstewie, ripsnort, sanglucci, etc.)
2. Twitter/X watchers: via Nitter RSS (TraderStewie, OptionsAction, WarriorTrading, TraderDante, etc.)
3. `fetch_competitor_items(config, candidate_tickers)` → `(list[RawItem], list[str])`
4. Each watcher has a `weight` (0.5–1.0) for signal quality
5. Source kind: `"competitor"` — must be in models.SourceKind Literal

## Ticker extraction (quality gate)

Transcripts flood false positives (`DAY`, `RED`, `COPY`, `OTM`, `ITM`, `ATM`, `PDT`, …).

Working rules:
1. Prefer `$TICKER` cashtags
2. YouTube standalone from **title+description only**; cashtags only from transcript
3. Single-source single-mention needs higher score bar
4. Multi-source confirmation is primary quality signal
5. YAML: quote `ON`/`OFF`/`YES`/`NO`/`OR` or they become bools

Support: `references/ticker-extraction-noise.md`

## Intelligence modules (13 modules, Phases 3–6)

Beyond source ingestion, these modules enrich, validate, and guard every signal:

| Module | File | Purpose |
|--------|------|---------|
| **Sentiment** | `sentiment.py` | Lightweight NLP — 30+ bullish patterns, 24+ bearish, conviction scoring. No LLM, no deps. |
| **Risk engine** | `risk.py` | Bankroll-aware position sizing. `RiskCard` with max loss, spread tax, IV crush flag, theta warning, correlation exposure. |
| **Options chains** | `options_chain.py` | Real bid/ask/mid/IV from yfinance. Replaces rough ATM estimates. `enrich_signals_with_chains()` |
| **Backtest** | `backtest.py` | Replay stored scan history. Signal-to-noise ratio, tier analysis (🔥/🟡/🔹/⬜), source diversity scoring. |
| **Gap scanner** | `gap_scanner.py` | Pre-market gap-up/down detection. Cross-references overnight social mentions + RSS catalysts. Morning only. |
| **Alerts** | `alerts.py` | Threshold-driven rule engine. 6 rule types: multi_source, score_threshold, ticker_watch, gap_alert, econ_event. Config: `configs/alerts.yaml`. |
| **Economic calendar** | `economic_calendar.py` | Pre-loaded 2026 FOMC/CPI/NFP/PPI dates. RSS supplement from investing.com. `econ_risk_flag()` → crush window flag. |
| **Signal accuracy** | `signal_accuracy.py` | Per-source directional accuracy from stored SQLite signals. "Reddit 62%, YouTube 71%." |
| **Paper trading** | `paper_trading.py` | Tradier/Alpaca/manual provider. Fill tracking, mark-to-market, P&L. Evening wraps include paper account. |
| **Correlation** | `correlation.py` | 8 default clusters (megacap AI, MAG7, meme, crypto, fintech, energy, defense, biotech). Warns when 3+ signals = 1 bet. Optional live Pearson matrix. |
| **Weekly scoring** | `weekly_scoring.py` | DTE bands: 0-2d (30% penalty, watch), 3-5d (15% penalty, weekly gamma), 6-10d (5% premium, preferred swing), 11-21d (neutral). |
| **Gateway plugin** | `gateway_plugin.py` | 7 slash commands: `$risk`, `$scan`, `$pnl`, `$gaps`, `$econ`, `$accuracy`, `$sources`. Drop-in for Hermes gateway. |
| **Recommendation engine** | `recommendation.py` | Generates specific trade recs: entry zone (3 levels with triggers), stop loss, graduated profit targets, options contract (strike/expiry/direction/premium), exit signals, invalidation rules. `generate_recommendation()` + `format_recommendation_discord()`. |
| **Recommendation ledger** | `rec_ledger.py` | SQLite-backed tracking of EVERY recommendation. Full lifecycle: pending → acted → closed (win/loss/expired/ignored). Fill tracking, exit tracking, realized P&L per rec. `ledger_summary()` for aggregate stats. CLI: `recs`, `act`, `close`, `ledger`. |
| **Live tracker** | `live_tracker.py` | Mark-to-market via yfinance quotes. Stop loss / profit target trigger detection. Auto-close triggered stops (optional). `fetch_live_status()` → `LiveUpdate` with positions + triggers. `format_live_discord()` for evening wrap. CLI: `live --auto-close`. |
| **Signal calls** | `signal_calls.py` | Crystal-clear one-liner trade signals: 🔥 STRONG BUY / 📈 BUY / 🔍 BUY WEAK / 👀 WATCH / ⛔ SKIP. Every call: ticker, contract spec, direction, entry trigger, stop loss, profit targets, premium estimate, conviction. `build_signal_call()`, `format_all_calls()`, `format_suggested_moves()` (pre-market briefing with clickable Webull links). `generate_calls_from_scan()` → (recs, calls) tuple. Includes `webull_quote_url()` and `webull_options_url()` builders with 80+ ticker exchange map. |
| **Trigger watch** | `trigger_watch.py` | Dedicated intraday position monitoring. Checks stop loss / profit target triggers on open positions, gap alerts on watchlist, econ event proximity. Cron-compatible: prints `[SILENT]` when nothing triggered. `run_trigger_watch()` → list of alert blocks. `trigger_watch_main()` for cron entry. |
| **Alert delivery** | `alert_delivery.py` | Orchestration layer for cron delivery. Combines trigger watch + signal calls + econ + ledger in one check cycle. Mode-aware: morning/intraday/evening/trigger_only. `alert_check_cycle(mode)` → combined Discord output. `alert_delivery_main()` for cron. |

All modules are optional — each has a config toggle in `sources.yaml`. Pipeline wires them in `run_scan()` with `extra_blocks` pattern in report formatter.

Support: `references/recommendation-engine.md`, `references/signal-calls.md`, `references/trigger-watch-cron.md`, `references/webull-deep-links.md`

## Knowledge tree (Phase 3)

Separate **system docs** (`docs/`) from **trading mind** (`knowledge/`):

```
knowledge/
├── policy/           # law-changelog.md, risk-policy.md, live-validation-framework.md
├── strategy/         # playbooks/ (multi-source-momentum, catalyst-follow-through)
│                     # frameworks/ (entry-invalidation, correlation-clusters)
├── notes/            # spread-tax.md, iv-crush.md, theta-dte.md
├── lessons/          # postmortem entries (YYYY-MM-DD-slug.md)
├── journal/          # dated session notes (YYYY-MM-DD.md)
└── templates/        # journal.md, playbook.md, lesson.md
```

**Laws** (`laws.md`) are binding hard rules. Policy files are tunable process. Strategy files are named setups with entry/invalidation/risk. Every strategy file must declare: horizon & instruments, max risk %, invalidation, which laws it depends on.

## Risk engine

- Config: `configs/bankroll.yaml` (sandbox default `$10,000`)
- Live override: `STOCK_SNIFFER_BANKROLL_USD` env (never commit)
- Caps: per-trade 1%, daily new 3%, open ceiling 10%, single-name 2%, sector cluster 5%
- Spread tax gate: hard flag at 8% (bid-ask)/mid, preferred 5%
- IV crush window: flag when earnings within 5 days
- DTE bands: 3-10 preferred, 1-2 watch only, 21+ different book
- `RiskCard` output: max loss $, suggested contracts, spread flag, crush flag, theta warning, research-only reason
- Multi-factor incomplete → `research-only` (never invents size)

## Gateway plugin

Slash commands for Discord/Telegram via Hermes gateway:
```
$risk NVDA          → bankroll-aware risk card
$scan intraday       → run scan, Discord report
$pnl                 → P&L summary
$gaps                → pre-market gaps
$econ                → economic calendar
$accuracy            → signal accuracy
$sources             → configured sources + bankroll
```
`route_message(message)` → response string or None. `get_help_text()` → markdown help.

## Report contract

Align with `discord-report-format`: bold header + ET time, bold sections, `━━━━` separators, `$TICKER · bias · score · sources`. Empty → `[SILENT]`. Ops failure with no content → short `❌` line.

## Greenfield sequence (updated Phase 5)

1. Private `gh repo create` + local init
2. `laws.md` + `AGENTS.md` first (binding rules before code)
3. Docs + configs (`sources.yaml`, `schedule.yaml`, `bankroll.yaml`, `alerts.yaml`)
4. `knowledge/` tree: policy, strategy/playbooks, strategy/frameworks, notes, templates, lessons, journal
5. Pure functions + pytest (all offline, no network)
6. Wire sources one at a time into pipeline; verify each
7. Wire intelligence modules behind config toggles
8. Live morning smoke; fix noise from real output
9. 102 tests passing; commit/push each phase
10. Register 5 weekday crons; note first auto-run (weekend create → next weekday)
11. Gateway plugin last (depends on all modules existing)

## Pitfalls

| Pitfall | Fix |
|---------|-----|
| YAML `ON`/`NO` bool crash | Quote tokens; skip bools in blocklist |
| Transcript standalone flood | Title/desc standalone; cashtag-only transcript |
| Reddit 403 | old/api host fallbacks |
| Handle 404 | ytsearch → channel_id |
| requests bumps past Hermes | Pin `requests==2.33.0` |
| Cron agent chatter | Final message exactly CLI stdout |
| Sports skill reused for equities | Keep domains separate |
| Gateway handler defined after COMMANDS list | Define all `_handle_*` functions BEFORE the `COMMANDS` list that references them |
| `GapSignal` dataclass init missing optional field | Always pass all optional fields explicitly in tests: `pre_market_volume=None` |
| New source not in `SourceKind` Literal | Add to `models.py` SourceKind, `sources/__init__.py`, and `SOURCE_NAMES` in pipeline |
| `extra_blocks` not in `format_discord()` signature | Add `extra_blocks: list[str] \| None = None` parameter and append loop at end of function |
| Module import fails in pipeline mid-scan | Wrap optional modules in try/except; add `enabled` config toggle per module in `sources.yaml` |
| SQLite `:memory:` data lost between connections | Each `_connect(":memory:")` opens a NEW in-memory DB. For tests needing shared state across calls, use `tempfile.mkstemp(suffix=".db")` + `os.close(fd)` + `os.unlink(path)` to let sqlite create fresh, then `os.unlink(path)` in finally. |
| Windows `NamedTemporaryFile` holds open handle | `with tempfile.NamedTemporaryFile(...) as f:` keeps the file locked. SQLite can't open it. Use `fd, path = tempfile.mkstemp(...); os.close(fd)` instead. |
| Patch tool escape-drift on quoted strings | When old_string/new_string contain `\"` that don't match the file, re-read the file segment with `read_file` and pass the literal content without backslash-escaping quotes. |
| `mark_closed` uses wrong column name | Ensure SQL references `acted_on`, not `act_on` — both exist in the schema but only `acted_on` is the column name. |
| `_build_contract` returns `strike=None` when `spot=None` | Pass a `ref_price = spot or 100.0` fallback before calling the contract builder — no chain data + no spot = no strike. |
| `signal_calls._build_contract` called with `None` spot from empty `signal.extras` | In `generate_recommendation()`, set `ref_price = spot or 100.0` before passing to `_build_contract()` — `spot` is `None` when signal has no market data in extras. |
| `generate_calls_from_scan` not imported in CLI | Import `from .signal_calls import generate_calls_from_scan, format_all_calls, format_premarket_briefing` in cli.py. |
| Trigger watch cron delivers even when silent | Use `no_agent=true` with a script that prints `[SILENT]` when no triggers. Verbose scripts will spam Discord every 15 min. |
| Signal calls not in pipeline extra_blocks | Add `rec_block, live_block, ledger_block` to the `extra_blocks` list in pipeline's `format_discord()` call. |
| Webull exchange prefix wrong for ticker | Keep a static `_WEBULL_EXCHANGE_MAP` (80+ tickers: nasdaq/nyse/nysearca) with `nasdaq` default. Verify URL with `requests.get(url)` → 200. QQQ is `nasdaq-qqq`, NOT `nysearca-qqq`. |
| Formatting Webull links in Discord | Use markdown links `[$NVDA](https://www.webull.com/quote/nasdaq-nvda)` — no HTML, no plain URLs. Contract links go to `/options` chain page. Add `[Open WebTrade](https://app.webull.com/)` footer link. |
| Patch tool escapes drift on multi-line strings | When inserting large multi-line formatter functions (with emoji, `━` separators, f-strings containing quotes), use `execute_code` with `pathlib.Path.write_text()` + `py_compile.compile()` verification instead of `patch` — fuzzy matching mangles indentation on long blocks. |

## Phase 5 noise tickers (live-verified 2026-08-09)

Added to DEFAULT_STOP after real scan runs showed these as top "tickers" — they're common English words caught by standalone ALLCAPS extraction:
- `ZERO`, `FIND`, `PICK`, `VIP`, `WORKS`, `BOOK`, `US`
- Also: `TODAY` (duplicate), `YEAR` (duplicate), `INTO` (duplicate) — already in stop set

## Production pointer

- Repo: `https://github.com/pmb2/stock-sniffer` (private)
- Path: `${USER_HOME}/Documents/github/stock-sniffer`
- CLI: `python -m stocksniffer.cli scan --mode morning|intraday|evening --format discord`
- Risk: `python -m stocksniffer.cli risk --ticker NVDA --bias bullish`
- Recs: `python -m stocksniffer.cli recs --ticker NVDA --acted --json`
- Act: `python -m stocksniffer.cli act --rec-id 20260810-NVDA --price 3.20`
- Close: `python -m stocksniffer.cli close --rec-id 20260810-NVDA --price 4.50 --reason win_t1`
- Live: `python -m stocksniffer.cli live --auto-close`
- Ledger: `python -m stocksniffer.cli ledger`
- Gaps: `python -m stocksniffer.cli gaps`
- Econ: `python -m stocksniffer.cli econ --window 7`
- Accuracy: `python -m stocksniffer.cli accuracy --days 30`
- P&L: `python -m stocksniffer.cli pnl`
- Paper: `python -m stocksniffer.cli paper`
- Correlation: `python -m stocksniffer.cli correlation`
- Backtest: `python -m stocksniffer.cli backtest`
- Calls: `python -m stocksniffer.cli calls --mode morning|intraday`
- Moves: `python -m stocksniffer.cli moves --mode morning|intraday|evening --limit 10` (Suggested Moves briefing with Webull links)
- Trigger: `python -m stocksniffer.cli trigger-watch`
- Test: `python -m pytest -q` (125 tests, all offline)

## Related skills

- `a betting-pipeline skill` — multi-scan/cron/Discord DNA, MLB sources
- `discord-report-format` — delivery + `[SILENT]`
- `youtube` — transcript batch patterns
- `web-scraping-scrapling` — browser fetch if public Reddit also fails
