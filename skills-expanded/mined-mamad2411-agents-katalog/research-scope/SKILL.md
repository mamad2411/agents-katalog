---
name: research-scope
description: "研究 Phase 1：問題定義、分類、背景調查、偏差預檢。Use when starting research, defining hypothesis, 'research scope', '定義問題'."
argument-hint: <hypothesis or research question>
allowed-tools: Read, Glob, Grep, WebSearch, WebFetch
---

# /research-scope — 問題定義 + 背景調查

**研究主題**: $ARGUMENTS

## Step 1: 分類研究類型

判斷屬於哪種類型：

| 類型 | 特徵 | 範例 |
|------|------|------|
| **ALPHA** | 超額報酬驗證 | "委員會主席交易是否有更高 alpha" |
| **SIGNAL** | 信號品質改進 | "PACS 加入社群情緒權重" |
| **DATA** | 新數據源整合 | "USASpending 合約交叉比對" |
| **TIMING** | 時機參數最佳化 | "Filing lag < 10d 的 alpha 差異" |

## Step 2: 建立研究卡片

```
======================================================
  RESEARCH CARD — RB-[XXX]
======================================================
  Type:       [ALPHA/SIGNAL/DATA/TIMING]
  Hypothesis: [一句話假說]
  Metric:     [主要衡量指標: CAR_5d/20d, hit rate, etc.]
  Baseline:   [對照基準: 全樣本 or SPY]
  Risk:       [可能的 look-ahead bias 風險]
  Effort:     [預估複雜度 1-5]
======================================================
```

## Step 3: 偏差預檢

在動手之前檢查假說本身是否有 look-ahead bias 風險：
- [ ] 是否會引入未來資訊？（filing_date 後才知道的資訊）
- [ ] 是否需要 point-in-time 資料？（委員會名單何時公布）
- [ ] 是否涉及存活偏差？（只看仍在職的議員）
- [ ] 是否隱含多重測試問題？（測太多分組）
- [ ] Hit rate > 75% 是否暗示過擬合？

如果有風險，標注並設計對應防護。

## Step 4: 專案內部掃描

檢查是否有人做過相似研究：
- 讀 `docs/research_log.md` — 過去研究記錄
- 讀 `docs/reports/Sprint_Roadmap_2026_Q2.md` — 路線圖
- 讀 MEMORY.md — Alpha Research Key Findings (RB-001 through RB-009)
- Grep 相關關鍵字在 `docs/` 和 `src/`

## Step 5: 文獻檢索

使用 WebSearch 搜尋：
- 學術論文（SSRN, arXiv — "congressional trading alpha"）
- 量化社群（Quiver Quantitative, r/algotrading）
- 競品分析（Capitol Trades, Unusual Whales 做法）

## Step 6: 輸出 Scope Report

```markdown
## Scope Report: [Topic] (RB-[XXX])

### Research Card
[Step 2 的卡片]

### Bias Pre-check
[Step 3 的結果]

### Prior Art
- 專案內: [列出相關 RB 研究]
- 文獻: [列出相關論文]

### Conclusion
[值得繼續 / 已有結論 / 需修改方向]

### Next: `/research-design`
```

向用戶報告結果，等待確認後再進入下一步。
