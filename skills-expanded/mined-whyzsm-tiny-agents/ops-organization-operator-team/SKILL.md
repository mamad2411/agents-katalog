---
name: ops-organization-operator-team
description: "组织运营师。用于小企业组织运营师，负责招聘入职、工具初始化和业务快照，让运营不掉链子。来源于 WorkBuddy 运营人力卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/运营人力/ops-organization-operator"
  workbuddy_card: "组织运营师"
  workbuddy_category: "运营人力"
---

# 组织运营师

Use this skill as the routing entry point for 组织运营师 work. It packages the WorkBuddy 运营人力 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `ops-organization-operator-intake`
- `ops-organization-operator-strategy`
- `ops-organization-operator-execution`
- `ops-organization-operator-quality`
- `ops-organization-operator-measurement`
- `ops-organization-operator-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 组织运营师 package, assemble the output set described in `references/workflow.md`.
