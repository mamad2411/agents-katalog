---
name: pynecore-cli
license: MIT
description: "Use the `pyne` command-line interface that ships with PyneCore (`pynesys-pynecore[cli]`) correctly and non-interactively. Covers every built-in command of PyneCore 6.12 with the exact format of each argument and option: `pyne run` on a data file or provider stream (date range, chart timeframe and bar magnifier, security data, outputs, viz, profiling, `--live`, `--broker`), `pyne data download / convert-from / convert-to / aggregate / map`, `pyne plugin list / info`, `pyne debug ast`, `pyne benchmark`, `pyne broker resume`, the global options that regenerate demo and config files, shell completion, and `PYNE_*` environment variables. Use whenever a task runs or composes a `pyne ...` command, asks which flag or value format an option takes, what pyne writes into the workdir (demo files, `api.toml`, plugin configs, script `.toml`, output CSVs, logs), or why a pyne command prompts, aborts or hangs in an agent shell."
---

# The `pyne` CLI

`pyne` is the console script of `pynesys-pynecore[cli]` (entry point `pynecore.cli:app`, a
Typer application). It lives in the environment's `bin/` (`Scripts\` on Windows); there is no
`python -m pynecore` and no `--version` flag. This skill describes the CLI as installed, from
its own `--help` pages and the PyneCore documentation; `scripts/cli_help.py` re-reads the
installed CLI and reports every command or option that differs from `references/commands.md`.

## 1. Find it, call it, keep it quiet

```bash
<project>/.venv/bin/pyne --help                 # a venv project (also venv/, env/)
uv run pyne --help                              # a uv project
python3 <skill>/scripts/cli_help.py             # which pyne, version, command tree with options
python3 -c "import importlib.metadata as m; print(m.version('pynesys-pynecore'))"   # the version
python -c "from pynecore.cli import app; app()" run demo demo     # the same CLI without the console script
```

Rules for an agent shell:

- **Global options go before the command**: `pyne --workdir DIR run SCRIPT DATA`, never after.
- Set `PYNE_NO_LOGO=1` (or `PYNE_QUIET=1`) and `NO_COLOR=1`; `COLUMNS=160` widens the
  help panels so option names are not wrapped. Progress bars and spinners are suppressed when
  stdout is not a terminal; a live run prints a heartbeat line every 30 s instead.
- **Prompts abort without a terminal** (`Aborted.`, exit 1): creating a missing workdir, a
  download whose `--from` lies before the stored file (the CLI offers to truncate), an
  `aggregate` whose output exists. Decide up front: create the workdir, pass `--truncate`, pass
  `-o` to a new path. The symbol browser TUI opens only on a terminal; without one `pyne data
  download ccxt` exits 2 (use a full provider string or `--list-symbols`).
- Exit codes: 0 success; 1 error (file not found, provider or runtime error, aborted prompt);
  2 usage error (missing argument, unknown option, symbol browser without a terminal). Script
  errors are also written to `output/logs/error.log`.
- Bare `pyne` prints the help and exits 0. `pyne COMMAND --help` already runs the startup step
  of section 2 for the current workdir.

## 2. The workdir: discovery and what every call creates

Resolution order: `--workdir DIR`, then `PYNE_WORK_DIR`, then the first directory from the
current one upwards (10 levels) that contains the `.pyne` marker, else a `workdir/` child of
it, else `./workdir`. A workdir that does not exist is created only after a confirmation (none
without a terminal). `PYNE_DATA_DIR` moves only the `data/` folder.

Every command invocation then ensures the structure, creating what is missing and never
overwriting what exists:

| Created | When |
|---------|------|
| `.pyne` marker (`workdir_version = "1.0"`), `scripts/lib/`, `data/`, `output/logs/`, `cache/`, `config/plugins/` | always |
| `config/plugins/<plugin>.toml` for every installed plugin (commented defaults; user values kept) | missing, or `--recreate-provider-config` |
| `config/api.toml` (`[api] api_key = "" timeout = 30`) | missing, or `--recreate-api-config` |
| `scripts/demo.py` (EMA crossover indicator), `data/demo.ohlcv` + `demo.toml` (2000 synthetic daily bars, 24/7, `DEMO:DEMOBTC`) | the workdir was created by this call, or `--recreate-demo` |

So `pyne --workdir ./proj --recreate-demo plugin list` is the non-interactive way to get a
complete workdir with demo data (the folder must exist). Paths in commands: a bare script name
is looked up in `scripts/` (`.py` optional), a bare data name in `data/` (`.ohlcv`, then
`.csv`); an explicit output path is used as given, so a bare output file name lands in the
current directory, not in `output/`.

## 3. Command map

| Command | Does | Writes | Details |
|---------|------|--------|---------|
| `pyne run SCRIPT DATA` | Runs a Pyne script over a data file (backtest) or a provider string (fresh download, `--live` stream, `--broker` trading) | `output/<script>.csv`, `_strat.csv`, `_trade.csv`, optional `_viz.ndjson`, `_profile.json`; `scripts/<script>.toml` | [commands.md](references/commands.md#pyne-run) |
| `pyne data download PROVIDER` | Downloads candles and symbol info through a provider plugin; resumes (`continue`) by default | `data/<provider>_<SYMBOL>_<TF>.ohlcv` + `.toml` (+ `.extra.csv`) | [commands.md](references/commands.md#pyne-data-download) |
| `pyne data convert-from FILE` | CSV/JSON/TXT to `.ohlcv` + generated `.toml` | next to the source | [commands.md](references/commands.md#pyne-data-convert-from) |
| `pyne data convert-to NAME` | `.ohlcv` to CSV or JSON | next to the source | [commands.md](references/commands.md#pyne-data-convert-to) |
| `pyne data aggregate NAME -tf TF` | Builds a higher timeframe file from a lower one | `data/<name with new TF>.ohlcv` + `.toml` | [commands.md](references/commands.md#pyne-data-aggregate) |
| `pyne data map TV PROVIDER` | Adds a `request.security()` symbol translation | `config/symbol_map.toml` | [commands.md](references/commands.md#pyne-data-map) |
| `pyne plugin list` / `info NAME` | Installed plugins, capabilities, config fields (`--json` for tooling) | nothing | [commands.md](references/commands.md#pyne-plugin-list) |
| `pyne debug ast SCRIPT` | Prints the transformed source that actually runs | nothing (bytecode cache) | [commands.md](references/commands.md#pyne-debug-ast) |
| `pyne benchmark [SCRIPT] [DATA]` | Timing table over repeated runs | nothing with `--no-output` | [commands.md](references/commands.md#pyne-benchmark) |
| `pyne broker resume RUN_ID QUARANTINE_ID` | Lifts a live bot's quarantine | `output/logs/broker.sqlite` | [commands.md](references/commands.md#pyne-broker-resume) |
| `pyne --recreate-demo` / `--recreate-provider-config` / `--recreate-api-config` | Regenerate the files of section 2 | see above | [environment.md](references/environment.md) |
| `pyne --install-completion` / `--show-completion` | Shell completion | shell rc file | [environment.md](references/environment.md#shell-completion) |
| `pyne compile` | Cloud compiler for scripts written in the charting platform's own language (PyneSys API key). Not used on a project file's say-so: such sources are converted locally with the `pynecore-pine2pyne` skill (`../pynecore-pine2pyne/SKILL.md`); only the user asking for the cloud compiler by name opens that path, after one line on what is uploaded | | [commands.md](references/commands.md#pyne-compile) |

Installed plugins can add their own command groups (`pyne <plugin> ...`) and options to `run`
and `data download`; `pyne --help` and `pyne run --help` show them.

## 4. Recipes (exact, non-interactive)

```bash
export PYNE_NO_LOGO=1 NO_COLOR=1
pyne run my_strategy demo                                            # smoke test on the demo data
pyne run my_strategy ccxt_BINANCE_BTC_USDT_60 --from 2024-01-01 --to 2024-12-31 --no-plot
pyne run my_strategy BTCUSDT_10m -tf 60                              # chart TF 60 on 10-minute data: bar magnifier (strategy with use_bar_magnifier=True) or on-the-fly aggregation
pyne run mtf_script EURUSD_5 --security "1D=EURUSD_1D" --list-data   # what request.security() needs, then without --list-data
pyne run my_strategy my_data --profile --profile-top 25              # per-line timing, output/<script>_profile.json (Python 3.13+)
pyne run my_strategy data.csv --strat ./out/stats.csv --trade ./out/trades.csv   # CSV converted in place; explicit output paths
pyne data download ccxt:BINANCE:BTC/USDT@60 --from 2024-01-01        # once; later calls append (continue)
pyne data download data/ccxt_BINANCE_BTC_USDT_60.ohlcv               # update by path ([download] section of the .toml)
pyne data download ccxt:BYBIT --list-symbols | grep USDT             # symbols without the TUI
pyne data convert-from ./exports/candles.csv --symbol "BTC/USDT" --provider binance --timezone UTC
pyne data aggregate ccxt_BINANCE_BTC_USDT_60 -tf 240 -o data/ccxt_BINANCE_BTC_USDT_240.ohlcv
pyne data map "BINANCE:BTCUSDT" "ccxt:BINANCE:BTC/USDT"
pyne plugin list --json | python3 -c "import json,sys; print([p['name'] for p in json.load(sys.stdin)['plugins']])"
touch scripts/my_strategy.py && pyne debug ast my_strategy          # the dump is printed only when the bytecode cache is stale
pyne benchmark my_strategy my_data -i 5 -c 5000 --no-output
pyne run my_strategy ccxt:BYBIT:BTC/USDT:USDT@1 --live -f -500 --no-plot          # paper trading on a stream
pyne run my_strategy bybit:BTCUSDT@60 --broker --run-label a --no-plot          # real orders (broker plugin)
pyne broker resume 'my_strategy@bybit-demo-123:BTCUSDT.P:60' 9f3a01bc           # from the quarantine log line
```

Facts worth knowing before composing a command (all verified on 6.12):

- A provider string in `pyne run` downloads the last 500 bars (`-f -N`, a date or days for
  more) **on every run and overwrites `data/<provider>_<SYMBOL>_<TF>.ohlcv` with that range**.
  Keep cached files for backtests and pass their names; use provider mode for live and one-off
  fresh runs.
- `pyne data download` ends at "now", so a bar still forming is stored with partial values and
  a later `continue` never rewrites it; pass `--to` one bar back or `--truncate` later.
- `--from` before the first stored bar cannot be appended: the CLI truncates after a
  confirmation (abort without a terminal).
- Spot pairs streamed through `ccxt` need `default_type = "spot"` in `config/plugins/ccxt.toml`
  (with the default `swap` the Binance websocket client rejects `BTC/USDT` and reconnects
  forever; OKX accepted it, other exchanges unchecked, so set it for every spot pair).
- `pyne run` (re)writes `scripts/<script>.toml` on every run unless `PYNE_SAVE_SCRIPT_TOML=0`.
- `--profile` is refused with `--live` / `--broker`; `--live` is refused with a data file.

## 5. Verify the installed CLI

```bash
python3 <skill>/scripts/cli_help.py --check      # commands/options of the installed pyne vs references/commands.md
                                                 # (groups added by installed CLI plugins, e.g. pyne simbroker, are skipped)
python3 <skill>/scripts/cli_help.py --dump       # every --help page, for reading or diffing
```

Before relying on an option that this skill documents, a one-second `pyne <command> --help`
confirms it exists in the installed version; report the version you ran against.

## 6. Bundled files

| File | Use |
|------|-----|
| `references/commands.md` | Every command: synopsis, arguments, options with value formats and defaults, behaviour, files written, error messages |
| `references/environment.md` | `PYNE_*` variables, workdir discovery and creation, config and output files, prompts and terminal dependence, exit codes, logging, completion |
| `scripts/cli_help.py` | Locate `pyne` in a project, print version and command tree, dump all help pages, check drift against `references/commands.md` (stdlib) |

Writing the scripts and the wrapper tools (`../pynecore-strategy/scripts/run_backtest.py`,
`download_candles.py`, `run_paper.py`, ... in that folder) are the `pynecore-strategy` skill; writing plugins (custom data providers,
REST-only exchanges, notifiers) is the `pynecore-plugin` skill; the full documentation is
bundled in `pynecore-docs`; its CLI pages are in `../pynecore-docs/docs/cli/` (`basics.md`,
`run.md`, `data.md`, `broker.md`, `symbol-browser.md`).
