---
name: tabular-classification-regression
version: 1.5.0
description: >
  Classification or regression on a table of independent rows (customers, orders, loans, houses): estimate one column from the others, find out how well it can be estimated and what drives it. Trains CatBoost against a linear / logistic baseline with ready-made scripts, and writes code, charts and a report for non-technical readers to one folder. Not for time series data (values of the same quantity measured period after period, to be forecast forward).
tags: [data, machine-learning, tabular, classification, regression]
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

# Tabular Classification and Regression Skill

Answers: **can this outcome be predicted from the available data, how well, and what drives it?** The model is an instrument, not the goal. CatBoost is the default because it performs well on tabular data with little tuning. The method stays the same whatever the model: framing, leakage checks, a clean split, a baseline, uncertainty and explanation.

**Do not use this skill for time series data.** If the rows are successive measurements of the same quantity over time (one row per day / week / month, for one series or for each store, product, sensor…) and the question is what the values will be next (next month's sales, next week's demand, tomorrow's traffic), this skill does not apply. Forecasting needs a backtest over several time-ordered windows, lag features and a seasonal-naive baseline, none of which this skill provides, and its scores would be misleading there. If you are unsure whether the data is a time series, ask the user before running anything.

A date column alone does not make data a time series. Independent cases that each carry a date (customers with a sign-up date, orders with an order date, loans with an issue date), predicted from their own attributes, belong here, and the time split in Step 2 handles the date.

**Use the ready-made scripts** (see **Scripts**) for the split, the baseline, CatBoost and the comparison. Write code only for what they don't cover. If the data hasn't been explored yet, profile it and check its quality first (**data-analysis** skill, Steps 1–3).

---

## Core Principles

1. **Start from the question, not the algorithm.** What is predicted, for whom, and for what decision. That sets the metric, the split and what counts as good enough.
2. **Always compare against a baseline.** A score means something only next to a linear / logistic regression and a trivial model. "AUC 0.82" says nothing; "0.82 against 0.81 for logistic regression" says the complexity bought almost nothing.
3. **The test set is touched once.** Tuning, early stopping and model choice use validation only. All models are scored on the same test rows, at the end.
4. **No leakage.** Remove columns known only after the outcome, or that copy the target, and say which ones and why.
5. **Report uncertainty.** A gap between models is a finding only if its confidence interval excludes zero.
6. **Recommend the simplest model that is good enough.** If the main model isn't clearly better, recommend the baseline.
7. **Predictive is not causal.** Never present feature importance as "what to change to move the outcome".
8. **Explain for everyone.** Every metric and chart in plain language and in this dataset's terms.
9. **Everything goes in one output folder.**

---

## Output Folder

- **Always pass `--out <run folder>`**: the scripts have no default. Use the location the user gives; if they give none, choose a new, descriptive folder yourself, and tell the user where it is. One folder per run: never reuse one that holds another run. The scripts create it, and refuse to mix runs with a different data file or target.
- **The layout is fixed**: `report.md` at the top, and **everything else in `files/`**:
  ```
  <run folder>/
  ├── report.md      ← you write it; the only file at the top
  └── files/         ← the scripts write here: the split, the models, metrics, predictions, charts, the copies of the scripts, and run.sh
  ```
  Pass the run folder as `--out` (not `files/`); every script writes into its `files/` by itself.
- `files/run.sh` holds the exact commands, with absolute paths, so `sh <run folder>/files/run.sh` rebuilds everything without the skill.
- Code you write yourself (a custom model, an extra chart) goes in `files/` too, and its command goes at the end of `files/run.sh` as `"$PY" <script>.py ...`, so it runs with the same interpreter as the scripts.
- An extra chart is drawn with `seaborn`: `import seaborn_style` (copied into `files/` by every script, with the `palette.json`, `typography.json` and `fonts/` it reads; all live in `../../resources/`) sets the house theme when imported. Make the figure with `fig, ax = seaborn_style.figure()`, title it with `seaborn_style.title(fig, ...)`, and save with `seaborn_style.save(fig, Path(__file__).resolve().parent, "<name>")`, which writes `<name>.png`. Colours by role from `seaborn_style.PALETTE` by key (`["charts"]["categorical"]` for series, `["text"]["light_background"]["muted"]` for reference lines) and `seaborn_style.colormap("sequential" | "diverging")` for scales, never as hex; pass `saturation=1` to seaborn's bar and box plots. The `charts` skill has the rest of the style.
- CatBoost writes `catboost_info/` into the current directory by default. The scripts turn this off. In any CatBoost code you write, pass `allow_writing_files=False`.
- Never modify the source data, and never write next to it.
- When done, give the user the folder path and the path of `report.md`.

---

## Step 1 — Check the Requirements

Do this before anything else. The scripts need these Python packages:

| Package | Needed for |
|---|---|
| `pandas`, `numpy` | every script |
| `scikit-learn` | the baselines, the split and the metrics |
| `catboost` | the main model (see **Choosing the Model** if it can't be installed) |
| `seaborn` | the charts (brings `matplotlib`) |
| `joblib` | saving the baseline model (installed with `scikit-learn`) |
| `pyarrow` | Parquet files only |
| `openpyxl` (`.xlsx`) / `xlrd` (`.xls`) | Excel files only |

- **First pick the Python that runs the scripts**, and use it for every script in the run. Run `which python` (or `python3`) to see which one that is. If the packages are missing there but installed in a project environment (a `.venv/bin/python` in the working directory, or the one `uv run` uses), run the scripts with that interpreter instead of installing them again. `files/run.sh` records the interpreter as `PY` and reruns with it. `PY=/path/to/python sh files/run.sh` reruns with another one.
- Check them with that interpreter: `python -c "import pandas, numpy, sklearn, catboost, seaborn, joblib"`, adding `pyarrow` or `openpyxl` when the data is in that format.
- **`catboost` is installed without asking** when it's missing, because it's the main model of every run. Install it into the environment that runs the scripts (`python -m pip install catboost`, or `uv pip install catboost` in a `uv` project). Then tell the user in one line that you installed it.
- **Ask before installing anything else** that's missing, and name the packages. Install into the user's environment only if they agree (`pip install pandas numpy scikit-learn seaborn`). With `uv`, `uv run --with pandas --with numpy --with scikit-learn --with catboost --with seaborn python <script> ...` leaves their environment untouched. It still downloads, though, so ask first.
- **Charts are PNGs**, drawn with `seaborn` (no browser needed). If the user asks for an interactive chart, draw it afterwards with the `interactive-charts` skill (Plotly, one self-contained HTML page per chart, about 4.8 MB each) from the files this run wrote, and save it in `files/`; the scripts never write pages.
- If an install fails (no network, no permission), or the user declines one of the others:
  - without `pandas`, `numpy` or `scikit-learn`, the scripts can't run. Say so, and don't train models by hand.
  - without `catboost`, use the fallback in **Choosing the Model**.

---

## Step 2 — Frame the Problem

Settle these before running anything. Ask only when the data can't answer:

- **Target**: which column. Ask if it isn't obvious.
- **Purpose**: what the prediction is for (ranking customers to contact, pricing, flagging risky cases). This decides which errors matter.
- **Task**:
  - **Classification** for a categorical or boolean target, or integer codes naming classes.
  - **Regression** for a quantity where distances matter.
  - Few-valued integers (ratings 1–5, counts) could be either, so ask.
- **Unit of prediction**: what one row is (a customer, an order, a day).
- **When the prediction is made**: only features known at that moment may be used. This is the most reliable leakage test.
- **Main metric**, chosen before seeing results:
  - **Binary**: ROC AUC, plus PR AUC when the positive class is under ~20% of rows.
  - **Multiclass**: ROC AUC (one-vs-rest), with macro F1 and balanced accuracy.
  - **Regression**: RMSE, or MAE if a few large errors shouldn't dominate. Report R² as well.
  - If one error is much costlier than another (a missed fraud against a false alarm), say so and report a metric that captures it (recall at a given precision, cost-weighted error).
- **Split**: `make_split.py` decides it (`--split auto`, the default), so don't choose it by hand. Check what it printed against the question:
  - **Time**, when there is one date column: train on the past, test on the most recent rows, as when the model predicts new cases.
  - **Group**, when there is no date column but one id-like column repeats (a customer on several rows): all of an entity's rows go to one side, so the test has only unseen customers.
  - **Random** otherwise, stratified for classification.
  - It stops when there are two candidates (two date columns, two repeated ids). Pass the one that fits, with `--time-col` or `--group-col`.
  - Override with `--split random|time|group` only for a reason, and give it in the report. For example: the date records when a row was *entered*, not when the prediction is made. Auto prefers time and group because an unneeded one only makes scores slightly pessimistic, while a missing one makes them optimistic.

**Out of scope**, so say so rather than force it: time series data, i.e. forecasting one or many series from their own past, images / audio / text as the main input, and causal effects ("what if we raise the price").

---

## Step 3 — Decide What to Exclude

The scripts do the mechanical preparation: missing targets, column types, the baseline's imputation, scaling and one-hot encoding, and date features (`--date-cols`). **What to exclude is your job.** Pass it with `--drop`, and list every exclusion with its reason in the report:

- **Identifiers**: a unique value per row.
- **Leaky columns**:
  - columns recorded after the outcome (`cancellation_date` when predicting churn)
  - columns derived from the target
  - any single feature that predicts the target almost perfectly. Treat it as suspicious until explained.
- **Free text**: leave it out unless asked, and say so.

Report how many rows had a missing target (`dropped_missing_target` in `split.json`).

---

## Choosing the Model

Every run trains a **trivial** model (the floor: one that doesn't beat it learned nothing), a **linear baseline** (the simple, interpretable reference) and a **main model** (which captures non-linear effects and interactions). Only the main model varies:

| Situation | Main model |
|---|---|
| Default | **CatBoost**, via the scripts |
| `catboost` can't be installed (the install failed) | scikit-learn's `HistGradientBoostingClassifier` / `HistGradientBoostingRegressor` (`categorical_features="from_dtype"` on `category` columns; `permutation_importance` for importance) |
| Under ~200 rows, or the model must be fully transparent | Run the comparison anyway, and expect to recommend the linear model |
| The user names a model (XGBoost, LightGBM, …) | That model, with everything else unchanged |

For a main model other than CatBoost:
1. Write `<task>_<name>.py` in `files/`, modelled on the CatBoost script.
2. Load the data with `common.load_dataset(args, task)`, after `common.base_parser`, so it uses the split `make_split.py` wrote.
3. Save test predictions with `common.save_predictions(out, "<name>", ...)`.
4. Run the compare script with `--main <name> --main-label "<Name>"`.

The report names the main model and says in one sentence what kind of model it is. For boosted trees: "many small decision trees, each correcting the previous ones' mistakes".

---

## Scripts

There are two places. Paths in this file are relative to this SKILL.md, whose location is the `[file: …]` line above this text: resolve them from its directory, never from the working directory.

- **This skill's scripts**, in `scripts/`, sharing `common.py`: `make_split.py`, and a separate set per task (`classification_*`, `regression_*`).
- **The scripts shared by all the data skills**, one level above this skill's folder, in `..` (`builtin/data/`):
  - `prepare_table.py`, the cleaning (the data-analysis skill's Step 3);
  - `data_utils.py`, the helpers every script uses.

  This skill's scripts find them there by themselves. Run everything in place, and don't move or copy scripts out of the skills.

`python <script> --help` documents every option.

| Script | Does |
|---|---|
| `classification_baseline.py` / `regression_baseline.py` | Logistic / linear regression with its preparation (median imputation and standardization for numeric features, one-hot encoding for categorical ones), plus the trivial model |
| `classification_catboost.py` / `regression_catboost.py` | CatBoost with early stopping on validation, optional `--tune`, feature importance, SHAP effect charts |
| `classification_compare.py` / `regression_compare.py` | Scores all models on test, bootstraps a 95% CI for CatBoost − baseline, writes the verdict and comparison charts |

**Before running**:
- Step 1: the requirements are installed.
- Steps 2 and 3: the problem is framed and the exclusions decided.

**Start from the prepared table when there is one.** If a data-analysis run on this data wrote a prepared table (`table.csv`), pass it with `--table`: the model is then trained on the data the analysis described, with the same cleaning. If the raw file needs cleaning (numbers or dates stored as text, placeholders like `-1`, duplicate rows), clean it first with the shared `prepare_table.py`, following the data-analysis skill's Step 3. A clean raw file can go to `--data` directly.

**Run in this order**. `make_split.py` is the only script that takes the data, the features and the split. The others take `--out`, and read everything else from its `split.json` (`regression_*` works the same way):

```bash
S=<dir of this SKILL.md>/scripts; OUT=<run folder>
python $S/make_split.py --table /abs/<analysis run folder>/files/table.csv --target churned --task classification --drop customer_id --out $OUT
# or, for a clean raw file: --data /abs/customers.csv
python $S/classification_baseline.py --out $OUT
python $S/classification_catboost.py --out $OUT
python $S/classification_compare.py --out $OUT
```

**Options**:

| Where | Option | Use |
|---|---|---|
| `make_split.py` | `--task classification\|regression` | required: from Step 2 |
| | `--table` / `--data` | the prepared table (typed; its date columns become date features by themselves), or a clean raw file |
| | `--sep ';'`, `--decimal ','`, `--encoding latin-1` | with `--data` only: how a CSV / TSV is read: separator (detected when omitted), decimal mark (`.`), encoding (`utf-8`). See **Reading the file** below. |
| | `--sheet NAME` | the Excel sheet to read (default: the first) |
| | `--drop col ...` | ids and leaky columns |
| | `--date-cols col ...` | turn dates into year / month / day-of-week / days-since features |
| | `--split auto\|random\|time\|group`, `--time-col`, `--group-col` | default `auto` (Step 2). Passing a column implies its split |
| | `--test-size`, `--valid-size`, `--seed` | defaults 0.2, 0.2, 42. Change them only with a reason, e.g. under ~1,000 rows a 0.25 test set gives steadier scores |
| baselines | `--min-frequency` | one-hot grouping of rare categories (default 10) |
| `classification_baseline.py` | `--C`, `--class-weight balanced` | regularization; class weighting |
| `regression_baseline.py` | `--alpha` | ridge instead of plain least squares, for many one-hot columns or when it overfits |
| `*_catboost.py` | `--tune` | depth × learning-rate grid chosen on validation. Use it when time allows. |
| | `--top-effects` | how many SHAP effect charts to draw (default 3) |
| `classification_catboost.py` | `--class-weight balanced` | try it on both models when a class is under ~10%, and compare on validation |
| `regression_catboost.py` | `--loss MAE` | when MAE is the metric or the target has extreme values |
| `*_compare.py` | `--metric`, `--main`, `--main-label`, `--baseline-label` | defaults `ROC_AUC` / `RMSE`, `catboost` |

**Reading the file** is where most failed runs start. The scripts detect the column separator of a CSV / TXT file (`,` `;` tab `|`) and print what they used. A file read with the wrong separator stops the script. A comma-decimal column read without `--decimal ','` only prints a warning, and would otherwise be treated as a category:

| Symptom | Cause | Fix |
|---|---|---|
| one column, whose name holds every header (`id;region;price`) | the separator isn't `,` | `--sep ';'` (or `'\|'`, `'\t'`) |
| numbers like `8,60` read as text, or split across two columns | comma decimal mark (European exports, usually `;`-separated) | `--decimal ','` |
| `UnicodeDecodeError`, or `Ã©` in place of `é` | the file isn't UTF-8 (typical of Excel exports) | `--encoding latin-1` or `cp1252` |
| the wrong Excel sheet | the scripts read the first sheet | `--sheet NAME` |

Lines starting with `#` before the header are skipped as comments and printed (`Skipped the first N line(s)…`). Read them, since they often give the units or the source. Do not edit the file to remove them: the scripts already skip them, and `run.sh` rebuilds from the original file.

Quote the separator on the command line (`--sep ';'`): an unquoted `;` or `|` is taken by the shell.

Only `make_split.py` takes reading options. The other scripts read the output folder.

**Guarantees**:
- `make_split.py` writes the split (`split.csv`) and its settings (`split.json`: data, reading options, `--drop`, `--date-cols`, the resolved split and why). Every later script rebuilds the same dataset from them. Rerunning `make_split.py` in the same folder with other settings is refused.
- It warns about id-like columns that are still features. Drop the ones that only name a row or an entity.
- The test set is only scored, never used for fitting or tuning.
- Wrong-task targets are refused: a non-numeric target for regression, a continuous one for classification. Classes under 10 rows get a warning.
- Each script copies itself, `common.py` and `data_utils.py` into `files/`, and logs its command in `files/run.sh`. The folder then reruns on its own.

**Outputs, and where each goes in the report**:

| File | Use it for |
|---|---|
| `comparison.md` | Finding 1: the metrics table for all three models, the CI and verdict; per-class recall (classification) or the share of rows predicted within ¼ / ½ / 1× the target's typical spread (regression). The tables are ready to paste. |
| `model_comparison.png` | Finding 1 |
| `confusion_matrices.png`, `roc_curves.png` (binary) / `predicted_vs_actual.png`, `error_distribution.png` | Finding 2: where the models are right and wrong |
| `catboost_feature_importance.png` / `.csv`, `baseline_coefficients.png` / `.csv` | Finding 3: what drives the predictions |
| `catboost_effect_<feature>.png` | Finding 4: how the top features act |
| `catboost_learning_curve.png`; `train` / `valid` / `test` in `*_metrics.json` | overfitting (Caveats) |
| `split.json` | the split and why it was chosen (`split`, `split_reason`), row counts, dropped rows and columns, feature types (The task, Method) |

The verdict in `comparison.json` is mechanical. The CI either includes zero ("not distinguishable") or it doesn't. Your recommendation also weighs whether the gain matters for the purpose.

**Adapting**:
- Never edit the scripts in the skill directory. Edit the copy in `files/` and run that copy, which is not overwritten.
- For anything else the scripts don't do, write a new script in `files/` and add it to `files/run.sh`.

---

## Step 4 — Interpret

Read the outputs above and explain them:

- **What matters**:
  - Compare CatBoost's importance (each feature's share of its decisions, summing to 100) with the baseline's coefficients. The coefficients are comparable across numeric features, which are standardized; each one-hot column counts on its own.
  - Agreement between the two makes the story credible. Disagreement usually means a non-linear effect or an interaction.
- **How the top features act**: a SHAP value is how much a feature pushed one prediction up or down.
  - A curve or threshold in the effect chart explains why CatBoost beat the baseline.
  - A straight line explains why it didn't.
- **Where the models fail**:
  - Classification: which classes get confused, and how often.
  - Regression: ranges of the target predicted consistently too high or too low.
- **Overfitting**:
  - A training score far above the test score belongs in Caveats.
- **Importance is not causation.** Say so whenever importance is discussed.

---

## Step 5 — Report

Write `report.md` at the top of the run folder, next to `files/`. Lead with the prediction problem and its answer: whether the outcome can be predicted, how well, and what drives it. Which model won comes second.

Every finding follows the **data-analysis** pattern:
1. **What we found**
2. the chart, placed inside the finding (there is no separate charts section)
3. **How to read this chart**
4. **What it means for this dataset**
5. **Technical detail**

```markdown
# Predicting [target]

### Summary
[3–5 plain sentences: what was predicted from what, and why; how well, in concrete terms; the recommended model and why; the 2–3 main drivers.]

### The task
[What a row is, what is predicted and when, train / validation / test sizes, what was excluded and why, the deciding metric.]

### The models
[One plain sentence each: trivial model, baseline, main model, and why each is there.]

### Findings
#### 1. [How predictable the outcome is, and how the models compare]
**What we found.** … ![...](files/model_comparison.png) **How to read this chart.** … **What it means for this dataset.** … **Technical detail.** [metrics table, 95% CI, best iteration]
#### 2. [Where the model is right and wrong]
#### 3. [What drives the predictions, compared across the two models]
#### 4. [How the top feature acts]

### Recommendation
[Which model and why; whether it is good enough for the stated purpose.]

### Caveats
[Exclusions, overfitting, small classes, drift into future use, importance ≠ causation, what the test set doesn't cover.]

### Next steps
[2–4 concrete follow-ups.]

### Method
[Source and size; target and task; split; each model and its settings; `sh files/run.sh` to reproduce.]
```

**Make every metric understandable**:
- Translate it into this dataset's terms:
  - RMSE 1.07 in €k: "typically off by about €1,000".
  - ROC AUC 0.82: "picking one churner and one non-churner, the model ranks the churner higher 82% of the time; 50% is a coin flip".
- Use counts: "of 100 customers who churned, the model flagged 72, the baseline 58".
- Put the gap in proportion: say whether it matters for this use.
- State the CI in words: "on resampled test data, the advantage stayed between X and Y, so it is / isn't reliable".

---

## Interaction Style

- If the target or the purpose is unclear, ask one focused question. Otherwise use sensible defaults and state them in the report.
- If a feature looks leaky, remove it and say so. Never keep or drop it silently.
- Don't overstate a win. "Both models perform the same, so use logistic regression" is a good outcome.
- Don't invent columns, results or business context. Say when a request needs something the data can't support (causal claims, forecasts beyond its time span).

---

## Quality Checklist

- [ ] Target, purpose, unit of prediction, metric and split were settled before training
- [ ] Ids and leaky columns were dropped and listed with reasons
- [ ] `make_split.py` settled the split, its choice (`split_reason`) fits the question or was overridden with a stated reason, and the test set was used only for the final scores
- [ ] The report gives the metric for all three models, with the 95% CI for the gap
- [ ] The recommendation follows from the CI and whether the gain matters, not from model sophistication
- [ ] Every metric is translated into plain terms; every chart sits inside its finding and is explained
- [ ] Importance is compared across the two models and comes with the "not causation" caveat
- [ ] `report.md` is at the top of the run folder, everything else (your own code included) is in its `files/`, and `sh files/run.sh` regenerates it
