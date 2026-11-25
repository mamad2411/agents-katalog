---
name: hs300-valuation-dca
description: Run digoal's CSI300 valuation DCA cron. Use when operating 沪深300 估值定投.
---

# CSI300 Valuation-Weighted DCA (digoal)

The owner's (digoal) reusable bundle for running, backtesting, and operating the
沪深300 (CSI300) valuation-weighted dollar-cost-averaging decision engine.

The algorithm is the result of 2026-08-27 backtest sessions: PE 60-month
rolling percentile + ERP (1/PE / 10Y Treasury yield) + trend filter (close vs
60-month MA × 0.85). Backtest on 2014-2026 confirmed the v4 multi-indicator
version (the owner-selected final variant) beats plain DCA, Alipay-style
"buy-only-below-30%-percentile", and a simpler two-band version on absolute
final value (¥207k vs ¥220k for plain DCA, but with 18% less capital deployed)
and on segmented drawdown (2021-2023 drawdown: -2.84% vs -5.90% for plain).

## When to Use

- User asks to deploy or operate the CSI300 valuation DCA cron
  ("沪深300 估值定投","hs300 valuation","110020").
- User asks to backtest or re-validate the algorithm against new data.
- User asks to manually fetch today's valuation decision.
- User asks to debug or extend the cron (push channel, parameters, indicators).

## When NOT to Use

- Generic index-investing analysis with no cron / no automation.
- Other indices (中证500, 中证1000, etc.) — needs adapter rewrite.
- A股个股决策 — different algorithm class entirely.

## Bundle Layout

```
.
├── SKILL.md
├── scripts/
│   ├── daily_decision.py                  # algorithm + decision engine
│   ├── hs300-valuation.sh                 # cron wrapper (bash)
│   ├── backtest_v2_extended.py            # final backtest
│   ├── backtest_v2_three_indicators.py    # intermediate backtest
│   └── backtest_valuation_dca.py          # initial backtest
├── templates/
│   ├── cron-prompt.md                     # cron create command + tuning
│   ├── feishu-push-message.md             # feishu push format spec
│   └── deploy-checklist.md                # new-machine deploy steps
└── references/
    ├── backtest-results.md                # detailed backtest outcomes
    ├── data-sources.md                    # akshare API details + dead ends
    └── pitfalls-detailed.md               # every pitfall with root cause + fix
```

The `scripts/` directory is canonical — the cron wrapper and the production
workdir both copy from here. The `references/` and `templates/` directories
are documentation only.

## Decision Algorithm (v4)

```
Inputs:
  pe_ttm         = CSI300 PE-TTM (monthly close)        # ak.stock_zh_index_hist_csindex
  close          = CSI300 close (monthly)                # same source
  cn10y          = China 10Y treasury yield (daily)      # ak.bond_zh_us_rate
  pe_pct         = current pe_ttm vs prior 60 months    # rolling percentile
  erp            = (1 / pe_ttm) / cn10y                  # equity risk premium ratio
  ma60           = 60-month MA of close
  trend_ok       = close > ma60 * 0.85

Output: monthly multiplier in {0, 0.3, 0.5, 1.5, 3.0}

Decision:
  if pe_pct > 0.50:                                          mult = 0      # high / mid-high, skip
  elif pe_pct > 0.30:                                        mult = 0.5    # mid-low
  elif pe_pct < 0.15 and erp > 3.0:                          mult = 3.0    # extreme low
  else:                                                      mult = 1.5    # ordinary low
  if not trend_ok:                                           mult *= 0.3  # bad-trend discount
```

The owner-selected deviation from the original proposal is the **50-70% band is
skip (0)**, not mid-buy (0.5x). That is intentional: the owner wants to save
capital for the deeper low-buy zone. Document this when proposing changes.

## Interpretation Framework (Section 7 of Article)

Each indicator gets a **semantic meaning label** in addition to its raw value
— defined in `scripts/daily_decision.py:interpret()`. The thresholds mirror
the article 《估值法定投原理》section 7:

| Indicator | Low | Mid | High |
|---|---|---|---|
| PE-TTM | <10 偏低 | 10-15 中性 | >15 偏高 |
| PE 60月分位 | <30% 低估(后 X% 便宜) | 30-70% 中性 | >70% 偏贵(前 X% 贵) |
| 10Y 国债 | <2% 极低 | 2-3.5% 中性 | >3.5% 偏高 |
| 股债比 (ERP) | <1.5 股票比债券贵 | 1.5-2.5 中性 | >2.5 便宜(分母<2% 时提示"分母低陷阱") |
| 现价 vs 60月均线 | <85% 趋势恶化 | 85-110% 趋势 OK | >110% 趋势强 |

The feishu push and the daily report both render these interpretations as a
"数据 → 含义" two-column table. This is the single most useful output for the
owner, because raw numbers alone (e.g. "PE 14.23") don't tell a non-finance
reader whether they should care.

See `references/backtest-results.md` for the current snapshot with the
interpretation table applied.

## Month-over-Month Comparison

In addition to the current snapshot, the script also computes a `vs last
month` diff (defined in `scripts/daily_decision.py:compare_to_last_month()`).
Output fields:

- `delta_close_pct`: CSI300 close percent change vs last month
- `delta_pe_pct_pp`: PE percentile change in percentage points
- `delta_decision`: e.g. "持平(0.0x)" or "从 0.5x → 0x(变贵,减仓)"
- `overall_dir`: `expensive` / `cheaper` / `flat`

The comparison is rendered both in the terminal output (`print_decision`)
and in the feishu push as a 3-row table. Currently (2026-08 vs 2026-07):
PE percentile dropped 11.7 pp (from 93.3% → 81.7%), close dropped 7.9%
(7386 → 6799) — **整体变便宜**, but decision is unchanged at 0x because
81.7% is still above the 50% skip threshold.

## 12-Month Trend Channel

`scripts/daily_decision.py:trend_n_months()` computes a rolling 12-month
trend across multiple indicators. Output fields:

- `overall_dir`: `expensive` / `cheaper` / `flat`
- `close_pct`: 12-month price channel change
- `pe_delta_pp`: 12-month PE percentile change
- `erp_delta`: 12-month ERP change
- `sparkline`: textual price path e.g. `6631 → 6912 → ... → 6799`
- `mult_changes`: how many times the decision multiplier switched bands

The channel direction is determined by **PE percentile + close jointly**;
when they disagree, PE percentile wins (because PE represents "expensive
relative to fundamentals", which is what the algorithm actually trades on).

## Next-Month Forecast (Trend Extrapolation, NOT Market Prediction)

`scripts/daily_decision.py:forecast_next_decision()` does a **linear
extrapolation** of the PE percentile trend. Output:

- `next_pe_pct_linear`: linear-extrapolated PE percentile for next month
- `next_mult_linear`: what the decision would be at that PE percentile
- `next_mult_naive`: baseline (next month = current month)
- `months_to_next_band`: months until the decision switches to the next
  tier, if the current trend continues. Returns `null` if the trend is
  moving away from the next tier (backlash).
- `caveat`: explicit warning that this is mechanical, not a forecast

**IMPORTANT:** This is the most dangerous part of the skill. The forecast
has no predictive power — it assumes next month behaves like the average
of the last 12. Real markets have regime changes (rate cuts, earnings
revisions, geopolitical events) that make this naive projection diverge
from reality within 2-3 months. The push message and terminal output both
flag this with a `⚠️` warning and label the section `🔮 下月预测`
(extrapolation, not forecast).

## Forecast Validation (Honest Assessment)

`scripts/forecast_backtest.py` ran a 79-month rolling backtest
(2015-01 → 2026-07). Honest results:

| Metric | Naive | Linear Extrapolation | Reality |
|---|---|---|---|
| MAE (avg abs error) | 11.19 pp | **12.13 pp** | Linear is **worse** than naive |
| Direction accuracy | 6.2% | 42.5% | Linear is "better than coin flip" only |
| Decision band accuracy | 66.2% | 63.7% | Both about the same |

**The linear extrapolation has NO predictive value.** Adding trend info
made MAE 8% worse because PE percentile is **mean-reverting** (high comes
back down, low bounces up), and a 12-month trend extrapolates the
opposite direction.

**The forecast still has utility, but not predictive:**
- The "trend direction" signal is more useful than the numeric estimate
- The "触达下一档" analysis is honest: tells you when the current trend
  makes the next tier unreachable (returns None) instead of pretending
  to give a number
- The PE-band breakdown shows high-percentile predictions have 100%
  decision-band accuracy (because 0x → 0x is the default); low-percentile
  predictions have ~59% (most regime-change happens there)

**Concrete consequences in production (2026-08-27):**
- The feishu push **dropped the numeric prediction table** (the naive vs.
  linear extrapolation rows). Kept only the "触达下一档分析" line +
  a short caveat about backtest accuracy.
- The terminal output similarly dropped the two numeric forecast rows.
- The `forecast_next` data is still written to `history.json` for future
  longitudinal analysis, but is not rendered to the user as a number.

**Recommendation:** Treat the `forecast_next` block as **trend monitoring
only**, not a prediction. Don't trust "next month PE = X%" numbers —
trust the "按当前速率永远到不了" / "5 个月后触达 1.5x" statements which
are honest about what the trend implies, nothing more.

See `references/forecast-validation.md` for the full report.

See `references/backtest-results.md` for the full breakdown by regime.

## How to Run Manually

```bash
# 1. Local one-shot run (writes reports/, appends to history.json)
#    Uses HS300_WORKDIR env var, defaults to digoal's production path
HS300_WORKDIR=/root/new/work/digoal/沪深300估值监控/2026-08-27 \
  python3 scripts/daily_decision.py --append --quiet

# 2. Just see the decision without appending to history:
python3 scripts/daily_decision.py --quiet

# 3. Re-run the final backtest (uses akshare live data):
python3 scripts/backtest_v2_extended.py

# 4. Trigger the cron right now (also pushes to feishu):
hermes cron run hs300-valuation-daily
```

## Cron Configuration

See `templates/cron-prompt.md` for the full create command and tuning options.

Key facts (verified at deploy time 2026-08-27):

- `--script` must be a bare filename; hermes resolves to
  `~/.hermes/profiles/digoal/scripts/`. Absolute paths and home-relative paths
  are rejected.
- `--workdir` accepts absolute paths but is normalized internally to the
  `/var/lib/postgresql/root/...` form. Both forms point at the same filesystem
  (bind mount) so scripts that write by either path land in the same location.
- Schedule `0 1 * * *` UTC = 09:00 Beijing. Cron expressions are UTC.
- `--no-agent` skips the LLM; the script's stdout is delivered verbatim. Do
  not add tqdm or ANSI color to stdout — it lands directly in feishu.

## Pitfalls (Quick List)

Full root-cause analysis in `references/pitfalls-detailed.md`. Top hits:

- **akshare `stock_index_pe_lg` and `stock_a_pe_pb` both fail** — legulegu.com
  adds a CSRF cookie gate. Use `stock_zh_index_hist_csindex` (PE-TTM is
  column 16).
- **akshare `stock_zh_index_value_csindex` returns a JPEG placeholder** —
  the oss-ch.csindex.com.cn URL it composes is dead. Don't try PB from this.
- **akshare `bond_china_yield` only spans 2020-2021.** Use `bond_zh_us_rate`.
- **`tqdm` progress bars in stdout land in feishu** — always pass `--quiet`
  or redirect 2>/dev/null.
- **heredoc + double-quoted `<<PY`** will try to execute `${VAR}` as a
  command. Use `<<'PY'` (single-quoted) and pass values via `sys.argv`.
- **First 60 months of PE percentile are NaN** — rolling window requires 60
  months. Backtests before 2019-01 will show all strategies as identical.

See `references/data-sources.md` for the full audit of every data-source
attempt (live, dead, paid).

## Deploying on a New Machine

See `templates/deploy-checklist.md` for step-by-step. Quick summary:

1. `pip install akshare pandas`
2. Copy `scripts/daily_decision.py` to your `<WORKDIR>/`.
4. Copy `scripts/hs300-valuation.sh` to `~/.hermes/profiles/digoal/scripts/`.
5. Run the `hermes cron create` command from `templates/cron-prompt.md`.
6. `hermes cron run hs300-valuation-daily` to verify the first feishu push.
7. Open feishu to confirm the message arrived (per-profile `.env` needs
   `FEISHU_*` credentials — not the global `/root/.hermes/.env`).

## Known Open Optimization Items

Tracked but **not yet implemented** — do not silently apply:

1. PB signal: csindex PB history URL is dead; needs custom calculation or
   alternate source.
2. Trend-filter coefficient 0.85 is empirical; sweep 0.80 / 0.90 not yet done.
3. Extreme-low thresholds `pe_pct < 0.15 AND erp > 3.0` never triggered in
   2014-2026; needs longer window to validate.
4. Earnings-revision filter (consensus EPS YoY) to discount false-cheap during
   earnings downgrades.
5. Multi-index adapter (中证500, 中证1000, 中证红利).

## Verification

After any change, run:

```bash
# 1. Algorithm still works against live data
python3 scripts/daily_decision.py --quiet

# 2. Backtest still produces sane numbers
python3 scripts/backtest_v2_extended.py 2>&1 | tail -20

# 3. Cron delivery channel is correct
hermes cron list | grep -A 8 hs300 | grep -E 'Deliver|Schedule'
```

A successful run shows: PE-TTM ~14, PE 60-month percentile in [0,1],
ERP around 3-5, and a decision in {0, 0.3, 0.5, 1.5, 3.0}.