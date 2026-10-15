---
name: service-innovation-workshop
description: Use when turning a service innovation problem into concept options, prototype testing, and risk checks, especially for 服務創新, 創新機會, 價值共創, 服務原型, SCAMPER, 購買者效用矩陣, 創新流程, 創新困境, or 服務體驗工程. Trigger when the task asks for practical innovation directions, concept generation, opportunity framing, or validation planning rather than only concept definitions.
---

# Service Innovation Workshop

## Overview

把服務創新題目整理成可比較、可測試、可執行的創新方案，先判斷創新機會與類型，再提出概念、原型測試與風險檢查。
如果任務已經轉成完整商業模式、營收結構或九宮格設計，提示銜接 `business-model-architect`。

## Input Contract

至少要有以下其中兩項：

- `innovation_goal`
- `target_users_or_market`
- `current_service_or_process`
- `pain_points_or_market_change`

可選：

- `competitive_context`
- `technology_or_resource_constraints`
- `desired_degree_of_innovation`
- `existing_assets`
- `requested_format`

資訊不足但使用者要求快速提案時，先列出 `3-5` 個假設，再繼續產出。

## Workflow

1. 定義 `innovation_challenge`，說清楚要改善什麼、為什麼現在要做。
2. 判斷 `innovation_type_and_opportunity_source`，分類創新類型、來源與拉力。
3. 生成 `concept_options`，至少提出 `3` 個方向，避免只給單一點子。
4. 收斂成 `recommended_service_innovation_concept`，說明為何優先。
5. 製作 `prototype_test_plan`，定義雛型、測試對象、學習目標與成功訊號。
6. 補上 `risk_and_pitfall_check`，避免落入技術本位、假服務、過度承諾等常見誤區。

## Output Contract

固定輸出以下段落：

- `innovation_challenge`
- `innovation_type_and_opportunity_source`
- `concept_options`
- `recommended_service_innovation_concept`
- `prototype_test_plan`
- `risk_and_pitfall_check`

預設使用繁體中文 Markdown。若使用者要課堂報告或簡報版，保留相同欄位，只壓縮成較可投影片化的句型。

## Quick Reference

- 分類、來源與流程：讀 [references/service-innovation-lenses.md](./references/service-innovation-lenses.md)
- 方法與發想工具：讀 [references/service-innovation-methods.md](./references/service-innovation-methods.md)
- 輸出模板：讀 [references/service-innovation-output-templates.md](./references/service-innovation-output-templates.md)

## Quality Rules

- 先判斷創新機會與類型，再提解法，不要直接丟點子。
- 至少同時看顧客需求變化、組織能力、技術或流程條件。
- 概念方案要能比較，避免三個方案其實只是同一件事換說法。
- 原型測試要寫可學到什麼，而不是只寫「先試試看」。
- 風險檢查要明講誤區與修正方式。

## Common Mistakes

- 把服務創新寫成單一促銷活動：沒有流程、體驗或服務內容變化。
- 只講技術新不新：沒有說為誰解決什麼需求。
- 直接挑一個方案：沒有先分類機會來源，也沒有比較替代概念。

## Suggested Prompt

Use `$service-innovation-workshop` to turn a service innovation challenge into Traditional Chinese concept options, a recommended direction, a prototype test plan, and a risk check.
