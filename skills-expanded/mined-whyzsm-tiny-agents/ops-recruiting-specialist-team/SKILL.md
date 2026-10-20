---
name: ops-recruiting-specialist-team
description: "招聘专家。用于精通人才招聘全流程，为团队找到最佳人才。来源于 WorkBuddy 运营人力卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/运营人力/ops-recruiting-specialist"
  workbuddy_card: "招聘专家"
  workbuddy_category: "运营人力"
---

# 招聘专家

Use this skill as the routing entry point for 招聘专家 work. It packages the WorkBuddy 运营人力 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `ops-recruiting-specialist-intake`
- `ops-recruiting-specialist-strategy`
- `ops-recruiting-specialist-execution`
- `ops-recruiting-specialist-quality`
- `ops-recruiting-specialist-measurement`
- `ops-recruiting-specialist-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 招聘专家 package, assemble the output set described in `references/workflow.md`.
