---
name: sales-meituan-life-assistant-team
description: "美团生活助手。用于帮您一键领取美团优惠券，搜索附近团购美食并下单，探索今日活动，覆盖餐饮饮品等生活服务，省钱省心。来源于 WorkBuddy 销售商务卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/销售商务/sales-meituan-life-assistant"
  workbuddy_card: "美团生活助手"
  workbuddy_category: "销售商务"
---

# 美团生活助手

Use this skill as the routing entry point for 美团生活助手 work. It packages the WorkBuddy 销售商务 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target customer, offer, sales stage, market, budget, data/file scope, constraints, timeline, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `coupon-discovery`
- `local-merchant-search`
- `deal-comparison`
- `order-guidance`
- `daily-activity-scout`
- `budget-summary`

## Output

Produce only the deliverables relevant to the request. For a full 美团生活助手 package, assemble the output set described in `references/workflow.md`.
