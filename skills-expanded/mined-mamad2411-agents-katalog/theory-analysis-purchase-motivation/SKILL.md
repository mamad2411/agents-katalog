---
name: theory-analysis-purchase-motivation
description: Use when coding cross-source evidence with Purchase Motivation Theory to classify functional, security, and relational drivers, and when optionally exporting theory_annotations compatible with review-mining-stp.
---

# Theory Analysis Purchase Motivation

## Overview

用購買動機理論（Purchase Motivation Theory）分析跨來源證據中的決策驅動因素。
來源可為訪談摘要、客服工單、社群貼文、研究筆記、觀察紀錄等。
本 skill 含完整理論章節，可在分析前先校準動機理論與判準邊界。
此 skill 可獨立使用，也可選擇將輸出銜接 `review-mining-stp`。

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

若缺必要欄位或沒有可用證據內容，輸出 `MissingDataOutput`，不做硬判讀。

```json
{
  "missing_fields": [],
  "why_needed": {},
  "questions_to_user": [],
  "next_step_rule": "Provide analysis_goal and at least one evidence item with item_id, content, and content_type, then rerun coding."
}
```

## Workflow

1. 先讀 `references/00-theory-foundation.md`，校準理論概念、核心動機與研究應用語境。
2. 讀 `references/01-input-and-gate.md`，完成輸入檢核。
3. 讀 `references/02-dimension-coding-rules.md`，依三種動機做證據標註：
   - `functional`
   - `security`
   - `relational`
4. 讀 `references/03-output-contract-json-markdown.md`，輸出 JSON + Markdown。
5. 需要範例時讀 `references/04-worked-example-turbocharger.md`。

## STP Integration

- `theory_annotations.family` 固定為 `purchase_motivation`
- `theory_annotations.subtheory` 只可使用：
  - `functional`
  - `security`
  - `relational`

輸出欄位可直接轉進 `review-mining-stp` 的理論標註層。
`review-mining-stp` 屬於 optional downstream，不是主流程前提。

## Quality Rules

- 每個動機結論必須至少有一則可稽核引文，否則標記 `insufficient`。
- 不能把運送、包裝、售後都直接歸到 `functional`，需依定義判斷。
- taxonomy 必須完全符合既有規則，不得自創 subtheory。

## Suggested Prompts

- `Use $theory-analysis-purchase-motivation to label purchase drivers from mixed evidence items and output JSON + Markdown in Traditional Chinese.`
- `請用 $theory-analysis-purchase-motivation 分析多來源證據中的購買動機，並產出可選串接 review-mining-stp 的 theory_annotations。`
