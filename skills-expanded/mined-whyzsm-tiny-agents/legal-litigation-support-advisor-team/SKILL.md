---
name: legal-litigation-support-advisor-team
description: "诉讼支持顾问。用于面向诉讼律师的案件支持专家，梳理案件、证据、时间线、质证准备、索赔图表和文书草稿。来源于 WorkBuddy 法务安全卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/法务安全/legal-litigation-support-advisor"
  workbuddy_card: "诉讼支持顾问"
  workbuddy_category: "法务安全"
---

# 诉讼支持顾问

Use this skill as the routing entry point for 诉讼支持顾问 work. It packages the WorkBuddy 法务安全 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `legal-litigation-support-advisor-intake`
- `legal-litigation-support-advisor-strategy`
- `legal-litigation-support-advisor-execution`
- `legal-litigation-support-advisor-quality`
- `legal-litigation-support-advisor-measurement`
- `legal-litigation-support-advisor-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 诉讼支持顾问 package, assemble the output set described in `references/workflow.md`.
