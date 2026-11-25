---
name: time-series-forecasting
version: 1.5.0
description: >
  Forecast or predict future values of one or many time series (sales, demand, traffic, revenue per period), e.g. "predict tomorrow's / next day's / next week's / next month's value", or find out how forecastable they are. Use it whenever the data is measured period after period and the question is about the next periods. Backtests CatBoost against ARIMA and seasonal naive with ready-made scripts, and writes forecasts, charts and a plain-language report to one folder.
tags: [data, forecasting, time-series, catboost, arima]
external_files:
  - scripts/
  - ../data_utils.py
  - ../prepare_table.py
  - ../prepare_series.py
  - ../series_format.py
  - ../../resources/seaborn_style.py
  - ../../resources/palette.json
  - ../../resources/typography.json
  - ../../resources/assets/fonts/
---

# Time Series Forecasting Skill

Answers: **what will this be over the next periods, how sure can we be, and is a model any better than repeating last season?** A forecast is only as credible as its backtest: every model forecasts periods it was not shown, several times, and is scored on what actually happened.

**Use the ready-made scripts** (see **Scripts**). Write code only for what they don't cover. If the series haven't been explored yet, run the **data-analysis** skill's time-series analysis first: it prepares the series in the format this skill reads, so the calendar decisions (frequency, aggregation, gaps) are made once. It prepares them without features: see Step 2.

---

## Core Principles

1. **Never let the future leak into the past.** No random splits, no features computed with later values. The scripts hold out whole periods at the end, and hide them from every step of fitting.
2. **Backtest over several windows.** One held-out window can be lucky. The backtest uses consecutive windows of `--horizon` periods ending at the last period. `forecast_split.py` sizes it from the history: by default 10% of the windows that fit, and at least 3.
3. **Always compare against seasonal naive** ("same as one season ago"). A model that doesn't beat it has learned nothing, and saying so is a finding.
4. **Recommend the simplest model that is good enough.** The order is seasonal naive, then ARIMA, then CatBoost. A more complex model must be *reliably* better (its confidence interval excludes zero) to be recommended.
5. **A forecast is a range, not a number.** Report the 80% prediction interval with every forecast, and whether the intervals held up in the backtest (coverage).
6. **Say how far ahead is credible.** Error grows with the distance ahead. Report it, and don't forecast beyond what the history supports (a 12-month forecast from 18 months of data isn't credible).
7. **Forecasting is not explaining.** A lag being important means the series repeats itself, not that anything causes anything.
8. **Explain for everyone**, in this dataset's units. **Everything goes in one output folder.**

---

## Output Folder

- **Always pass `--out <run folder>`**: the scripts have no default. Use the location the user gives; if they give none, choose a new, descriptive folder yourself, and tell the user where it is. One folder per run: never reuse one that holds another run. The scripts refuse to mix runs with different series or settings.
- **The layout is fixed**: `report.md` at the top, and **everything else in `files/`**:
  ```
  <run folder>/
  ├── report.md      ← you write it; the only file at the top
  └── files/         ← the scripts write here: the backtest split, the forecasts, metrics, charts, the copies of the scripts, and run.sh
  ```
  Pass the run folder as `--out` (not `files/`); every script writes into its `files/` by itself.
- `files/run.sh` holds the exact commands, with absolute paths, so `sh <run folder>/files/run.sh` rebuilds everything without the skill.
- An extra chart is drawn with `seaborn`: `import seaborn_style` (copied into `files/` by every script, with the `palette.json`, `typography.json` and `fonts/` it reads; all live in `../../resources/`) sets the house theme when imported. Make the figure with `fig, ax = seaborn_style.figure()`, title it with `seaborn_style.title(fig, ...)`, and save with `seaborn_style.save(fig, Path(__file__).resolve().parent, "<name>")`, which writes `<name>.png`. Colours by role from `seaborn_style.PALETTE` by key (`["charts"]["categorical"]` for series, `["text"]["light_background"]["muted"]` for reference lines) and `seaborn_style.colormap("sequential" | "diverging")` for scales, never as hex; pass `saturation=1` to seaborn's bar and box plots. The `charts` skill has the rest of the style.
- The prepared `series.csv` stays where it was prepared: in the analysis run's `files/` when the data-analysis skill prepared it, otherwise in this run's `files/`. Don't copy it, and don't prepare it again.
- Never modify the source data, and never write next to it.
- When done, give the user the folder path and the path of `report.md`.

---

## Step 1 — Check the Requirements

| Package | Needed for |
|---|---|
| `pandas`, `numpy` | every script |
| `statsforecast` | ARIMA (AutoARIMA) |
| `catboost` | the main model |
| `seaborn` | the charts (brings `matplotlib`) |
| `pyarrow` / `openpyxl` | Parquet / Excel input only |

- **First pick the Python that runs the scripts**, and use it for every script in the run. Run `which python` (or `python3`) to see which one that is. If the packages are missing there but installed in a project environment (a `.venv/bin/python` in the working directory, or the one `uv run` uses), run the scripts with that interpreter instead of installing them again. `files/run.sh` records the interpreter as `PY` and reruns with it. `PY=/path/to/python sh files/run.sh` reruns with another one.
- Check them with that interpreter: `python -c "import pandas, numpy, statsforecast, catboost, seaborn"`.
- **`statsforecast` and `catboost` are installed without asking** when they're missing, because every run compares ARIMA and CatBoost. Install them into the environment that runs the scripts (`python -m pip install statsforecast catboost`, or `uv pip install statsforecast catboost` in a `uv` project). Then tell the user in one line what you installed.
- **Ask before installing anything else** that's missing, and name the packages. Install only if the user agrees (`pip install pandas numpy seaborn`). With `uv`, `uv run --with ... python <script>` leaves their environment untouched, but still downloads, so ask first.
- **Charts are PNGs**, drawn with `seaborn` (no browser needed). If the user asks for an interactive chart, draw it afterwards with the `interactive-charts` skill (Plotly, one self-contained HTML page per chart, about 4.8 MB each) from the files this run wrote, and save it in `files/`; the scripts never write pages.
- If an install fails (no network, no permission), or the user declines one of the others:
  - without `statsforecast`: skip `forecast_baseline.py`'s ARIMA by writing `arima_backtest.csv` / `arima_forecast.csv` with `statsmodels`' `SARIMAX` (see **Adapting**), or compare CatBoost against seasonal naive only, and say so in the report.
  - without `catboost`: run the baselines and compare with `--main arima --baseline seasonal_naive`.

---

## Step 2 — Prepare the Series (once)

**First check whether it's already done.** If a data-analysis run on this data wrote `series.csv` and `series.json`, open that `series.json` before reusing it:
- **`features` is empty and `unused_columns` lists columns** (the analysis prepares without features): decide which are worth using (see **Features** below). If any, write the spec and add them with `prepare_series.py --from-series <analysis folder>/files/series.csv --features <run folder>/files/features.json --out <run folder>` (plus `--future` for known ones), then pass this run's `series.csv` to `forecast_split.py`. It reuses the analysis' source and settings and checks the target comes out identical, so the forecast is on the series the analysis described. If none is worth using, say why in the report.
- **Otherwise** pass that `series.csv` to `forecast_split.py` and skip this step.

`forecast_split.py` warns when the series carry no features but their source had numeric columns: don't leave that warning unanswered. If the analysis wrote a prepared table (`table.csv`) but no series, start from that table: `prepare_series.py --table <that folder>/table.csv`.

The data needs cleaning first (numbers or dates stored as text, placeholders like `-1`, duplicate rows) when the raw file has any of those problems. Clean it with the shared `prepare_table.py`, following the data-analysis skill's Step 3, then prepare the series from its table. A clean raw file can go to `prepare_series.py --data` directly.

`prepare_series.py` (shared, in `..`) writes the **one format every time-series script reads**, whichever skill runs it:

```
series.csv                     series.json
id,period,y                    {"target": "sales", "freq": "M", "season_length": 12,
north,2024-01,1520.0            "source": "/abs/sales.csv", "layout": "long", ...}
north,2024-02,1611.0
south,2024-01,980.0
```

- **Long format: one row per series per period.** This is the standard layout for forecasting tools, and what the scripts need. `id` names the series (`series` when there's only one), `period` is the period label, and `y` is the value.
- Every series is on a regular calendar, from its first period to its last, with **no missing periods, no missing values and one row per period**. The scripts refuse anything else.

What the source looks like decides the flags:

| The source has… | Example | Pass |
|---|---|---|
| one row per series per period (long) | `date, store, sales` | `--layout long --time-col date --target sales --id-cols store` |
| one row per series, one column per period (wide, typical of Excel) | `store, 2024-01, 2024-02, …` | `--layout dates-as-columns --id-cols store --target sales` |
| one row per period, one column per series | `date, north, south, …` | `--layout series-as-columns --time-col date --target sales` |
| one row per event (orders, visits, transactions) | `timestamp, shop, amount` | `--layout long … --freq D --aggregate sum` (or `W`, `M`): totals per period |
| several columns identifying a series | `store, product, date, units` | `--id-cols store product` (joined as `north \| shoes`) |
| a single series | `month, revenue` | leave out `--id-cols` |

Decide these, and state each decision in the report:
- **Frequency** (`--freq D|W|M|Q|Y|h`). It's inferred when the dates are regular. Choose it from the decision the forecast serves: weekly staffing needs `W`, even when the data is per order.
- **Aggregation** (`--aggregate sum|mean|last`). Use `sum` for amounts and counts, `mean` for rates and prices, and `last` for balances and stock levels.
- **Gaps** (`--fill-gaps zero|interpolate`). The script lists the gaps first. Use `zero` only when a missing row means nothing happened (no sales that day). Use `interpolate` when a measurement wasn't recorded. If the gaps are many, or the meaning is unclear, ask.
- **A partial last period.** A current month that is only half over looks like a collapse and drags every forecast down. Exclude it when preparing the table, with a rule and its reason: `"exclude": [{"column": "date", "outside": [null, "2024-11-30"], "reason": "December 2024 is incomplete"}]`. Then say so in the report. The data-analysis time-series analysis flags it.

### Features

Other columns measured per series and period (a holiday flag, a promotion, the temperature, a price) can go into both ARIMA (as regressors) and CatBoost (as extra features). They are declared in a spec, `files/features.json`, which you write and pass with `--features` (long layout only), either when preparing from the table or with `--from-series` on series already prepared (Step 2):

```json
{
  "holiday":    {"use": "known",  "aggregate": "max",
                 "reason": "public holidays are set years ahead"},
  "promo":      {"use": "known",  "aggregate": "max",
                 "reason": "promotions are planned a quarter ahead"},
  "temp":       {"use": "lagged", "aggregate": "mean"},
  "weathersit": {"use": "lagged", "aggregate": "mean", "lags": [1, 7]}
}
```

**For each feature, decide whether it is known or lagged.** This is the one decision that can make a backtest lie.
- **`known`**: the value for a period is known before that period starts (holidays, the calendar, planned promotions, a price set in advance). The models use the value of the period they forecast. It needs a `reason`, because it's a claim: if the value is only known afterwards (the actual weather, the actual footfall), every backtest has seen the future and looks better than it will perform.
- **`lagged`**: only known once the period is over (the weather, a competitor's price, other measurements). The models use only its past values: `lags` (default: the horizon). Every lag must be at least `--horizon`, because a forecast 7 days ahead can't use yesterday's weather for day 7. The scripts refuse shorter lags.
- If you're unsure whether a value is known in advance, it's `lagged`, or ask the user.
- **`aggregate`**: how rows sharing a period combine, like `--aggregate` for the target: `max` for flags (a holiday in any hour makes the day a holiday), `mean` for levels (temperature), `sum` for amounts. The default is `mean`.
- Features must be numbers or booleans. Turn categories into numbers in the cleaning spec, or into one 0 / 1 column per category.
- Leave out columns derived from the target (`casual` and `registered` when `cnt = casual + registered`), and ids.

**Known features need their future values**: the forecast itself uses the value of each period it forecasts. Pass them with `--future`, a file with the same time and id columns and the known features, covering at least the `--horizon` periods after the history. The rows after each series' last period are used, so the data file itself works when it already holds them. If the user hasn't given them, build them when they are derivable (a holiday calendar for the next periods), say how in the report, and otherwise ask. Without them `forecast_split.py` stops.

**Say in the report** which features were used, which were known and which lagged, and why. CatBoost's feature importance and ARIMA's regression (in `arima_orders.csv`) show whether they mattered. To measure what they add, rerun in a second folder without `--features` and compare the backtests.

---

## Step 3 — Frame the Forecast

Settle these before running anything. Ask only when the data can't answer:

- **What is forecast, at what level, and for what decision**: total sales, or per store for store orders? That decides the series and the frequency (Step 2).
- **Horizon** (`--horizon`): how many periods ahead the decision needs. It should be at most about a third of the history, and ideally no more than one seasonal cycle.
- **Backtest size** (`--windows-share`, default `0.10`). This is the share of the available windows to backtest. A window is available when it fits after two seasonal cycles of training. The script:
  - uses at least 3 windows when that many fit;
  - caps windows × series at `--max-fits` (2000), because every window refits ARIMA for every series;
  - prints the resulting number of forecast points per model.

  For example, 731 days forecast 1 day ahead get 72 windows, and 7 years of monthly data forecast 6 months ahead get 3.
  - **Read the point count.** Fewer than about 30 points per model with one or a few series makes the comparison thin.
  - With history to spare, raise `--windows-share`, e.g. to `0.25`. Say why in the report.
  - With little history, lower `--horizon` before thinning the backtest further, and say the backtest is thin.
  - `--windows N` sets an exact number, for a reason you state.
- **Season length**: taken from `series.json` (7 daily, 52 weekly, 12 monthly, 4 quarterly, 24 hourly). Override `--season-length` only for a different cycle, like 5 for weekday-only data.
- **Deciding metric**: `MASE` by default, for stable series. It is scale-free, so every series counts equally. Use `WAPE_%` when big series should count more (total volume matters), and say so.
  - **Not MASE for non-stationary series**: a trend, a level shift, or noise that grows or shrinks over the history. MASE divides by the seasonal-naive error averaged over the whole history, which doesn't fit the recent periods of such a series, so MASE values can't be read against 1. Use `MAE` (or `RMSE` when large misses matter most) for a single series, and `WAPE_%` for several.
  - Decide from the time-series analysis when it shows a trend or a break. `forecast_compare.py` also checks every series, and warns when MASE is the deciding metric and one of them is non-stationary (`nonstationary` and `mase_warning` in `comparison.json`). Then rerun only `forecast_compare.py` with `--metric`: the models don't need refitting.

---

## The Models

Every run compares three models, on exactly the same forecast points:

| Role | Model | What it is, in one sentence for the report |
|---|---|---|
| trivial floor | **Seasonal naive** | "the same as one season ago" |
| baseline | **ARIMA** (AutoARIMA, one per series) | a classical statistical model fitted to each series' own history, capturing its trend, seasonality and recent momentum; with features, a regression on them with ARIMA errors |
| main model | **CatBoost** (one model across all series) | many small decision trees that learn, from all series at once, how the next value depends on recent values, the same period last season, the calendar and the features |

Both models see the same features, at the same periods (Step 2, **Features**), so the comparison stays fair. Seasonal naive uses none.

**When to expect which to win**:
- CatBoost tends to win with **many related series** (it learns shared patterns) and with long histories.
- ARIMA tends to win on a **single, short or smooth series**.
- With a **strong steady trend**, rerun CatBoost with `--difference` in a second folder (trees can't forecast beyond the values they were trained on), and compare the two runs' backtest scores.
- With **intermittent series** (mostly zeros), all three struggle. Say so, and recommend the simplest.

---

## Scripts

There are two places. Paths in this file are relative to this SKILL.md, whose location is the `[file: …]` line above this text: resolve them from its directory, never from the working directory.

- **This skill's scripts**, in `scripts/`, sharing `common.py`: `forecast_split.py`, `forecast_baseline.py`, `forecast_catboost.py`, `forecast_compare.py`.
- **The scripts shared by all the data skills**, one level above this skill's folder, in `..` (`builtin/data/`):
  - `prepare_table.py`, the cleaning (the data-analysis skill's Step 3);
  - `prepare_series.py` and `series_format.py`, the series format of Step 2 (the data-analysis skill uses the same);
  - `data_utils.py`, the helpers every script uses.

  This skill's scripts find them there by themselves. Run everything in place, and don't move or copy scripts out of the skills.

`python <script> --help` documents every option.

| Script | Does |
|---|---|
| `prepare_series.py` (shared, `..`) | Step 2, from a prepared table (`--table`) or a clean raw file (`--data`) |
| `forecast_split.py` | sets up the backtest once: which series take part, how many windows, and which periods each window holds out. The only script that takes `--series`, `--horizon`, the window options and `--season-length` |
| `forecast_baseline.py` | seasonal naive and AutoARIMA: backtest and future forecast, and the ARIMA order per series |
| `forecast_catboost.py` | CatBoost on lag, rolling-mean and calendar features (plus series id and size with several series), recursive multi-step forecast, early stopping on the periods just before each window (at least one season, and at least 8), and intervals from rolling forecasts over that span |
| `forecast_compare.py` | scores all models on the shared backtest points, bootstraps a 95% CI for CatBoost − ARIMA and CatBoost − seasonal naive, and writes the verdict and charts |

**Run in this order**. The model scripts take only `--out`, and read the series and the backtest from `split.json`:

```bash
S=<dir of this SKILL.md>/scripts; D=<dir of this SKILL.md>/..; OUT=<run folder>
# Step 2, only if no series.csv exists yet (from the prepared table, or --data for a clean raw file):
python $D/prepare_series.py --table /abs/<analysis run folder>/files/table.csv --time-col date --target sales --id-cols store --out $OUT
python $S/forecast_split.py --series $OUT/files/series.csv --horizon 6 --out $OUT   # or the analysis folder's series.csv
python $S/forecast_baseline.py --out $OUT
python $S/forecast_catboost.py --out $OUT
python $S/forecast_compare.py --out $OUT
```

**Options**:

| Where | Option | Use |
|---|---|---|
| `prepare_series.py` | `--table` / `--data` | the prepared table, or a clean raw file |
| | `--sep ';'`, `--decimal ','`, `--encoding latin-1`, `--sheet NAME` | with `--data` only: how the raw file is read. Same symptoms and fixes as in the data-analysis skill's **Reading the file** |
| | `--value-cols ...` | wide layouts: only these period / series columns |
| `forecast_split.py` | `--horizon` (required), `--windows-share` (0.10) or `--windows N`, `--max-fits` (2000), `--season-length` (from `series.json`) | Step 3: size the backtest from the printed point count |
| `forecast_baseline.py` | `--jobs N` | ARIMA fits run in parallel on all cores by default (`-1`), across series and windows alike. It fits once per series and window, so with thousands of series expect minutes. `--jobs 1` only on a machine that must keep cores free |
| | `--exact-arima` | search the ARIMA orders by full maximum likelihood instead of the default approximation (conditional sum of squares for the search, maximum likelihood for the chosen model). Several times slower, and rarely changes the forecasts: use it only to check a surprising ARIMA result |
| `forecast_catboost.py` | `--difference` | trending series (see **The Models**) |
| | `--lags 1 2 3 7 14` | override the default lags (1, 2, 3, one and two seasons, when the history allows) |
| | `--loss MAE`, `--depth`, `--learning-rate` | as in the tabular-classification-regression skill |
| `forecast_compare.py` | `--metric MASE\|WAPE_%\|MAE\|RMSE` | the deciding metric (Step 3) |
| | `--main`, `--main-label`, `--baseline`, `--baseline-label` | compare other models (see **Adapting**) |
| | `--examples N` | series drawn in the charts (the largest, default 4) |

**Guarantees**:
- `forecast_split.py` fixes the series and windows in `split.json`, and prints each window's dates. Every model script reads them from there. Rerunning it in the same folder with other settings is refused.
- For each window, every model sees only the periods before it.
- CatBoost's early stopping and intervals use the `--horizon` periods just before each window, never the window itself.
- A series takes part in a window only with at least `max(2 × horizon, 8)` periods before it (`series_included` in `split.json`). Series that stop before the last period are left out (`series_left_out_ended_early`).
- Each script copies itself and the shared modules into `files/`, and logs its command in `files/run.sh`.

**Outputs, and where each goes in the report**:

| File | Use it for |
|---|---|
| `comparison.md` | Finding 1: metrics for all three models, the CI and verdict against ARIMA and against seasonal naive, the metric per window. Tables are ready to paste. |
| `model_comparison.png` | Finding 1 |
| `backtest_examples.png` | Finding 2: what the forecasts looked like against what happened |
| `error_by_step.png` | Finding 3: how far ahead the forecast stays useful |
| `future_forecast.png`, `<model>_forecast.csv` | Finding 4: the forecast itself, with 80% / 95% intervals (`lo80`, `hi80`, …) |
| `catboost_feature_importance.png` | what CatBoost relies on (Finding 2 or Method) |
| `arima_orders.csv`, `baseline_metrics.json` | Method: the ARIMA chosen per series, and how many fell back to seasonal naive |
| `coverage80_%` / `coverage95_%` in `comparison.md` | Caveats: intervals that cover well under 80 / 95% are too narrow; say so |
| `split.json` | The task and Method: windows (how many were available, and why this many: `windows_reason`), periods, series included and left out |

The verdict in `comparison.json` is mechanical. Your recommendation also weighs whether the gain matters for the decision, and how consistent it is across windows.

**Adapting**:
- Never edit the scripts in the skill directory. Edit the copy in `files/`, and run that copy.
- **Another model** (ETS, Prophet, LightGBM, a foundation model): write `forecast_<name>.py` in `files/`, modelled on `forecast_baseline.py`. Load with `common.load_panel(args)` (after `common.base_parser`), and for each window forecast from `panel.origins[w]` using only `panel.history(i, origin)`. Save with `common.backtest_frame` / `common.future_frame` / `common.save_forecasts(out, "<name>", ...)`. Then run `forecast_compare.py --main <name> --main-label "<Name>"`.
- **Drivers** (holidays, promotions, prices, the weather): declare them as features (Step 2, **Features**). Drivers that aren't in the data can't be used: say so in the Caveats.

---

## Step 4 — Interpret

- **Is it forecastable at all?** Compare the models to seasonal naive first, with the CI against it in `comparison.md`. On a stable series, MASE below 1 beats "same as one season ago" on past data, and near 1 means the series barely does better than repeating itself. On a non-stationary series, don't read MASE against 1 (see Step 3).
- **When the metrics disagree** (one model better on MAE, the other on RMSE or bias), say so, and say what each one means for the decision: RMSE punishes large misses, MAE the typical error, bias a systematic lean. Don't name a winner from the deciding metric alone.
- **Which model**: the CI against ARIMA, then consistency. A model that wins on average but loses in one window of three is less dependable than the average says.
- **How far ahead**: read `error_by_step.png`. Say up to which step the forecast stays better than seasonal naive, or within an error the decision tolerates.
- **Bias**: `bias_%` far from 0 means the model systematically over- or under-forecasts. For stock decisions this matters more than the average error.
- **Intervals**: coverage close to 80 / 95% means the ranges can be trusted. Report the range, not just the line.
- **Where it fails**: series or windows with much higher error. Check them in the time-series analysis for a break, an outlier or a partial period.

---

## Step 5 — Report

Write `report.md` at the top of the run folder, next to `files/`. Lead with the forecast and how far to trust it. Which model produced it comes second.

Every finding follows the **data-analysis** pattern: **What we found**, the chart, **How to read this chart**, **What it means for this dataset**, and **Technical detail**.

```markdown
# Forecasting [target]

### Summary
[3–5 plain sentences: what was forecast, at what level, how far ahead; the forecast in words with its range; how accurate it was in the backtest, in concrete terms; the recommended model and why.]

### The task
[What a series and a period are, the history span, the horizon, the backtest windows (dates), preparation decisions (frequency, aggregation, gaps, partial period), the deciding metric.]

### The models
[One plain sentence each: seasonal naive, ARIMA, CatBoost, and why each is there.]

### Findings
#### 1. [How forecastable the series are, and how the models compare]
#### 2. [What the forecasts looked like against what happened]
#### 3. [How far ahead the forecast stays useful]
#### 4. [The forecast for the next N periods]

### Recommendation
[Which model and why; whether it is good enough for the decision; how far ahead to use it.]

### Caveats
[Short history, thin backtest (few windows or one series: the CI is optimistic), interval coverage, trend or break risk, drivers not modelled (or only lagged), intermittent series, series left out.]

### Next steps
[2–4 concrete follow-ups: add known drivers, forecast at another level, re-forecast monthly, monitor error.]

### Method
[Source; preparation; windows; each model and its settings (ARIMA orders, CatBoost features and rounds); `sh files/run.sh` to reproduce.]
```

**Make every metric understandable**:
- MASE 0.7, on a stable series: "its errors were 30% smaller than simply repeating last season's values".
- WAPE 8%: "over all stores and months, forecasts were off by 8% of actual sales".
- Bias −3%: "it tended to under-forecast, by about 3% of sales".
- Interval: "for March, 5,100 units, and 80% likely between 4,700 and 5,500".
- The CI in words: "across resampled stores, CatBoost's advantage stayed between X and Y, so it is / isn't reliable".

---

## Interaction Style

- If the horizon, the level or the purpose is unclear, ask one focused question. Otherwise use sensible defaults, and state them.
- Don't overstate a win. "ARIMA is as good, and simpler" is a good outcome, and so is "nothing beats last season's values".
- Never present a forecast without its range, or beyond what the history supports.
- Don't invent drivers, events or business context. If a break (COVID, a relaunch) is visible, ask about it rather than guess.

---

## Quality Checklist

- [ ] The data was cleaned once (`prepare_table.py`) when it needed it, the series were prepared once from it in the shared format, and the cleaning and preparation decisions are stated
- [ ] Every feature's known / lagged choice is stated with its reason, and known features' future values are real, not guessed
- [ ] Horizon, level, windows and metric were settled before fitting, and MASE was not the deciding metric for a non-stationary series
- [ ] The scripts ran (or a documented replacement, modelled on them) with the same series and settings, and the backtest windows were never seen by any model
- [ ] The report compares all three models, with the 95% CI against ARIMA and against seasonal naive, and the consistency across windows
- [ ] The recommendation follows from the CI and the decision's needs, not from model sophistication
- [ ] The forecast is given with its 80% interval, and the interval coverage is reported
- [ ] Every metric is translated into plain terms; every chart sits inside its finding and is explained
- [ ] `report.md` is at the top of the run folder, everything else is in its `files/`, and `sh files/run.sh` regenerates it
