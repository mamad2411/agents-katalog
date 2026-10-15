---
name: data-source-eval
description: >
  評估新數據源的可行性、整合難度和預期 alpha 貢獻。標準化 Spike 框架：
  目標定義 → API 文件搜尋 → 技術可行性 → 整合架構 → 成本分析 → 建議評級。
  適用於評估新 API、替代數據源、競品數據、政府公開資料。
  觸發詞: 評估數據源, evaluate data source, 新 API, 可行性, feasibility,
  spike, 技術評估, 整合評估, 新數據, data source, API 評估, 數據源調研,
  能不能用, 怎麼接, 資料來源, alternative data, 政府資料, 公開API
---

# Data Source Evaluation — 新數據源 Spike 框架

本 Skill 提供標準化的新數據源技術評估流程。
每次評估產出一份結構化的 Spike Report，供 CDO/CTO 決策。

## 評估框架 (5 維度)

### Dimension 1: 數據品質 (Data Quality) — 30%

| 指標 | 問題 | 評分 |
|------|------|------|
| 覆蓋度 | 數據涵蓋多少 ticker/議員/時間範圍？ | 0-100 |
| 即時性 | 更新頻率？延遲多久？ | 0-100 |
| 準確性 | 有無已知錯誤/遺漏？ | 0-100 |
| 結構化程度 | JSON/CSV/HTML/PDF？需要多少解析？ | 0-100 |
| 歷史深度 | 可回溯多久？回測可行嗎？ | 0-100 |

### Dimension 2: 技術整合 (Integration) — 25%

| 指標 | 問題 | 評分 |
|------|------|------|
| API 品質 | RESTful? 文件完善? SDK? | 0-100 |
| 認證 | API key? OAuth? 無需認證? | 0-100 |
| Rate Limit | 每分/每日請求上限？ | 0-100 |
| 輸出格式 | JSON (理想) / CSV / HTML / PDF (最差) | 0-100 |
| 與現有架構相容 | 能否直接接入 ETL pipeline? | 0-100 |

### Dimension 3: Alpha 潛力 (Alpha Potential) — 25%

| 指標 | 問題 | 評分 |
|------|------|------|
| 理論基礎 | 為何此數據源能預測股價? | 0-100 |
| 學術文獻 | 有無學術研究支持? | 0-100 |
| 與現有信號獨立性 | 和 congress_trades 的相關性? | 0-100 |
| 可回測性 | 能否用歷史數據驗證? | 0-100 |
| 競品使用 | 其他平台有在用嗎? | 0-100 |

### Dimension 4: 成本 (Cost) — 10%

| 指標 | 問題 | 評分 |
|------|------|------|
| API 費用 | 免費/低成本/中等/昂貴 | 0-100 |
| 開發工時 | 1天/1週/1月? | 0-100 |
| 維護成本 | 穩定API? 可能被封? | 0-100 |

### Dimension 5: 合規風險 (Compliance) — 10%

| 指標 | 問題 | 評分 |
|------|------|------|
| 數據授權 | 公開資料? 需授權? ToS 限制? | 0-100 |
| 個資風險 | 涉及個人資料嗎? | 0-100 |
| 抓取合法性 | robots.txt? rate limit 合規? | 0-100 |

## 執行流程

### Step 1: 目標定義

明確回答:
- 數據源名稱和 URL
- 預期用途 (新的 alpha 因子? 增強現有信號? 風險管理?)
- 預期與 PAM 的整合方式

### Step 2: API/文件搜索

用 WebSearch 搜尋:
1. 官方 API 文件
2. 開發者社群討論 (GitHub issues, Stack Overflow)
3. 費率和限制頁面
4. 學術論文引用此數據源

### Step 3: 技術可行性測試

嘗試用 WebFetch 或 curl 做一次最小請求:
- 回應格式和欄位
- 認證方式
- 回應時間
- 錯誤處理

### Step 4: 與 PAM 架構對比

評估整合進 `src/etl/` 的難度:
- 需要新建 fetcher? 還是現有 fetcher 可擴充?
- 需要新 DB 表? 還是可加入現有表?
- 需要新的 LLM prompt? 還是結構化數據可直接解析?

### Step 5: 產出 Spike Report

```markdown
# Data Source Spike: [數據源名稱]

**評估日期**: YYYY-MM-DD
**評估員**: [agent name]
**研究代號**: RB-XXX

## 概要
[1-2 句描述此數據源和預期用途]

## 評分卡 (Scorecard)
| 維度 | 權重 | 分數 | 說明 |
|------|------|------|------|
| 數據品質 | 30% | XX/100 | ... |
| 技術整合 | 25% | XX/100 | ... |
| Alpha 潛力 | 25% | XX/100 | ... |
| 成本 | 10% | XX/100 | ... |
| 合規風險 | 10% | XX/100 | ... |
| **加權總分** | 100% | **XX/100** | **[GO/NO-GO/NEEDS-MORE-DATA]** |

## 評級
- 80+: STRONG GO — 立即開發
- 60-79: GO — 排入本季度
- 40-59: CONDITIONAL — 需要更多驗證
- <40: NO-GO — 不建議投資

## API 細節
- 端點: [URL]
- 認證: [方式]
- Rate Limit: [限制]
- 輸出格式: [JSON/CSV/etc]
- 費用: [免費/$/$$/$$$]

## 整合架構建議
[如何接入 PAM 的 ETL pipeline，需要哪些新模組]

## 風險與限制
[主要風險點和緩解方案]

## 建議下一步
- [ ] [具體行動項目]
```

## PAM 已評估 / 計畫中的數據源

詳見 references/: Read `.claude/skills/data-source-eval/references/known-sources.md`

**已整合**: Senate EFD, House Clerk, Capitol Trades, SEC EDGAR Form 4, Twitter/X, Truth Social, Reddit, Kenneth French Data Library
**計畫中**: Congress.gov Committee API (RB-008), USASpending (RB-009), Earnings Calendar (RB-010), Lobbying Disclosure (RB-012)
