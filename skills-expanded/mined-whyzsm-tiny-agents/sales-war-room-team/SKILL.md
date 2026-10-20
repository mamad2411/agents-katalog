---
name: sales-war-room-team
description: "销售作战团队。用于销售攻坚体系，客户研究锁定目标、外联策略提升触达、竞品情报预警风险、销售预测优化资源分配。来源于 WorkBuddy 销售商务卡片，并转换为 Codex 可安装的专家团入口格式。"
metadata:
  source: "workbuddy-expert-center/销售商务/sales-war-room"
  workbuddy_card: "销售作战团队"
  workbuddy_category: "销售商务"
---

# 销售作战团队

Use this skill as the routing entry point for 销售作战团队 work. It packages the WorkBuddy 销售商务 expert-team card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, source material, business or legal boundary, data/file scope, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata and available marketplace candidates, not from a hidden expert-detail prompt.
5. Return concrete deliverables, verification evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `account-research`
- `outreach-strategy`
- `competitive-intel`
- `sales-forecast`
- `deal-playbook`
- `resource-allocation`

## Output

Produce only the deliverables relevant to the request. For a full 销售作战 package, assemble the output set described in `references/workflow.md`.
