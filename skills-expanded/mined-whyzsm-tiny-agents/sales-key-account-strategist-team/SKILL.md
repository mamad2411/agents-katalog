---
name: sales-key-account-strategist-team
description: "大客户策略师。用于精通大客户经营和账户扩展策略，将客户发展为长期战略伙伴。来源于 WorkBuddy 销售商务卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/销售商务/sales-key-account-strategist"
  workbuddy_card: "大客户策略师"
  workbuddy_category: "销售商务"
---

# 大客户策略师

Use this skill as the routing entry point for 大客户策略师 work. It packages the WorkBuddy 销售商务 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target customer, offer, sales stage, market, budget, data/file scope, constraints, timeline, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `account-mapping`
- `account-plan`
- `stakeholder-strategy`
- `expansion-strategy`
- `risk-management`
- `qbr-playbook`

## Output

Produce only the deliverables relevant to the request. For a full 大客户策略师 package, assemble the output set described in `references/workflow.md`.
