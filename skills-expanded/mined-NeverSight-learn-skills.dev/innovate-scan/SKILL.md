---
name: innovate-scan
description: "創新 Phase 1：方向偵測 + 前沿掃描。搜論文、GitHub、社群找最新方法。Use when 'frontier scan', '搜論文', 'explore new tech', '前沿掃描'."
argument-hint: [topic or direction]
allowed-tools: Read, Glob, Grep, WebSearch, WebFetch
---

# /innovate-scan — 方向偵測 + 前沿掃描

**探索方向**: $ARGUMENTS

## Step 1: 分類象限

判斷屬於哪個象限：

| 象限 | 策略 | PAM 範例 |
|------|------|---------|
| OPTIMIZE | 搜最佳實踐，benchmark 比較 | "PACS 權重用 ML 動態調整" |
| TRANSFER | 找其他領域的解法 | "ESG 情緒分析用在議員交易" |
| DISCOVER | 評估新數據源的 alpha | "委員會聽證文字稿做信號" |
| FRONTIER | 探索最新研究 | "GNN 建模議員社交網路" |

## Step 2: 學術論文搜尋

**搜尋策略**（按優先級）：
1. `site:ssrn.com "congressional trading" OR "political alpha" 2025 2026`
2. `site:arxiv.org "<topic>" finance NLP 2025 2026`
3. `"<topic>" insider trading alpha empirical evidence`

**篩選標準**：
- 2024-2026 年優先
- 有實證數據（不只理論）
- 有開源實作更好
- 注意是否考慮 look-ahead bias

## Step 3: 開源實作搜尋

搜尋 GitHub：
- `"congressional trading" OR "political trading" Python`
- `"<topic>" alpha signal backtest`

評估：Stars > 50 優先、近 6 個月有更新、有測試覆蓋。

## Step 4: 社群與競品掃描

- 量化社群：r/algotrading, QuantConnect
- 競品功能：Quiver Quantitative, Unusual Whales, Capitol Trades
- 政治數據社群：OpenSecrets, ProPublica Congress API

## Step 5: 輸出 Frontier Report

```markdown
## Frontier Scan Report: [Topic]
**Quadrant**: [OPTIMIZE/TRANSFER/DISCOVER/FRONTIER]

### Top 3 Papers/Sources
1. [Title] ([Year]) — [1句摘要] — 相關性: [H/M/L]
2. ...

### Top 3 GitHub Repos / Tools
1. [Repo] (Stars N) — [描述] — [可直接用/需適配/僅參考]
2. ...

### Community & Competitor Intel
- 主流做法: [...]
- 競品差異化: [...]
- 未覆蓋領域: [...]

### Initial Feasibility
| 維度 | 評估 |
|------|------|
| 技術可行性 | [H/M/L] |
| 數據可得性 | [H/M/L] |
| 預期 alpha 增量 | [H/M/L] |
| 實作複雜度 | [1-5] |

### Next: `/innovate-map`
```

向用戶報告，等待確認。
