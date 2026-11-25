---
name: sales-sg-business-development-team
description: "Sg Business Development。用于帮助企业在新加坡发现客户、伙伴、渠道、供应商与代理商，对接园区、展会、招商资源并确认市场进入路径。来源于 WorkBuddy 销售商务卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/销售商务/sales-sg-business-development"
  workbuddy_card: "Sg Business Development"
  workbuddy_category: "销售商务"
---

# Sg Business Development

Use this skill as the routing entry point for Sg Business Development work. It packages the WorkBuddy 销售商务 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target customer, offer, sales stage, market, budget, data/file scope, constraints, timeline, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `market-entry`
- `customer-discovery`
- `partner-channel`
- `event-resource`
- `localization-strategy`
- `bd-action-plan`

## Output

Produce only the deliverables relevant to the request. For a full Sg Business Development package, assemble the output set described in `references/workflow.md`.
