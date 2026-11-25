---
name: innovate-map
description: "創新 Phase 2：跨域映射 + 數據源評估。分析技術遷移可行性與新數據源 alpha 潛力。Use when 'cross-domain mapping', '跨域映射', 'data source evaluation', '數據源評估'."
allowed-tools: Read, Glob, Grep, WebSearch, WebFetch
---

# /innovate-map — 跨域映射 + 數據源評估

讀 `docs/innovation_state.json` 取得前沿掃描結果。

## Part A: 跨域映射（TRANSFER/FRONTIER 象限）

### Step 1: 建立映射表

```
源域: [e.g., ESG Sentiment Analysis]
  ↓ 映射
目標域: PAM Congressional Trading Signals

| 源域概念 | 目標域對應 | 適配難度 |
|---------|-----------|---------|
| ESG sentiment score | Social alignment score | Low |
| Company ESG rating | Politician PIS grade | Medium |
| ESG controversy events | Filing lag anomalies | High |
```

### Step 2: 可遷移性評估

| 維度 | 問題 | 答案 |
|------|------|------|
| 數據 | 目標域有等價數據？ | |
| 時間尺度 | 原方法適合事件驅動？ | |
| 市場結構 | 議員交易是否適用？ | |
| 樣本量 | 5000+ trades 夠嗎？ | |
| 信號衰減 | Filing lag 影響大嗎？ | |

## Part B: 數據源評估（DISCOVER 象限）

### Step 3: 評估矩陣（使用 /data-source-eval 標準）

| 評估項 | 結果 |
|--------|------|
| 可得性 | [免費/付費] via [API/爬蟲/手動] |
| 覆蓋率 | [X] politicians, [Y] years |
| 更新頻率 | [日/週/月/即時] |
| Point-in-time | [可得/不可得] |
| 法規風險 | [Low/Medium/High] |
| 維護成本 | [工程投入評估] |
| 與現有系統整合 | [需改多少模組] |

### Step 4: Alpha 潛力初估

- 與現有 PACS/SQS 信號的理論獨立性
- 預期 alpha 範圍（基於文獻和類比推理）
- 與 RB-001~009 已有發現的互補性

## 輸出映射報告

```markdown
## Mapping Report: [Topic]

### Cross-Domain Mapping (if applicable)
[映射表 + 可遷移性評估]

### Data Source Assessment (if applicable)
[評估矩陣]

### Alpha Potential
- 理論獨立性: [High/Medium/Low]
- 預期 alpha 範圍: [X%-Y% CAR_20d]
- 與現有研究互補性: [High/Medium/Low]
- 建議: [INTEGRATE / PILOT / MONITOR / SKIP]

### Next: `/innovate-poc`
```

向用戶報告，等待確認。
