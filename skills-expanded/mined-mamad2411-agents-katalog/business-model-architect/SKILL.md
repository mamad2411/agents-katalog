---
name: business-model-architect
description: Use when designing, evaluating, or refining a business model with nine elements, including value proposition (價值主張), target customers (目標客群), channels (通路), customer relationships (顧客關係), revenue streams (收益流), key resources (關鍵資源), key activities (關鍵活動), key partners (關鍵合作夥伴), and cost structure (成本結構), especially for new products, pivots, monetization, and go-to-market decisions.
---

# Business Model Architect

## Overview

用高密度策略推演設計可執行的商業模式，並以固定順序完成 `What -> Who -> How` 九要素。  
預設輸出語言為繁體中文；若使用者明確指定其他語言，再切換。

## When to Use

Use when:
- 使用者要你「設計商業模式」或「重做商業模式」。
- 任務包含九要素：價值主張、目標客群、通路、顧客關係、收益流、關鍵資源、關鍵活動、關鍵合作夥伴、成本結構。
- 需要比較多個商模選項、找差異化策略、或規劃 30 天驗證實驗。
- 涉及市場切入、定價與收益、或商業可行性評估。

Do not use:
- 只需要單純文案潤稿，且不涉及商業模式設計。
- 純技術除錯或與商業策略無關的任務。

## Input Contract

必要欄位（缺一不可）:
- `product_or_service`: 產品或服務描述
- `target_customer_context`: 目標客群與使用情境
- `market_context`: 市場、競品與替代方案現況
- `constraints`: 時間、預算、法規、能力邊界
- `goal_kpi`: 成功指標（營收、留存、轉換、毛利等）

建議欄位（可選）:
- `pricing_context`
- `distribution_constraints`
- `existing_assets`
- `team_capabilities`
- `strategic_horizon`

## Data Sufficiency Gate

若必要欄位缺失，先輸出 `MissingDataOutput`，不得直接產出完整商模。

```json
{
  "missing_fields": [],
  "why_needed": {},
  "questions_to_user": [],
  "temporary_assumptions": [],
  "assumption_risks": []
}
```

規則:
- 問題要短、可回答、可直接推進下一步。
- 若必須先假設，需明確標記 `temporary_assumptions` 與對應風險。
- 缺資料時最多先做「暫行版」框架，不得宣稱已完成可落地方案。

## Output Contract

最終輸出必須包含以下五個主體:
- `business_model_9_elements`
- `strategic_differentiation_map`
- `assumption_and_risk_register`
- `30_day_validation_experiments`
- `priority_roadmap`

### 1) `business_model_9_elements`

必須依序輸出 1-9，且不得跳序：
1. `value_proposition`
2. `target_customers`
3. `channels`
4. `customer_relationships`
5. `revenue_streams`
6. `key_resources`
7. `key_activities`
8. `key_partners`
9. `cost_structure`

每一要素至少包含:
- `design`
- `why_this_works`
- `execution_notes`

### 2) `strategic_differentiation_map`

至少 3 個差異化策略，每個策略必含:
- `strategy_name`
- `core_hypothesis`
- `mechanism`
- `defensibility`
- `key_risks`

### 3) `assumption_and_risk_register`

每筆至少包含:
- `assumption`
- `risk_if_wrong`
- `early_signal`
- `mitigation`

### 4) `30_day_validation_experiments`

至少 3 個實驗，每個實驗必含:
- `experiment_name`
- `target_element`
- `method`
- `success_metric`
- `decision_rule`

### 5) `priority_roadmap`

固定分為:
- `Now`（0-30 天）
- `Next`（31-90 天）
- `Later`（90 天以上）

## Workflow (Fixed)

Step 1. 資料閘門  
- 先檢查必要欄位，缺資料則輸出 `MissingDataOutput`。

Step 2. 創新策略推演（先做差異化）  
- 先建立差異化假說，再回填到九要素，避免產出同質化商模。

Step 3. 依序完成九要素  
- 嚴格依 `What -> Who -> How` 順序，不跳步、不合併。

Step 4. 一致性與可行性檢核  
- 檢查九要素是否互相支持，成本結構是否與收益流一致，資源活動是否可執行。

Step 5. 產出行動化結果  
- 輸出風險登錄、30 天驗證實驗、以及 `Now/Next/Later` 路線圖。

## Quality Rules

- 不得只給抽象建議；每個要素都要有可執行動作。
- 至少提出 3 個差異化策略，且各自有可驗證假說。
- 明確區分「已知事實」與「策略假設」。
- 若有高不確定性，優先給低成本、快速驗證實驗。
- 任何結論都需可追溯到輸入條件與檢核邏輯。

## References

- Intake 與缺資料模板: [references/01-intake-and-constraint-gate.md](./references/01-intake-and-constraint-gate.md)
- 九要素順序與定義: [references/02-nine-element-design-sequence.md](./references/02-nine-element-design-sequence.md)
- 創新策略引擎: [references/03-innovation-strategy-engine.md](./references/03-innovation-strategy-engine.md)
- 通路與收益流策略: [references/04-channel-revenue-design-playbook.md](./references/04-channel-revenue-design-playbook.md)
- 成本與可行性檢核: [references/05-cost-risk-feasibility-checks.md](./references/05-cost-risk-feasibility-checks.md)
- 輸出模板與評分: [references/06-output-template-and-rubric.md](./references/06-output-template-and-rubric.md)
- 可重用報告骨架: [assets/templates/business-model-canvas-report.md](./assets/templates/business-model-canvas-report.md)

## Suggested Prompt

Use `$business-model-architect` to design a complete business model in Traditional Chinese using the fixed nine-element sequence (`What -> Who -> How`) with at least three differentiation strategies, a risk register, and 30-day validation experiments.
