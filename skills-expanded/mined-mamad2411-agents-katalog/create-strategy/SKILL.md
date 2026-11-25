---
name: create-strategy
description: Turn a natural-language strategy idea into a testable market hypothesis and strategy JSON, then create a saved strategy file that can be handed to backtest. Use for creating a new strategy or revising a hypothesis after reviewing backtest results. Strategy creation, hypothesis design, strategy JSON, strategy create, strategy revision, -v2 generation. Use when the user describes a trading idea or hypothesis in natural language, or asks to revise a strategy or create a new version (-v2) after reviewing backtest results.
compatibility: Requires uv, write access to {data_root}/strategies/, network access for Upbit market validation
metadata:
  version: "0.1"
---

# create-strategy

This skill turns a natural-language strategy idea into a saved strategy JSON file ready to hand off to the backtest skill.

Idea → hypothesis → design negotiation → approval → ConditionGroup JSON → validation → save `{data_root}/strategies/{slug}.json` → hand off to backtest.

This skill is the **strategy-design stage in the hypothesis-to-falsification workflow**: it turns a natural-language idea into one or more concrete JSON strategy definitions. Backtesting is a tool for falsifying hypotheses, and this skill turns the hypothesis into something executable.

Domain catalogs and detailed rules are split into references/:
- 15 JSON indicator types / 16 target indicator catalog: [references/indicators.md](references/indicators.md)
- JSON schema, validation constraints, and nested patterns: [references/schema.md](references/schema.md)
- 9 validation-error self-correction patterns: [references/error-recovery.md](references/error-recovery.md)
- Empty strategy template: [assets/strategy-template.json](assets/strategy-template.json)
- Public examples: [strategies/examples/](../../strategies/examples/)

Load `skills/references/glossary.md` when explaining metric names, indicator names, or strategy terms in Korean.

---

## Data Root and Execution Mode

At the start of work, identify the mode and resolve `{data_root}` as an absolute path.

| Mode | Detection | `{data_root}` |
|---|---|---|
| clone mode | Running in the upbit-strategy-toolkit repo workspace/cwd | The repo root (absolute). The wrapper pins it to the repo root regardless of your cwd, so cache/strategies/reports always land under the repo even when invoked from a subdirectory. |
| agent skills mode | Only the skill was installed with `npx skills`, and the repo is not in the current workspace | `$HOME/.upbit-strategy-toolkit` |

After user approval, save the strategy JSON to `{data_root}/strategies/{slug}.json`. If the same slug already exists, use a new filename such as `-v2`/`-v3`; do not overwrite.

Use this skill's wrapper for tool calls instead of running `upbit-strategy-toolkit` directly.

```bash
bash scripts/upbit-strategy-toolkit.sh ...
```

## Routing Contract

- Role: save natural-language strategy ideas as testable strategy JSON
- Prerequisite/recovery: route to `setup` when uv is missing, the wrapper fails, or the CLI fails
- Next step: `backtest`
- Handoff: `slug`, `hypothesis`, `falsification_criterion`, `notes`
- Out of scope: this skill does not run backtests or interpret results

---

## Triggers

- "Create a Bitcoin trading strategy using a golden cross"
- "Build a strategy that buys RSI oversold and sells RSI overbought"
- "After seeing the backtest result, tighten the stop-loss" (existing strategy -v2)
- "Let's draft a strategy from this hypothesis: volume spike + trend reversal = entry"

## Do Not

- **Do not connect to automated/live trading** - see [Live Trading Guardrail](#live-trading-guardrail) when requested.
- **Do not recommend assets, entry timing, trade prices, target returns, or holding periods** - this skill structures user-provided ideas into testable rules; it does not make investment recommendations.
- **Do not save JSON before user approval** - do not write files before the STEP 2 gate passes.
- **Do not push the user to edit JSON directly** - the skill synthesizes JSON; the user negotiates only in natural language.
- **Do not guess indicators outside the catalog** - reject anything outside the 15 JSON types / 16 target indicators ([references/indicators.md](references/indicators.md)).
- **Do not hand validation failures to the user** - handle validation errors through the self-correction loop ([references/error-recovery.md](references/error-recovery.md)).

---

## Investment Recommendation Guardrail

If the user asks what to buy, sell, hold, choose, when to trade, what target return to pursue, what price to trade at, or how long to hold, do not answer the recommendation itself.

Put the following notice at the end of the response exactly as written. If the user's message is in Korean, use the Korean version; otherwise use the English version.

Korean:
```text
Upbit Strategy Toolkit은 어떠한 경우에도 특정 종목, 거래 시점, 투자 방식, 투자 전략 등을 추천·권유하지 않습니다. 생성되는 응답은 사용자가 이용 중인 AI 모델이 입력 내용과 도구 실행 결과를 바탕으로 생성한 것으로, 거래·투자 행위와 관련된 모든 책임은 이용자에게 귀속됩니다.
```

English:
```text
Upbit Strategy Toolkit does not, under any circumstances, recommend, advise on, or solicit the purchase, sale, timing, method, or strategy of any specific asset or investment. Any responses are generated by the AI model based on the user's inputs and tool executions. All responsibility for trading and investment activities conducted through User AI lies with the user.
```

Then redirect the user to a supported input such as:
- a market hypothesis they want to test,
- concrete entry/exit/stop-loss/take-profit rules they want structured,
- or an existing strategy they want revised for another backtest.

This skill may structure user-specified rules into `buy` / `sell` / `stop-loss` / `take-profit` fields, but it must not decide those actions for the user.

---

## Workflow

### STEP 1. Listen for the Hypothesis + Draft a Four-Part Strategy Structure

Reduce the natural-language idea to one **testable market hypothesis** sentence, then propose all four parts (buy/sell/stop-loss/take-profit) without blanks.

**Hypothesis statement format**: "When condition X occurs, price movement in direction Y happens more often"

Good examples:
- "When the 5-day moving average crosses above the 20-day moving average, a short-term uptrend tends to continue afterward"
- "When RSI < 30, short-term rebounds occur more often (mean reversion)"

**Presentation format**:

```
create-strategy

Strategy: {strategy name}
Hypothesis: {one-sentence market hypothesis}

Structured draft:
- Buy: {condition in natural language}
- Sell: {condition in natural language}
- Stop-loss: -{N}% from entry price
- Take-profit: +{N}% from entry price
- Target: {market} / {exchange} / {timeframe}

How this hypothesis is falsified:
- {example: "If it frequently reaches a wide stop-loss, the trend-following hypothesis is broken"}

Proceed with this? Tell me which items to revise.
```

**Defaults** (do not ask again; user-specified values take priority): `market=KRW-BTC`, `exchange=kr`, `timeframe=1d`, `stop_loss=5`, `take_profit=15`.

**Market substitution rule**: If the requested market is unsupported, **ask the user before substituting** (e.g., "SGD-DOGE is not supported. Use KRW-DOGE instead?"). Proceed only after explicit confirmation, then update `Strategy: {strategy name}` to reflect the confirmed market.

Only `kr` exchange is currently supported. If the user requests a different exchange, explain it is not supported and default to `kr`.

### STEP 2. Explicit Approval Gate

Do not proceed to STEP 3 before **explicit approval**, such as "proceed", "OK", "yes", or "do it that way". On revision requests, return to STEP 1 and present the proposal again.

### STEP 3. Convert to JSON + Strategy Validation Loop

Synthesize the approved four parts into ConditionGroup JSON. Pre-check these core constraints during synthesis:

1. `indicators[*].type` must be one of the 15 catalog JSON types - [references/indicators.md](references/indicators.md)
2. `ref` values must not be duplicated, and each `IndicatorOperand.ref` in conditions must use `indicator_ref.output_key` and be valid through the output key
3. Literals are forbidden on both sides of `cross_above`/`cross_below`
4. Express `ichimoku_cloud` cloud conditions by comparing `close` with `ichi.Leading1` and `ichi.Leading2` separately. Use `offset: 26` on the indicator operand when the cloud is displaced 26 bars into the future in the chart (e.g. `{"type": "indicator", "ref": "ichi.Leading1", "offset": 26}`)

Full validation constraints and Operand/op tables are in [references/schema.md](references/schema.md). Copy and edit the empty strategy skeleton in [assets/strategy-template.json](assets/strategy-template.json).

Before validation, write the approved JSON draft to `{data_root}/strategies/{slug}.json`.
If validation fails, patch the same file up to 3 times. Do not report save completion to the user before validation passes.

Validation:

```bash
STRATEGY_PATH="{data_root}/strategies/{slug}.json"
bash scripts/upbit-strategy-toolkit.sh strategy validate "$STRATEGY_PATH"
```

On validation success, `OK` is printed. On failure, the validation error message is printed to stderr -> self-correction loop.

#### Self-Correction Loop (3 Attempts)

Only the most common cases are inline - all 9 patterns are in [references/error-recovery.md](references/error-recovery.md).

| Error message pattern | Patch |
|---|---|
| `... unregistered indicator` | Replace with the closest catalog indicator (for example, `bollinger` -> `bollinger_bands`) |
| `references undefined ref/output ...` | Add it to the indicators array or fix the `indicator_ref.output_key` typo |
| `cross_above/cross_below ... Literal cannot be used` | Use time series on both sides (for example, `rsi cross_above 30` is invalid -> use `gt 30`) |

If it does not pass within 3 attempts, report the diagnosis to the user and renegotiate the hypothesis.

### STEP 4. Confirm Save + Handoff

When validation passes, confirm the saved `{data_root}/strategies/{slug}.json`.

**Slug rule**: `name` -> lowercase hyphenated ASCII. Slug is derived from the **final approved name** (post-substitution), not the original request. If the same slug exists, automatically increment to `-v2`/`-v3` (no overwrites). Backtest-based revisions are also saved as new versions.

**Completion report + handoff**:

```
Saved {data_root}/strategies/{slug}.json

Hypothesis: {one-line hypothesis summary}
Buy: {condition summary}
Sell: {condition summary}
Stop-loss -{stop_loss}% / take-profit +{take_profit}%
Target: {market} / {timeframe}

Next step: test this hypothesis with the backtest skill.
- slug: {slug}
- Falsification criterion: {falsification condition defined in STEP 1}
- The backtest skill automatically selects the period for the timeframe.
```

---

## Handoff Payload

When STEP 4 completes, explicitly pass the following to the backtest skill:

```
slug: {slug}
hypothesis: {one-sentence hypothesis statement from STEP 1}
falsification_criterion: {falsification criterion - for example, "win rate < 40% or max drawdown > 25%"}
notes: {free-form notes - optional}
```

> **Do not send a period.** `timeframe` is already in the JSON, and the backtest skill chooses the matching default period. This keeps period selection in one place (backtest) so two skills cannot compute conflicting periods.

If the backtest result falsifies the hypothesis, the user returns to this skill and creates a new version (`-v2`). Repeat bidirectionally.

---

## Live Trading Guardrail

When any of the following utterance patterns are detected, immediately explain and stop work. Block command, question, bypass, indirect, and confusion patterns equally:

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
이 도구는 백테스트(과거 데이터 시뮬레이션) 전용입니다.
실시간 거래, 자동 주문, 실전 매매는 지원하지 않습니다.
실전 매매가 필요하다면 [upbit-agent-skills](https://github.com/upbit-official/upbit-agent-skills)를 이용해주세요.

이 스킬은 전략 JSON 생성 및 백테스트 검증만 지원합니다.
```

English:
```text
This tool is for backtesting (historical data simulation) only.
Real-time trading, automated orders, and live trading are not supported.
Use the separate [upbit-agent-skills](https://github.com/upbit-official/upbit-agent-skills) tool for live trading.

This skill only supports strategy JSON creation -> backtest validation.
```

---

## Execution Rule Summary

- Do not save JSON without approval
- Strategy revisions also go through this skill -> new version (`-v2`, etc.)
- Indicator types must come only from the 15 JSON type catalog ([references/indicators.md](references/indicators.md))
- Validation failure self-correction is limited to 3 attempts ([references/error-recovery.md](references/error-recovery.md)); if it still fails, ask the user to renegotiate the hypothesis
- Refuse live trading requests and point to [upbit-agent-skills](https://github.com/upbit-official/upbit-agent-skills)
