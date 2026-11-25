---
name: legal-compliance-reviewer-team
description: "法律合规审查员。用于确保业务运营和产品功能符合法律法规要求，防范合规风险。来源于 WorkBuddy 法务安全卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/法务安全/legal-compliance-reviewer"
  workbuddy_card: "法律合规审查员"
  workbuddy_category: "法务安全"
---

# 法律合规审查员

Use this skill as the routing entry point for 法律合规审查员 work. It packages the WorkBuddy 法务安全 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `legal-compliance-reviewer-intake`
- `legal-compliance-reviewer-strategy`
- `legal-compliance-reviewer-execution`
- `legal-compliance-reviewer-quality`
- `legal-compliance-reviewer-measurement`
- `legal-compliance-reviewer-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 法律合规审查员 package, assemble the output set described in `references/workflow.md`.
