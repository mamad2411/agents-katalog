---
name: service-design-workshop
description: Use when turning a service design problem into a structured workshop output, especially for 服務設計, 服務藍圖, 服務流程, 接觸點, 前台後台, 服務實證, 顧客體驗, 利害關係人, 服務概念, or 服務架構. Trigger when the task asks for a practical service design brief, blueprint-ready structure, touchpoint analysis, or prototype and validation next steps rather than only theory review.
---

# Service Design Workshop

## Overview

把服務設計題目整理成可執行的工作坊輸出，先定義問題與場域，再整理利害關係人、服務概念、架構、接觸點與驗證步驟。
如果需求其實是 persona 或 customer journey map 本身，停止並改用 `customer-persona-framer` 或 `customer-journey-mapper`。

## Input Contract

至少要有以下其中兩項：

- `service_problem`
- `target_users_or_customers`
- `service_context`
- `pain_points_or_failure_points`

可選：

- `business_goal`
- `constraints`
- `existing_touchpoints`
- `known_stakeholders`
- `requested_format`

資訊不足但使用者要快速草稿時，先列出 `3-5` 個假設，再繼續輸出。

## Workflow

1. 定義 `problem_and_context`，說清楚現況、場域、限制與設計目標。
2. 整理 `stakeholders_and_needs`，區分顧客、第一線、後台、合作方。
3. 形成 `service_concept_and_architecture`，明確說明價值、階段、接口與關鍵體驗。
4. 展開 `frontstage_backstage_touchpoints`，至少區分前台、後台、支援系統、服務實證。
5. 產出 `prototype_and_validation_next_steps`，把雛型、測試方式、觀察指標寫清楚。

## Output Contract

固定輸出以下段落：

- `service_design_brief`
- `problem_and_context`
- `stakeholders_and_needs`
- `service_concept_and_architecture`
- `frontstage_backstage_touchpoints`
- `prototype_and_validation_next_steps`

優先使用繁體中文 Markdown。若使用者要求簡報或課堂作業格式，保留同樣資訊架構，只改成較適合投影片或報告的表述。

## Quick Reference

- 定義與流程：讀 [references/service-design-principles-and-process.md](./references/service-design-principles-and-process.md)
- 方法與工具：讀 [references/service-design-methods.md](./references/service-design-methods.md)
- 輸出模板：讀 [references/service-design-output-templates.md](./references/service-design-output-templates.md)

## Quality Rules

- 先定義問題，再提方案，不要直接跳結論。
- 用顧客體驗與服務運作雙視角，不只寫行銷話術。
- 接觸點必須對應到服務階段與前後台，不要只列通路名稱。
- 把服務實證寫成可觀察物件，例如空間、介面、通知、文件、制服、包裝。
- 驗證步驟要包含原型形式、測試對象、成功訊號。

## Common Mistakes

- 把服務設計寫成單純 customer journey：缺少前後台、服務架構與實證。
- 把方法名詞堆滿：沒有回到題目的痛點、場域與利害關係人。
- 只寫理想體驗：沒有執行限制、營運支撐或驗證方法。

## Suggested Prompt

Use `$service-design-workshop` to turn a service design challenge into a Traditional Chinese workshop output with problem framing, stakeholders, service architecture, frontstage/backstage touchpoints, and prototype validation steps.
