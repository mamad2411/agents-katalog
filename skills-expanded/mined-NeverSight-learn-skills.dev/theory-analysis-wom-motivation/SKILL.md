---
name: theory-analysis-wom-motivation
description: Use when coding cross-source evidence with Word-of-Mouth Motivation Theory to classify altruistic, social identity, self-enhancement, and emotional expression motives, and when optionally exporting theory_annotations compatible with review-mining-stp.
---

# Theory Analysis WOM Motivation

## Overview

用口碑動機理論（Word-of-Mouth Motivation Theory）解析證據提供者為何願意分享經驗或態度。
來源可為訪談摘要、客服對話、社群貼文、研究筆記、觀察紀錄等，不限於評論。
本 skill 含完整理論章節，可在分析前先校準口碑動機的判讀邏輯。
此 skill 可單獨使用，也可選擇把結構化結果交給 `review-mining-stp`。

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

缺必要資訊時，輸出 `MissingDataOutput`，不直接推論口碑動機。

```json
{
  "missing_fields": [],
  "why_needed": {},
  "questions_to_user": [],
  "next_step_rule": "Provide analysis_goal and at least one evidence item with item_id, content, and content_type, then rerun coding."
}
```

## Workflow

1. 先讀 `references/00-theory-foundation.md`，校準理論概念、動機類型與研究應用語境。
2. 讀 `references/01-input-and-gate.md`，檢核資料完整度。
3. 讀 `references/02-dimension-coding-rules.md`，依四種口碑動機做證據標註：
   - `altruistic`
   - `social_identity`
   - `self_enhancement`
   - `emotional_expression`
4. 讀 `references/03-output-contract-json-markdown.md`，輸出 JSON + Markdown。
5. 用 `references/04-worked-example-turbocharger.md` 對齊格式與深度。

## STP Integration

- `theory_annotations.family` 固定為 `wom_motivation`
- `theory_annotations.subtheory` 只可使用：
  - `altruistic`
  - `social_identity`
  - `self_enhancement`
  - `emotional_expression`

結果可直接對接 `review-mining-stp` 的理論標註。
`review-mining-stp` 屬於 optional downstream，不是本 skill 的必要依賴。

## Quality Rules

- 口碑動機需要有可辨識意圖，若無意圖訊號需標記 `insufficient`。
- `self_enhancement` 與 `social_identity` 必須區分：
  - 前者偏「展現專業或能力」
  - 後者偏「取得社群認同或歸屬」
- 所有結論都要可被 `evidence_quotes` 追溯。

## Suggested Prompts

- `Use $theory-analysis-wom-motivation to code sharing motives from mixed evidence items and return JSON + Markdown in Traditional Chinese.`
- `請用 $theory-analysis-wom-motivation 分析多來源證據中的口碑動機，並輸出可選串接 review-mining-stp 的 theory_annotations。`
