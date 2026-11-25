---
name: legal-skill-governance-team
description: "法律技能治理专家。用于面向法律运营和技能开发者的治理助手，评估技能来源、工具权限、新鲜度、许可证和信任边界。来源于 WorkBuddy 法务安全卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/法务安全/legal-skill-governance"
  workbuddy_card: "法律技能治理专家"
  workbuddy_category: "法务安全"
---

# 法律技能治理专家

Use this skill as the routing entry point for 法律技能治理专家 work. It packages the WorkBuddy 法务安全 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `legal-skill-governance-intake`
- `legal-skill-governance-strategy`
- `legal-skill-governance-execution`
- `legal-skill-governance-quality`
- `legal-skill-governance-measurement`
- `legal-skill-governance-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 法律技能治理专家 package, assemble the output set described in `references/workflow.md`.
