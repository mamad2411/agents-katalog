---
name: sales-revenue-growth-team
description: "营收增长师。用于小企业营收增长师，从线索打分到内容策略再到营销活动，一条龙驱动营收增长。来源于 WorkBuddy 销售商务卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/销售商务/sales-revenue-growth"
  workbuddy_card: "营收增长师"
  workbuddy_category: "销售商务"
---

# 营收增长师

Use this skill as the routing entry point for 营收增长师 work. It packages the WorkBuddy 销售商务 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target customer, offer, sales stage, market, budget, data/file scope, constraints, timeline, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `lead-scoring`
- `content-strategy`
- `campaign-design`
- `funnel-operations`
- `revenue-metrics`
- `growth-experiment`

## Output

Produce only the deliverables relevant to the request. For a full 营收增长师 package, assemble the output set described in `references/workflow.md`.
