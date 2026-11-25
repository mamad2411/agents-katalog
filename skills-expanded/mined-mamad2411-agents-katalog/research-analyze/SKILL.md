---
name: research-analyze
description: "研究 Phase 4：回測結果分析、A/B 比較、偏差快篩。Use when 'analyze results', '分析結果', 'compare backtest'."
allowed-tools: Read, Glob, Grep, Bash
---

# /research-analyze — 結果分析

讀 `docs/research_state.json` 取得實驗資訊。

## Step 1: 收集結果

從實驗腳本輸出收集：
- Event Study CAR 數據
- 統計檢定結果
- 分組比較表

## Step 2: A/B 比較表

```markdown
## A/B Comparison: [Topic] (RB-[XXX])

| Metric | Baseline (A) | Treatment (B) | Delta | p-value | Pass? |
|--------|-------------|---------------|-------|---------|-------|
| CAR_5d | X.XX% | Y.YY% | +Z.ZZ% | 0.XXX | [Y/N] |
| CAR_20d | X.XX% | Y.YY% | +Z.ZZ% | 0.XXX | [Y/N] |
| Hit Rate | X% | Y% | +Z% | — | [Y/N] |
| Sample Size | N | N | — | — | — |
| Alpha vs SPY | X.XX% | Y.YY% | +Z.ZZ% | 0.XXX | [Y/N] |
```

標注 Primary Metric 是否達標。

## Step 3: 偏差快篩

**必做 5 項檢查**：

| # | 檢查項 | 結果 |
|---|--------|------|
| 1 | Alpha ≤ 5% CAR？ | [PASS/FAIL] |
| 2 | Hit Rate ≤ 75%？ | [PASS/FAIL] |
| 3 | 樣本量 ≥ 30？ | [PASS/FAIL] |
| 4 | 使用 filing_date 非 transaction_date？ | [PASS/FAIL] |
| 5 | Benchmark = SPY 同期？ | [PASS/FAIL] |

**如果 Alpha > 5% CAR，立即停止分析**，報告：
> Alpha = [X.XX%] 超過 5% 門檻。疑似 look-ahead bias。建議人工審查事件日定義和數據來源。

## Step 4: 統計顯著性

- t-test / Mann-Whitney U：p-value < 0.05？
- Bootstrap 95% CI：是否排除 0？
- Effect size (Cohen's d)：small(0.2)/medium(0.5)/large(0.8)
- 與已知 RB 研究對比（RB-001 Buy CAR_5d = +0.77%）

## Step 5: 輸出分析報告

```markdown
## Analysis Report: [Topic] (RB-[XXX])

### A/B Comparison
[Step 2 的表格]

### Bias Screen
[Step 3 的結果]
- All checks: [PASS/FAIL]

### Statistical Significance
- p-value: [X.XXX]
- 95% CI: [lower, upper]
- Effect size: [X.XX] ([small/medium/large])

### Primary Metric Assessment
- Target: [metric] ≥ [threshold]
- Result: [ACHIEVED / NOT ACHIEVED]

### Recommendation
[初步建議: ADOPT / ITERATE / REJECT / INCONCLUSIVE]
- 理由: [2-3 句]

### Next: `/research-log`
```

向用戶報告分析結果，等待確認。
