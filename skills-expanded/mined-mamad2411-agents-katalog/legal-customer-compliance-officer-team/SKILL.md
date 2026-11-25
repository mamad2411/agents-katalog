---
name: legal-customer-compliance-officer-team
description: "客户与合规官。用于小企业客户与合规官，处理客户反馈、客诉工单、CRM 清理和合同风险审查。来源于 WorkBuddy 法务安全卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/法务安全/legal-customer-compliance-officer"
  workbuddy_card: "客户与合规官"
  workbuddy_category: "法务安全"
---

# 客户与合规官

Use this skill as the routing entry point for 客户与合规官 work. It packages the WorkBuddy 法务安全 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `legal-customer-compliance-officer-intake`
- `legal-customer-compliance-officer-strategy`
- `legal-customer-compliance-officer-execution`
- `legal-customer-compliance-officer-quality`
- `legal-customer-compliance-officer-measurement`
- `legal-customer-compliance-officer-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 客户与合规官 package, assemble the output set described in `references/workflow.md`.
