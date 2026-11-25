---
name: sales-discovery-coach-team
description: "需求发现教练。用于训练销售掌握深度需求挖掘技巧，发现真正的业务痛点。来源于 WorkBuddy 销售商务卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/销售商务/sales-discovery-coach"
  workbuddy_card: "需求发现教练"
  workbuddy_category: "销售商务"
---

# 需求发现教练

Use this skill as the routing entry point for 需求发现教练 work. It packages the WorkBuddy 销售商务 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target customer, offer, sales stage, market, budget, data/file scope, constraints, timeline, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `discovery-plan`
- `question-framework`
- `pain-mapping`
- `customer-insight`
- `active-listening`
- `discovery-review`

## Output

Produce only the deliverables relevant to the request. For a full 需求发现教练 package, assemble the output set described in `references/workflow.md`.
