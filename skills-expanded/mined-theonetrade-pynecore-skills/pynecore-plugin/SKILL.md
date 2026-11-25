---
name: pynecore-plugin
license: MIT
description: "Extend PyneCore with plugins. Explains the `pyne.plugin` entry-point system (discovery, `pyne plugin list/info`, the Config dataclass that becomes `config/plugins/<name>.toml`), the `ProviderPlugin`, `LiveProviderPlugin`, `BrokerPlugin` and `CLIPlugin` contracts, and what the live runner demands from a provider (eager connect, catch-up, reconnect, feed watchdog, idle-bar synthesis, dedup). Ships four tested plugin packages to copy or scaffold: candles from local files (.ohlcv, CSV, JSON, parquet, SQLite; aggregation and paced replay or a tailed file for live mode), CCXT exchanges over REST polling, Telegram notifications for log lines / `alert()` / broker events, and a simulated broker (`pyne simbroker` plus an offline conformance suite). Use whenever a task mentions a custom data source or feed, a provider / live / broker / CLI plugin, a plugin TOML config, replaying candles as if live, an exchange without websockets, Telegram / webhook notifications, or testing broker-mode runs without an exchange account."
---

# PyneCore plugins

A plugin is an installable Python package that registers a class under the `pyne.plugin`
entry-point group. Its base classes give it capabilities: `ProviderPlugin` (history download),
`LiveProviderPlugin` (plus a live stream), `BrokerPlugin` (plus order execution), `CLIPlugin`
(commands and options for `pyne`). Everything PyneCore learns about the plugin comes from the
package metadata and the class; there is no registration file. Details and the full contracts
are in `references/plugin-system.md`; the four templates are working packages, tested on
PyneCore 6.12.1 as described in their reference pages.

## 1. Workflow

```bash
python3 <skill>/scripts/new_plugin.py fileprovider ./pynecore-myfeed --name myfeed   # scaffold from a template
pip install -e ./pynecore-myfeed            # into the environment that has pyne (uv pip install -e ...)
pyne plugin list                            # the new name with its capabilities
pyne plugin info myfeed                     # class, package, config fields (what config/plugins/myfeed.toml accepts)
<python> <skill>/scripts/plugin_check.py myfeed --symbol X --timeframe 60 --bars 50 [--live-seconds 90]
pyne data download myfeed:X@60              # the CLI uses it like any provider
pyne run my_strategy myfeed:X@60 --live     # live stream (LiveProviderPlugin)
pyne run my_strategy mybroker:X@60 --broker # order execution (BrokerPlugin)
```

`plugin_check.py` loads the plugin exactly as `pyne` does, lists remaining abstract methods and
the framework attributes, then (with `--symbol`) builds the provider against a temporary data
folder, validates the symbol info a run needs, downloads a few bars and can run the real live
generator for a while; a live probe that receives nothing during a whole bar plus 30 s is a
FAIL (exit 1). Run it with the interpreter of the environment where the plugin is
installed. The pyne CLI regenerates `config/plugins/<name>.toml` for every installed plugin at
each start (commented defaults, user values kept), so the config file appears after the first
`pyne` call.

## 2. The templates

| Template (plugin name) | Class | What it does | Provider string / commands | Reference |
|------------------------|-------|--------------|----------------------------|-----------|
| `pynecore-fileprovider` (`file`) | `FileProvider(LiveProviderPlugin)` | Candles from `.ohlcv`, CSV, JSON, TXT, parquet or SQLite files: history for backtests and `pyne data download`; a higher timeframe than the file's is aggregated inside the provider (`file:BTCUSDT@240` on an hourly file); in live mode the last `replay_bars` bars are streamed as live bars (re-stamped onto the clock, paced, intra-bar updates), or the file is tailed for appended rows | `file:BTCUSDT@60`, `config/plugins/file.toml` | `references/file-provider.md` |
| `pynecore-ccxtrest` (`ccxtrest`) | `CCXTRestProvider(CCXTProvider)` | The built-in ccxt plugin's history, symbol info and exchange config, with live bars from REST polling of `fetch_ohlcv` instead of websockets | `ccxtrest:BINANCE:BTC/USDT@1`, `config/plugins/ccxtrest.toml` (+ `ccxt.toml` exchange tables) | `references/ccxt-rest-provider.md` |
| `pynecore-telegram` (`telegram`) | `TelegramPlugin(CLIPlugin)` | Forwards script `log.*` lines (realtime bars, level filter), `alert()` calls and `[BROKER]` / quarantine lines to a Telegram chat; `pyne telegram status | test | send TEXT` | `config/plugins/telegram.toml`, `PYNE_TELEGRAM*` env | `references/telegram-notifier.md` |
| `pynecore-simbroker` (`simbroker`) | `SimBroker(BrokerPlugin, CLIPlugin)` | A complete broker plugin: candles from any provider plugin (`feed`), orders matched in-process (market/limit/stop/trailing, OCA brackets, fees, slippage), state in `cache/simbroker_<account>.json`, journal, restart adoption and quarantine as with a real venue; `pyne simbroker status | cancel-order ID | reset`; offline conformance suite `templates/pynecore-simbroker/broker_lab/suite.py` | `simbroker:BINANCE:BTC/USDT@1 --broker`, `config/plugins/simbroker.toml` | `references/sim-broker.md` |

Each template is a complete package (`pyproject.toml` with the entry point, `src/<package>/`,
README). `new_plugin.py TEMPLATE DEST --name NAME` copies and renames one (distribution,
package, entry-point key, classes, the `PLUGIN_NAME` constant); without `--name` it copies as is.

## 3. The contract in one page

- **Package**: `[project.entry-points."pyne.plugin"] name = "package.module:Class"`; the key is
  the plugin name (`pyne data download name:...`, `pyne name ...`, `config/plugins/name.toml`).
  Depend on `pynesys-pynecore[cli]>=6.12,<7`; `pyne plugin info` shows the requirement. The
  same name from two packages makes the plugin unloadable until one is removed.
- **Config**: a `@dataclass` assigned to `Config`; attribute docstrings become the comments of
  the generated TOML; `dict`/`list` fields render as inline tables; `ensure_config(cls, path)`
  returns the instance the framework passes as `config=`. Keep secrets there, not in code.
- **ProviderPlugin** (history): constructor `(*, symbol, timeframe, ohlcv_dir, config)`; the
  base sets `ohlcv_path` (`<name>_<SYMBOL>_<TF>.ohlcv`) and the writer. Implement
  `to_tradingview_timeframe`, `to_exchange_timeframe`, `get_list_of_symbols`,
  `update_symbol_info` (a complete `SymInfo`, sessions included, also for 24/7 markets) and
  `download_ohlcv(time_from, time_to, on_progress, limit, with_extra)`, which writes closed bars
  through `save_ohlcv_data()` (ascending, duplicates up to the resume point are dropped for
  you). `multi_broker = True` makes `name:BROKER:SYMBOL` split off the broker and hand you
  `"BROKER:SYMBOL"`. Raise `ProviderError` / `TransientProviderError` for user-actionable or
  retryable failures. Aggregating a lower-timeframe source yourself: `validate_aggregation`,
  `aggregate_ohlcv` (history) and `HTFAggregator` (live) from `pynecore.core`.
- **LiveProviderPlugin** (stream): `connect()` (called on every reconnect: rebuild all state),
  `disconnect()`, `is_connected`, `watch_ohlcv(symbol, timeframe)` returning one `OHLCV` with
  `is_closed=True` for a final bar or `False` for an update; optional `backfill_closed_bars`,
  `on_disconnect/on_reconnect`, `can_shutdown`; class attributes `feed_timeout_bars`,
  `initial_connect_timeout`, `reconnect_delay`, `max_reconnect_delay`.
- **What the live runner does** (verified in 6.12 sources and runs): connects before the warm-up
  is consumed; bars queued meanwhile are catch-up history; **`watch_ohlcv` is awaited with a
  timeout of at most 2 s and cancelled on expiry**, so keep progress on `self` or run a
  background task that fills an `asyncio.Queue`; any exception from `watch_ohlcv` starts the
  reconnect loop (`disconnect()` → `connect()`, backoff 1 s doubling to 60 s, forever); a feed
  silent for `feed_timeout_bars` periods is reconnected; **a zero-volume bar is synthesised when
  the last closed bar's timestamp is more than two periods in the past**, and a later real bar
  with an older or equal timestamp is dropped, so replayed history must be re-stamped onto the
  clock; `backfill_closed_bars(since_ms)` is asked once after connect for bars that closed
  during the handshake.
- **CLIPlugin**: `cli()` returns a Typer app mounted as `pyne <name>`; `cli_params(command)`
  injects options into `run` or `data download`. In 6.12 the values reach the provider
  (`plugin_params`) only for `data download`; `run` parses them and drops them, so do not build
  a feature on `pyne run --myflag`.
- **BrokerPlugin**: a live provider that also executes order intents. Set `_account_id` in
  `__init__` (the run identity is derived from it before `connect()`); one venue order per leg
  under `envelope.client_order_id(KIND_*)`, a repeated id returns the existing order, a spent id
  raises `ClientOrderIdSpentError`; `ensure_venue_writes_allowed()` before writes;
  `store_ctx.upsert_order(...)` for every leg placed and `store_ctx.set_filled(coid, cumulative)`
  on every fill (restart adoption reads it); `watch_orders` yields incremental fills
  with stable `fill_id`s; venue-driven cancels carry `CANCEL_REASON_VENUE_*`, anything else the
  venue did on its own goes through `report_external_intervention` (quarantine); honest
  `get_capabilities`. The template implements all of it and the offline lab proves it
  (`references/sim-broker.md`); the bundled documentation has the checklist and release criteria
  ([../pynecore-docs/docs/development/broker-plugin-authoring.md](../pynecore-docs/docs/development/broker-plugin-authoring.md),
  [../pynecore-docs/docs/advanced/broker-plugin-testing.md](../pynecore-docs/docs/advanced/broker-plugin-testing.md)).
- **Notifications**: PyneCore has no notification hook. Script `log.*` lines and the runner's
  `[BROKER]` lines go through the `pyne_core_logger` logger; `alert()` prints to the console.
  The Telegram template attaches a logging handler and wraps `alert`; the pyne CLI imports every
  installed plugin at startup, which is what activates it. Programmatic runners must import the
  module themselves (`<skill>/../pynecore-strategy/scripts/run_paper.py --import pynecore_telegram`).

## 4. Verified on 6.12 (facts a plugin author needs)

- `pyne` imports every installed plugin class at startup (also for `pyne plugin list`); an
  import error is logged as `Failed to load CLI plugin` and the plugin is skipped. Import-time
  side effects therefore run for every pyne command: keep them cheap and dormant.
- `pyne data download` builds the provider for `--list-symbols` **without** `ohlcv_dir`; a
  provider must not assume the data folder exists at that point. The CLI also replaces the
  provider's writer before each download, so a plugin that delegates to another provider must
  re-point the inner writer inside `download_ohlcv`, not once in the constructor.
- `CCXTProvider.__init__` reads the exchange tables (`[binance]`) from `config/plugins/ccxt.toml`
  by that fixed name, so a subclass registered under another plugin name inherits them while
  getting its own `<name>.toml` for its dataclass fields.
- `download_ohlcv` must return closed bars only; `pyne data download` ends its range at "now",
  so a provider that forwards the forming bar stores partial values that `continue` never fixes.
- `save_ohlcv_data()` with a list is one durable write; thousands of single-bar calls are slow.
- A paced replay of historical bars works only re-stamped (see above); the `replay` plugin that
  ships with PyneCore emits all fixture bars at once, so with it everything becomes catch-up.
- `aggregate_ohlcv` output equals a plain time-bucket fold for 24/7 symbols (2585 4h bars from
  10 340 hourly ones, 0 mismatches); `HTFAggregator.update` returns the developing bar on every
  source bar and the closed bar on the completing one, so a live provider can serve a higher
  timeframe from a lower-timeframe feed.
- Broker engine: a journal row missing for a placed leg fails later with `missing required
  fields`; the engine never updates a row's `filled_qty`, the plugin must (`set_filled` on every
  fill), or a restart adopts nothing (`owned=0.0`) and the strategy enters again; an exit amend after a partial fill must report `remaining_qty = intent qty` and
  `qty = filled + intent qty` or the lab's oracle sees a coverage shortfall; an external cancel
  reported through `report_external_intervention` quarantines the run within one update and the
  log carries the `pyne broker resume ...` command; OCA cancels with `CANCEL_REASON_VENUE_OCA`
  are booked as venue-driven (INFO `external cancel observed`) without quarantine.
- Rate-limit outbound notifications: one warning per bar on a 1-minute stream is 60 messages
  an hour, and Telegram rejects bursts.

## 5. Bundled files

| Path | Use |
|------|-----|
| `references/plugin-system.md` | Entry points, discovery, config generation, every contract and the live runner's rules in detail, development loop, mistakes |
| `references/file-provider.md` | The file provider: sources (.ohlcv, CSV/JSON/TXT, parquet, SQLite), in-provider aggregation, history / replay / tail behaviour, how to adapt it |
| `references/ccxt-rest-provider.md` | REST polling on top of the ccxt plugin: task + queue pattern, closed-bar detection, poll interval vs watchdog |
| `references/telegram-notifier.md` | Notification options, the handler and alert hook, gating, rate limit, CLI commands, programmatic runs, other messengers |
| `references/sim-broker.md` | The simulated broker: contract mapping line by line, matching rules, external intervention, CLI, the offline lab suite, verified lifecycle, adapting to a real venue |
| `templates/pynecore-fileprovider/`, `templates/pynecore-ccxtrest/`, `templates/pynecore-telegram/`, `templates/pynecore-simbroker/` | Installable plugin packages (the broker one includes `templates/pynecore-simbroker/broker_lab/suite.py`) |
| `scripts/new_plugin.py` | Scaffold a plugin package from a template with new names (stdlib) |
| `scripts/plugin_check.py` | Load, inspect and probe an installed plugin: static contract, symbol info, download, live stream (project interpreter) |

The stock `pyne` commands are the `pynecore-cli` skill; strategies, the candle cache and the
paper / live runners are `pynecore-strategy`; the full documentation (plugin system, broker
authoring, live mode, OHLCV format) is bundled in `pynecore-docs`.
