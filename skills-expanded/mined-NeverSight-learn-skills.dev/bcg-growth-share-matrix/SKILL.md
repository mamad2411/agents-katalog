---
name: bcg-growth-share-matrix
description: Use when analyzing a group, business-unit, product-line, or brand portfolio with the BCG growth-share matrix, especially when the task involves relative market share, market growth, quadrant classification, capital allocation, portfolio prioritization, or deciding whether to invest, maintain, harvest, reposition, or exit.
---

# BCG 成長佔有率矩陣

## Overview

用 BCG 成長佔有率矩陣分析集團或產品組合，將各事業體依 `relative market share` 與 `market growth rate` 放入四象限，並產出資本配置、風險說明與後續追蹤動作。

此 skill 預設以繁體中文輸出，但保留 `Cash Cows / Stars / Question Marks / Dogs` 英文對照。把 BCG 當成投資組合篩選器，不把它當成唯一決策器。

## Trigger Map

Use when:
- 使用者要分析集團、SBU、產品線、品牌組合的資源配置
- 問題明確提到 `BCG matrix`、`growth-share matrix`、`relative market share`、`market growth`
- 問題使用別名詞彙，例如 `Pets`、`Problem Child`、`Wild Cat`、`搖錢母牛`
- 需要在 `投資 / 維持 / 收割 / 退出 / 重定位` 之間做組合判斷
- 需要條列式輸出每個事業體的象限、依據、策略與資本優先序
- 需要把成熟業務的現金來源與成長業務的投資需求串成 portfolio view

Do not use:
- 單一事業的競爭策略深挖，但沒有組合資本配置問題
- 需要更細的產業吸引力與競爭力評估時；那通常要升級成 GE/McKinsey 或更完整策略框架
- 只有模糊敘述、沒有市場佔有率或市場成長資訊，且不允許做任何暫時假設

## Input Contract

必要輸入：
- `group_context`: 集團簡述、戰略目標、資金限制、時間範圍
- `business_units[]`: 至少 2 個事業體或產品
- 每個 `business_unit` 至少包含：
  - `name`
  - `market_share`
  - `largest_competitor_share` 或 `relative_market_share`
  - `market_growth_rate`

建議補充：
- `revenue_size`
- `cash_generation`
- `strategic_synergy`
- `competitive_moat`
- `capex_intensity`
- `time_horizon`
- `thresholds`

`thresholds` 若有提供，優先使用：
```json
{
  "relative_market_share_cutoff": 1.0,
  "market_growth_cutoff": 10.0,
  "borderline_band": 2.0
}
```

## Data Sufficiency Gate

資料不足時不要直接硬分類，先輸出 `MissingDataOutput`：

```json
{
  "missing_fields": [],
  "why_needed": {},
  "questions_to_user": [],
  "temporary_assumptions": [],
  "assumption_risks": [],
  "next_step_rule": "若缺口影響象限判定或資本建議，先補資料再分析；若可暫時假設，必須顯示假設與風險。"
}
```

缺資料時的規則：
- 缺 `largest_competitor_share` 且無 `relative_market_share`，不可假裝能精準判定競爭力
- 若只有「高/中/低」而非數值，先要求轉為數值或明示為粗估
- 若接近 cut-off，必須標記 `borderline`，不要用武斷口吻
- 若存在明顯協同效應、法規屏障、平台網路效應或共享基礎設施，需放入例外說明

## Classification Rules

分類時固定先做以下步驟：

1. 先確認市場邊界是否可比  
- 事業體必須落在可比較的市場定義中，否則 BCG 座標不可靠。

2. 計算或讀取 `relative_market_share`  
- 若有 `relative_market_share`，直接使用  
- 否則用：
```text
relative_market_share = market_share / largest_competitor_share
```

3. 決定高低門檻  
- `relative_market_share >= 1.0` 預設視為高 share  
- `market_growth_rate > 10%` 預設視為高 growth  
- 若使用者提供產業門檻，覆蓋預設  
- 若落在 `borderline_band` 內，要加註敏感度與替代判讀

4. 套入四象限  
- `high share + high growth` -> `Stars`
- `high share + low growth` -> `Cash Cows`
- `low share + high growth` -> `Question Marks`
- `low share + low growth` -> `Dogs`

5. 給每個事業體一個發展潛力分級  
- `high`: 可見成長與份額改善路徑，且資本效率可接受
- `medium`: 可改善但有關鍵風險未解
- `low`: 份額/經濟性/協同任一核心條件不足

6. 再做第二層校正  
- 檢查 `cash_generation`、`strategic_synergy`、`competitive_moat`、`capex_intensity`
- 若量化象限與商業重要性衝突，保留象限不變，但在建議中加入 `exception note`

## Output Contract

輸出物件固定包含：
- `portfolio_snapshot`
- `matrix_plot_data`
- `unit_classification_table`
- `quadrant_recommendations`
- `capital_allocation_actions`
- `portfolio_rebalance_priorities`
- `assumptions_and_limitations`
- `next_90_day_followups`

### `portfolio_snapshot`
- 3-5 點摘要整體組合結構
- 說明現金來源、投資壓力、最大斷層與最危險象限偏斜

### `matrix_plot_data`
固定欄位：
- `x_axis`: `relative_market_share`
- `y_axis`: `market_growth_rate`
- `quadrant_cutoffs`
- `points[]`，每筆包含：
  - `name`
  - `x`
  - `y`
  - `quadrant`
  - `borderline`

### `unit_classification_table`
每個事業體固定欄位：
- `name`
- `market_share`
- `largest_competitor_share`
- `relative_market_share`
- `market_growth_rate`
- `quadrant`
- `classification_reason`
- `borderline_or_exception`
- `development_potential`
- `likely_transition_path`
- `transition_condition`
- `strategy_posture`
- `capital_priority`

### `quadrant_recommendations`
依四象限分組，說明：
- 象限特性
- 典型策略姿態
- 何時加碼、何時維持、何時收割、何時退出

### `capital_allocation_actions`
至少包含：
- 哪些 `Cash Cows` 應提供資金
- 哪些 `Stars` 應優先防守或擴張
- 哪些 `Question Marks` 應做階段式實驗
- 哪些 `Dogs` 應收割、出售、關閉或僅因協同而保留

### `portfolio_rebalance_priorities`
固定用：
- `Now (0-30 days)`
- `Next (31-90 days)`
- `Later (90+ days)`

### `assumptions_and_limitations`
固定包含：
- 使用了哪些門檻
- 哪些資料為暫時假設
- 哪些判斷可能因市場定義或資料品質而改變
- 為什麼 BCG 不是唯一決策依據

### `next_90_day_followups`
至少列出：
- 要補的資料
- 要做的實驗或財務驗證
- 要追蹤的 KPI

## Workflow

1. 讀 [references/02-intake-and-data-sufficiency.md](./references/02-intake-and-data-sufficiency.md) 做資料檢查  
2. 讀 [references/01-bcg-foundation-and-metrics.md](./references/01-bcg-foundation-and-metrics.md) 確認計算與門檻  
3. 讀 [references/03-quadrant-strategy-playbook.md](./references/03-quadrant-strategy-playbook.md) 產出各象限策略  
4. 讀 [references/04-modern-caveats-and-portfolio-logic.md](./references/04-modern-caveats-and-portfolio-logic.md) 加上現代化 caveats  
5. 若使用者要快速交付版，套用 [assets/templates/bcg-portfolio-analysis-template.md](./assets/templates/bcg-portfolio-analysis-template.md)

## Quality Rules

- 一律顯示 `relative_market_share` 的來源或計法
- 一律明示 `market_growth_cutoff`，未提供時說明暫用 `10%`
- 一律輸出 `matrix_plot_data`，且每個事業體都要有座標點
- 一律說明分類依據，不只給象限名稱
- 一律提供每個事業體的 `likely_transition_path` 與 `transition_condition`
- 一律提供 portfolio-level 資本重配，不只逐點評論單一事業
- `Dogs` 不得一律直接判死刑；若存在協同、平台入口、法規牌照、防禦價值，需說明例外
- `Question Marks` 不得一律說「加碼」；必須加入投資條件與停損條件
- `Cash Cows` 不得只寫「維持」；要說明要不要擠現金、是否有被技術或需求轉移侵蝕的風險
- `Stars` 不得只寫「投資」；要說明是防守份額、加速滲透還是提升經濟性
- 一律加入 `assumptions_and_limitations`

## References

- BCG 基礎與衡量：[references/01-bcg-foundation-and-metrics.md](./references/01-bcg-foundation-and-metrics.md)
- 資料齊備與追問：[references/02-intake-and-data-sufficiency.md](./references/02-intake-and-data-sufficiency.md)
- 四象限策略手冊：[references/03-quadrant-strategy-playbook.md](./references/03-quadrant-strategy-playbook.md)
- 現代化限制與組合邏輯：[references/04-modern-caveats-and-portfolio-logic.md](./references/04-modern-caveats-and-portfolio-logic.md)
- 常見用例與 prompts：[references/05-use-cases-and-prompts.md](./references/05-use-cases-and-prompts.md)
- 輸出模板：[assets/templates/bcg-portfolio-analysis-template.md](./assets/templates/bcg-portfolio-analysis-template.md)

## Suggested Prompt

Use `$bcg-growth-share-matrix` to analyze a group or product portfolio in Traditional Chinese, classify each business into Cash Cows, Stars, Question Marks, or Dogs, show the relative market share logic, and recommend portfolio-level capital allocation with caveats and next-step actions.
