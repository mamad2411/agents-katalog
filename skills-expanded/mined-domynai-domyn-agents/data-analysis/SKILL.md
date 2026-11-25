---
name: data-analysis
version: 1.5.0
description: >
  Explore, clean, summarize or answer questions about a tabular dataset (CSV, Excel, Parquet, JSON, or a pasted table): distributions, outliers, correlations, group comparisons, trends, seasonality. Use whenever the answer must be computed from rows and columns. Writes code, charts and a plain-language report to one folder.
tags: [data, analysis, statistics, pandas]
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

# Data Analysis Skill

Answers questions about tabular data by **computing** the answer, never by estimating it from a glance at the rows. The output is a sourced report: what was asked, what the data says, how it was computed, and what it cannot tell you.

**Use the ready-made scripts** (see **Scripts**) for profiling, cleaning, the default analysis and time series. Write code only for the question-specific part.

---

## Core Principles

1. **Compute, don't eyeball.** Every number you report comes from code run on the full dataset. If you cannot run code, say so and label every figure as read by hand from the visible rows.
2. **Look before you analyze.** Shape, columns, types and missing values come first. Most wrong answers come from a column that was not what its name suggested.
3. **Never modify the source file.** Cleaning writes a new, prepared table to the output folder (Step 3); the source stays as it was.
4. **Say what the data cannot support.** Small samples, heavy missingness and correlation-not-causation belong in the answer, not in a footnote.
5. **Answer the question first.** Lead with the result; the method follows.
6. **Everything goes in one output folder**, so the analysis can be read, shared and rerun as a unit.
7. **Explain every finding in terms of this dataset.** A statistic alone is not a finding. Say in plain language what it means here and why it matters, so a non-technical stakeholder can follow the whole report.

---

## Output Folder

- **Always pass `--out <run folder>`**: the scripts have no default. Use the location the user gives; if they give none, choose a new, descriptive folder yourself, and tell the user where it is. One folder per run: never reuse one that holds another analysis.
- **The layout is fixed**: `report.md` at the top, and **everything else in `files/`**:
  ```
  <run folder>/
  ├── report.md      ← you write it; the only file at the top
  └── files/         ← the scripts write here: the profile, `cleaning.json` and the prepared table, the analysis outputs, every chart, the copies of the scripts, and run.sh
  ```
  Pass the run folder as `--out` (not `files/`); every script writes into its `files/` by itself.
- `files/run.sh` holds the exact commands, with absolute paths, so `sh <run folder>/files/run.sh` rebuilds everything without the skill.
- Your own files go in `files/` too: `cleaning.json`, `analysis.py`, any extra chart.
- `sh files/run.sh` must regenerate every number and chart. Add a line for `analysis.py` at the end of `files/run.sh`: `"$PY" analysis.py`, so it runs with the same interpreter as the scripts.
- `analysis.py`:
  - lives in `files/`, reads the **prepared table** (`files/table.csv`) by its absolute path, and writes only to its own folder, `files/` (`Path(__file__).resolve().parent`);
  - can `import common` (copied into `files/`, with `data_utils.py`, `seaborn_style.py` and the `palette.json`, `typography.json` and `fonts/` it reads) for loading, and then `import seaborn_style` for charts in the house style (see **Charts**). Load with `common.load(Path("<abs>/table.csv"))`, which restores the column types. A bare `pd.read_csv` would turn codes like `"007"` into numbers and dates into text;
  - does no cleaning: a cleaning decision goes in `cleaning.json` (Step 3), so every result uses it;
  - holds everything that produces a reported number or chart. Exploratory snippets can run inline.
- `report.md` links charts relative to itself (`![...](files/name.png)`), so the folder can be moved or zipped.
- Never write next to the source data unless the user asks.
- When done, give the user the folder path and the path of `report.md`.

---

## Step 1 — Check the Requirements

Do this before anything else. The scripts need these Python packages:

| Package | Needed for |
|---|---|
| `pandas`, `numpy` | every script |
| `seaborn` | the charts (brings `matplotlib`) |
| `pyarrow` | Parquet files only |
| `openpyxl` (`.xlsx`) / `xlrd` (`.xls`) | Excel files only |

- **First pick the Python that runs the scripts**, and use it for every script in the run. Run `which python` (or `python3`) to see which one that is. If the packages are missing there but installed in a project environment (a `.venv/bin/python` in the working directory, or the one `uv run` uses), run the scripts with that interpreter instead of installing them again. `files/run.sh` records the interpreter as `PY` and reruns with it. `PY=/path/to/python sh files/run.sh` reruns with another one.
- Check them with that interpreter: `python -c "import pandas, numpy, seaborn"`, adding `pyarrow` or `openpyxl` when the data is in that format.
- **`seaborn` is installed without asking** when it's missing, because every analysis includes charts. Install it into the environment that runs the scripts (`python -m pip install seaborn`, or `uv pip install seaborn` in a `uv` project). Then tell the user in one line that you installed it.
- **Charts are PNGs**, drawn with `seaborn` (no browser needed). If the user asks for an interactive chart, draw it afterwards with the `interactive-charts` skill (Plotly, one self-contained HTML page per chart, about 4.8 MB each) from the files this run wrote, and save it in `files/`; the scripts never write pages.
- **Ask before installing anything else** that's missing, and name the packages. Install into the user's environment only if they agree (`pip install pandas numpy`). With `uv`, `uv run --with pandas --with numpy --with seaborn python <script> ...` leaves their environment untouched. It still downloads, though, so ask first.
- If the user declines, or an install fails (no network, no permission):
  - without `pandas` or `numpy`, the scripts can't run. Fall back to the standard library (`csv`, `json`, `statistics`, `collections.Counter`), and say so in the report.
  - without `seaborn`, the numbers are still computed but there are no charts (see **Charts**).

---

## Step 2 — Load and Profile

- Find the file (`glob_files` / `list_dir`) and check its size before reading anything. Don't use `read_file` for more than a few hundred rows: it returns a window, not the dataset.
- Run `profile_data.py`. If the file is a CSV that looks wrong (one column, numbers as text), fix how it is read first (see **Reading the file** under **Scripts**): every later step depends on it. The profile reports:
  - rows, columns, types and a sample of rows
  - missing values, including placeholders like `-1`, `"N/A"`, `"unknown"`
  - duplicates
  - numbers or dates stored as text
  - categories spelled several ways
  - suspicious values
  - the columns the default analysis will skip
  - codes whose leading zeros the reading drops (`"02134"` read as `2134`)
  - a **draft cleaning spec**, `cleaning_suggested.json`, for Step 3
- For large files (hundreds of MB or more), pass `--nrows` first, and say you are working on a sample until the full file is confirmed to fit.
- Tell the user briefly: rows, columns, the columns that matter for their question, and anything suspicious.

### Is it a time series?

**Decide this explicitly after profiling, before any analysis, and state the answer in the report's About the data.** It changes which analysis applies.

It **is** a time series when a numeric measure is recorded **repeatedly over time for the same thing**: one series (monthly revenue), or several (daily sales per store). Look for:
- a date or time column whose values repeat across rows of the same entity, or that forms a regular sequence (every day, every month);
- a question about change, trend, seasonality, growth, peaks, or what comes next.

These are **also** time series, once aggregated per period:
- **event logs**: one row per order, visit or transaction, with a timestamp. The series is the count or total per day / week / month.
- **wide tables**: one column per month (`2024-01`, `2024-02`, …), or one column per series (`date, north, south`).

It is **not** a time series when the date is just an attribute of each row: a customer's signup date, a product's launch date, a patient's birth date. There is one row per thing, never the same thing measured again. Treat those dates as ordinary columns (parsed in Step 3).

When it **is** a time series:
1. Clean the data as usual (Step 3), then prepare the series **once** from the prepared table with `prepare_series.py` (see **Time Series**). The time-series-forecasting skill reads the same `series.csv`, so a forecast later keeps the same frequency, aggregation and gap filling. Prepare without `--features`: which columns a forecast may use (and whether each is known in advance) is that skill's decision, and it adds them to these series with `--from-series`.
2. Run `timeseries_analysis.py` as part of Step 4, alongside the usual analysis of the other columns.

If it's unclear (a date column, but it's not obvious whether rows repeat per entity), check it with code: count rows per entity and per date. Ask only if the data can't answer.

---

## Step 3 — Clean: the Prepared Table

Cleaning is decided once, written down in `cleaning.json`, and applied by `prepare_table.py`, which writes the **prepared table** that every later step uses. The same table is what the tabular-classification-regression and time-series-forecasting skills read, so an analysis followed by a model or a forecast works on the same data.

1. **Start from the draft.** `profile_data.py` wrote `cleaning_suggested.json`:
   - what its checks found goes under the spec's keys (`numbers`, `dates`, `missing`, `categories`, `trim`, `types`);
   - what only you can decide goes under `_to_decide`: numeric placeholders like `-1` or `999`, and duplicate rows.
2. **Decide each entry**, and save the result as `$OUT/files/cleaning.json`:

| Problem | Spec key | Decide |
|---|---|---|
| numbers stored as text (`"1.234,50"`, `"$5"`, `"12%"`) | `numbers`: `{"price": {"thousands": ".", "decimal": ","}}`, `{"discount": {"percent": true}}` | set `thousands` / `decimal` when the file is consistent; leave `{}` to detect them per value |
| dates stored as text | `dates`: `{"order_date": {"dayfirst": true}}` or `{"format": "%d.%m.%Y"}` | `dayfirst` for 31/01/2024 |
| codes with leading zeros (zip codes, ids) | `types`: `{"zip": "string"}` | always, for codes: they are read as text, never numbers |
| placeholders for missing (`-1`, `999`, `"N/A"`, `"unknown"`) | `missing`: `{"age": [-1, 999], "*": ["unknown"]}` | only when the value really means "not recorded". `"*"` applies to text columns only |
| one value spelled several ways | `categories`: `{"city": {"NYC": "New York"}}`, plus `trim` for stray spaces | the spelling to keep |
| yes / no columns | `booleans`: `{"active": {"true": ["yes", "Y"], "false": ["no", "N"]}}` | the values meaning each |
| duplicate rows, or ids that should be unique (`--id-cols` in the profile) | `duplicates`: `{"subset": ["order_id"], "keep": "first", "reason": "…"}` | whether they are copies; the `reason` is required |
| impossible or out-of-scope rows (negative ages, test orders) | `exclude`: `[{"column": "age", "outside": [0, 120], "reason": "…"}]` (or `equals`, or `missing: true`) | only with a reason you can state; the `reason` is required |
| columns not to analyse | `drop`: `{"internal_note": "free text"}` | |
| unclear units or grain (mixed currencies, what one row is) | — | ask the user |

3. **Run it** (see **Scripts**), and **profile the result** with `profile_data.py --table $OUT/files/table.csv`. Repeat until the profile shows only what you decided to keep.

Rules:
- Outliers that are real stay. Remove rows only with `exclude` and a reason; never drop them silently.
- **Every row removed has its decision on record.** `table.md` lists each removal (duplicates, each `exclude` rule) with its reason and how many rows it removed, then every step with the values it changed. Its content goes in the report's Method section, and removals also go in About the data.
- Nothing is cleaned anywhere else: not in `analysis.py`, not by hand. If the spec can't express something, do it in `analysis.py` and say in the report that it is outside the prepared table.

---

## Step 4 — Analyze

- **A specific question:** do the smallest analysis that answers it, in `analysis.py`.
- **No specific question** ("analyze this", "what's in this file"): run the **Default Analysis**.

| Question | Approach |
|---|---|
| What's typical? | mean **and** median, std, quantiles. Use the median when the distribution is skewed. |
| How is it distributed? | value counts (categorical); quantiles and a histogram (numeric) |
| How do groups compare? | per group: count, mean, median. Always show the group size. |
| How does it change over time? | the time series is prepared and `timeseries_analysis.py` is run (see **Time Series**); beware incomplete first / last periods |
| Are these related? | Pearson, or Spearman for ranks and outliers; sanity-check with a scatter or crosstab |
| What stands out? | IQR rule or z-scores, top / bottom N, share of total |

Rules:
- Show **counts next to rates and averages**. "Conversion 50%" from 2 rows is not a finding.
- Always say what a percentage's denominator is.
- Round only for display, and consistently.
- The code is the evidence: everything reported comes from the scripts or `analysis.py`.

---

## Default Analysis

- Run `default_analysis.py` on the prepared table (`--table`), with `--target` if there is an obvious outcome column. It computes:
  - **numeric columns:** missing %, mean, median, std, variance, min / max, 1–25–75–99% quantiles, skewness, excess kurtosis, IQR outliers
  - **categorical columns:** distinct values, the top values with their shares
  - **date columns:** range, rows per period, empty periods
  - **relationships:** Pearson and Spearman correlations, the strongest pairs, near-duplicate features, and what relates to the target
  - **the default charts**
- It skips ids, constant columns and free text; add more with `--skip`.

`default_analysis.md` lists the flags. Interpret them this way:

| Flag | Meaning for the report |
|---|---|
| skewed (\|skew\| > 1) | describe the column by its median and IQR, not its mean and std |
| fat tails (excess kurtosis > 3) | extreme values are more common than a normal distribution gives |
| outliers (IQR rule), max far above the 99% quantile | check the top values: real, errors or placeholders? |
| more than 5% missing | say how it affects the column's numbers |
| one value covers more than 95% of rows | the column says little; say so |
| Pearson and Spearman disagree | the relationship is non-linear or driven by outliers |
| near-duplicate features (\|r\| ≥ 0.95) | one may be derived from the other; ask or check |

When the data is a time series (Step 2), the default analysis also includes `timeseries_analysis.py` (see **Time Series**).

Report only what is notable. Each notable result becomes a finding (Step 5). Unremarkable columns share one summary table. Say which columns were skipped. End the report with 2–4 follow-up questions the results raise, e.g. "`price` and `cost` are 0.97 correlated — is one derived from the other?"

---

## Charts

**Every analysis includes charts for its key findings**, not just when the user asks.

- **Which ones:**
  - at least one per key finding: the distribution of the outcome, the strongest relationship, any notable group comparison
  - don't chart noise
  - `default_analysis.py` draws its default set, and `default_analysis.md` says what each shows
- **Custom charts** go in `analysis.py`:
  - use `seaborn`, and `import seaborn_style` after `import common`: importing it sets the house theme (colours from `../../resources/palette.json`, the same palette the slides use; DM Sans and the slides' type sizes; axes), so every figure matches the default charts. Make each figure with `fig, ax = seaborn_style.figure()` and title it with `seaborn_style.title(fig, "...")`; never `plt.show()`; save with `seaborn_style.save(fig, out, "<name>")`, which writes `<name>.png` for the report and returns its name. The `charts` skill has the rest of the style (legends, seaborn defaults to override)
  - colours by role, from `seaborn_style.PALETTE` (the loaded `palette.json`) by key, never as hex: `PALETTE["charts"]["categorical"]` in order for series, `seaborn_style.colormap("sequential")` for magnitude, `colormap("diverging")` (`PALETTE["charts"]["negative"]` / `["positive"]`) around a meaningful zero, `PALETTE["text"]["light_background"]["muted"]` for reference lines
  - give each chart a title, axis labels with units, and a legend when there are several series
  - keep styling consistent across the report
  - don't distort: start bar and count axes at zero, and don't truncate axes unless flagged
- **Chart types:**
  - numeric distribution: histogram or boxplot
  - categorical: bar chart with counts
  - group comparison: grouped bars, or boxplots for median and spread
  - two numeric columns: scatter
  - correlations: heatmap
  - over time: line (for time series, `timeseries_analysis.py` draws the default set)
- **If `seaborn` is still missing** because installing it failed (Step 1), or the PNGs couldn't be written, say in the report's Summary that charts were left out, and why. Never leave them out silently.

---

## Scripts

There are two places. Paths in this file are relative to this SKILL.md, whose location is the `[file: …]` line above this text: resolve them from its directory, never from the working directory.

- **This skill's scripts**, in `scripts/`: `profile_data.py`, `default_analysis.py`, `timeseries_analysis.py`, and `common.py`, which they share.
- **The scripts shared by all the data skills**, one level above this skill's folder, in `..` (`builtin/data/`):
  - `prepare_table.py`, the cleaning of Step 3;
  - `prepare_series.py` and `series_format.py`, for time series;
  - `data_utils.py`, the helpers every script uses.

  This skill's scripts find `data_utils.py` there by themselves. Run everything in place, and don't move or copy scripts out of the skills.

Their requirements are in Step 1. `python <script> --help` documents every option.

```bash
S=<dir of this SKILL.md>/scripts; D=<dir of this SKILL.md>/..; OUT=<run folder>
python $S/profile_data.py --data /abs/sales.csv --out $OUT [--id-cols order_id]
# Step 3: review $OUT/files/cleaning_suggested.json, save your decisions as $OUT/files/cleaning.json
python $D/prepare_table.py --data /abs/sales.csv --spec $OUT/files/cleaning.json --out $OUT
python $S/profile_data.py --table $OUT/files/table.csv --out $OUT          # check the result
python $S/default_analysis.py --table $OUT/files/table.csv --out $OUT [--target revenue]
```

| Option | Use |
|---|---|
| `--data FILE` / `--table TABLE.csv` | the raw source (`profile_data.py`, `prepare_table.py`) or the prepared table (every later step; `profile_data.py` too, to check it) |
| `--sep ';'`, `--decimal ','`, `--encoding latin-1` | how a raw CSV / TSV is read: separator (detected when omitted), decimal mark (`.`), encoding (`utf-8`). See **Reading the file** below. Pass the same ones to `profile_data.py` and `prepare_table.py`; a prepared table needs none. |
| `--nrows N`, `--sheet NAME` | a sample of a large file; an Excel sheet (default: the first) |
| `--skip col ...`, `--target col`, `--top N`, `--max-charts N` | `default_analysis.py` only: exclude columns, relate everything to an outcome, top values per category (5), charts per kind (4) |

**Reading the file** is where most failed runs start. It only concerns the raw file: the prepared table is always plain CSV. The scripts detect the column separator of a CSV / TXT file (`,` `;` tab `|`) and print what they used. Check the first rows and the column count before going further:

| Symptom | Cause | Fix |
|---|---|---|
| one column, whose name holds every header (`id;region;price`) | the separator isn't `,` | `--sep ';'` (or `'\|'`, `'\t'`) |
| numbers like `8,60` read as text, or split across two columns | comma decimal mark (European exports, usually `;`-separated) | `--decimal ','` |
| `UnicodeDecodeError`, or `Ã©` in place of `é` | the file isn't UTF-8 (typical of Excel exports) | `--encoding latin-1` or `cp1252` |
| the wrong Excel sheet | the scripts read the first sheet | `--sheet NAME` |

Lines starting with `#` before the header are skipped as comments and printed (`Skipped the first N line(s)…`). Read them, since they often give the units or the source. Do not edit the file to remove them: the scripts already skip them, and `run.sh` rebuilds from the original file.

Quote the separator on the command line (`--sep ';'`): an unquoted `;` or `|` is taken by the shell.

Outputs: `profile.md` / `.json` and `cleaning_suggested.json`; `table.csv` / `table.json` / `table.md` (the prepared table, its column types, and every cleaning step with its counts); `default_analysis.md` / `.json` (tables ready to paste, flags, and which chart shows what); the charts; and `run.sh`, which starts from the raw file and rebuilds everything.

- Never edit the scripts in the skill directory. Edit the copy in `files/`, and run that copy.
- For anything else, write `analysis.py`.

---

## Time Series

For data that Step 2 decided is a time series. `timeseries_analysis.py` is in `scripts/`; `prepare_series.py` is one of the shared scripts in `..`, and the time-series-forecasting skill uses the same one.

**1. Prepare once**: `prepare_series.py --table $OUT/files/table.csv …` reshapes the prepared table into `series.csv` and `series.json` in the run's `files/`. This is the one format both skills' time-series scripts accept. It is **long**: one row per series per period (`id,period,y`), on a regular calendar, with no gaps and no repeated periods.

| The source has… | Pass |
|---|---|
| one row per series per period (`date, store, sales`) | `--layout long --time-col date --target sales --id-cols store` |
| one column per period (`store, 2024-01, 2024-02, …`) | `--layout dates-as-columns --id-cols store --target sales` |
| one column per series (`date, north, south, …`) | `--layout series-as-columns --time-col date --target sales` |
| one row per event (`timestamp, shop, amount`) | `--layout long … --freq D --aggregate sum` (or `W`, `M`) |
| a single series | leave out `--id-cols` |

- The script refuses several rows in one period unless `--aggregate sum|mean|last` says how to combine them. Use `sum` for amounts and counts, `mean` for rates and prices, and `last` for balances.
- It refuses gaps unless `--fill-gaps zero|interpolate` says how to fill them. Use `zero` only when a missing row means nothing happened. It lists the gaps first; state the choice and the count in the report.
- The frequency is inferred when the dates are regular; otherwise pass `--freq D|W|M|Q|Y|h`.
- Start from the prepared table (`--table`), so the cleaning applies to the series too. `--data` with the reading options reads a raw file, for data that needs no cleaning.

**2. Analyse**: `timeseries_analysis.py --series $OUT/files/series.csv --out $OUT`. Per series, it reports:
- the span and level;
- the trend per seasonal cycle, and the last cycle against the previous one;
- **trend and seasonal strength** (0–1, from a classical decomposition), with the peak and trough positions (month, weekday, …) and the seasonal swing;
- autocorrelation at lag 1 and one season;
- the share of zeros;
- outlier periods;
- a possibly incomplete last period.

The charts are `timeseries_overview`, `timeseries_decomposition`, `timeseries_seasonal_profile`, `timeseries_autocorrelation`, and `timeseries_strength` (with 5 or more series). Use `--decompose <id>` to choose which series is decomposed (default: the largest).

```bash
S=<dir of this SKILL.md>/scripts; D=<dir of this SKILL.md>/..; OUT=<run folder>
python $D/prepare_series.py --table $OUT/files/table.csv --time-col date --target sales --id-cols store --out $OUT
python $S/timeseries_analysis.py --series $OUT/files/series.csv --out $OUT
```

`timeseries_analysis.md` holds the tables and flags. Interpret them this way:

| Flag / value | Meaning for the report |
|---|---|
| seasonal strength ≥ 0.6 | a clear repeating pattern. Name the peak and trough, and the swing ("December runs about 25% above the trend") |
| trend strength ≥ 0.6 | a sustained rise or fall. Give it per cycle ("about +4% a year") |
| strength < 0.3 | weak; don't describe a pattern that isn't there |
| last period far below expected | likely a partial period (the current month). Exclude it, or say so, before stating any "drop" |
| outlier periods | check them against known events. Never drop them silently |
| intermittent (≥ 30% zeros) | averages and trends mislead; describe how often it is non-zero, and the size when it is |
| short (under two cycles) | seasonality can't be measured; say so |
| autocorrelation high at one season | confirms seasonality independently of the decomposition |

Correlating two trending series finds a relationship even when there is none (both just grow). Compare their changes (period-on-period differences) instead, and say so.

If the user also wants a forecast, hand over to the **time-series-forecasting** skill with the same `series.csv`, and for a classification or regression model to the **tabular-classification-regression** skill with the same `table.csv`. Don't prepare either again from scratch. If `prepare_series.py` printed a `NOTE` listing numeric columns not carried as features (recorded as `unused_columns` in `series.json`), mention them in the handover: the forecasting skill decides whether to add them.

---

## Step 5 — Report

Write `report.md` at the top of the run folder, next to `files/`, and give the key answer in chat with its path. **Readers need not be technical**: someone who doesn't know what a standard deviation is must still follow every finding. Technical detail stays, as evidence, always with a plain-language explanation.

```markdown
# [Dataset name] — Analysis

### Summary
[3–5 plain sentences: what the data is, the direct answer, the 2–3 findings that matter most.]

### About the data
[What one row is, rows and columns, time span, what was cleaned and why: from `table.md`, with every removal and its reason.]

### Findings
#### 1. [Headline stating the finding in plain words]
**What we found.** [The result, with key numbers and group sizes.]
![...](files/name.png)
**How to read this chart.** [Axes, marks, where to look.]
**What it means for this dataset.** [Why it matters here, e.g. "the average order (€120) overstates what a typical customer spends (median €45)".]
**Technical detail.** [The statistics and what each says, e.g. "skewness 4.7 (above 1 is strongly skewed)".]

### Caveats
[What the data cannot support: missing data, small groups, sampling, correlation ≠ causation, assumptions.]

### Next steps
[2–4 follow-ups, each with why it is worth doing.]

### Method
[Source and size before and after cleaning; every cleaning step and the values or rows it affected (`table.md`); methods; `sh files/run.sh` to reproduce.]
```

Rules for findings:
- **Charts sit inside the finding they support**, after "What we found". There is no separate charts section. Every chart belongs to a finding. Every key finding with a visual shape (distribution, trend, comparison, relationship) gets one.
- **Every chart is explained**: what it shows, how to read it, what to take from it. A caption alone isn't enough.
- **Every statistic gets its significance on this dataset.** Not "correlation 0.82", but "heavier products almost always cost more (Spearman 0.82, n=4,310)", plus what that implies for the question.
- **Define technical terms on first use**, in one clause: "the median (the middle value when all orders are lined up)".
- **Use concrete magnitudes**: "about 1 order in 14" rather than "7.1%", "twice as high" rather than "ratio 2.03".
- **State confidence in words**: "clear, from thousands of rows" or "suggestive, from 40 customers".
- Use small tables for grouped results: the rows that matter, plus an "other" line.

---

## Interaction Style

- If the question is vague, don't ask what to analyze: run the Default Analysis and report what stands out.
- If a column's meaning is ambiguous and it changes the answer, ask rather than guess.
- If the data contradicts the user's premise, say so plainly, with the numbers.
- Don't invent columns, rows or values. If something needed is missing, say so.

---

## Quality Checklist

- [ ] Every reported number came from code run on the data (or is labelled as not)
- [ ] The profile was run, every quality issue was decided in `cleaning.json`, `prepare_table.py` applied it, and the re-profile shows only what was kept on purpose
- [ ] Every analysis ran on the prepared table, and every removed row has its reason in `table.md` and the report
- [ ] Whether the data is a time series was decided and stated; if it is, it was prepared once in the shared format and `timeseries_analysis.py` was run
- [ ] Row counts before and after cleaning are stated; averages and rates show group sizes; percentages have clear denominators
- [ ] The source file was not modified
- [ ] `report.md` is at the top of the run folder, everything else is in its `files/`, and `sh files/run.sh` regenerates every number and chart
- [ ] Every chart sits inside its finding, with a "How to read this chart" explanation
- [ ] Every finding says what it means for this dataset; technical terms are defined on first use
- [ ] Caveats are stated, including correlation vs. causation where relevant
- [ ] The answer to the actual question comes first
