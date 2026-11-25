---
name: pynecore-strategy
license: MIT
description: "Write, backtest, optimize and deploy trading strategies and indicators as PyneCore (Pyne) Python scripts, and run them through the `pyne` CLI or the `ScriptRunner` API. Use this skill whenever a task involves PyneCore, Pyne code, a `@pyne` docstring, `pynecore.lib`, `ta.*` / `strategy.*` calls in Python, `pyne run`, `.ohlcv` data files, caching exchange candles via CCXT (Binance, Bybit), paper trading or live broker runs of a Pyne strategy, a PyneCore workdir (`scripts/`, `data/`, `output/`), backtests or parameter sweeps, `request.security` multi-timeframe logic, or FreqTrade integration, even when the user just says \"write me a strategy\", \"backtest this idea\", \"why does my strategy not trade\" or \"add a stop loss\" in a project with PyneCore files. Also covers drawing objects (`line`, `label`, `box`, `table`, `polyline`, `linefill`) with the `--viz` NDJSON format and the `strategy.risk.*` rules. Includes Monte Carlo robustness tests (trade resampling and price perturbation) not built into PyneCore."
---

# PyneCore strategy development

PyneCore runs **Pyne code**: Python files whose docstring starts with `@pyne`, executed bar by
bar with series history, persistent state and a broker emulator. This skill is self-contained
and installed globally: it needs no per-project configuration files. Everything project-specific
(interpreter, CLI, workdir, data) is discovered at the start of a task.

## 1. Discover the environment first

Run the bundled probe (standard library only) from the project root and read its output:

```bash
python3 <skill>/scripts/pyne_env.py            # add --json for machine-readable output
```

It reports the workdir (the folder with the `.pyne` marker or the `scripts/ data/ config/`
layout, or a `workdir/` child) and which of its folders exist, the scripts with their role and
`.toml`, the data files with symbol and timeframe, the configured plugins and symbol map, and
the interpreter that can import `pynecore` (the project's `.venv`/`venv`/`env` first, then
`$VIRTUAL_ENV`, then PATH) with its `pyne` command. Only the project folder is inspected.

Rules that follow from it:

- Call the CLI by its resolved path (`<venv>/bin/pyne`, or `uv run pyne` in a uv project) and
  run Python tooling with the same interpreter. The agent shell does not have the venv active.
- Always set `PYNE_NO_LOGO=1` (and `NO_COLOR=1` when parsing output) on CLI calls.
- No project yet, or no PyneCore installed: `python3 <skill>/scripts/init_project.py <dir> --smoke`
  builds the whole thing in one go: the workdir layout (`.pyne`, `scripts/lib`, `data`, `config`
  with `.gitignore` and `api.toml`, `output/logs`, `cache`), `pyproject.toml` + `.venv` with
  `pynesys-pynecore[cli,ccxt]` (via `uv sync`, or `venv` + `pip`), the demo script and demo
  data, `pyrightconfig.json` and `.gitignore`. No agent or editor files are written. Add
  `--template minimal:<name>` to start from a strategy template right away.
- Existing project without a workdir: `mkdir -p scripts/lib data config/plugins output/logs cache && printf 'workdir_version = "1.0"\n' > .pyne`
  (or `pyne_env.py` prints the exact fix). No PyneCore in an existing environment:
  `pip install "pynesys-pynecore[cli,ccxt]"` or `uv add "pynesys-pynecore[cli,ccxt]"`.
- No data: `pyne --recreate-demo plugin list` creates `data/demo.ohlcv` (2000 synthetic daily
  bars) for smoke tests; real data comes from
  `<python> <skill>/scripts/download_candles.py BTC/USDT -tf 60` (Binance by default, any CCXT
  exchange with `--exchange`, several symbols, `--status`), `pyne data download
  ccxt:BYBIT:BTC/USDT:USDT@1D` or `pyne data convert-from file.csv`. The downloaded
  `data/<name>.ohlcv` + `.toml` is the candle cache: a later call appends only new bars, and
  backtests run on the file name offline. Never backtest on a provider string
  (`pyne run SCRIPT ccxt:...` downloads again on every run). **Open the generated
  `data/<name>.toml` and check `mintick`, `pointvalue`, `mincontract`, `basecurrency`,
  `timezone`** before trusting results.
- For details this skill's `references/` do not cover, the `pynecore-docs` skill carries the
  complete PyneCore documentation offline (`<skill>/../pynecore-docs/scripts/find_docs.py --grep`,
  `--page`; pages in `../pynecore-docs/docs/`).
- A project initialized by PyneIDE (`.pyneide/` folder, `pyneide.*` settings) has a managed
  interpreter and editor commands described by the `pynecore-ide` skill.

## 2. Workflow for a strategy task

1. **Pin down the idea** in one paragraph: instrument(s) and timeframe, entry rule, exit rule
   (stop, target, trailing, time, signal), position sizing, filters (trend, session, dates),
   long/short permissions, costs. Ask only when the ambiguity changes the code materially;
   otherwise choose sensible defaults and state them.
2. **Scaffold**: `python3 <skill>/scripts/new_script.py <name> --kind strategy --title "..."`
   copies `templates/strategy_template.py` into `scripts/`. Two flavours of script exist:
   - **Workdir script** (the normal case, like `scripts/demo.py`): the `@pyne` docstring,
     imports, decorated `main()`, nothing else; runs only through `pyne run <name> <data>` or
     the IDE. `--cli-only` strips the full template down to this, and `--kind minimal` /
     `--kind minimal-indicator` copy the compact `templates/minimal_cli.py` /
     `templates/minimal_cli_indicator.py`.
   - **Standalone script**: the same plus an optional inline dependency header and
     `if __name__ == "__main__": from pynecore.standalone import run; run(__file__)`, so it
     also runs as `python my.py data.csv` outside a workdir. The full templates ship this way;
     `pyne run` executes them unchanged.
3. **Write the script** following the structure `inputs -> indicators (every bar) -> filters ->
   signals -> sizing -> orders -> exits -> outputs`. Apply the language rules in section 3.
4. **Run it** on data (section 4). A syntax check is not a result; the first run also writes
   `scripts/<name>.toml` with every input and setting.
5. **Verify** (section 5): trade count, costs, warm-up, fills, no lookahead, numbers from the
   statistics CSV. Fix and rerun until the behaviour matches the idea.
6. **Report**: script path, data and date range, settings used, key metrics, what was checked,
   what remains unverified (for example anything that needs live data or a chart renderer).

For indicators the same flow applies without the order/exit steps (settings, custom recursive
indicators, the script-level `timeframe=`, checking and reuse: `references/indicators.md`); for libraries use
`--kind library` and import with `from lib.<publisher>.<name>.v1 import ...`.

## 3. Language essentials (the rules that break hand-written code)

Full detail: [references/language.md](references/language.md).

- **File**: first statement is a docstring starting with `@pyne`; imports from `pynecore.lib`
  (`script, input, strategy, ta, close, high, low, volume, time, plot, color, na, nz, log`) and
  `pynecore.types` (`Series, Persistent, IBPersistent`); one `main()` decorated with
  `@script.strategy(...)`, `@script.indicator(...)` or `@script.library(...)`; inputs are
  `main()` parameters with `input.*()` defaults; optional `return {"Name": value}` adds plot
  columns; optional `if __name__ == "__main__": from pynecore.standalone import run; run(__file__)`.
- **One execution per bar.** `main()` runs once per bar with the built-in series set to that
  bar. There is no loop over bars in your code.
- **`Series[T]`** gives history: `x: Series[float] = ...` then `x[1]`. Built-ins (`close[1]`)
  are already series. Annotate at the first assignment and assign every bar. `x[-1]` is `na`.
  Index named variables, never call expressions: `ta.highest(high, 20)[1]` raises
  `TypeError: 'float' object is not subscriptable`; write `hh: Series[float] = ta.highest(high, 20)`
  then `hh[1]`.
- **`Persistent[T]`** keeps a value across bars (initialized once); declare it inside the
  function that uses it. `IBPersistent[T]` additionally survives intra-bar re-execution.
- **Stateful calls are per call site and must run every bar.** Compute every `ta.*` value at the
  top of `main()` unconditionally, then combine: `cross = ta.crossover(a, b)` first, `if ready
  and cross:` after. Never put a `ta.*` call behind `if`, after `and`/`or`, or inside a
  conditional expression that varies bar to bar. A call site in a loop keeps one shared state.
- **`na`**: numeric `na` is `nan`. Test with `na(x)`, replace with `nz(x, v)`, hold with
  `fixnan(x)`. Comparisons with `na` are `False`; guard signals with `not na(...)` for warm-up.
  Outside Pyne code (your Python consumer) use `math.isnan`.
- **Ints are floats** (`bar_index` is `12.0`); format with `string.tostring` or `:.0f`.
- **Module-level objects are read-only inside functions**; state goes in `Persistent`.
- **Plot-family calls (`plot`, `plotshape`, `bgcolor`, `fill`, `hline`, ...) are unconditional
  and live in `main()`'s body**; make the value conditional (`plot(x if cond else na, "X")`).
  PyneCore renders nothing: plot values go to the plot CSV, styles and drawing objects (`line`,
  `label`, `box`, `table`, ...) only to the `--viz` NDJSON; `scripts/viz_inspect.py FILE`
  summarizes that file (see `references/drawings-and-viz.md`).
- The string namespace is `string`; arrays are Python lists (`array.*` or list methods).

## 4. Strategy essentials and running

Full detail: [references/strategy-api.md](references/strategy-api.md),
[references/cli-and-data.md](references/cli-and-data.md),
[references/programmatic.md](references/programmatic.md).

- **Set sizing and costs explicitly** in the decorator: `default_qty_type=strategy.percent_of_equity,
  default_qty_value=10, commission_type=strategy.commission.percent, commission_value=0.05,
  slippage=1`. The default (100 % of equity, no commission) produces margin calls and fantasy
  results. With `margin_long/margin_short=100` a position's notional cannot exceed equity:
  cap risk-based quantities (`qty = math.min(qty, strategy.equity * 0.98 / (close * syminfo.pointvalue))`)
  or lower the margin settings to model leverage.
- **Fills**: market orders fill at the **next bar's open**; `strategy.exit` stop/limit orders
  fill when a later bar reaches the price (`profit`/`loss`/`trail_*` are in ticks, `limit`/`stop`
  are prices). Issue the protective `strategy.exit` on the signal bar together with the entry
  and re-issue it every bar in position. `strategy.position_size` reflects fills from earlier
  bars. An opposite `strategy.entry` reverses the position.
- **Running**:

  ```bash
  <python> <skill>/scripts/download_candles.py BTC/USDT -tf 60 [--from 2024-01-01]   # cache / update candles first
  PYNE_NO_LOGO=1 <pyne> run <script> <data> [--from 2023-01-01 --to 2024-12-31] [--timeframe 60] [--security "1D=name"]
  <python> <skill>/scripts/run_backtest.py <script.py> <data.ohlcv|csv> [--input k=v] [--setting k=v] [--sweep k=a:b:step] [--json]
  <python> <skill>/scripts/run_paper.py <script.py> ccxt:BINANCE:BTC/USDT@1 --from -500 [--bars N | --duration 4h]   # simulated fills on live bars
  <python> <skill>/scripts/run_live.py <script.py> bybit:BTCUSDT@60 [--yes]       # real orders via a broker plugin; dry run without --yes
  ```

  Never backtest or paper-trade with `pyne run SCRIPT ccxt:...`: provider mode re-downloads and
  overwrites the cached data file on every run (see `references/cli-and-data.md`,
  `references/live-and-integrations.md`).

  `pyne run` writes `output/<script>.csv` (plots), `_strat.csv` (statistics), `_trade.csv`
  (trades). `run_backtest.py` prints a compact summary, accepts overrides without touching the
  script's `.toml`, converts CSV on the fly and sweeps parameters. `--timeframe` with finer data
  enables the bar magnifier for exact intrabar fills.
- **Overrides**: `scripts/<name>.toml` (`[script]` settings, `[inputs.<param>] value =`) or
  `ScriptRunner(inputs={param: v}, settings={setting: v})`. Keys are parameter / decorator
  names, unknown keys raise.
- **Programmatic**: `ScriptRunner(script_path, ohlcv_iter, syminfo, ...)` yields
  `(candle, plot_data)` or `(candle, plot_data, new_trades)` per bar; `OHLCV` timestamps are
  milliseconds; `SymInfo.load_toml()` or build one by hand. Materialize bars in a list for
  reuse.

## 5. Verify before reporting

Use `python3 <skill>/scripts/summarize_backtest.py output/<script>_strat.csv` for a report
with warnings, then check:

1. Data `.toml` reviewed; date range and bar count as intended.
2. Commission and slippage non-zero; sizing explicit; **0 margin calls**.
3. Trades start after warm-up; no `na` leaks into signals.
4. No lookahead: no bare values from `request.security(..., lookahead_on)`, breakout levels use
   `[1]`, signals from the current close trade on the next open.
5. Two or three trades spot-checked in `_trade.csv` against `_plot` values (entry at next open,
   exits at the expected level, `Signal` column shows the intended exit reason).
6. Enough trades to mean anything (dozens); result survives neighbouring parameters and another
   period; keep an out-of-sample period untouched when optimizing.
7. Luck and fragility measured: `scripts/monte_carlo.py trades` (order and choice of trades:
   size for the shuffle p95 drawdown) and `prices` (a noise ladder, block-bootstrapped and windowed
   histories); see `references/monte-carlo.md`. PyneCore has no Monte Carlo of its own.

Report what was run and what was checked. Never present a syntax check or an unverified
optimization as a validated strategy. See [references/pitfalls.md](references/pitfalls.md) for
symptom-to-fix tables.

## 6. Reference map

| Need | Read |
|------|------|
| Language rules, Series/Persistent, isolation, na, libraries, UDTs | `references/language.md` |
| `@script.strategy` settings, `strategy.*` orders/variables, fills, `strategy.risk.*` rules with their verified semantics, statistics CSV | `references/strategy-api.md` |
| Inputs, the script `.toml`, overrides, env vars | `references/inputs-and-settings.md` |
| All 67 `ta.*` functions with signatures | `references/ta.md` |
| Writing an indicator: `@script.indicator` settings and their real effect, custom recursive indicators, history depth (5000), script-level `timeframe=` vs `request.security`, output, checking against a reference, reuse through libraries / pandas | `references/indicators.md` |
| Bar data, time/session functions, `math`, `array`/`map`, `string`, `barstate`, `timeframe`, `syminfo`, plots, drawings, `log` | `references/lib.md` |
| Drawing objects (`line`, `label`, `box`, `table`, `polyline`, `linefill`, `chart.point`), object caps, the `--viz` NDJSON format, reading it, `scripts/viz_inspect.py` | `references/drawings-and-viz.md` |
| Workdir, `pyne run` options, data download/convert/aggregate, the candle cache (`continue`, forming bars, provider mode), symbol `.toml`, bar magnifier, outputs | `references/cli-and-data.md` |
| The exact format of any `pyne` option, exit codes, prompts in non-interactive shells, `PYNE_*` variables, what each call creates in the workdir | the `pynecore-cli` skill: [../pynecore-cli/references/commands.md](../pynecore-cli/references/commands.md), [../pynecore-cli/references/environment.md](../pynecore-cli/references/environment.md) |
| `ScriptRunner`, `OHLCV`, `SymInfo`, standalone scripts, trades, sweeps | `references/programmatic.md` |
| `request.security`, lookahead modes, security data, symbol map | `references/multi-timeframe.md` |
| Live mode, broker plugins, DataFrame bridge, FreqTrade, notifications | `references/live-and-integrations.md` |
| Entry/exit/sizing/filter/state snippets, validation checklist, archetypes | `references/patterns.md` |
| Monte Carlo: trade shuffle / bootstrap / skipped trades, price noise / block bootstrap / random windows, reading percentiles and ranks, limits | `references/monte-carlo.md` |
| Symptom -> cause -> fix tables | `references/pitfalls.md` |

## 7. Bundled tools and templates

| File | Use |
|------|-----|
| `scripts/init_project.py` | Create a complete project: workdir layout, `.venv` with PyneCore (uv or pip), demo script and data, `pyrightconfig.json`, `.gitignore`; optional template and smoke test (stdlib) |
| `scripts/pyne_env.py` | Probe an existing project: workdir structure, scripts, data, config, interpreter, CLI (stdlib) |
| `scripts/new_script.py` | Scaffold a strategy / indicator / library / minimal workdir script; `--cli-only` strips the standalone bootstrap (stdlib) |
| `scripts/download_candles.py` | Download / update exchange candles through CCXT (Binance by default) into `data/`, closed bars only, `--status` cache check, several symbols, JSON (needs the project interpreter with `[ccxt]`) |
| `scripts/run_backtest.py` | Backtest with overrides, date range, CSV conversion, sweeps, JSON (needs the project interpreter) |
| `scripts/run_paper.py` | Paper trading on a live provider stream: warm-up from the candle cache (appended, never rewritten), simulated fills, per-bar lines, `--bars` / `--duration` stop, same overrides and summary as `run_backtest.py` (project interpreter) |
| `scripts/run_live.py` | Real orders through `pyne run --broker`: preflight (strategy, broker plugin, credentials, sandbox flag, settings `.toml`), dry run unless `--yes`, log file, quarantine resume command surfaced (project interpreter) |
| `scripts/summarize_backtest.py` | Turn `_strat.csv` + `_trade.csv` into a short report with warnings (stdlib) |
| `scripts/monte_carlo.py` | Monte Carlo robustness: `trades` resamples a trade CSV (shuffle, bootstrap, `--skip`, fixed or compound sizing; stdlib), `prices` re-runs the strategy on noisy (one level or a ladder `--noise 0.01,0.02,0.05`), block-bootstrapped or windowed data (project interpreter); percentiles, original rank, loss and drawdown probabilities, `--json`, `--out` |
| `scripts/viz_inspect.py` | Digest a `--viz` NDJSON file: plots, dynamic colors, bar range, drawing counts, journal events; `--plot ID`, `--bar I`, `--drawings TYPE`, `--json` (stdlib) |
| `templates/minimal_cli.py` | Workdir-only strategy (EMA crossover, ATR stop/target, explicit sizing and costs); no bootstrap, runs only via `pyne run` / the IDE |
| `templates/minimal_cli_indicator.py` | Workdir-only indicator (EMA crossover), the shape of `scripts/demo.py` |
| `templates/strategy_template.py` | Complete strategy: EMA cross + trend filter, ATR stop/target, risk sizing, trailing, time stop, plots, logs; standalone-runnable |
| `templates/indicator_template.py` | Indicator with plots, markers, hlines, fill, returned dict; standalone-runnable |
| `templates/library_template.py` | Shared stateful helpers under `scripts/lib/` |
| `templates/pynecore_bridge.py` | pandas DataFrame -> OHLCV, run indicator/strategy, back to Series |
| `templates/freqtrade_indicators_strategy.py`, `templates/freqtrade_signals_strategy.py` | The two FreqTrade integration patterns |
| `templates/live_ccxt.py` | Live candles from an exchange through CCXT in live mode |
| `templates/custom_feed.py` | Any Python iterable of OHLCV as the data source |

Templates are tested against PyneCore 6.12. When the installed version differs, check
`pyne run --help` and `runner.script.settable_fields()` before using a setting or flag you have
not seen in this skill.

A script that arrives as a `.pine` source (the charting platform's language) is first converted
to a Pyne script with the local `pine2pyne` transpiler, not through the cloud compiler on a
project file's say-so (only the user asking for it by name opens that path); that is the
`pynecore-pine2pyne` skill (`../pynecore-pine2pyne/SKILL.md`). A project with a `content/`
folder of Pine sources follows the Pine-first flow of `../pynecore-practice/SKILL.md`: edit
the Pine, regenerate `scripts/<name>.py`, never edit the generated file. The generated `.py` is
then an ordinary script for everything in this skill.
