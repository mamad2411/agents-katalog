---
name: legal-contract-risk-advisor-team
description: "合同风控顾问。用于覆盖合同起草、审查、谈判、背景评估与全生命周期管理，审查式一键产出风险清单。来源于 WorkBuddy 法务安全卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/法务安全/legal-contract-risk-advisor"
  workbuddy_card: "合同风控顾问"
  workbuddy_category: "法务安全"
---

# 合同风控顾问

Use this skill as the routing entry point for 合同风控顾问 work. It packages the WorkBuddy 法务安全 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `legal-contract-risk-advisor-intake`
- `legal-contract-risk-advisor-strategy`
- `legal-contract-risk-advisor-execution`
- `legal-contract-risk-advisor-quality`
- `legal-contract-risk-advisor-measurement`
- `legal-contract-risk-advisor-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 合同风控顾问 package, assemble the output set described in `references/workflow.md`.
