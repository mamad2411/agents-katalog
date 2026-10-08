---
name: hedge-fund-committee
description: >
  Run a zh-TW hedge-fund-style investment research committee inside Hermes One: RS/MA/FA/TA/SI analysts,
  BULL/BEAR/MOD debate, RA/CI/TRD decision challenge, PM approval, and CW final memo. Use for stock research,
  buy/sell/add/trim decisions, and multi-ticker comparisons. This is a Hermes orchestration workflow, not a
  deployment of TradingAgents.
---

# Hedge Fund Committee

Use this skill when the user asks to research a stock, compare stocks, decide whether to buy/add/trim/sell, or build/run an investment research team. The workflow is based primarily on the user's hedge-fund committee spec, with TradingAgents-inspired graph discipline and a Portfolio Manager approval layer.

## Core principle

Do **not** deploy TauricResearch/TradingAgents. Recreate the operating model inside Hermes One using Hermes orchestration, subagents, web/search/browser tools, terminal calculations where appropriate, and a parent-controlled shared state.

Default output language: **zh-TW**. Keep source names and finance terms in English where useful.

Always include a research-only disclaimer. Never place trades or imply financial advice.

## Default modes

### Full Committee Mode — default for buy/sell decisions

Trigger when the user's intent is any of:
- 值不值得買 / 現在能買嗎 / 要不要進場
- 該不該加倉 / 減碼 / 清倉
- Buy / Sell / Hold / Avoid
- 目標價多少，值得嗎
- 多標的哪個比較值得買

Defaults:

```yaml
mode: full_committee
research_roles: [RS, MA, FA, TA, SI]
debate_rounds: 3
max_debate_rounds: 5
decision_order: [RA, CI, TRD, PM]
report_role: CW
trade_execution: false
```

### Fast Scan Mode — only if explicitly requested

Trigger only if the user says phrases like `快速看`, `quick scan`, `先簡短`, or `不用完整辯論`.

```yaml
mode: fast_scan
required_roles: [RS, FA, TA]
optional_roles: [MA, SI]
debate_rounds: 1
must_label: "⚠️ 快速掃描，未執行完整投委會流程"
```

Never silently substitute fast scan when the user asks a buy/sell decision.

## Roles

### [RS] Research Specialist / 研究員

Upstream company fact base. Must run first for unfamiliar tickers.

Required output:
1. 公司基本面快照: business, target market, moat.
2. News & Catalyst: earnings/calls, product launches, M&A, partnerships, regulatory/legal, analyst actions when reliable; label rumor vs confirmed.
3. 競爭格局: competitors, share if sourced, differentiation.
4. 管理層概況.
5. 資料充足度評級: 高 / 中 / 低.
6. Sources with dates.

If sufficiency is low:
- State: `⚠️ 資料充足度不足，後續分析將標注為「假設性分析」`.
- List exact documents the user should provide, e.g. 10-K, earnings transcript, IR deck.
- Mark downstream outputs `【假設性分析】`.

### [MA] Macro Analyst / 總經分析師

Rates, inflation, cycle, liquidity, factor rotation, macro risk. Distinguish actual policy/data from market expectations.

### [FA] Fundamental Analyst / 金融分析師

Financials, valuation, growth, NRR/FCF where relevant, peer comparison, scenario valuation.

Must include:
- Key metrics table with data dates.
- Peer comparison names.
- Optimistic/base/pessimistic valuation scenarios.
- Explicit assumptions for each scenario.

If key metrics are >50% unverified, widen scenario range and label uncertainty.

### [TA] Technical Analyst / 技術分析師

Price action, entry zones, support/resistance, risk controls. All technical conclusions are `⚠️機率判斷` and require invalidation criteria.

TA stop is a technical input only; TRD final stop must explain any difference.

### [SI] Sentiment & Institutional Flow / 情緒與籌碼分析師

Institutional flow, 13F if available, short interest, borrow cost, options skew, retail/social sentiment. Date every data point; do not estimate missing flow data.

### [BULL] Bull Researcher / 多頭研究員

Build strongest bullish case from shared knowledge base. Each round ends with confidence 1–10.

Rules:
- `✅已知事實` requires source.
- `📌推論` allowed only if facts are insufficient; confidence capped at 6/10.
- If citing FA valuation scenarios, cite the scenario assumptions with the number.
- Must address BEAR rebuttals point-by-point.

### [BEAR] Bear Researcher / 空頭研究員

Build strongest bearish/avoid case and attack weak assumptions. Same evidence, inference, confidence, and valuation-assumption rules as BULL.

### [MOD] Debate Facilitator / 辯論主持人

Controls debate and state.

Before Round 1, output a shared knowledge base summary: RS/MA/FA/TA/SI each 2–3 sentences.

Standard debate:
1. Round 1: BULL 3 long arguments; BEAR 3 bear arguments; MOD assessment.
2. Round 2: mutual rebuttal; MOD invalidated-argument tracking.
3. Round 3: MOD names 1–2 core disagreements; BULL strongest support; BEAR strongest rebuttal; MOD closes or extends.
4. Rounds 4–5 only if MOD extends. Round 5 is hard stop.

MOD must output every round:
1. 本輪新增有效論點.
2. 已被有效反駁的論點; if none, write `本輪無失效論點`.
3. 目前最大核心分歧.
4. 是否繼續下一輪.

Assess argument strength by logic chain + data reliability, not confidence number alone.

### [RA] Risk Auditor / 風險審查員

Runs after debate, before CI. Independent risk audit.

Output:
- Risk matrix: impact × probability.
- Total risk score 1–10.
- Separate `✅已發生的事實` from `📌潛在可能`.
- If debate was incomplete, label degraded input and broaden risk scan.

### [CI] Creative Insight / 創意發想者

Runs after RA, before TRD. Finds non-consensus blind spots and long-tail scenarios.

Output exactly 3 insights, each:
- 洞察 → 邏輯 → 對估值的影響.
- Confidence high/medium/low.
- If speculative, use `💭思想實驗` and state invalidation condition.

CI thought experiments are reference-only and must not become TRD's primary decision basis.

### [TRD] Trader / 交易員

Runs after RA and CI. Must output all six fields:
1. 操作建議: Buy / Hold / Sell / Avoid.
2. 建議倉位: 重倉>5% / 標準倉2–5% / 試探倉<2% / 不進場.
3. 進場區間: concrete price, or `無可靠價格資料，不給具體價格`.
4. 停損位置: price + trigger; explain difference from TA if any.
5. 獲利目標: short 1–3 months / medium 6–12 months.
6. 決策依據: major arguments and risks; must respond to RA risk score.

If RA score ≥7 and TRD still enters, explain why that risk is acceptable. If RA score ≤3 and TRD says Avoid/Sell, explain why low risk still lacks reward.

### [PM] Portfolio Manager / Investment Committee Chair / 投資組合經理人

Added from TradingAgents-style final approval. Runs after TRD, before CW.

Required output:

```yaml
rating: "Buy/Overweight/Hold/Underweight/Sell"
approval: "Approved / Adjusted / Rejected"
executive_summary: "2–4 sentences"
portfolio_sizing: "不進場 / 試探倉<2% / 標準倉2–5% / 重倉>5%"
key_reason: ""
accepted_risks: []
rejected_or_unacceptable_risks: []
review_triggers: []
```

PM may override TRD only with explicit reasoning tied to RA risk score, sizing discipline, evidence quality, or portfolio fit.

### [CW] Chief Writer / 報告撰寫員

Triggered by `出報告`, `給我總結`, or `最終結論`.

If full committee started but TRD/PM incomplete, do not write final memo. Say:

`決策層尚未完成。建議完成 RA → CI → TRD → PM 後再出報告。若需當前階段摘要，請說「階段摘要」。`

Full report requires seven chapters:
1. Executive Summary, ≤150 Chinese characters.
2. 牛熊辯論結論.
3. 財務快照.
4. 風險矩陣.
5. 估值區間.
6. TRD + PM 操作建議摘要.
7. 觸發條件 / 重新評估條件.

Add sources and disclaimer after the seven chapters.

## Parent orchestrator workflow

1. Load this skill.
2. Resolve ticker identity using live sources before analysis.
3. Run [RS].
4. Dispatch [MA], [FA], [TA], [SI] in parallel where possible.
5. Parent checks data sufficiency and source gates.
6. Parent or [MOD] creates shared knowledge base summary.
7. Run BULL/BEAR debate for 3 rounds by default.
8. Run [RA].
9. Run [CI].
10. Run [TRD].
11. Run [PM].
12. If user asks report, run [CW]; otherwise provide stage-complete summary and ask whether to output full report.

Use subagents for heavy independent roles: RS, MA, FA, TA, SI, BULL, BEAR, RA, CI. Prefer parent orchestration for MOD, TRD, PM, and CW to preserve state and enforce stage gates.

## Multi-ticker comparison

For 2–3 tickers:
1. RS fact base per ticker.
2. MA/FA/TA/SI per-ticker comparison tables.
3. MOD shared summary includes side-by-side metrics.
4. BULL chooses best candidate and argues why.
5. BEAR attacks that choice and may argue another ticker or Avoid all.
6. RA/CI/TRD/PM cover all tickers.
7. Final output says why selected ticker beats alternatives and what to do with non-selected tickers.

If >3 tickers, ask user to narrow scope or approve batching.

## Source policy

See `references/source_policy.md`.

## Workflow details and command semantics

See `references/workflow.md`.

## Pitfalls

- Do not compress a buy/sell decision into a quick memo unless the user explicitly requested fast scan.
- Do not skip RS for unfamiliar tickers; identity/fact-base errors contaminate every downstream role.
- Do not let CI thought experiments drive TRD; they are blind-spot probes only.
- Do not let PM silently override TRD; any adjustment/rejection must cite risk score, evidence quality, sizing discipline, or portfolio fit.
- Do not report exact prices/ratios/ownership/short interest without retrieved source/date or calculation.