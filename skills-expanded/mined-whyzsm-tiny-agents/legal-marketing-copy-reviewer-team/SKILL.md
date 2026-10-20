---
name: legal-marketing-copy-reviewer-team
description: "营销文案审查官。用于按规则扫描营销文案，定位广告法与隐私合规风险，输出分级 Excel 与 HTML 审查报告。来源于 WorkBuddy 法务安全卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/法务安全/legal-marketing-copy-reviewer"
  workbuddy_card: "营销文案审查官"
  workbuddy_category: "法务安全"
---

# 营销文案审查官

Use this skill as the routing entry point for 营销文案审查官 work. It packages the WorkBuddy 法务安全 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `legal-marketing-copy-reviewer-intake`
- `legal-marketing-copy-reviewer-strategy`
- `legal-marketing-copy-reviewer-execution`
- `legal-marketing-copy-reviewer-quality`
- `legal-marketing-copy-reviewer-measurement`
- `legal-marketing-copy-reviewer-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 营销文案审查官 package, assemble the output set described in `references/workflow.md`.
