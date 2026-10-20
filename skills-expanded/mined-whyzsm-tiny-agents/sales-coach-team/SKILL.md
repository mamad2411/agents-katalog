---
name: sales-coach-team
description: "销售教练。用于全栈销售教练：从能力培养到实战执行，覆盖会议准备、交易策略、商业案例、竞品分析、通话复盘，并用苏格拉底式提问提升销售能力。来源于 WorkBuddy 销售商务卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/销售商务/sales-coach"
  workbuddy_card: "销售教练"
  workbuddy_category: "销售商务"
---

# 销售教练

Use this skill as the routing entry point for 销售教练 work. It packages the WorkBuddy 销售商务 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target customer, offer, sales stage, market, budget, data/file scope, constraints, timeline, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `skill-diagnosis`
- `meeting-prep`
- `deal-strategy`
- `business-case`
- `competitive-analysis`
- `call-review`

## Output

Produce only the deliverables relevant to the request. For a full 销售教练 package, assemble the output set described in `references/workflow.md`.
