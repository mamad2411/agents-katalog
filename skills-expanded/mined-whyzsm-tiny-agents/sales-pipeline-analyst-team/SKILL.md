---
name: sales-pipeline-analyst-team
description: "销售管道分析师。用于用数据驱动方法分析销售管道健康度，让预测从猜测变科学。来源于 WorkBuddy 销售商务卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/销售商务/sales-pipeline-analyst"
  workbuddy_card: "销售管道分析师"
  workbuddy_category: "销售商务"
---

# 销售管道分析师

Use this skill as the routing entry point for 销售管道分析师 work. It packages the WorkBuddy 销售商务 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target customer, offer, sales stage, market, budget, data/file scope, constraints, timeline, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `pipeline-health`
- `forecast-model`
- `conversion-analysis`
- `cohort-segmentation`
- `resource-optimization`
- `dashboard-report`

## Output

Produce only the deliverables relevant to the request. For a full 销售管道分析师 package, assemble the output set described in `references/workflow.md`.
