---
name: marketing-geo-visibility-diagnostician-team
description: "品牌 GEO 可见度诊断师。用于品牌 GEO 可见度诊断专家，覆盖基建评估、AI 收录、竞品对标，输出 AIVO 评分报告。来源于 WorkBuddy 营销增长卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/营销增长/marketing-geo-visibility-diagnostician"
  workbuddy_card: "品牌 GEO 可见度诊断师"
  workbuddy_category: "营销增长"
---

# 品牌 GEO 可见度诊断师

Use this skill as the routing entry point for 品牌 GEO 可见度诊断师 work. It packages the WorkBuddy 营销增长 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `marketing-geo-visibility-diagnostician-intake`
- `marketing-geo-visibility-diagnostician-strategy`
- `marketing-geo-visibility-diagnostician-execution`
- `marketing-geo-visibility-diagnostician-quality`
- `marketing-geo-visibility-diagnostician-measurement`
- `marketing-geo-visibility-diagnostician-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 品牌 GEO 可见度诊断师 package, assemble the output set described in `references/workflow.md`.
