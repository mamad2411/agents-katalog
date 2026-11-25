---
name: quant-algo-backtest-report
description: VWAP backtest on OHLCV data, train/test split, report.
metadata:
  source_frontmatter:
    version: 1.0.0
  imported_from: hermes
---

# Quant Algorithm Backtest & Report

Use when a quant course/internship task asks to implement a trading algorithm (e.g. VWAP, TWAP, participation) against a benchmark on OHLCV data, evaluate train/test performance, and write a report. Proven on Quant Academy Project 1 Part 2 (AAPL VWAP).

## Data conventions (1-min OHLCV, FirstRate sample)

- CSV columns: `timestamp,open,high,low,close,volume`. Timestamps are **US Eastern time** — a day spans 04:00–19:59 (pre-market 04:00, regular 09:30–16:00, after-hours to 19:59). Do NOT assume UTC.
- Regular session filter: `09:30 ≤ time ≤ 16:00` (391 minutes/day, includes open/close auction prints).
- Assignment assumption "minute average price": `typical = (high + low) / 2`. Benchmark VWAP = `Σ typical_t·vol_t / Σ vol_t`.
- Sanity checks before modelling: NaN counts, non-positive prices/volumes, rows/day distribution, min/max timestamps, unique days.

## Algorithm pattern (no look-ahead)

1. Split **by date**: first 75% of sorted unique dates = train, last 25% = test (report both). `n_train = floor(0.75·n_days)`.
2. Volume profile `F(t)` = mean cumulative fraction of daily volume per minute-of-day, built on **train days only** (forward-fill missing minutes). Typical AAPL shape: F(10:30)≈0.23, F(12:00)≈0.42, F(15:30)≈0.75.
3. Schedule `Q` shares/day (e.g. 1M; check it's small vs avg daily volume, ~1.7% for AAPL). Residual schedule: `q_t = (Q − Σ_{s<t} q_s) · (F(t)−F(t−1)) / (1−F(t−1))`. When Q ≪ daily volume a per-minute participation cap never binds and static == residual — say so explicitly in the report.
4. Execution assumed at minute typical price (same convention as benchmark), so deviation is purely volume-timing, cleanly attributable.
5. Variants worth trying: signal tilt (scale slice by `1 + θ·sign(trailing-VWAP − last price)`, grid-search θ on train). On 1-min data mean-reversion tilts usually add no value — report the honest negative result; the brief itself expects not beating VWAP.
6. Metrics per day: dev_bps = (algo−bench)/bench·1e4; report mean, median, std, mean|·|, %days within ±2/5/10 bps, max|·|, intraday max tracking error (|cum traded − cum vol|). Also early-half vs late-half of test set (performance-worsening check) and a worst-days table.

## User deliverable format rules (critical)

- **LaTeX by default** (xelatex + Times New Roman, compile twice) UNLESS the task text explicitly says "word document" — then .docx via python-docx (compact: margins 1.1–1.4 cm, 9pt body, Table Grid) and LaTeX is not a substitute. Check the task wording before choosing.
- **"Less than N pages" means ≤ N pages** (user: "<2 的意思是1或2"). Verify page count: `soffice --headless --convert-to pdf --outdir /tmp/x file.docx` then `fitz.open(...)` → `len(doc)`; same for LaTeX after xelatex. If over, shrink margins/font/table size first, then trim prose.
- Repo policy: `*.pdf` is gitignored — commit SVG charts + generator scripts, generate PDFs locally for embedding.
- Keep analysis reproducible: `scripts/` .py files (not just notebooks), cleaned CSV in `data/`, exported LaTeX tables (`tab_*.tex`) + `stats.txt` in `report/`.

## Pitfalls

- **Never name an analysis script `inspect.py`** — it shadows stdlib `inspect`, numpy/pandas fail with a confusing "partially initialized module ... circular import" error. Use e.g. `data_inspect.py`.
- Google Drive folder links: `pip install gdown; gdown.download_folder(url, use_cookies=False)`. The folder may NOT contain every ticker the brief names — check the actual download list.
- Zero-tolerance for fabrication: save the brief VERBATIM to `task.md`; if the PDF text is self-contradictory (e.g. a garbled no-look-ahead assumption), keep verbatim text + add a Notes line stating the intended meaning; never silently rewrite.
- git: `git add <specific paths>` only; check `git status` first so an unrelated uncommitted WIP file doesn't get swept into your commit; commit+push immediately after file changes.

## Reference

- `references/vwap-aapl-example.md` — working AAPL example: cleaning script, profile numbers, algorithm code sketch, full result tables (train/test), charts list.
- `references/hkex-official-sources.md` — verified HKEX official URLs + current facts (trading hours, POS/CAS mechanics, VCM bands, Phase-2 tick-size table, severe-weather SWT) for the exchange-mechanics report.
