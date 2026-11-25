---
name: backtest
description: Run a backtest for a saved strategy file and interpret the result. Strategy validation, backtest, hypothesis falsification, result interpretation, performance analysis, strategy test. Use when the user asks to validate an existing {data_root}/strategies/{slug}.json file, or immediately after receiving a create-strategy handoff payload (slug + hypothesis + falsification_criterion) that needs hypothesis validation.
compatibility: Requires uv, network access for Upbit candle API, write access to {data_root}/reports/
metadata:
  version: "0.1"
---

# backtest

Start from a JSON strategy file, run the backtest tool, interpret results as **factual statements + benchmark comparison + hypothesis falsification judgment**, and hand findings back to create-strategy when revision is needed.

This skill is the **CLI wrapper and result interpretation guide in the hypothesis-to-falsification workflow**: the tool returns deterministic results, and the skill explains what those results mean. Never recalculate or estimate the result values.

Detailed guides are split into references/:
- Result interpretation principles and report format: [references/result-interpretation.md](references/result-interpretation.md)
- Benchmark comparison method: [references/benchmark.md](references/benchmark.md)
- Timeframe-specific default periods: [references/period-defaults.md](references/period-defaults.md)
- Official market-rule sources for manual checks: [references/market-rules.md](references/market-rules.md)

Load `skills/references/glossary.md` when explaining metric names, indicator names, or strategy terms in Korean.

---

## Data Root and Execution Mode

At the start of work, identify the mode and resolve `{data_root}` as an absolute path.

| Mode | Detection | `{data_root}` |
|---|---|---|
| clone mode | Running in the upbit-strategy-toolkit repo workspace/cwd | The repo root (absolute). The wrapper pins it to the repo root regardless of your cwd, so cache/strategies/reports always land under the repo even when invoked from a subdirectory. |
| agent skills mode | Only the skill was installed with `npx skills`, and the repo is not in the current workspace | `$HOME/.upbit-strategy-toolkit` |

Interpret slug-based requests as `{data_root}/strategies/{slug}.json`. Always pass the absolute strategy JSON path to the wrapper.

Use this skill's wrapper for tool calls instead of running `upbit-strategy-toolkit` directly.

```bash
bash scripts/upbit-strategy-toolkit.sh ...
```

## Routing Contract

- Role: run saved strategies and interpret results
- Prerequisite/recovery: route to `setup` when uv is missing, the wrapper fails, or the CLI fails
- Next step: use `create-strategy` if the strategy needs revision after result interpretation
- Out of scope: this skill does not synthesize strategies

---

## Triggers

- "Run a backtest for this strategy"
- "Validate {slug}"
- "Review the backtest result"
- Immediately after a create-strategy handoff when the payload includes hypothesis/falsification criteria

## Do Not

- **Do not recalculate or estimate result values** - quote tool stdout exactly. Do not recalculate or approximate total return, MDD, Sharpe, or CAGR. See [Result Recalculation Guardrail](#result-recalculation-guardrail).
- **Do not judge good/bad** - state facts only, such as "return +12%, +4%p ahead of benchmark +8%". Do not say "performance is good". See [Result Judgment Guardrail](#result-judgment-guardrail).
- **Do not recommend a strategy, asset, trade timing, trade price, target return, or holding period** - keep the output on factual comparison, hypothesis judgment, and revision candidates only.
- **Do not hide tool limitations from the user** - slippage, order book liquidity, and partial fills are not reflected. Mention this once in the report.
- **Do not connect to live trading** - see [Live Trading Guardrail](#live-trading-guardrail).
- **Do not ask for start/end every time** - apply the timeframe-specific defaults in [references/period-defaults.md](references/period-defaults.md) first, and override them only when the user explicitly provides a period.
- **Do not modify user-specified dates on period errors** - if the user explicitly provides start/end dates and the tool returns a period error, report the error and ask the user before running with any different dates.

---

## Investment Recommendation Guardrail

If the user asks which strategy is better, more profitable, worth choosing, whether a result means they should buy/sell/hold, when they should trade, what price they should trade at, what return they should target, or how long they should hold, do not answer the recommendation itself.

Put the Investment Recommendation Notice from `## Required Notices` at the end of the response. If the user's message is in Korean, use the Korean version; otherwise use the English version.

Then limit the response to:
- factual metric comparison from the tool output,
- hypothesis falsification status when available,
- limitations such as sample size, slippage, liquidity, and fees,
- supported next steps such as running another backtest or revising user-specified rules in `create-strategy`.

Do not turn factual comparisons into a recommendation about which strategy to use.

---

## Result Recalculation Guardrail

If the user asks to recalculate, re-derive, or adjust a reported metric (for example, excluding fees, applying slippage, or converting to a different unit), even if the arithmetic looks simple, do not perform the calculation yourself. Treat this as an intent-based rule, not a keyword-only rule, and apply it across languages.

Refuse the calculation and state the reason: backtest result values are interpreted exactly as reported by the tool, not recalculated or estimated outside the toolkit. All metric values must come only from a toolkit CLI backtest run, so limit the response to running a new backtest with different run arguments (`fee_rate`, period, etc.) - never manual arithmetic on the existing result.

---

## Result Judgment Guardrail

If the user asks whether a backtest result is good, bad, satisfying, or worth trusting in evaluative terms, do not answer with an adjective judgment. Treat this as an intent-based rule, not a keyword-only rule, and apply it across languages.

If the question shifts into whether to buy/sell/hold, or which strategy is more profitable, apply [Investment Recommendation Guardrail](#investment-recommendation-guardrail) instead - that guardrail takes priority when both could apply.

Decline the adjective judgment and state that this judgment belongs to the user. Then redirect to the allowed evaluation scope: logical consistency, hypothesis falsification, overfitting risk, risk-management concerns, and data/sample caveats, framed as evidence review, not a verdict.

---

## Workflow

### Market/Exchange Mismatch Handling

If the user requests a market or exchange that differs from the strategy file, **do not bypass with a temporary file.**
Update the strategy through the `create-strategy` skill first.

Present choices to the user with the `AskUserQuestion` tool:

```
Strategy file market: KRW-BTC
Requested market:     KRW-ETH  <- mismatch detected

-> AskUserQuestion tool call:
  question: "The strategy file market (KRW-BTC) differs from the requested market (KRW-ETH). What should I do?"
  header: "Market mismatch"
  options:
    - Update existing file: change {slug}.json market to KRW-ETH
    - Save as new file: save as {slug}-eth.json
    - Cancel: stop the backtest
  (The Other option can accept free-form input)
```

### Timeframe Mismatch Handling

Before running the backtest, read the strategy JSON to get the `timeframe` field.
If the user requests a timeframe that differs from the strategy file's `timeframe`, **do not run with the mismatched timeframe.**
Update the strategy through the `create-strategy` skill first.

Present choices to the user with the `AskUserQuestion` tool (options: create new strategy file via `create-strategy`, use existing timeframe, or cancel).

If "Create new strategy file" is chosen, hand off to `create-strategy` with the slug and new timeframe.
If "Use existing timeframe" is chosen, continue with STEP 2 using the strategy file's timeframe.

### STEP 1. Parse Input - Handoff vs Direct Call

Identify which mode applies:

**Mode A: immediately after a create-strategy handoff**

The payload contains:

```
slug: {slug}
hypothesis: {one-sentence hypothesis}
falsification_criterion: {falsification criterion - for example, "win rate < 40% or MDD > 25%"}
notes: {free-form notes such as period-adjustment reason, optional}
```

-> Use the hypothesis/falsification criterion as provided. **Do not accept a period** - the timeframe-specific default in STEP 2 decides it.

**Mode B: direct user call**

No `hypothesis` / `falsification_criterion`. The period is also decided in STEP 2.

**Presentation format**:

```
backtest

Strategy: {slug}.json / {market} / {timeframe}
Period: {start} ~ {end} (timeframe={tf} default or user-specified)
Hypothesis: {show only in Mode A}
Falsification criterion: {show only in Mode A}

Proceeding.
```

### STEP 2. Decide the Period

The backtest period is **UTC-based**. When a `YYYY-MM-DD` date string is passed to the CLI as-is, the tool interprets it as UTC 00:00. Convert to UTC only when the user specifies a timezone such as "KST 2024-01-01" (for example, KST 2024-01-01 00:00 -> UTC 2023-12-31).

| Priority | Source |
|---|---|
| 1 | start/end explicitly stated by the user |
| 2 | Timeframe-specific default - [references/period-defaults.md](references/period-defaults.md) |

**Only the backtest skill owns period selection.** create-strategy does not send a separate recommended period — if it did, that period could conflict with the timeframe-specific defaults defined here.

**Summary of timeframe-specific defaults** (full table in references):
- `1d` -> last 1 year
- `1h` -> last 3 months
- `1m` -> last 1 week
- Other timeframes are calculated around roughly 250 candles

`end_date` defaults to yesterday (today - 1, UTC) because the historical data service does not serve the current day by spec — see [references/period-defaults.md](references/period-defaults.md). Warn once before calling when the request implies a large candle count (for example, user-forced `1m x 1 year`).

### STEP 3. Call run_backtest + Save CSV

The backtest tool **saves the CSV automatically**. The skill does not save it separately. The CSV is automatically saved to `{data_root}/reports/{slug}-{YYYYMMDD_HHMMSS}.csv`.

```bash
STRATEGY_PATH="{data_root}/strategies/{slug}.json"
bash scripts/upbit-strategy-toolkit.sh backtest run "$STRATEGY_PATH" --start {start_date} --end {end_date}
```

Add options when overrides are needed:
- `--capital FLOAT` : initial capital (when omitted, defaults to a quote-appropriate value: KRW 1,000,000 / USDT 1,000 / BTC 0.01)
- `--fee-rate FLOAT` : fee rate (when omitted, the exchange/market default from market rules is applied automatically)
- `--no-verbose` : suppress stdout summary, CSV path, and trade highlights (default: verbose)
- `--force-refresh` : ignore cache and refetch candles from the API

#### Investment Caution Handling

Always run the first attempt with no stdin input piped in. The CLI prompts interactively for a caution-flagged market; with no stdin data available in agent environments, the prompt hits EOF immediately and the run auto-cancels with exit code 1.

Detect caution by checking both conditions:
- exit code is 1
- stdout contains `"investment caution"`

**If caution is detected — pause and ask the user before re-running:**

> ⚠️ **{market} is currently under investment caution.**
> The backtest was cancelled. Would you like to proceed anyway?

- **Yes** → re-run the same command with `y` piped into stdin (e.g. `echo y | bash scripts/upbit-strategy-toolkit.sh backtest run ...`), then continue to STEP 4
- **No** → stop and inform the user the backtest was cancelled

If exit code is 1 but stdout does **not** contain `"investment caution"`, treat it as a normal error (report stderr to the user, do not re-run). See **Unsupported Period Handling** and **Unsupported Exchange/Timeframe Handling** below for the candle-data error cases.

When the backtest proceeds with investment caution confirmed (re-run with `y` piped via stdin), always include the following notice in the report:

> ⚠️ {market} is currently under investment caution.

#### Unsupported Period Handling

Detect by checking:
- exit code is 1
- stderr contains `"Backtesting is not available for the selected period"`

The requested date range has no candle data. If the user explicitly set the dates, quote the exact tool error and ask for a new period:

```text
Backtesting is not available for the selected period.
Please provide a different period. You can check available data at: https://www.upbit.com/historical_data/download?prefix=candle
```

**Never re-run with a different date without explicit confirmation, and do not probe for the earliest supported date.**

#### Unsupported Exchange/Timeframe Handling

Detect by checking:
- exit code is 1
- stderr contains `"Historical candle data"`

The strategy's exchange or timeframe is permanently unsupported (no date range works). Route to `create-strategy` to switch to a backtestable timeframe (`1M` or shorter) or the `kr` exchange.

#### Run Output

Items printed to stdout (quote these values exactly):

```
Period      YYYY-MM-DD ~ YYYY-MM-DD (trading bars: N, warmup bars: N)
Benchmark   +N.NN%
Total Return +N.NN%
CAGR        +N.NN%
MDD         N.NN%
Sharpe      N.NN  (Rf=0, portfolio / full equity curve)
Sharpe      N.NN  (Rf=0, trades / position holding periods only)
* Sharpe ratio is unreliable for 1m/1s: annualization amplifies microstructure noise.  ← 1m/1s TF일 때만 출력
Trades      N  Win Rate N% (before fees)
Profit Factor  N.NN (before fees)
SL N / TP N / sell N / final_bar N
Total Fees  N
```

When the actual data range differs from the requested period, this notice is always printed (outside verbose mode, before the disclaimer). See **## Data Availability Notice** for the EN/KR text.

When there are `0 executed trades`, stdout uses the tool-provided undefined markers directly:

```text
Trades      0  Win Rate N/A (0 executed trades) (before fees)
Profit Factor  N/A (0 executed trades) (before fees)
```

### STEP 4. Interpret Results + Bidirectional Handoff
Report format (details in [references/result-interpretation.md](references/result-interpretation.md)):

**a) Summary** - quote stdout exactly + CSV path + (Mode A) restate hypothesis/falsification criterion.

**b) Trade highlights** - notable points from first entry / highest-profit trade / largest-loss trade / exit_reason distribution (`SL`/`TP`/`sell`/`final_bar`). Extract from CSV `# section: trades`.

**c) Comment (1-2 lines, factual statements)** - only relationships between values. Examples are in [references/result-interpretation.md](references/result-interpretation.md).

> "MDD is larger than total return. Drawdown accumulated across positions even though each position's stop-loss was capped."
> "Among N trades, SL N vs TP N - stop-loss fired more often than take-profit."

**d) Hypothesis falsification judgment** - Mode A only. Compare each `falsification_criterion` item directly with result values and state **falsified / retained / inconclusive**.

> Falsification criterion: "win rate < 40% or MDD > 25%"
> Result: win rate N% / MDD N.NN%
> -> [falsified / retained] : {which item met or did not meet which criterion}

**e) Next revision candidates + handoff payload** - use this payload format when handing back to create-strategy:

```
slug: {original slug}
result_summary:
  total_return_pct: {stdout exactly}
  benchmark_pct: {stdout exactly}
  win_rate_pct: {stdout exactly}
  mdd_pct: {stdout exactly}
  trades: {N}
  exit_reasons: SL N / TP N / sell N / final_bar N
benchmark_comparison: {+/-N.NN%p vs benchmark - see references/benchmark.md for detailed interpretation}
hypothesis_status: {falsified / retained / inconclusive}
suggested_next_directions:  # 2-3 neutral revision candidates, based on factual statements
  - "Revision candidate: review stop-loss width because MDD is larger than the per-trade stop-loss"
  - "Revision candidate: review entry strictness because win rate and trade count may indicate the entry rule is loose or strict"
next_slug_proposal: {slug}-v2
```

When the user passes this payload to create-strategy as-is, a new version (`-v2`) is created.

**f) Disclaimer** - At the end of the report, output the Tool Limitations Notice and Backtesting Disclaimer from `## Required Notices`, in that order.

#### 0-Trade Case Handoff

If there are 0 executed trades, stdout already marks undefined metrics as `N/A (0 executed trades)`. Fill the payload with these rules. Do not estimate or recalculate values; state sample insufficiency as a fact:

```
result_summary:
  total_return_pct: 0
  benchmark_pct: {stdout exactly - buy-and-hold is independent of 0 trades}
  win_rate_pct: N/A (0 executed trades)
  mdd_pct: 0
  trades: 0
  exit_reasons: SL 0 / TP 0 / sell 0 / final_bar 0
benchmark_comparison: "0 executed trades - comparison is not meaningful"
hypothesis_status: inconclusive  # sample is insufficient for both falsified and retained
suggested_next_directions:
  - "Revision candidate: review entry strictness because 0 executed trades were observed"
  - "Revision candidate: review whether all entry conditions are required simultaneously"
  - "Revision candidate: extend the period and recheck whether entry signals occur"
next_slug_proposal: {slug}-v2
```

Key point: `hypothesis_status` is **inconclusive** (neither falsified nor retained), and `suggested_next_directions` should stay as neutral revision candidates or additional checks derived from the factual result. Result interpretation details are in [references/result-interpretation.md](references/result-interpretation.md#b-trade-highlights).

---

## Live Trading Guardrail

Same policy as create-strategy. Block command, question, bypass, indirect, and confusion patterns equally:

**Command**
- "Start automated trading with this strategy"
- "Place a real-time order" / "Execute a buy order" / "Turn on live trading"

**Question**
- "Can I run this strategy live?"
- "Is real-time trading possible?"

**Bypass**
- "What do I need to automate this strategy as-is?"
- "Can I put this JSON directly into a live trading bot?"

**Indirect**
- "The backtest result looks good; can I move it straight to live trading?"
- "Let's validate this hypothesis in live trading as-is"

**Confusion**
- "upbit-strategy-toolkit can do live trading too, right?"
- "Does this tool also provide an order API?"

**Response template** (apply to all patterns above): If the user's message is in Korean, use the Korean version; otherwise use the English version.

Korean:
```text
> 이 도구는 백테스트(과거 데이터 시뮬레이션) 전용입니다.
> 실시간 거래, 자동 주문, 실전 매매는 지원하지 않습니다.
> 실전 매매가 필요하다면 [upbit-agent-skills](https://github.com/upbit-official/upbit-agent-skills)를 이용해주세요.
> 
> 이 스킬은 전략 JSON 검증 및 결과 해석만 지원합니다.
```

English:
```text
> This tool is for backtesting (historical data simulation) only.
> Real-time trading, automated orders, and live trading are not supported.
> Use the separate [upbit-agent-skills](https://github.com/upbit-official/upbit-agent-skills) tool for live trading.
> 
> This skill only supports strategy JSON validation and interpretation.
```

---

## Data Availability Notice

Include only when the actual data range differs from the requested period. Use the Korean version if the user's message is in Korean; otherwise use the English version.

English:
```text
> Some data was unavailable for the requested period, so the backtest was run over the available range ({min_date} - {max_date}).
```

Korean:
```text
> 일부 기간의 데이터가 없어, 수집된 구간({min_date} ~ {max_date}) 기준으로 백테스트를 진행했습니다.
```

---

## Required Notices

Legal notices. Output the text below verbatim — do not summarize, translate, or omit.

### Backtesting Disclaimer

Always include at the end of every backtest report. Use the Korean version if the user's message is in Korean; otherwise use the English version.

Korean:
```text
> 백테스트 결과는 과거 데이터를 기초로 한 것이며, 장래 또는 실제 거래에서 동일하거나 유사한 투자 성과로 이어질 것임을 보장하지 않습니다.
```

English:
```text
> Backtesting results are based on historical data and do not guarantee that the same or similar investment performance will be achieved in the future or in actual trading.
```

### Tool Limitations Notice

Include at the end of every backtest report, on the line immediately above the Backtesting Disclaimer. Use the Korean version if the user's message is in Korean; otherwise use the English version.

Korean:
```text
> 슬리피지, 호가창 유동성, 부분 체결은 반영되지 않으며 다음 캔들 시가에 전량 체결로 가정합니다.
```

English:
```text
> Slippage, order book liquidity, and partial fills are not reflected. The tool assumes full execution at the next candle open.
```

### Investment Recommendation Notice

Include at the end of the response when the user requests an investment recommendation. Use the Korean version if the user's message is in Korean; otherwise use the English version.

Korean:
```text
> Upbit Strategy Toolkit은 어떠한 경우에도 특정 종목, 거래 시점, 투자 방식, 투자 전략 등을 추천·권유하지 않습니다. 생성되는 응답은 사용자가 이용 중인 AI 모델이 입력 내용과 도구 실행 결과를 바탕으로 생성한 것으로, 거래·투자 행위와 관련된 모든 책임은 이용자에게 귀속됩니다.
```

English:
```text
> Upbit Strategy Toolkit does not, under any circumstances, recommend, advise on, or solicit the purchase, sale, timing, method, or strategy of any specific asset or investment. Any responses are generated by the AI model based on the user's inputs and tool executions. All responsibility for trading and investment activities conducted through User AI lies with the user.
```

---

## Execution Rule Summary

- Do not recalculate or estimate stdout values - quote them exactly
- Do not judge good/bad - state facts only
- Benchmark comparison uses the tool stdout `Benchmark` value - no separate calculation. See [references/benchmark.md](references/benchmark.md) for detailed interpretation
- The backtest tool automatically saves the CSV to `{data_root}/reports/{slug}-{ts}.csv` - the skill does not save separately
- Apply timeframe-specific default periods - [references/period-defaults.md](references/period-defaults.md). Do not ask the user every time
- State hypothesis falsification judgment only in Mode A (handoff) - Mode B stops at factual statements
- Route strategy revision/new version requests to create-strategy - use the handoff payload format
- Refuse live trading and point to [upbit-agent-skills](https://github.com/upbit-official/upbit-agent-skills)
- Always deliver the backtesting disclaimer to the user in every backtest report
- When backtest proceeds with investment caution confirmed, always include the ⚠️ caution notice in the report
- Never modify user-specified dates on period errors — report the exact error from stderr and ask the user to provide a new period, or explain the permanent limit if the timeframe/exchange is not backtestable.
- Before running, check the strategy file's `timeframe` — if it differs from the user's request, present options (create new strategy file via create-strategy, use existing timeframe, cancel) and do not run with the mismatched timeframe
