---
name: theory-analysis-product-positioning
description: Use when coding cross-source evidence with Product Positioning Theory to classify attributes, functions, benefits, and usage/service context, and when optionally exporting theory_annotations compatible with review-mining-stp.
---

# Theory Analysis Product Positioning

## Overview

用產品定位理論（Product Positioning Theory）分析跨來源證據，輸出可讀報告與可機器串接的結構化結果。
可用來源包含訪談摘要、客服工單、社群貼文、研究筆記、觀察紀錄等，不限於評論探勘。
本 skill 含完整理論章節，可在分析前先校準理論概念與構面判準。
此 skill 可獨立使用，也可選擇把 `theory_annotations` 與 `stp_mapping` 交給 `review-mining-stp`。

## Input Contract

至少提供：

- `analysis_goal: string`
- `evidence_items: array`
  - `item_id: string`
  - `content: string`
  - `content_type: string`

建議可選：

- `source_type: string`
- `source_ref: string`
- `context_tags: string[]`

## Data Sufficiency Gate

若缺少必要欄位或沒有可用證據內容，回傳 `MissingDataOutput`，不要硬做推論。

```json
{
  "missing_fields": [],
  "why_needed": {},
  "questions_to_user": [],
  "next_step_rule": "Provide analysis_goal and at least one evidence item with item_id, content, and content_type, then rerun coding."
}
```

## Workflow

1. 先讀 `references/00-theory-foundation.md`，校準理論概念、核心構面與研究應用語境。
2. 讀 `references/01-input-and-gate.md`，做輸入檢查與缺資料判定。
3. 讀 `references/02-dimension-coding-rules.md`，依四個構面做證據標註：
   - `attributes`
   - `functions`
   - `benefits`
   - `usage_context_service_experience`
4. 讀 `references/03-output-contract-json-markdown.md`，輸出 JSON 與 Markdown。
5. 需要示範格式時，參考 `references/04-worked-example-turbocharger.md`。

## STP Integration

- `theory_annotations.family` 固定為 `product_positioning`
- `theory_annotations.subtheory` 只可使用：
  - `attributes`
  - `functions`
  - `benefits`
  - `usage_context_service_experience`

可搭配 `review-mining-stp` 的 `dimension_catalog` 與 `stat_roles` 進一步分析。
`review-mining-stp` 屬於 optional downstream，不是本 skill 的必經流程。

## Quality Rules

- 引文必須保留原句，不可改寫成看似直接引述。
- 每個構面摘要至少要有一則證據或明確標示 `insufficient`。
- 不可輸出 taxonomy 之外的 subtheory。

## Suggested Prompts

- `Use $theory-analysis-product-positioning to code mixed evidence items and output JSON + Markdown in Traditional Chinese.`
- `請用 $theory-analysis-product-positioning 分析多來源證據，並提供可選串接 review-mining-stp 的 theory_annotations。`
